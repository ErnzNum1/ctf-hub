"""
Content for the Learn page (roadmap + glossary).
Edit freely. Roadmap `platform` uses the platform slug (or None).
"""

ROADMAP = [
    {
        "title": "Learn the basics first",
        "text": "Get comfortable with how the internet and websites work, the Linux "
                "command line, and a little Python. You do not need to be an expert.",
        "platform": None,
    },
    {
        "title": "Try a beginner CTF in your browser",
        "text": "Play simple challenges to understand what a flag is and how points work.",
        "platform": "csplusplus",
    },
    {
        "title": "Follow guided rooms",
        "text": "Do the beginner learning paths. Each room explains a topic and then lets you practice it.",
        "platform": "tryhackme",
    },
    {
        "title": "Hack realistic machines",
        "text": "Start with the beginner area and Easy machines, then move up when ready.",
        "platform": "hackthebox",
    },
    {
        "title": "Write about it and join events",
        "text": "Record videos, write down what you learned, and try live CTF competitions with a team.",
        "platform": None,
    },
]

GLOSSARY = [
    ("Flag", "A secret piece of text hidden in a challenge. When you find it and submit it, "
             "you earn points. It often looks like flag{some_text}."),
    ("CTF (Capture The Flag)", "A security game where you solve challenges to find flags. "
                               "It is used to practice and compete legally."),
    ("Jeopardy-style CTF", "A CTF with a board of separate challenges in categories (web, crypto, "
                           "forensics...). Each one is worth points."),
    ("Attack-defense CTF", "A CTF where teams defend their own servers and attack the others at the same time."),
    ("Vulnerability", "A weakness in software or a system that could be abused."),
    ("Exploit", "A way of using a vulnerability to make a system do something it should not."),
    ("Payload", "The data or code that an exploit delivers to do the actual job."),
    ("Reconnaissance (Recon)", "Gathering information about a target before doing anything else."),
    ("Enumeration", "Carefully listing what a target exposes: open ports, services, users, folders "
                    "and versions. Good enumeration shows you where to look next."),
    ("Port scan", "Checking which network ports on a machine are open to see which services are running."),
    ("Nmap", "A popular tool used to scan networks and find open ports and services."),
    ("Brute force", "Trying many possible passwords or values until one works."),
    ("SQL injection (SQLi)", "A web bug where user input is mixed into a database query in an unsafe way, "
                             "so an attacker can change what the query does."),
    ("XSS (Cross-site scripting)", "A web bug where an attacker's script runs in another user's browser "
                                   "because the site did not handle input safely."),
    ("CSRF", "Tricking a logged-in user's browser into sending a request they did not mean to make."),
    ("Burp Suite", "A tool that sits between your browser and a website so you can see and change "
                   "web requests. Used a lot for web CTFs."),
    ("Reverse shell", "A connection where the target machine connects back to the tester and gives "
                      "command-line access. It is a common step in penetration testing labs."),
    ("Privilege escalation", "Going from a limited user to a more powerful one, such as admin or root."),
    ("Hash", "A fixed-length fingerprint made from data. Passwords are often stored as hashes."),
    ("Encryption", "Scrambling data with a key so only someone with the right key can read it."),
    ("Cryptography (Crypto)", "A CTF category about codes, ciphers and encryption mistakes."),
    ("Forensics", "A CTF category about investigating files, disk images, memory or network "
                  "captures to find hidden evidence."),
    ("Steganography", "Hiding information inside something else, such as a picture or audio file."),
    ("Reverse engineering", "Studying a program to understand how it works without having the source code."),
    ("Pwn (Binary exploitation)", "A CTF category about finding and abusing bugs in compiled programs."),
    ("Write-up", "A document or video explaining step by step how you solved a challenge."),
    ("Virtual machine (VM)", "A computer simulated inside your computer. Many labs use VMs as targets."),
    ("VPN", "A secure tunnel to another network. Some platforms use it to connect you to their lab."),
]
