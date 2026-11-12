"""
The text content for the 3 platforms and default videos.

HOW TO EDIT: change the text below, then DELETE the file `ctf.db` and run
`python app.py` again. The database will be rebuilt with your new text.

- Paragraphs are separated by a blank line.
- In `features` and `tips`, each line becomes one bullet point.
"""

PLATFORMS = [
    {
        "slug": "tryhackme",
        "name": "TryHackMe",
        "tagline": "Learn cyber security through guided, hands-on rooms.",
        "website": "https://tryhackme.com",
        "founded": "2018",
        "founder": "Ashu Savani and Ben Spring",
        "headquarters": "United Kingdom",
        "pricing": "Free tier + paid subscription",
        "difficulty": "Beginner friendly",
        "accent": "#e83e3e",
        "description": (
            "TryHackMe is an online learning platform for cyber security. Instead of "
            "only reading theory, you learn by doing: each topic is a \"room\" with "
            "explanations, questions and a virtual machine you can attack.\n\n"
            "It is widely seen as one of the easiest places to start. Rooms are grouped "
            "into learning paths (for example pre-security, web hacking and "
            "penetration testing), so you always know what to learn next. You can "
            "use their in-browser machine (AttackBox) so you do not need to install "
            "anything at the start."
        ),
        "history": (
            "TryHackMe was started in 2018 in the United Kingdom by Ashu Savani and "
            "Ben Spring. The idea was to make learning security less intimidating "
            "than platforms that drop beginners straight into hard challenges.\n\n"
            "Since then it has grown into a large community with learning paths, "
            "guided rooms, king-of-the-hill style games, competitions and "
            "content for schools and companies."
        ),
        "about": (
            "TryHackMe teaches with a step-by-step style: read a short lesson, answer "
            "questions, then hack a target machine to find the flag. Flags are "
            "usually text you submit to prove you completed a task.\n\n"
            "It is a good first stop before moving to harder platforms such as "
            "Hack The Box."
        ),
        "features": (
            "Guided rooms with questions and flags\n"
            "Learning paths from beginner to advanced\n"
            "In-browser AttackBox (no setup needed)\n"
            "Points, badges, streaks and leaderboards\n"
            "Competitions and team/classroom features"
        ),
        "best_for": "Absolute beginners and anyone who likes guided learning.",
        "tips": (
            "Start with the beginner/pre-security style paths.\n"
            "Take notes of every command you use.\n"
            "Try each room again without the walkthrough hints."
        ),
    },
    {
        "slug": "hackthebox",
        "name": "Hack The Box",
        "tagline": "Hack realistic machines and challenges. Level up your skills.",
        "website": "https://www.hackthebox.com",
        "founded": "2017",
        "founder": "Haris Pylarinos",
        "headquarters": "Greece / United Kingdom",
        "pricing": "Free tier + paid subscriptions",
        "difficulty": "Intermediate to advanced",
        "accent": "#9fef00",
        "description": (
            "Hack The Box (HTB) is a cyber security training platform where you "
            "attack realistic virtual machines and solve challenges to earn flags "
            "and points. Compared with guided platforms, HTB gives you much less "
            "hand-holding, which makes it great for building real problem-solving "
            "skills.\n\n"
            "You connect to the HTB network with a VPN (or use their browser "
            "tools), find a vulnerable machine, break in, and collect the "
            "user flag and root flag."
        ),
        "history": (
            "Hack The Box was founded in 2017 by Haris Pylarinos. It became "
            "famous in the community for its original invite system: to join, you "
            "had to hack a challenge on the website to discover your invite code.\n\n"
            "Over the years it added more areas: Starting Point for beginners, "
            "Academy for structured learning, Pro Labs for company-style "
            "networks, and team competitions and CTF events."
        ),
        "about": (
            "HTB is popular with people preparing for penetration testing roles and "
            "certifications. Machines are rated from easy to insane, and active "
            "machines are retired over time so there is always something new.\n\n"
            "It also runs CTF events for universities, companies and "
            "the public."
        ),
        "features": (
            "Active and retired vulnerable machines\n"
            "Challenges (web, crypto, reversing, forensics, pwn and more)\n"
            "Starting Point for beginners\n"
            "HTB Academy for guided modules\n"
            "Pro Labs and team CTF events\n"
            "Ranks and seasonal leaderboards"
        ),
        "best_for": "Learners who already know the basics and want realistic practice.",
        "tips": (
            "Begin with Starting Point and Easy machines.\n"
            "Do proper enumeration before trying exploits.\n"
            "Write your own notes or write-ups after each machine."
        ),
    },
    {
        "slug": "csplusplus",
        "name": "CS++",
        "tagline": "Free computer science courses with a beginner CTF in your browser.",
        "website": "https://csplusplus.com",
        "founded": "N/A",
        "founder": "Founded by a 20+ year AP Computer Science teacher",
        "headquarters": "N/A",
        "pricing": "Free account (optional paid extras)",
        "difficulty": "Beginner (school level)",
        "accent": "#f5b800",
        "description": (
            "CS++ is an online computer science education platform with free "
            "courses such as AP Computer Science Principles, AP CS A (Java), AP "
            "Cybersecurity, Intro to Python, Intro to Java and more, plus in-browser "
            "coding tools.\n\n"
            "Its Cybersecurity Capture the Flag is a beginner CTF with 100 "
            "challenges that run completely in your web browser. There is "
            "nothing to install, no virtual machine and no command line needed."
        ),
        "history": (
            "CS++ comes from a long-time AP Computer Science teacher who wanted "
            "to build free, classroom-friendly tools for students and teachers.\n\n"
            "Its CTF was made for high-school and AP classrooms, so it works "
            "even on locked-down school devices and Chromebooks. "
            "(Add more history here once you have verified details.)"
        ),
        "about": (
            "Guests can try a short preview of the CTF without logging in. With a "
            "free account you unlock almost all of the challenges, save your "
            "score across devices and can join classroom competitions. A few "
            "AI-themed challenges need a membership or class seat.\n\n"
            "Because flags are checked by the server and there is a leaderboard, "
            "it feels like a real CTF, but at a gentle difficulty."
        ),
        "features": (
            "100 beginner cybersecurity CTF challenges\n"
            "Runs fully in the browser (no install, no VM)\n"
            "Server-verified flags and classroom leaderboards\n"
            "Free guest preview, free account for more\n"
            "Also has free Python, Java and web design courses"
        ),
        "best_for": "Students and total beginners who want a safe first CTF.",
        "tips": (
            "Try the guest preview first, then make a free account.\n"
            "Read each challenge carefully; hints are often in the wording.\n"
            "Move on to TryHackMe or Hack The Box when it feels too easy."
        ),
    },
]

