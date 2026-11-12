"""
Builds the downloadable challenge files (note.txt, letter.txt, picture.png,
secret.txt, access.log). Runs every time the app starts, so the files always
contain the current flags from challenges_data.py.

Only Python's standard library is used.
"""
import base64
import os
import random
import struct
import zlib


def _caesar(text, shift):
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)


def _png_bytes(width=160, height=100):
    """A small colourful gradient picture that is a real, valid PNG."""
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter type 0 for every row
        for x in range(width):
            raw += bytes((x * 255 // (width - 1), y * 255 // (height - 1), 180))

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def _access_log(flag):
    rng = random.Random(1337)  # fixed seed = same file every time
    paths = ["/", "/index.html", "/about", "/login", "/products", "/products/12", "/products/7",
             "/cart", "/contact", "/static/app.js", "/static/style.css", "/favicon.ico", "/blog/hello-world"]
    agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/118.0",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) Safari/605.1.15",
              "Mozilla/5.0 (X11; Linux x86_64) Chrome/117.0 Safari/537.36",
              "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) Mobile/15E148"]
    ips = [f"198.51.100.{n}" for n in range(2, 60)]
    secret_line = 217
    decoys = {90: b"hello world", 160: b"not the flag", 250: b"keep looking"}

    lines = []
    seconds = 9 * 3600
    for i in range(300):
        seconds += rng.randint(1, 20)
        stamp = "06/Nov/2026:%02d:%02d:%02d +0000" % (seconds // 3600, seconds % 3600 // 60, seconds % 60)
        if i == secret_line:
            data = base64.b64encode(flag.encode()).decode()
            lines.append(f'203.0.113.99 - - [{stamp}] "GET /api/export?data={data} HTTP/1.1" 200 1024 "-" "python-requests/2.31"')
        elif i in decoys:
            data = base64.b64encode(decoys[i]).decode()
            lines.append(f'198.51.100.{rng.randint(2, 59)} - - [{stamp}] "GET /api/ping?data={data} HTTP/1.1" 200 64 "-" "{rng.choice(agents)}"')
        else:
            status = rng.choice([200, 200, 200, 200, 304, 404])
            size = rng.randint(200, 9000)
            lines.append(f'{rng.choice(ips)} - - [{stamp}] "GET {rng.choice(paths)} HTTP/1.1" {status} {size} "-" "{rng.choice(agents)}"')
    return "\n".join(lines) + "\n"


def build_challenge_files(directory, flags):
    """Write all challenge files into `directory` using the given flags."""
    os.makedirs(directory, exist_ok=True)

    def write(name, data):
        mode = "wb" if isinstance(data, bytes) else "w"
        kwargs = {} if isinstance(data, bytes) else {"encoding": "utf-8", "newline": "\n"}
        with open(os.path.join(directory, name), mode, **kwargs) as f:
            f.write(data)

    # Easy: Base64 note
    encoded = base64.b64encode(flags["base64-note"].encode()).decode()
    write("note.txt",
          "Hey team,\n\nI hid the password in this note so nobody can read it.\n\n"
          f"{encoded}\n\n- Admin\n")

    # Medium: Caesar letter (shift of 7)
    secret = _caesar("Dear friend, I hope you are well. The secret you asked for is: " + flags["caesar"], 7)
    write("letter.txt", secret + "\n\nSee you soon!\n")

    # Medium: flag appended after the end of a valid PNG
    write("picture.png", _png_bytes() + b"\n\n[note to self] " + flags["hidden-in-image"].encode() + b"\n")

    # Hard: XOR with a repeating 3 byte key
    key = b"ctf"
    cipher = bytes(b ^ key[i % len(key)] for i, b in enumerate(flags["xor"].encode()))
    write("secret.txt",
          "I locked the flag with a short secret key that repeats.\n\n"
          f"Ciphertext (hex):\n{cipher.hex()}\n")

    # Hard: web server log with one odd request
    write("access.log", _access_log(flags["logs"]))
