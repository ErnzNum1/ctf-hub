"""
CTF Hub - a small Flask website about 3 Capture The Flag platforms.

Run with:   python app.py
Then open:  http://127.0.0.1:5000
"""
import base64
import hmac
import json
import os
import re
import secrets
import sqlite3
import time
import uuid
from collections import defaultdict, deque
from functools import wraps

from flask import (Flask, Response, abort, flash, g, make_response, redirect,
                   render_template, request, send_from_directory, session,
                   url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from challenge_files import build_challenge_files
from challenges_data import CHALLENGES
from learn_data import GLOSSARY, ROADMAP
from quiz_data import QUESTIONS, REASONS
from seed_data import PLATFORMS, VIDEOS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Where ctf.db and secret.key are kept. Normal run: the project folder.
# In Docker we set CTF_DATA_DIR=/data so they live outside the container.
DATA_DIR = os.path.abspath(os.environ.get("CTF_DATA_DIR", BASE_DIR))
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "ctf.db")
VIDEO_DIR = os.path.join(BASE_DIR, "static", "videos")
ALLOWED_VIDEO_EXT = {"mp4", "webm", "mov", "m4v"}

# Accounts that are created automatically the first time the app starts.
# (They are only created if the username does not exist yet, so changing a
# password later on the Account page is never undone by restarting the app.)
DEFAULT_ACCOUNTS = [
    # (username, password, role)
    ("capturetheflag", "ubuntu", "admin"),
    ("ubuntu", "capturetheflag", "user"),
]


def load_secret_key():
    """Use CTF_SECRET_KEY if set, otherwise create a random key once and keep it in secret.key."""
    env_key = os.environ.get("CTF_SECRET_KEY")
    if env_key:
        return env_key
    path = os.path.join(DATA_DIR, "secret.key")
    try:
        with open(path, encoding="utf-8") as f:
            key = f.read().strip()
        if key:
            return key
    except OSError:
        pass
    key = secrets.token_hex(32)
    with open(path, "w", encoding="utf-8") as f:
        f.write(key)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return key


app = Flask(__name__)
app.config["SECRET_KEY"] = load_secret_key()
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1 GB upload limit
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

os.makedirs(VIDEO_DIR, exist_ok=True)


def video_file_exists(filename):
    """True if the video file is really inside the static/videos folder."""
    if not filename:
        return False
    path = os.path.normpath(os.path.join(VIDEO_DIR, filename))
    return path.startswith(VIDEO_DIR + os.sep) and os.path.isfile(path)


# lets the templates ask "is this video file really there?"
app.jinja_env.globals["video_file_exists"] = video_file_exists


def warn_missing_videos():
    """Print a clear message in the terminal for every video that has no file yet."""
    db = sqlite3.connect(DB_PATH)
    try:
        for (name,) in db.execute("SELECT filename FROM videos WHERE filename IS NOT NULL"):
            if not video_file_exists(name):
                print(f"[CTF Hub] WARNING: video file not found: {name}")
                print(f"          Copy it into this folder: {VIDEO_DIR}")
    finally:
        db.close()


# Challenges ------------------------------------------------------------------
CHALLENGE_DIR = os.path.join(BASE_DIR, "challenge_files")
FLAGS = {c["id"]: c["flag"] for c in CHALLENGES}
CHALLENGES_BY_ID = {c["id"]: c for c in CHALLENGES}
# Same data WITHOUT the flag. Only this version is ever given to a template.
PUBLIC_CHALLENGES = [{k: v for k, v in c.items() if k != "flag"} for c in CHALLENGES]
PUBLIC_BY_ID = {c["id"]: c for c in PUBLIC_CHALLENGES}
build_challenge_files(CHALLENGE_DIR, FLAGS)

# Platforms that no longer exist on the site. Removed from the database at startup.
REMOVED_PLATFORMS = ["portswigger"]

# Text of the About page (the admin can change it; these are the defaults)
ABOUT_DEFAULTS = {
    "about_name": "Your Name",
    "about_intro": (
        "I'm learning cyber security by playing Capture The Flag. This website is "
        "where I share what I learn on TryHackMe, Hack The Box and CS++, "
        "and I upload my own videos of me solving challenges."
    ),
    "about_goal": (
        "To get better at ethical hacking, record the journey, and help other beginners "
        "who feel lost like I did at the start."
    ),
    "about_email": "",
    "about_youtube": "",
    "about_github": "",
}


