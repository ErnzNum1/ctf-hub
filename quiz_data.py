"""
Questions for the "Which platform should I start with?" quiz.

Each answer adds points to one or more platforms. The platform with the most
points is the recommendation. You can edit the questions and points freely.

Platform names used in the points: tryhackme, hackthebox, portswigger, csplusplus
"""

QUESTIONS = [
    {
        "id": "level",
        "text": "How much do you know about computers and hacking right now?",
        "answers": [
            {"id": "zero", "text": "Almost nothing. I'm brand new.",
             "points": {"csplusplus": 3, "tryhackme": 2}},
            {"id": "some", "text": "I know the basics (internet, a bit of Linux or coding).",
             "points": {"tryhackme": 3, "portswigger": 2, "csplusplus": 1}},
            {"id": "good", "text": "I'm comfortable with Linux, networking and tools.",
             "points": {"hackthebox": 3, "portswigger": 2}},
        ],
    },
    {
        "id": "money",
        "text": "What about money?",
        "answers": [
            {"id": "free", "text": "I only want free stuff.",
             "points": {"portswigger": 3, "csplusplus": 3, "tryhackme": 1, "hackthebox": 1}},
            {"id": "paid", "text": "I can pay a little if it is worth it.",
             "points": {"tryhackme": 2, "hackthebox": 2}},
        ],
    },
    {
        "id": "goal",
        "text": "What do you want to practice?",
        "answers": [
            {"id": "general", "text": "A bit of everything. I want to explore cyber security.",
             "points": {"tryhackme": 3, "csplusplus": 1}},
            {"id": "web", "text": "Websites (bug bounty, web hacking).",
             "points": {"portswigger": 4, "tryhackme": 1}},
            {"id": "machines", "text": "Hacking realistic machines like a real pentester.",
             "points": {"hackthebox": 4, "tryhackme": 1}},
            {"id": "school", "text": "Simple CTF challenges for school or a first try.",
             "points": {"csplusplus": 4}},
        ],
    },
    {
        "id": "style",
        "text": "How do you like to learn?",
        "answers": [
            {"id": "guided", "text": "Step by step, with explanations and questions.",
             "points": {"tryhackme": 3, "portswigger": 2, "csplusplus": 1}},
            {"id": "alone", "text": "Figure it out myself with little help.",
             "points": {"hackthebox": 3}},
            {"id": "browser", "text": "Everything inside my browser, nothing to install.",
             "points": {"csplusplus": 3, "tryhackme": 2}},
        ],
    },
]

# Why we recommend each platform (shown on the result page).
REASONS = {
    "tryhackme": "It teaches step by step with guided rooms, so you always know what to do next.",
    "hackthebox": "It gives you realistic machines with little hand-holding, great for building real skill.",
    "portswigger": "It is free and the best place to learn how web vulnerabilities really work.",
    "csplusplus": "It runs in your browser with simple challenges, a gentle and safe first CTF.",
}