VIDEOS = [
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Offensive Security Intro - Task 1 (Think like a Hacker!)",
        "description": (
            "Offensive Security is about thinking like an attacker to find weaknesses "
            "before real hackers do. In this task, we learn the core concept of simulating "
            "a hacker's actions to identify security vulnerabilities in a safe and legal environment."
        ),
        "filename": "TRYHACKME-OFF (1).mp4",
        "tags": "tryhackme,offensive-security,beginner,task-1",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Offensive Security Intro - Task 2 (Starting the Lab)",
        "description": (
            "This room uses a virtual desktop to simulate a real system running FakeBank, "
            "a fake banking web application. In this step, we launch the target site and "
            "identify the target bank account number (8881)."
        ),
        "filename": "TRYHACKME-OFF (2).mp4",
        "tags": "tryhackme,offensive-security,fakebank,task-2",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Offensive Security Intro - Task 3 (Find Hidden Pages)",
        "description": (
            "Goal: Find a weakness in the FakeBank application where hidden pages are left "
            "publicly accessible. We launch the terminal on the attack machine and run "
            "dirbuster to brute-force and discover hidden directories."
        ),
        "filename": "TRYHACKME-OFF (3).mp4",
        "tags": "tryhackme,dirbuster,enumeration,task-3",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Offensive Security Intro - Task 4 (Attack the Admin Page)",
        "description": (
            "After discovering the hidden admin panel (/bank-transfer), we access it through "
            "the browser, deposit $2000 into account number 8881, and confirm that the balance "
            "turns positive to capture the flag (BANK-HACKED)."
        ),
        "filename": "TRYHACKME-OFF (4).mp4",
        "tags": "tryhackme,web-exploitation,fakebank,task-4",
    },
    # ------------------------------------------------------------------
    # Defensive Security Intro (room tasks 1 to 4)
    # ------------------------------------------------------------------
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Defensive Security Intro - Task 1 (You're the First Line of Defence)",
        "description": (
            "What does a defender actually do? Hackers are always quietly testing company "
            "websites, and the people whose job is to notice them, protect the company and "
            "stop them are called defenders. In this task, we learn what a defender does when "
            "a hack is detected, before experiencing the role in the next tasks."
        ),
        "filename": "TRYHACKME-DEF (1).mp4",
        "tags": "tryhackme,defensive-security,beginner,task-1",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Defensive Security Intro - Task 2 (Something Looks Wrong...)",
        "description": (
            "We launch the site and step into a defender's shoes using a simulated security "
            "dashboard. We review the recent alerts, spot the most suspicious one (a hacker "
            "has just triggered it), and find the IP address the attack is coming from."
        ),
        "filename": "TRYHACKME-DEF (2).mp4",
        "tags": "tryhackme,defensive-security,security-dashboard,alerts,task-2",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Defensive Security Intro - Task 3 (What are Hackers Looking For?)",
        "description": (
            "Thinking like a hacker helps us defend better. In the Security Dashboard we click "
            "\"Investigate\", look at the pages the hacker has tried to visit, and find the most "
            "recent page the hacker found."
        ),
        "filename": "TRYHACKME-DEF (3).mp4",
        "tags": "tryhackme,defensive-security,investigation,security-dashboard,task-3",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Defensive Security Intro - Task 4 (Stop The Hack)",
        "description": (
            "Now we stop the attack. Defenders block the hacker's connection and IP address, "
            "slow down how quickly important pages can be accessed, and turn on protection so "
            "the same hack cannot happen again. After all 3 protections are on, the dashboard "
            "shows a flag as proof that the hacker was stopped."
        ),
        "filename": "TRYHACKME-DEF (4).mp4",
        "tags": "tryhackme,defensive-security,blocking,protection,task-4",
    },
    # ------------------------------------------------------------------
    # Search Skills (room tasks 1 to 6)
    # ------------------------------------------------------------------
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Search Skills - Task 1 (Introduction)",
        "description": (
            "This room shows examples of popular websites and services used to gather "
            "information for cyber security, both offensive and defensive. Knowing where to "
            "search is just as important as knowing what to search for. This task is the "
            "introduction and needs no answer."
        ),
        "filename": "TRYHACKME-SEARCH (1).mp4",
        "tags": "tryhackme,search-skills,osint,beginner,task-1",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Search Skills - Task 2 (Shodan / TryScanMe)",
        "description": (
            "We use TryScanMe, the room's simulation of Shodan, to see how a search engine "
            "for internet-connected devices can be used to gather information for security "
            "work."
        ),
        "filename": "TRYHACKME-SEARCH (2).mp4",
        "tags": "tryhackme,search-skills,shodan,osint,task-2",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Search Skills - Task 3 (VirusTotal / TryDetectMe)",
        "description": (
            "VirusTotal collects results from over 70 antivirus engines and website scanners "
            "in one place. You can submit a file, URL, domain or file hash and see whether any "
            "engine flags it as malicious. We try it in the TryDetectMe simulation."
        ),
        "filename": "TRYHACKME-SEARCH (3).mp4",
        "tags": "tryhackme,search-skills,virustotal,malware-analysis,task-3",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Search Skills - Task 4 (Vulnerability Databases / CVE)",
        "description": (
            "The CVE programme is the closest thing to a universal dictionary of known "
            "vulnerabilities. Each one gets an identifier like CVE-YEAR-NUMBER and a CVSS score "
            "based on factors such as impact, complexity and availability. We look up "
            "vulnerabilities in a database in this task."
        ),
        "filename": "TRYHACKME-SEARCH (4).mp4",
        "tags": "tryhackme,search-skills,cve,cvss,vulnerability-database,task-4",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Search Skills - Task 5 (Technical Documentation / MAN)",
        "description": (
            "The official documentation of a tool is the most reliable and up-to-date place "
            "to learn it. We learn about Linux man pages (run man followed by a command) and "
            "practise reading them in a simulation of the manual pages."
        ),
        "filename": "TRYHACKME-SEARCH (5).mp4",
        "tags": "tryhackme,search-skills,man-pages,linux,documentation,task-5",
    },
    {
        "platform_slug": "tryhackme",
        "title": "TryHackMe: Search Skills - Task 6 (GitHub)",
        "description": (
            "GitHub is a great place to follow the latest threats and vulnerabilities, because "
            "researchers often publish proof-of-concept code and technical reports there. We "
            "review a repository for a fictitious CVE and read its README. Always check what "
            "you are about to run, since some PoC repositories can be malicious."
        ),
        "filename": "TRYHACKME-SEARCH (6).mp4",
        "tags": "tryhackme,search-skills,github,poc,cve,task-6",
    },
    # ------------------------------------------------------------------
    # CS++ Cybersecurity CTF - General Skills (warm-ups: encodings)
    # ------------------------------------------------------------------
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - Sanity Check",
        "description": (
            "The beginner warm-up challenge (10 points) in the General Skills category. "
            "It helps us get used to how the CS++ CTF works and how a flag is found and "
            "submitted."
        ),
        "filename": "CSPLUS (1).mp4",
        "tags": "csplusplus,ctf,general-skills,sanity-check,beginner",
    },
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - Base64 Basics",
        "description": (
            "Easy challenge (15 points). Base64 turns data into plain text using 64 characters "
            "(letters, numbers, + and /) and often ends with = signs. We decode the text to "
            "reveal the flag."
        ),
        "filename": "CSPLUS (2).mp4",
        "tags": "csplusplus,ctf,general-skills,base64,encoding,easy",
    },
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - Hexadecimal",
        "description": (
            "Easy challenge (15 points). Hexadecimal is base 16 (0-9 and a-f), and every byte "
            "is written as two hex characters. We convert the hex back into readable text to "
            "find the flag."
        ),
        "filename": "CSPLUS (3).mp4",
        "tags": "csplusplus,ctf,general-skills,hexadecimal,encoding,easy",
    },
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - Binary Decoder",
        "description": (
            "Easy challenge (15 points). Computers store text as 0s and 1s, and every group "
            "of 8 bits makes one character. We decode the binary to get the flag."
        ),
        "filename": "CSPLUS (4).mp4",
        "tags": "csplusplus,ctf,general-skills,binary,encoding,easy",
    },
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - URL Encoded",
        "description": (
            "Easy challenge (15 points). Web addresses replace special characters with a % "
            "sign followed by two hex digits (for example %20 is a space). We decode the "
            "URL-encoded text to reveal the flag."
        ),
        "filename": "CSPLUS (5).mp4",
        "tags": "csplusplus,ctf,general-skills,url-encoding,encoding,easy",
    },
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - Base85",
        "description": (
            "Easy challenge (20 points). Base85 packs data into text more compactly than "
            "Base64 by using 85 printable characters. We decode it to find the flag."
        ),
        "filename": "CSPLUS (6).mp4",
        "tags": "csplusplus,ctf,general-skills,base85,encoding,easy",
    },
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - Base32",
        "description": (
            "Easy challenge (15 points). Base32 uses only capital letters A-Z and the numbers "
            "2-7, and is often padded with = signs. We decode it to get the flag."
        ),
        "filename": "CSPLUS (7).mp4",
        "tags": "csplusplus,ctf,general-skills,base32,encoding,easy",
    },
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - ROT47",
        "description": (
            "Easy challenge (20 points). ROT47 is a cousin of ROT13: it shifts the 94 "
            "printable characters by 47 places, so applying it again gives back the original "
            "text. We use it to read the hidden flag."
        ),
        "filename": "CSPLUS (8).mp4",
        "tags": "csplusplus,ctf,general-skills,rot47,cipher,easy",
    },
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - Base58",
        "description": (
            "Easy challenge (25 points). Base58 is like Base64 but leaves out look-alike "
            "characters (0, O, I and l) and the symbols + and /. It is best known from "
            "Bitcoin addresses. We decode it to find the flag."
        ),
        "filename": "CSPLUS (9).mp4",
        "tags": "csplusplus,ctf,general-skills,base58,encoding,easy",
    },
    {
        "platform_slug": "csplusplus",
        "title": "CS++ CTF: General Skills - Double Encoded",
        "description": (
            "Easy challenge (20 points). The text was encoded two times, so one decoding "
            "step is not enough. We peel the layers off one by one, in the right order, to "
            "reach the flag."
        ),
        "filename": "CSPLUS (10).mp4",
        "tags": "csplusplus,ctf,general-skills,multi-layer,encoding,easy",
    },
    {
        "platform_slug": "hackthebox",
        "title": "Hack The Box: Starting Point - Meow (Part 1) Setting Up and Connecting",
        "description": (
            "We connect to the Hack The Box VPN, spawn the Starting Point machine called Meow and check that we can reach the target."
        ),
        "filename": "HACKTHEBOXMEOW (1).mp4",
        "tags": "hackthebox,starting-point,meow,easy,setup,vpn,connect",
    },
    {
        "platform_slug": "hackthebox",
        "title": "Hack The Box: Starting Point - Meow (Part 2) Scanning with Nmap",
        "description": (
            "We scan the target with Nmap to find which ports are open and which services are running on them."
        ),
        "filename": "HACKTHEBOXMEOW (2).mp4",
        "tags": "hackthebox,starting-point,meow,easy,nmap,scanning,enumeration",
    },
    {
        "platform_slug": "hackthebox",
        "title": "Hack The Box: Starting Point - Meow (Part 3) Finding the Telnet Service",
        "description": (
            "We read the Nmap result and find the Telnet service on port 23, then explain what Telnet is and why it is not safe."
        ),
        "filename": "HACKTHEBOXMEOW (3).mp4",
        "tags": "hackthebox,starting-point,meow,easy,telnet,port-23,enumeration",
    },
    {
        "platform_slug": "hackthebox",
        "title": "Hack The Box: Starting Point - Meow (Part 4) Connecting with Telnet",
        "description": (
            "We connect to the machine with the telnet command and see the login prompt."
        ),
        "filename": "HACKTHEBOXMEOW (4).mp4",
        "tags": "hackthebox,starting-point,meow,easy,telnet,login,linux",
    },
    {
        "platform_slug": "hackthebox",
        "title": "Hack The Box: Starting Point - Meow (Part 5) Trying Default Logins",
        "description": (
            "We try common default usernames. The machine has no password for the root account, which is a very common misconfiguration."
        ),
        "filename": "HACKTHEBOXMEOW (5).mp4",
        "tags": "hackthebox,starting-point,meow,easy,default-credentials,root,misconfiguration",
    },
    {
        "platform_slug": "hackthebox",
        "title": "Hack The Box: Starting Point - Meow (Part 6) Getting Access",
        "description": (
            "We log in as root and look around the system to confirm we have full access."
        ),
        "filename": "HACKTHEBOXMEOW (6).mp4",
        "tags": "hackthebox,starting-point,meow,easy,root,shell,linux",
    },
    {
        "platform_slug": "hackthebox",
        "title": "Hack The Box: Starting Point - Meow (Part 7) Capturing the Flag",
        "description": (
            "We find flag.txt, read it with cat, and submit it on Hack The Box to finish the machine."
        ),
        "filename": "HACKTHEBOXMEOW (7).mp4",
        "tags": "hackthebox,starting-point,meow,easy,flag,cat,submit",
    },
]