# ----------------------------------------------------------------------------
# Database helpers
# ----------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create tables, the 3 platforms, default accounts, and seeded videos (only what is missing)."""
    db = sqlite3.connect(DB_PATH)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS platforms (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            slug         TEXT UNIQUE NOT NULL,
            name         TEXT NOT NULL,
            tagline      TEXT,
            website      TEXT,
            founded      TEXT,
            founder      TEXT,
            headquarters TEXT,
            pricing      TEXT,
            difficulty   TEXT,
            accent       TEXT,
            description  TEXT,
            history      TEXT,
            about        TEXT,
            features     TEXT,
            best_for     TEXT,
            tips         TEXT,
            sort_order   INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS videos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            platform_id INTEGER NOT NULL REFERENCES platforms(id) ON DELETE CASCADE,
            title       TEXT NOT NULL,
            description TEXT,
            filename    TEXT,
            youtube_url TEXT,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            role          TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS challenge_progress (
            user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            challenge_id TEXT NOT NULL,
            solved_at    TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, challenge_id)
        );
        CREATE TABLE IF NOT EXISTS site_content (
            key   TEXT PRIMARY KEY,
            value TEXT
        );
        """
    )
    # Upgrade an older database: add the "tags" column to videos if it is missing
    video_cols = [row[1] for row in db.execute("PRAGMA table_info(videos)")]
    if "tags" not in video_cols:
        db.execute("ALTER TABLE videos ADD COLUMN tags TEXT")

    # Platforms that were removed from the site (their videos are deleted too)
    db.execute("PRAGMA foreign_keys = ON")
    for old_slug in REMOVED_PLATFORMS:
        db.execute("DELETE FROM platforms WHERE slug = ?", (old_slug,))

    for i, p in enumerate(PLATFORMS):
        db.execute(
            """
            INSERT OR IGNORE INTO platforms
            (slug, name, tagline, website, founded, founder, headquarters, pricing,
             difficulty, accent, description, history, about, features, best_for,
             tips, sort_order)
            VALUES (:slug, :name, :tagline, :website, :founded, :founder,
                    :headquarters, :pricing, :difficulty, :accent, :description,
                    :history, :about, :features, :best_for, :tips, :sort_order)
            """,
            {**p, "sort_order": i},
        )

    for username, password, role in DEFAULT_ACCOUNTS:
        exists = db.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
        if not exists:
            db.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), role),
            )

    for v in VIDEOS:
        plat = db.execute("SELECT id FROM platforms WHERE slug = ?", (v["platform_slug"],)).fetchone()
        exists = db.execute("SELECT 1 FROM videos WHERE filename = ?", (v["filename"],)).fetchone()
        if plat and not exists:
            db.execute(
                "INSERT INTO videos (platform_id, title, description, filename, tags) VALUES (?, ?, ?, ?, ?)",
                (plat[0], v["title"], v["description"], v["filename"], v.get("tags")),
            )

    db.commit()
    db.close()


# ----------------------------------------------------------------------------
# Template helpers
# ----------------------------------------------------------------------------
@app.template_filter("lines")
def split_lines(text):
    """Turn a multi-line string into a list of non-empty lines."""
    return [ln.strip() for ln in (text or "").splitlines() if ln.strip()]


@app.template_filter("paragraphs")
def split_paragraphs(text):
    return [p.strip() for p in (text or "").split("\n\n") if p.strip()]


@app.template_filter("youtube_embed")
def youtube_embed(url):
    """Convert a normal YouTube link into an embeddable link."""
    if not url:
        return ""
    m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})", url)
    return f"https://www.youtube.com/embed/{m.group(1)}" if m else ""


# ----------------------------------------------------------------------------
# Accounts: who is logged in, CSRF protection, login throttle
# ----------------------------------------------------------------------------
USERNAME_RE = re.compile(r"[A-Za-z0-9_.-]{3,30}")
MIN_PASSWORD = 8
MAX_PASSWORD = 128
DUMMY_HASH = generate_password_hash(secrets.token_hex(8))  # keeps login timing similar

MAX_FAILS = 5          # wrong passwords allowed...
FAIL_WINDOW = 300      # ...within this many seconds (per IP address + username)
_failed_logins = defaultdict(deque)


def _recent_fails(key):
    now = time.time()
    q = _failed_logins[key]
    while q and now - q[0] > FAIL_WINDOW:
        q.popleft()
    if not q:
        _failed_logins.pop(key, None)
    return len(q)


def csrf_token():
    """A secret value that every form must send back. Stops other sites from posting for you."""
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


@app.before_request
def load_user_and_check_csrf():
    g.user = None
    if request.endpoint == "static":
        return
    uid = session.get("user_id")
    if uid:
        g.user = get_db().execute(
            "SELECT id, username, role FROM users WHERE id = ?", (uid,)
        ).fetchone()
        if g.user is None:  # account was removed
            session.pop("user_id", None)
    if request.method == "POST":
        sent = request.form.get("csrf_token", "")
        expected = session.get("csrf_token", "")
        if not expected or not hmac.compare_digest(sent.encode(), expected.encode()):
            abort(400)


@app.context_processor
def inject_globals():
    return {"current_user": g.get("user"), "csrf_token": csrf_token}


def safe_next(target):
    """Only allow redirects to pages on this same site."""
    if target and target.startswith("/") and not target.startswith("//") and "\\" not in target:
        return target
    return None


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            flash("Please log in first.", "warning")
            nxt = request.full_path.rstrip("?") if request.method == "GET" else None
            return redirect(url_for("login", next=nxt) if nxt else url_for("login"))
        return view(*args, **kwargs)

    return wrapper


def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            flash("Please log in as admin.", "warning")
            nxt = request.full_path.rstrip("?") if request.method == "GET" else None
            return redirect(url_for("login", next=nxt) if nxt else url_for("login"))
        if g.user["role"] != "admin":
            abort(403)
        return view(*args, **kwargs)

    return wrapper


def start_session(user_id):
    session.clear()  # new session on login (prevents session fixation)
    session["user_id"] = user_id


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if g.user:
        return redirect(url_for("index"))
    username = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        errors = []
        if not USERNAME_RE.fullmatch(username):
            errors.append("Username must be 3 to 30 characters: letters, numbers, dot, dash or underscore.")
        if len(password) < MIN_PASSWORD:
            errors.append(f"Password must be at least {MIN_PASSWORD} characters.")
        elif len(password) > MAX_PASSWORD:
            errors.append(f"Password is too long (max {MAX_PASSWORD} characters).")
        elif password != confirm:
            errors.append("The two passwords do not match.")
        if not errors:
            db = get_db()
            try:
                cur = db.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'user')",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except sqlite3.IntegrityError:
                errors.append("That username is already taken. Please choose another one.")
            else:
                start_session(cur.lastrowid)
                flash(f"Welcome, {username}! Your account was created.", "success")
                return redirect(url_for("index"))
        for e in errors:
            flash(e, "danger")
    return render_template("signup.html", username=username, min_password=MIN_PASSWORD)


@app.route("/login", methods=["GET", "POST"])
def login():
    nxt = safe_next(request.values.get("next"))
    if g.user and request.method == "GET":
        return redirect(nxt or url_for("index"))
    username = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")[:MAX_PASSWORD]
        key = (request.remote_addr, username.lower())
        if _recent_fails(key) >= MAX_FAILS:
            flash("Too many wrong attempts. Please wait 5 minutes and try again.", "danger")
            return render_template("login.html", username=username, next=nxt), 429
        user = get_db().execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
        password_ok = check_password_hash(user["password_hash"] if user else DUMMY_HASH, password)
        if user and password_ok:
            _failed_logins.pop(key, None)
            start_session(user["id"])
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(nxt or url_for("index"))
        _failed_logins[key].append(time.time())
        flash("Wrong username or password.", "danger")
    return render_template("login.html", username=username, next=nxt)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You are logged out.", "info")
    return redirect(url_for("index"))


@app.route("/admin/login")
def admin_login_old_address():
    return redirect(url_for("login"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    db = get_db()
    if request.method == "POST":
        current = request.form.get("current_password", "")[:MAX_PASSWORD]
        new = request.form.get("new_password", "")
        confirm = request.form.get("confirm", "")
        row = db.execute("SELECT password_hash FROM users WHERE id = ?", (g.user["id"],)).fetchone()
        if not check_password_hash(row["password_hash"], current):
            flash("Your current password is wrong.", "danger")
        elif len(new) < MIN_PASSWORD:
            flash(f"New password must be at least {MIN_PASSWORD} characters.", "danger")
        elif len(new) > MAX_PASSWORD:
            flash(f"New password is too long (max {MAX_PASSWORD} characters).", "danger")
        elif new != confirm:
            flash("The two new passwords do not match.", "danger")
        else:
            db.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                       (generate_password_hash(new), g.user["id"]))
            db.commit()
            flash("Password changed.", "success")
        return redirect(url_for("account"))
    solved = solved_ids()
    return render_template(
        "account.html",
        solved_count=len(solved),
        total=len(CHALLENGES),
        points=sum(c["points"] for c in CHALLENGES if c["id"] in solved),
        total_points=sum(c["points"] for c in CHALLENGES),
        min_password=MIN_PASSWORD,
    )


# ----------------------------------------------------------------------------
# Public pages
# ----------------------------------------------------------------------------
@app.route("/")
def index():
    db = get_db()
    platforms = db.execute(
        """
        SELECT p.*, (SELECT COUNT(*) FROM videos v WHERE v.platform_id = p.id) AS video_count
        FROM platforms p ORDER BY sort_order
        """
    ).fetchall()
    return render_template("index.html", platforms=platforms)


@app.route("/platform/<slug>")
def platform(slug):
    db = get_db()
    p = db.execute("SELECT * FROM platforms WHERE slug = ?", (slug,)).fetchone()
    if p is None:
        abort(404)
    videos = db.execute(
        "SELECT * FROM videos WHERE platform_id = ? ORDER BY id ASC", (p["id"],)
    ).fetchall()
    all_platforms = db.execute(
        "SELECT slug, name FROM platforms ORDER BY sort_order"
    ).fetchall()
    return render_template("platform.html", p=p, videos=videos, all_platforms=all_platforms)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """'Which platform should I start with?' quiz (scored here in Python)."""
    if request.method == "GET":
        return render_template("quiz.html", questions=QUESTIONS, result=None, chosen={})

    chosen = {q["id"]: request.form.get(q["id"]) for q in QUESTIONS}
    if not all(chosen.values()):
        flash("Please answer all the questions.", "warning")
        return render_template("quiz.html", questions=QUESTIONS, result=None, chosen=chosen)

    db = get_db()
    platforms = db.execute("SELECT * FROM platforms ORDER BY sort_order").fetchall()
    scores = {p["slug"]: 0 for p in platforms}
    max_scores = {p["slug"]: 0 for p in platforms}

    for q in QUESTIONS:
        for a in q["answers"]:
            if a["id"] == chosen[q["id"]]:
                for slug, pts in a["points"].items():
                    if slug in scores:
                        scores[slug] += pts
        for slug in max_scores:
            max_scores[slug] += max(a["points"].get(slug, 0) for a in q["answers"])

    ranked = sorted(platforms, key=lambda p: scores[p["slug"]], reverse=True)  # stable on ties
    result = [
        {
            "platform": p,
            "score": scores[p["slug"]],
            "percent": round(100 * scores[p["slug"]] / max_scores[p["slug"]]) if max_scores[p["slug"]] else 0,
            "reason": REASONS.get(p["slug"], ""),
        }
        for p in ranked
    ]
    return render_template("quiz.html", questions=QUESTIONS, result=result, chosen=chosen)


@app.route("/compare")
def compare():
    db = get_db()
    platforms = db.execute("SELECT * FROM platforms ORDER BY sort_order").fetchall()
    return render_template("compare.html", platforms=platforms)


@app.route("/learn")
def learn():
    db = get_db()
    names = {r["slug"]: r["name"] for r in db.execute("SELECT slug, name FROM platforms")}
    return render_template("learn.html", roadmap=ROADMAP, glossary=sorted(GLOSSARY), names=names)


@app.route("/videos")
def videos():
    """All videos, with search (title / description / tags) and platform filter."""
    q = request.args.get("q", "").strip()
    platform_slug = request.args.get("platform", "").strip()
    db = get_db()

    sql = (
        "SELECT v.*, p.name AS platform_name, p.slug AS platform_slug, p.accent AS accent "
        "FROM videos v JOIN platforms p ON p.id = v.platform_id WHERE 1=1"
    )
    params = []
    if platform_slug:
        sql += " AND p.slug = ?"
        params.append(platform_slug)
    if q:
        like = f"%{q}%"
        sql += " AND (v.title LIKE ? OR v.description LIKE ? OR v.tags LIKE ? OR p.name LIKE ?)"
        params += [like, like, like, like]
    sql += " ORDER BY v.id ASC"

    results = db.execute(sql, params).fetchall()
    platforms = db.execute("SELECT slug, name FROM platforms ORDER BY sort_order").fetchall()
    return render_template(
        "videos.html", videos=results, platforms=platforms, q=q, selected=platform_slug
    )


def get_about():
    rows = get_db().execute("SELECT key, value FROM site_content WHERE key LIKE 'about_%'").fetchall()
    data = dict(ABOUT_DEFAULTS)
    data.update({r["key"]: r["value"] or "" for r in rows})
    return data


@app.route("/about")
def about():
    return render_template("about.html", a=get_about())


# ----------------------------------------------------------------------------
# Challenges (logged-in visitors solve these and submit flags; progress is
# saved in the database)
# ----------------------------------------------------------------------------
def solved_ids():
    if g.user is None:
        return set()
    rows = get_db().execute(
        "SELECT challenge_id FROM challenge_progress WHERE user_id = ?", (g.user["id"],)
    ).fetchall()
    return {r["challenge_id"] for r in rows} & set(CHALLENGES_BY_ID)


@app.route("/challenges")
def challenges():
    solved = solved_ids()
    groups = [
        (level, [c for c in PUBLIC_CHALLENGES if c["difficulty"] == level])
        for level in ("easy", "medium", "hard")
    ]
    return render_template(
        "challenges.html",
        groups=groups,
        solved=solved,
        total=len(CHALLENGES),
        solved_count=len(solved),
        points=sum(c["points"] for c in CHALLENGES if c["id"] in solved),
        total_points=sum(c["points"] for c in CHALLENGES),
    )


@app.route("/challenges/<cid>")
def challenge(cid):
    c = PUBLIC_BY_ID.get(cid)
    if c is None:
        abort(404)
    return render_template("challenge.html", c=c, solved=cid in solved_ids())


@app.route("/challenges/<cid>/submit", methods=["POST"])
def submit_flag(cid):
    c = CHALLENGES_BY_ID.get(cid)
    if c is None:
        abort(404)
    if g.user is None:
        flash("Please log in to submit flags. Your progress is saved to your account.", "warning")
        return redirect(url_for("login", next=url_for("challenge", cid=cid)))
    guess = request.form.get("flag", "").strip()
    if hmac.compare_digest(guess.encode(), c["flag"].encode()):
        db = get_db()
        cur = db.execute(
            "INSERT OR IGNORE INTO challenge_progress (user_id, challenge_id) VALUES (?, ?)",
            (g.user["id"], cid),
        )
        db.commit()
        if cur.rowcount:
            flash(f"Correct! You earned {c['points']} points.", "success")
        else:
            flash("Correct! (You had already solved this one, so no new points.)", "info")
    else:
        flash("That is not the right flag. Try again!", "danger")
    return redirect(url_for("challenge", cid=cid))


@app.route("/challenges/<cid>/file/<name>")
def challenge_file(cid, name):
    c = PUBLIC_BY_ID.get(cid)
    if c is None or name not in c["files"]:
        abort(404)
    return send_from_directory(CHALLENGE_DIR, name, as_attachment=True)


@app.route("/challenges/reset", methods=["POST"])
@login_required
def reset_progress():
    db = get_db()
    db.execute("DELETE FROM challenge_progress WHERE user_id = ?", (g.user["id"],))
    db.commit()
    flash("Your progress was reset.", "info")
    return redirect(url_for("challenges"))


@app.route("/practice")
def practice():
    return render_template("practice.html")


# ----------------------------------------------------------------------------
# Challenge "labs": small practice pages that belong to the challenges.
# They are intentionally weak, but they cannot touch the real website data.
# ----------------------------------------------------------------------------
@app.route("/lab/welcome")
def lab_welcome():
    # The flag is placed in an HTML comment inside the template.
    return render_template("lab_welcome.html", flag=FLAGS["view-source"])


@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow: /lab/vault-7c41/\n", mimetype="text/plain")


@app.route("/lab/vault-7c41/")
def lab_vault():
    return render_template("lab_message.html", title="Secret Vault",
                           message="You found the hidden page!", flag=FLAGS["robots"])


@app.route("/lab/cookie")
def lab_cookie():
    role = request.cookies.get("role")
    if role == "admin":
        resp = make_response(render_template(
            "lab_message.html", title="Admin Area",
            message="Welcome back, admin!", flag=FLAGS["cookie"]))
    else:
        resp = make_response(render_template(
            "lab_message.html", title="Members Only",
            message="Access denied. You are logged in as a normal user. "
                    "Only admins can see the flag.", flag=None))
        if role is None:
            resp.set_cookie("role", "user", path="/lab")
    return resp


def _read_pass(raw):
    """Decode the Base64 JSON pass. Returns a dict or None."""
    try:
        padded = raw + "=" * (-len(raw) % 4)
        data = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


@app.route("/lab/pass")
def lab_pass():
    raw = request.cookies.get("pass")
    new_token = None
    if raw is None:
        guest = json.dumps({"user": "guest", "admin": False}, separators=(",", ":"))
        new_token = base64.b64encode(guest.encode()).decode().rstrip("=")
        raw = new_token
    data = _read_pass(raw)
    if data and data.get("user") == "admin" and data.get("admin") is True:
        resp = make_response(render_template(
            "lab_message.html", title="Vault Door", message="The door opens. Welcome, admin!",
            flag=FLAGS["forged-pass"]))
    else:
        resp = make_response(render_template(
            "lab_message.html", title="Vault Door",
            message="Access denied. Your access pass is stored in a cookie named pass. "
                    "Only an admin pass opens this door.", flag=None))
    if new_token:
        resp.set_cookie("pass", new_token, path="/lab")
    return resp


@app.route("/lab/login", methods=["GET", "POST"])
def lab_login():
    """
    INTENTIONALLY VULNERABLE (SQL injection practice).
    It only talks to a throw-away database that lives in memory and is deleted
    after each request, so it can never reach the real website database
    (and it has nothing to do with the real login of this website).
    """
    result = None
    flag = None
    if request.method == "POST":
        username = request.form.get("username", "")[:100]
        password = request.form.get("password", "")[:100]
        fake_db = sqlite3.connect(":memory:")
        try:
            fake_db.execute("CREATE TABLE users (username TEXT, password TEXT, role TEXT)")
            fake_db.executemany(
                "INSERT INTO users VALUES (?, ?, ?)",
                [("admin", secrets.token_hex(12), "admin"),
                 ("guest", "guest123", "user"),
                 ("bob", "bob-password", "user")],
            )
            # <-- the weak part: user input is pasted straight into the query
            query = ("SELECT username, role FROM users WHERE username = '"
                     + username + "' AND password = '" + password + "'")
            row = fake_db.execute(query).fetchone()
            if row is None:
                result = ("danger", "Wrong username or password.")
            elif row[1] == "admin":
                result = ("success", "Logged in as admin. Welcome!")
                flag = FLAGS["login-bypass"]
            else:
                result = ("warning", f"Logged in as {row[0]}, but you are not an admin.")
        except sqlite3.Error as err:
            result = ("warning", f"Database error: {err}")
        finally:
            fake_db.close()
    return render_template("lab_login.html", result=result, flag=flag)


# ----------------------------------------------------------------------------
# Error pages
# ----------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def forbidden(_e):
    return render_template(
        "error.html", code=403, title="Admins only",
        message="Your account does not have permission to open this page."), 403


@app.errorhandler(400)
def bad_request(_e):
    return render_template(
        "error.html", code=400, title="Please try again",
        message="Your session expired or the form was not valid. Go back, refresh the page "
                "and send the form again. (Cookies must be turned on.)"), 400


@app.errorhandler(413)
def too_large(_e):
    return render_template(
        "error.html", code=413, title="File too big",
        message="That upload is larger than 1 GB. For big videos, paste a YouTube link instead."), 413


# ----------------------------------------------------------------------------
# Admin area: upload videos, edit the pages, see users
# ----------------------------------------------------------------------------
URL_RE = re.compile(r"https?://[^\s<>\"']+")
ACCENT_RE = re.compile(r"#[0-9a-fA-F]{6}")
EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

# (column, maximum length) for the plain text boxes of a platform
PLATFORM_TEXT_FIELDS = [
    ("tagline", 200), ("founded", 200), ("founder", 200), ("headquarters", 200),
    ("pricing", 200), ("difficulty", 200), ("best_for", 300),
    ("description", 6000), ("history", 6000), ("about", 6000),
    ("features", 3000), ("tips", 3000),
]
PLATFORM_EDIT_COLUMNS = ["name", "website", "accent"] + [c for c, _ in PLATFORM_TEXT_FIELDS]


def clean_text(value):
    """Browsers send Windows line breaks (\\r\\n) from text boxes. Use plain \\n."""
    return (value or "").replace("\r\n", "\n").replace("\r", "\n").strip()


@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    db = get_db()
    if request.method == "POST":
        platform_id = request.form.get("platform_id", type=int)
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        youtube_url = request.form.get("youtube_url", "").strip()
        # tags: "web, sqli, easy" -> "web,sqli,easy"
        tags = ",".join(t.strip().lower() for t in request.form.get("tags", "").split(",") if t.strip())
        file = request.files.get("video_file")

        if not platform_id or not title:
            flash("Please choose a platform and write a title.", "danger")
            return redirect(url_for("admin"))
        if not db.execute("SELECT 1 FROM platforms WHERE id = ?", (platform_id,)).fetchone():
            flash("That platform does not exist.", "danger")
            return redirect(url_for("admin"))

        filename = None
        if file and file.filename:
            ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
            if ext not in ALLOWED_VIDEO_EXT:
                flash("Video must be: " + ", ".join(sorted(ALLOWED_VIDEO_EXT)), "danger")
                return redirect(url_for("admin"))
            filename = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            file.save(os.path.join(VIDEO_DIR, filename))

        if not filename and not youtube_url:
            flash("Upload a video file OR paste a YouTube link.", "danger")
            return redirect(url_for("admin"))

        db.execute(
            "INSERT INTO videos (platform_id, title, description, filename, youtube_url, tags) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (platform_id, title, description, filename, youtube_url or None, tags or None),
        )
        db.commit()
        flash("Video added!", "success")
        return redirect(url_for("admin"))

    platforms = db.execute("SELECT id, name FROM platforms ORDER BY sort_order").fetchall()
    videos = db.execute(
        "SELECT v.*, p.name AS platform_name FROM videos v "
        "JOIN platforms p ON p.id = v.platform_id ORDER BY v.created_at DESC"
    ).fetchall()
    return render_template("admin.html", platforms=platforms, videos=videos)


@app.route("/admin/delete/<int:video_id>", methods=["POST"])
@admin_required
def delete_video(video_id):
    db = get_db()
    v = db.execute("SELECT * FROM videos WHERE id = ?", (video_id,)).fetchone()
    if v:
        if v["filename"]:
            path = os.path.join(VIDEO_DIR, v["filename"])
            if os.path.exists(path):
                os.remove(path)
        db.execute("DELETE FROM videos WHERE id = ?", (video_id,))
        db.commit()
        flash("Video deleted.", "info")
    return redirect(url_for("admin"))


@app.route("/admin/platforms")
@admin_required
def admin_platforms():
    platforms = get_db().execute("SELECT slug, name, tagline, accent FROM platforms ORDER BY sort_order").fetchall()
    return render_template("admin_platforms.html", platforms=platforms)


def parse_platform_form(form):
    """Check the edit form. Returns (values, errors)."""
    values, errors = {}, []

    name = clean_text(form.get("name"))
    if not name:
        errors.append("Name cannot be empty.")
    elif len(name) > 100:
        errors.append("Name is too long (max 100 characters).")
    values["name"] = name

    website = clean_text(form.get("website"))
    if not URL_RE.fullmatch(website) or len(website) > 300:
        errors.append("Website must be a full link that starts with http:// or https://")
    values["website"] = website

    accent = clean_text(form.get("accent"))
    if not ACCENT_RE.fullmatch(accent):
        errors.append("Colour must look like #aabbcc.")
    values["accent"] = accent

    for column, max_len in PLATFORM_TEXT_FIELDS:
        text = clean_text(form.get(column))
        if len(text) > max_len:
            errors.append(f"'{column}' is too long (max {max_len} characters).")
        values[column] = text
    return values, errors


@app.route("/admin/platform/<slug>", methods=["GET", "POST"])
@admin_required
def admin_platform_edit(slug):
    db = get_db()
    p = db.execute("SELECT * FROM platforms WHERE slug = ?", (slug,)).fetchone()
    if p is None:
        abort(404)
    values = dict(p)
    if request.method == "POST":
        parsed, errors = parse_platform_form(request.form)
        values.update(parsed)
        if errors:
            for e in errors:
                flash(e, "danger")
        else:
            assignments = ", ".join(f"{c} = ?" for c in PLATFORM_EDIT_COLUMNS)  # column names are constants
            db.execute(
                f"UPDATE platforms SET {assignments} WHERE slug = ?",
                [values[c] for c in PLATFORM_EDIT_COLUMNS] + [slug],
            )
            db.commit()
            flash("Saved! The page was updated.", "success")
            return redirect(url_for("admin_platform_edit", slug=slug))
    return render_template("admin_platform_edit.html", p=p, v=values)


@app.route("/admin/platform/<slug>/restore", methods=["POST"])
@admin_required
def admin_platform_restore(slug):
    seed = next((s for s in PLATFORMS if s["slug"] == slug), None)
    if seed is None:
        abort(404)
    assignments = ", ".join(f"{c} = ?" for c in PLATFORM_EDIT_COLUMNS)
    db = get_db()
    db.execute(
        f"UPDATE platforms SET {assignments} WHERE slug = ?",
        [seed[c] for c in PLATFORM_EDIT_COLUMNS] + [slug],
    )
    db.commit()
    flash("The original text was restored.", "info")
    return redirect(url_for("admin_platform_edit", slug=slug))


@app.route("/admin/about", methods=["GET", "POST"])
@admin_required
def admin_about():
    db = get_db()
    values = get_about()
    if request.method == "POST":
        limits = {"about_name": 60, "about_intro": 2000, "about_goal": 1000,
                  "about_email": 100, "about_youtube": 300, "about_github": 300}
        errors = []
        for key, max_len in limits.items():
            text = clean_text(request.form.get(key))
            if len(text) > max_len:
                errors.append(f"'{key.replace('about_', '')}' is too long (max {max_len} characters).")
            values[key] = text
        if not values["about_name"]:
            errors.append("Name cannot be empty.")
        if values["about_email"] and not EMAIL_RE.fullmatch(values["about_email"]):
            errors.append("Email does not look right.")
        for key in ("about_youtube", "about_github"):
            if values[key] and not URL_RE.fullmatch(values[key]):
                errors.append("Links must start with http:// or https://")
        if errors:
            for e in errors:
                flash(e, "danger")
        else:
            for key, text in values.items():
                db.execute("INSERT OR REPLACE INTO site_content (key, value) VALUES (?, ?)", (key, text))
            db.commit()
            flash("About page saved.", "success")
            return redirect(url_for("admin_about"))
    return render_template("admin_about.html", v=values)


@app.route("/admin/users")
@admin_required
def admin_users():
    db = get_db()
    users = db.execute("SELECT id, username, role, created_at FROM users ORDER BY id").fetchall()
    solved_by_user = defaultdict(set)
    for row in db.execute("SELECT user_id, challenge_id FROM challenge_progress"):
        if row["challenge_id"] in CHALLENGES_BY_ID:
            solved_by_user[row["user_id"]].add(row["challenge_id"])
    rows = [
        {
            "username": u["username"], "role": u["role"], "created_at": u["created_at"],
            "solved": len(solved_by_user[u["id"]]),
            "points": sum(CHALLENGES_BY_ID[c]["points"] for c in solved_by_user[u["id"]]),
        }
        for u in users
    ]
    return render_template("admin_users.html", rows=rows, total=len(CHALLENGES),
                           total_points=sum(c["points"] for c in CHALLENGES))


# Create the database when the app starts
init_db()
warn_missing_videos()

if __name__ == "__main__":
    app.run(debug=True)