"""
chat.py - WhatsApp Group Chat Generator
Group: IIT Bombay CS-108 Sem 2024

Usage: python chat.py <vocabulary.txt>
Output: chat.txt in current directory
"""

import random
import numpy as np
from datetime import datetime, timedelta
import sys, os

def load_vocabulary(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    words = [w.strip() for w in content.split(',') if w.strip()]
    return words

emojis = ['🤪','🫠','🤓','🫡','🤠','👽','🤖','👀','💀💀','😭😭','😂💀','💀🔥','💙','💜','🫶','🤝','👊','🤜🤛','✨']

# ── 8 CS-108 group members with distinct social personalities ──────────────
MEMBERS = [
    {
        "name": "Aryan",
        "personality": "Chatterbox",
        "freq_weight": 5.0,
        "hour_weights": [0.3,0.2,0.1,0.1,0.1,0.2,0.4,0.7,1.0,1.2,1.5,1.5,
                         1.8,2.0,2.0,1.8,1.5,1.5,1.2,1.0,0.8,0.6,0.5,0.4],
        "msg_len_min": 1, 
        "msg_len_max": 5,
        "streak_prob": 0.45, 
        "max_streak": 5,
        "emoji_prob": 0.12,
    },
    {
        "name": "Priya",
        "personality": "Night Owl",
        "freq_weight": 1.8,
        "hour_weights": [3.0,3.5,3.0,2.5,1.5,0.5,0.1,0.0,0.0,0.0,0.0,0.0,
                         0.0,0.0,0.0,0.0,0.0,0.3,0.5,0.8,1.0,1.5,2.5,3.0],
        "msg_len_min": 8, "msg_len_max": 30,
        "streak_prob": 0.15, "max_streak": 2,
        "emoji_prob": 0.20,
    },
    {
        "name": "Rohan",
        "personality": "One-Liner King",
        "freq_weight": 2.5,
        "hour_weights": [0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.8,1.2,1.5,1.5,1.5,
                         1.5,1.5,1.5,1.5,1.2,1.0,0.8,0.5,0.3,0.2,0.1,0.0],
        "msg_len_min": 1, "msg_len_max": 3,
        "streak_prob": 0.20, "max_streak": 3,
        "emoji_prob": 0.25,
    },
    {
        "name": "Sneha",
        "personality": "Essay Writer",
        "freq_weight": 1.0,
        "hour_weights": [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.5,1.0,1.5,1.8,
                         1.5,1.5,1.8,1.5,1.2,1.0,0.8,0.5,0.3,0.1,0.0,0.0],
        "msg_len_min": 20, "msg_len_max": 60,
        "streak_prob": 0.08, "max_streak": 1,
        "emoji_prob": 0.10,
    },
    {
        "name": "Dev",
        "personality": "Ghoster",
        "freq_weight": 0.9,
        "hour_weights": [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,
                         0.8,1.2,1.5,1.8,2.0,2.0,1.8,1.5,1.2,0.8,0.5,0.2],
        "msg_len_min": 3, "msg_len_max": 12,
        # PERSONALITY: Sends 4-7 consecutive messages then vanishes (Ghoster)
        "streak_prob": 0.65, "max_streak": 7,
        "emoji_prob": 0.08,
    },
    {
        "name": "Kavya",
        "personality": "Lurker",
        "freq_weight": 0.3,
        # PERSONALITY: Barely ever messages; low frequency weight
        "hour_weights": [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.5,0.8,1.5,
                         1.5,1.0,0.8,0.5,0.3,0.2,0.1,0.0,0.0,0.0,0.0,0.0],
        "msg_len_min": 1, "msg_len_max": 4,
        "streak_prob": 0.05, "max_streak": 1,
        "emoji_prob": 0.30,
    },
    {
        "name": "Mihir",
        "personality": "Conversation Starter",
        "freq_weight": 2.0,
        # Active broadly throughout the day; breaks long silences
        "hour_weights": [0.2,0.1,0.0,0.0,0.0,0.3,0.8,1.5,1.8,1.5,1.2,1.0,
                         1.5,1.8,1.5,1.2,1.0,1.2,1.5,1.8,1.5,1.0,0.8,0.5],
        "msg_len_min": 6, "msg_len_max": 18,
        "streak_prob": 0.20, "max_streak": 3,
        "emoji_prob": 0.15,
    },
    {
        "name": "Tanvi",
        "personality": "Emoji Queen",
        "freq_weight": 2.8,
        "hour_weights": [0.2,0.1,0.1,0.0,0.0,0.1,0.3,0.5,0.8,1.0,1.2,1.2,
                         1.5,1.5,1.8,2.0,2.0,2.0,1.8,1.5,1.2,1.0,0.7,0.4],
        "msg_len_min": 3, "msg_len_max": 15,
        "streak_prob": 0.30, "max_streak": 4,
        # PERSONALITY: Adds 1-3 emojis to almost every message
        "emoji_prob": 0.95,
    },
]

def generate_message(words, member):
    """Build a message with vocabulary words, respecting personality length."""
    length = random.randint(member["msg_len_min"], member["msg_len_max"])
    msg = " ".join(random.choice(words) for _ in range(length))
    if random.random() < member["emoji_prob"]:
        n = random.randint(1, 3) if member["personality"] == "Emoji Queen" else 1
        for _ in range(n):
            msg += " " + random.choice(emojis)
    return msg

def get_random_hour(member):
    """Sample an active hour weighted by this member's activity pattern."""
    w = np.array(member["hour_weights"], dtype=float)
    total = w.sum()
    if total == 0:
        return random.randint(0, 23)
    return int(np.random.choice(24, p=w / total))

def generate_chat(vocabulary_path, output_path="chat.txt", num_messages=900):
    """Generate the full chat simulation and write to output_path."""
    words = load_vocabulary(vocabulary_path)
    print(f"Loaded {len(words)} vocabulary words.")

    current_time = datetime(2024, 7, 22, 10, 0, 0)
    end_time     = datetime(2024, 11, 20, 23, 59, 59)

    freq_probs = np.array([m["freq_weight"] for m in MEMBERS], dtype=float)
    freq_probs /= freq_probs.sum()

    messages = []

    while len(messages) < num_messages and current_time < end_time:
        member = MEMBERS[int(np.random.choice(len(MEMBERS), p=freq_probs))]

        # Time gap with realistic distribution
        r = random.random()
        if r < 0.05:
            gap = random.randint(60, 2880)   # long silence
        elif r < 0.30:
            gap = random.randint(5, 60)
        else:
            gap = random.randint(1, 8)

        current_time += timedelta(minutes=gap)
        if current_time > end_time:
            break

        # Snap to this member's active hours
        hour = get_random_hour(member)
        current_time = current_time.replace(hour=hour, minute=random.randint(0, 59))

        ts = current_time.strftime("%d/%m/%y, %H:%M")
        messages.append(f"{ts} - {member['name']}: {generate_message(words, member)}")

        # Streak / Ghoster: same member fires multiple messages in a row
        if random.random() < member["streak_prob"]:
            for _ in range(random.randint(1, member["max_streak"])):
                current_time += timedelta(minutes=random.randint(1, 4))
                ts = current_time.strftime("%d/%m/%y, %H:%M")
                messages.append(f"{ts} - {member['name']}: {generate_message(words, member)}")
                if len(messages) >= num_messages:
                    break

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(messages))
    print(f"Generated {len(messages)} messages → {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chat.py <vocabulary.txt>")
        sys.exit(1)
    out = sys.argv[2] if len(sys.argv) > 2 else "chat.txt"
    generate_chat(sys.argv[1], out)
