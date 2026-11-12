# CTF Hub

A website about 4 Capture The Flag platforms: TryHackMe, Hack The Box,
PortSwigger Web Security Academy and CS++.

- Frontend: Bootstrap 5
- Backend: Python (Flask)
- Database: SQLite (the file `ctf.db` is created automatically)

## Folder layout

```
ctf_site/
  app.py             <- the Python backend (pages, login, admin, database)
  seed_data.py       <- the ORIGINAL text for each platform
  challenges_data.py <- the challenges and their flags (answers!)
  quiz_data.py       <- quiz questions
  learn_data.py      <- roadmap and glossary
  requirements.txt   <- list of Python packages
  ctf.db             <- database (created when you first run the app)
  secret.key         <- created automatically (keeps logins safe). Do not share it.
  templates/         <- HTML pages
  static/css/        <- styles
  static/videos/     <- videos you upload are saved here
```

## Step-by-step: run the website

1. Install Python 3.10 or newer from https://www.python.org/downloads/
   (on Windows, tick "Add Python to PATH" during install).

2. Open VS Code, choose File > Open Folder, and pick the `ctf_site` folder.
   Then open the terminal: Terminal > New Terminal.

3. Create a virtual environment (only the first time):

   Windows:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   Mac / Linux:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install Flask (only the first time):

   ```
   pip install -r requirements.txt
   ```

5. Start the website:

   ```
   python app.py
   ```

6. Open your browser and go to: http://127.0.0.1:5000

7. Press `Ctrl + C` in the terminal to stop it.

Next time you only need: `venv\Scripts\activate` and then `python app.py`.

## Accounts: login, logout, sign up

There are two kinds of accounts:

| Role | What it can do |
|------|----------------|
| **user** | Log in, solve challenges, and have the progress saved in the database. |
| **admin** | Everything a user can do, plus: upload and delete videos, edit the platform pages, edit the About page, and see all users and their progress. |

These two accounts are created automatically the first time the app starts:

| Role | Username | Password |
|------|----------|----------|
| admin | `capturetheflag` | `ubuntu` |
| user | `ubuntu` | `capturetheflag` |

- Anyone can create their own account with **Sign up** (top right). New accounts are
  always normal users. Username: 3 to 30 characters. Password: at least 8 characters.
- Passwords are stored as hashes (scrambled), never as plain text.
- After 5 wrong passwords in a row, login is blocked for 5 minutes.
- **Please change the two default passwords** before showing the site to other people
  (these passwords are easy to guess). Log in, click your name at the top right,
  choose **My account**, then **Change password**.
- Forgot the admin password? Stop the app, delete `ctf.db`, and start it again.
  The two default accounts are created again. (This also deletes videos, edits
  and progress.)

## Admin: upload videos

1. Log in as admin, then click **Admin** at the top.
2. In **Videos**, pick the platform, write a title, then EITHER upload a video file
   OR paste a YouTube link (YouTube is better for big videos).
3. Click **Add video**. It now appears on that platform's page and in the Videos page.

## Admin: edit the pages

1. Log in as admin, click **Admin**, then **Edit platform pages**.
2. Choose a platform. Change the quick facts, description, history, about,
   features or tips, then click **Save changes**.
   - A new paragraph = leave an empty line between paragraphs.
   - In Key Features and Tips, write one point per line.
3. Made a mistake? Click **Restore original text** (it brings back the text from `seed_data.py`).
4. To change the About page (your name, story, email, links): **Edit About page**.

Your edits are saved in the database, so they stay after you restart the app.

## Challenge progress

- Anyone can read the challenges, but **you must log in to submit a flag**.
- Every solved challenge is saved in the database table `challenge_progress`,
  so progress stays when you log out, close the browser, or use another computer.
- The admin can see everybody's progress in **Admin > Users & progress**.
- Visitors can reset their own progress at the bottom of the Challenges page.

## Pages on the website

| Page | Address | What it is |
|------|---------|------------|
| Home | `/` | The 4 platform cards |
| Quiz | `/quiz` | "Which platform should I start with?" |
| Challenges | `/challenges` | 10 CTF challenges (3 easy, 3 medium, 4 hard) |
| Practice Labs | `/practice` | Links to open-source apps made for hacking practice (run on your own PC) |
| Compare | `/compare` | Side-by-side table of the 4 platforms |
| Learn | `/learn` | Beginner roadmap + glossary (with search box) |
| Videos | `/videos` | All videos, search by title/description/tag, filter by platform |
| About | `/about` | About me |
| Log in / Sign up | `/login`, `/signup` | Accounts |
| My account | `/account` | Your progress and change password |
| Admin | `/admin` | Videos, edit pages, users (admin only) |

Light/dark mode: use the sun/moon button at the top right.

## About the challenges

- Visitors download files or open small practice pages, find a flag that looks like
  `CTF{...}`, and submit it.
- Flags are checked on the server. The downloadable files (note.txt, letter.txt,
  picture.png, secret.txt, access.log) are created automatically in the folder
  `challenge_files/` every time you start the app. You can ignore that folder.
- Answers are in `challenges_data.py`. **Don't share that file** (for example on
  GitHub) unless you change the flags first, because it contains the answers.
- The web challenges (`/lab/...`) are weak on purpose. The login challenge only uses
  a fake database that lives in memory. It has nothing to do with the real login of
  this website and cannot touch your real data.

## Which file do I edit to change...

- Platform text, price, difficulty -> log in as admin and use **Edit platform pages**
- About page (name, email, links) -> log in as admin and use **Edit About page**
- Default accounts -> `DEFAULT_ACCOUNTS` near the top of `app.py` (only used when the
  database is created; later change passwords on the **My account** page)
- Challenges, flags, hints, points -> `challenges_data.py` (flags in the files update
  automatically when you restart the app)
- Quiz questions and points -> `quiz_data.py`
- Roadmap steps and glossary words -> `learn_data.py`

After editing a `.py` file, stop the app (`Ctrl + C`) and run `python app.py` again.

## Updating from the older version

Don't delete anything. Copy the new files over the old ones and choose "Replace".
Your `ctf.db` (platform text, videos) is upgraded automatically, and the two default
accounts are added. Challenge progress saved before in a browser is not moved to the
database (everyone starts from 0 once, because now it belongs to an account).

## Before putting the site on the internet

- Change both default passwords (see above).
- Do not use `python app.py` as it is: it runs with `debug=True`, which is only for
  your own computer. Ask me and I will prepare it for PythonAnywhere or another host.
- Use HTTPS (hosting sites give this for free).
- Keep `ctf.db` and `secret.key` private. Don't upload them to GitHub (the included
  `.gitignore` already skips them).

## Notes

- The text about each platform is a short summary. Please double-check the
  details (dates, names, prices) on each official website, since they can
  change. The CS++ "History" section is intentionally short; add what you verify.
- Bootstrap loads from the internet (CDN), so you need internet to see the
  styling.
