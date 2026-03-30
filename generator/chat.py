import random
import numpy as np
from datetime import datetime, timedelta
import sys, os

def load_vocabulary(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('\n', ',').replace('\r', ',')
    words = [w.strip() for w in content.split(',') if w.strip()]
    if not words:
        print("WARNING: vocabulary.txt appears empty or unreadable.")
    return words

EMOJIS =  [
  "😀", "😂", "😂😂", "😍", "😎", "🤔", "😢", "😭", "😭💀",
  "🔥", "🚀", "🎯", "💡", "📚", "⚡", "🌍", "🎉", "🧠",
  "🥀", "🥺", "🤣", "🤡", "🥲", "👍", "👍👍"
]

MEMBERS = [
    {
        # ARYAN — The Chatterbox
        # Never shuts up. Sends rapid-fire short messages all day long,
        # Sends 5x more messages than anyone else.
        "name": "Aryan",
        "personality": "Chatterbox",
        "traits": {
            "chatterbox": 0.9,
            "hype": 0.6,
            "emoji": 0.3,
            "dry": 0.2,
            "essay": 0.1,
            "ghost": 0.0,
            "lurker": 0.0,
            "conversation_starter": 0.6,
            "night_owl": 0.2
        },
        "freq_weight": 5.0,
        "response_delay": (1, 3),
        "hour_weights": [0.3,0.2,0.1,0.1,0.1,0.2,0.4,0.7,1.0,1.2,1.5,1.5,
                         1.8,2.0,2.0,1.8,1.5,1.5,1.2,1.0,0.8,0.6,0.5,0.4],
        "msg_len_min": 2, "msg_len_max": 5,
        "streak_prob": 0.65, "min_streak": 2, "max_streak": 5,
        "post_streak_silence": None,
        "max_messages": 10, "window_minutes": 40,
    },

    {
        # AKSHIT — The Night Owl
        # Completely dead during the day. Comes alive after 10pm and peaks
        # around 1–2am. Sends medium-length messages 
        "name": "Akshit",
        "personality": "Night Owl",
        "traits": {
            "night_owl": 0.9,
            "essay": 0.2,
            "emoji": 0.5,
            "chatterbox": 0.2,
            "ghost": 0.2,
            "lurker": 0.2,
            "hype": 0.3,
            "dry": 0.2,
            "conversation_starter": 0.2
        },
        "freq_weight": 1.8,
        "response_delay": (5, 15),
        "hour_weights": [3.0,3.5,3.0,2.5,1.5,0.5,0.1,0.0,0.0,0.0,0.0,0.0,
                         0.0,0.0,0.0,0.0,0.0,0.3,0.5,0.8,1.0,1.5,2.5,3.0],
        "msg_len_min": 2, "msg_len_max": 10,
        "streak_prob": 0.15, "min_streak": 1, "max_streak": 2,
        "post_streak_silence": None,
        "max_messages": 6, "window_minutes": 60,
    },

    {
        # Yash — The Dry Texter
        # Man of few words. Replies with 1–3 words maximum — "lol", "ok",
        # "yeah fr", "nah". Never writes essays, barely uses emojis.
        "name": "Yash",
        "personality": "Dry Texter",
        "traits": {
            "dry": 0.95,
            "lurker": 0.3,
            "emoji": 0.1,
            "chatterbox": 0.1,
            "ghost": 0.2,
            "hype": 0.0,
            "essay": 0.0,
            "conversation_starter": 0.2,
            "night_owl": 0.2
        },
        "freq_weight": 2.5,
        "response_delay": (3, 10),
        "hour_weights": [0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.8,1.2,1.5,1.5,1.5,
                         1.5,1.5,1.5,1.5,1.2,1.0,0.8,0.5,0.3,0.2,0.1,0.0],
        "msg_len_min": 1, "msg_len_max": 3,
        "streak_prob": 0.20, "min_streak": 1, "max_streak": 3,
        "post_streak_silence": None,
        "max_messages": 5, "window_minutes": 45,
    },

    {
        # Shreya — The Essay Writer
        # When she replies, it's never less than a paragraph.
        # Slow to respond (she's composing a novel). Active mid-morning to
        # evening. Uses emojis to soften her walls of text.
        "name": "Shreya",
        "personality": "Essay Writer",
        "traits": {
            "essay": 0.95,
            "chatterbox": 0.1,
            "emoji": 0.5,
            "conversation_starter": 0.3,
            "ghost": 0.1,
            "lurker": 0.1,
            "hype": 0.2,
            "dry": 0.0,
            "night_owl": 0.3
        },
        "freq_weight": 1.0,
        "response_delay": (7, 30),
        "hour_weights": [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.5,1.0,1.5,1.8,
                         1.5,1.5,1.8,1.5,1.2,1.0,0.8,0.5,0.4,0.2,0.1,0.0],
        "msg_len_min": 20, "msg_len_max": 60,
        "streak_prob": 0.08, "min_streak": 1, "max_streak": 2,
        "post_streak_silence": None,
        "max_messages": 3, "window_minutes": 90,
    },

    {
        # DEV — The Ghoster
        # Appears out of nowhere, fires 4–7 messages in a burst, then
        # vanishes completely for hours. You never know when he'll show up.
        # After a streak, enforces a hard silence of 2–8 hours.
        "name": "Dev",
        "personality": "Ghoster",
        "traits": {
            "ghost": 0.95,
            "lurker": 0.4,
            "dry": 0.3,
            "chatterbox": 0.3,
            "essay": 0.2,
            "emoji": 0.1,
            "hype": 0.3,
            "conversation_starter": 0.1,
            "night_owl": 0.2
        },
        "freq_weight": 0.9,
        "response_delay": (5, 25),
        "hour_weights": [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,
                         0.8,1.2,1.5,1.8,2.0,2.0,1.8,1.5,1.2,0.8,0.5,0.2],
        "msg_len_min": 3, "msg_len_max": 12,
        "streak_prob": 0.70, "min_streak": 4, "max_streak": 7,
        "post_streak_silence": (120, 480),
        "max_messages": 8, "window_minutes": 30,
    },

    {
        # KAVYA — The Lurker
        # She's there. She's reading everything. She just… doesn't reply.
        # A response from Kavya is a rare event.
        "name": "Kavya",
        "personality": "Lurker",
        "traits": {
            "lurker": 0.95,
            "dry": 0.5,
            "emoji": 0.3,
            "ghost": 0.3,
            "chatterbox": 0.0,
            "essay": 0.0,
            "hype": 0.1,
            "conversation_starter": 0.0,
            "night_owl": 0.1
        },
        "freq_weight": 0.3,
        "response_delay": (30, 120),
        "hour_weights": [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.5,0.8,1.5,
                         1.5,1.0,0.8,0.5,0.3,0.2,0.1,0.0,0.0,0.0,0.0,0.0],
        "msg_len_min": 1, "msg_len_max": 4,
        "streak_prob": 0.05, "min_streak": 1, "max_streak": 1,
        "post_streak_silence": None,
        "max_messages": 2, "window_minutes": 60,
    },

    {
        # JOSHMITHA — The Conversation Starter
        # The group would be dead without her
        # replies fairly quickly, keeps the energy moving
        "name": "Joshmitha",
        "personality": "Conversation Starter",
        "traits": {
            "conversation_starter": 0.95,
            "chatterbox": 0.6,
            "hype": 0.4,
            "emoji": 0.6,
            "essay": 0.3,
            "ghost": 0.1,
            "lurker": 0.0,
            "dry": 0.2,
            "night_owl": 0.3
        },
        "freq_weight": 2.0,
        "response_delay": (2, 6),
        "hour_weights": [0.2,0.1,0.0,0.0,0.0,0.3,0.8,1.5,1.8,1.5,1.2,1.0,
                         1.5,1.8,1.5,1.2,1.0,1.2,1.5,1.8,1.5,1.0,0.8,0.5],
        "msg_len_min": 4, "msg_len_max": 18,
        "streak_prob": 0.20, "min_streak": 1, "max_streak": 3,
        "post_streak_silence": None,
        "max_messages": 7, "window_minutes": 45,
    },

    {
        # TANVI — The Emoji Queen + Hype Person
        # Every message has emojis. Every. Single. One. Doubles as the
        # never lurks. The chat feels quieter without her.
        # replies almost instantly 
        "name": "Tanvi",
        "personality": ["Emoji Queen", "Hype Person"],
        "traits": {
            "emoji": 0.95,
            "hype": 0.9,
            "chatterbox": 0.7,
            "conversation_starter": 0.5,
            "essay": 0.2,
            "ghost": 0.1,
            "lurker": 0.0,
            "dry": 0.0,
            "night_owl": 0.4
        },
        "freq_weight": 3.2,
        "response_delay": (0,3),
        "hour_weights": [0.5,0.3,0.1,0.0,0.0,0.1,0.3,0.5,0.8,1.0,1.2,1.2,
                         1.5,1.5,1.8,2.0,2.0,2.0,1.8,1.5,1.3,1.1,0.9,0.7],
        "msg_len_min": 3, "msg_len_max": 15,
        "streak_prob": 0.30, "min_streak": 1, "max_streak": 4,
        "post_streak_silence": None,
        "max_messages": 9, "window_minutes": 35,
    },
]
def generate_message(words, member):
    length = random.randint(member["msg_len_min"], member["msg_len_max"])

    # Always produce a plain string from the sampled words
    msg = " ".join(random.sample(words, k=length))

    if random.random() < member["traits"]["emoji"]:
        personality = member["personality"]
        emoji_queen = isinstance(personality, list) and "Emoji Queen" in personality
        if emoji_queen:
            n = random.randint(1, 4)
            emoji_part = random.choices(EMOJIS, k=n)
            # Mix emojis into the word tokens for a natural feel
            tokens = msg.split() + emoji_part
            random.shuffle(tokens)
            msg = " ".join(tokens)
        else:
            n = random.randint(1, 2)
            emoji_part = random.choices(EMOJIS, k=n)
            tokens = msg.split() + emoji_part
            random.shuffle(tokens)
            msg = " ".join(tokens)

    return msg

def get_random_hour(member):
    w = np.array(member["hour_weights"], dtype=float)
    total = w.sum()
    if total <= 0:
        return random.randint(0, 23)
    return int(np.random.choice(len(w), p=w / total))

def get_next_member(current_time, recent_msgs):
    """
    Select the next sender weighted by freq_weight * hour_weight.
    Applies a FATIGUE PENALTY if a member has sent too many messages
    in their personal fatigue window — prevents any one person from
    monopolising the chat for hours on end.

    recent_msgs: dict  name -> list of datetime objects (recent send times)
    """
    hour = current_time.hour
    weights = []
    for m in MEMBERS:
        base = m["freq_weight"] * m["hour_weights"][hour]

        # Count how many of this member's recent messages fall inside their window
        cutoff = current_time - timedelta(minutes=m["window_minutes"])
        msgs_in_window = sum(1 for t in recent_msgs[m["name"]] if t >= cutoff)

        # If they have hit or exceeded their fatigue limit, slash their weight
        # 0.05 multiplier means they CAN still send, just very unlikely
        if msgs_in_window >= m["max_messages"]:
            base *= 0.05

        weights.append(base)

    combined = np.array(weights, dtype=float)
    total = combined.sum()
    if total <= 0:                          # fallback: ignore fatigue
        combined = np.array([m["freq_weight"] for m in MEMBERS], dtype=float)
        total = combined.sum()
    return MEMBERS[int(np.random.choice(len(MEMBERS), p=combined / total))]

def time_gap(current_time):
    """
    Move the clock forward by a random gap.
    5%  → long silence (1 h – 48 h)  — group goes quiet
    25% → medium gap  (5 – 60 min)
    70% → quick reply (1 – 8 min)
    Time ONLY ever moves forward.
    """
    r = random.random()
    if r < 0.05:
        gap = random.randint(60, 2880)
    elif r < 0.30:
        gap = random.randint(5, 60)
    else:
        gap = random.randint(1, 8)
    return current_time + timedelta(minutes=gap)

def track_recent_messages(recent_msgs, name, ts):
    """Append ts to this member's recent send log (keep last 50 only)."""
    recent_msgs[name].append(ts)
    if len(recent_msgs[name]) > 50:
        recent_msgs[name].pop(0)


def generate_chat(vocabulary_path, output_path="chat.txt"):
    words = load_vocabulary(vocabulary_path)

    current_time = datetime(2024, 7, 22, 10, 0, 0)
    end_time     = datetime(2024, 11, 20, 23, 59, 59)

    messages = []

    # Track per-member "silent until" for the Ghoster's post-burst blackout.
    silent_until = {m["name"]: datetime.min for m in MEMBERS}

    # Track recent send timestamps per member for fatigue calculation.
    # Each entry is a list of datetimes of recent sends.
    recent_msgs = {m["name"]: [] for m in MEMBERS}

    while current_time <= end_time:

        # Always move the clock forward first
        current_time = time_gap(current_time)
        if current_time > end_time:
            break

        # Pick a sender weighted by activity at current hour + fatigue state
        member = get_next_member(current_time, recent_msgs)

        # Respect post-streak silence (Ghoster goes dark after a burst)
        if current_time < silent_until[member["name"]]:
            continue

        ts = current_time.strftime("%d/%m/%y, %H:%M")
        messages.append(f"{ts} - {member['name']}: {generate_message(words, member)}")
        track_recent_messages(recent_msgs, member["name"], current_time)

        # Streak logic — all follow-ups still move time forward
        if random.random() < member["streak_prob"]:
            streak_len = random.randint(member["min_streak"], member["max_streak"])
            for _ in range(streak_len):
                current_time += timedelta(minutes=random.randint(1, 4))
                if current_time > end_time:
                    break
                ts = current_time.strftime("%d/%m/%y, %H:%M")
                messages.append(
                    f"{ts} - {member['name']}: {generate_message(words, member)}"
                )
                track_recent_messages(recent_msgs, member["name"], current_time)

            # After the Ghoster's burst, enforce a hard silence window
            if member["post_streak_silence"]:
                lo, hi = member["post_streak_silence"]
                blackout_minutes = random.randint(lo, hi)
                silent_until[member["name"]] = current_time + timedelta(
                    minutes=blackout_minutes
                )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(messages))
    print(f"Generated {len(messages)} messages : {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 chat.py <vocabulary.txt>")
        sys.exit(1)
    out = sys.argv[2] if len(sys.argv) > 2 else "chat.txt"
    generate_chat(sys.argv[1], out)