import random
import numpy as np
from datetime import datetime, timedelta
import sys
 
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
            "conversation_starter": 0.15,
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
            "chatterbox": 0.2,
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
        "freq_weight": 1.2,
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
            "essay": 0.2,
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
            "conversation_starter": 0.25,
            "essay": 0.2,
            "ghost": 0.1,
            "lurker": 0.0,
            "dry": 0.0,
            "night_owl": 0.4
        },
        "freq_weight": 3.2,
        "response_delay": (0,2),
        "hour_weights": [0.5,0.3,0.1,0.0,0.0,0.1,0.3,0.5,0.8,1.0,1.2,1.2,
                         1.5,1.5,1.8,2.0,2.0,2.0,1.8,1.5,1.3,1.1,0.9,0.7],
        "msg_len_min": 3, "msg_len_max": 15,
        "streak_prob": 0.30, "min_streak": 1, "max_streak": 4,
        "post_streak_silence": None,
        "max_messages": 9, "window_minutes": 35,
    },
]

def generate_message(words, member):
    traits = member["traits"]

    length = random.randint(member["msg_len_min"], member["msg_len_max"])

    # essay writers sometimes go longer than their max (30% chance of 1.5x words)
    if traits.get("essay", 0) > 0.5 and random.random() < 0.3:
        length = int(length * 1.5)

    # dry texters always send the shortest possible message, ignoring the random length
    if traits.get("dry", 0) > 0.7:
        length = member["msg_len_min"]

    msg = " ".join(random.sample(words, k=length))

    # add emojis based on the member's emoji trait probability
    if random.random() < traits["emoji"]:
        personality = member["personality"]
        # emoji queen sends more emojis per message than everyone else
        emoji_queen = isinstance(personality, list) and "Emoji Queen" in personality
        n = random.randint(1, 4) if emoji_queen else random.randint(1, 2)
        emoji_part = random.choices(EMOJIS, k=n)
        # shuffle so emojis are mixed into the message, not just at the end
        tokens = msg.split() + emoji_part
        random.shuffle(tokens)
        msg = " ".join(tokens)

    return msg


def get_next_member(current_time, recent_msgs, last_message_time=None):
    hour = current_time.hour

    all_recent = [t for name in recent_msgs for t in recent_msgs[name]]
    last_ts = max(all_recent) if all_recent else None

    cutoff_10 = current_time - timedelta(minutes=10)
    recent_activity = sum(1 for name in recent_msgs for t in recent_msgs[name] if t >= cutoff_10)

    # track how long the chat has been silent so we can boost conversation starters
    silence_minutes = 0
    if last_message_time is not None:
        silence_minutes = (current_time - last_message_time).total_seconds() / 60

    weights = []
    for m in MEMBERS:
        # start with base weight: frequency * how active this person is at this hour
        base = m["freq_weight"] * m["hour_weights"][hour]

        # hype people are more likely to reply when the chat is already active
        if m["traits"].get("hype", 0) > 0.7 and recent_activity >= 2:
            base *= 1.4

        # after a long silence, conversation starters get a big weight boost
        if silence_minutes >= 60:
            cs = m["traits"].get("conversation_starter", 0)
            base *= (1 + cs * 15)

        # if someone already sent too many messages in their window, reduce their weight a lot
        cutoff = current_time - timedelta(minutes=m["window_minutes"])
        msgs_in_window = sum(1 for t in recent_msgs[m["name"]] if t >= cutoff)
        if msgs_in_window >= m["max_messages"]:
            base *= 0.05

        # reduce chance of the same person speaking twice in a row
        if last_ts and recent_msgs[m["name"]] and recent_msgs[m["name"]][-1] == last_ts:
            base *= 0.4

        weights.append(base)

    combined = np.array(weights, dtype=float)
    total = combined.sum()
    if total <= 0:
        combined = np.array([m["freq_weight"] for m in MEMBERS], dtype=float)
        total = combined.sum()
    return MEMBERS[int(np.random.choice(len(MEMBERS), p=combined / total))]

def time_gap(current_time, member=None):
    """
    Move the clock forward by a random gap.
    5%  → long silence (1h – 48h)   — group goes quiet
    25% → medium gap  (5 – 60 min)  — someone takes a while to reply
    70% → quick reply                — uses member's response_delay
    response_delay values are treated as (min, max) scaled by 10 into seconds
    e.g. (1, 3) → 10s–30s,  (30, 120) → 300s–1200s
    Time ONLY ever moves forward.
    """
    r = random.random()
    if r < 0.05:
        gap = timedelta(minutes=random.randint(60, 2880))
    elif r < 0.30:
        gap = timedelta(minutes=random.randint(5, 60))
    else:
        if member and "response_delay" in member:
            lo, hi = member["response_delay"]
        else:
            lo, hi = 15, 90
        gap = timedelta(seconds=random.randint(lo * 10, hi * 10))
    return current_time + gap


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
    # silent_until blocks a member from sending after their streak ends (used by Dev the Ghoster)
    silent_until    = {m["name"]: datetime.min for m in MEMBERS}
    recent_msgs     = {m["name"]: [] for m in MEMBERS}
    last_message_time = None

    while current_time <= end_time:
        current_time = time_gap(current_time, None)
        if current_time > end_time:
            break

        member = get_next_member(current_time, recent_msgs, last_message_time)

        # skip this member if they are in their post-streak silence period
        if current_time < silent_until[member["name"]]:
            continue

        ts = current_time.strftime("%d/%m/%y, %H:%M")
        messages.append(f"{ts} - {member['name']}: {generate_message(words, member)}")
        track_recent_messages(recent_msgs, member["name"], current_time)
        last_message_time = current_time

        # streak: same person sends multiple messages in a row with very short gaps
        if random.random() < member["streak_prob"]:
            streak_len = random.randint(member["min_streak"], member["max_streak"])
            for _ in range(streak_len):
                current_time += timedelta(seconds=random.randint(5, 45))
                if current_time > end_time:
                    break
                if current_time < silent_until[member["name"]]:
                    break
                ts = current_time.strftime("%d/%m/%y, %H:%M")
                messages.append(
                    f"{ts} - {member['name']}: {generate_message(words, member)}"
                )
                track_recent_messages(recent_msgs, member["name"], current_time)
                last_message_time = current_time

            # after the streak, force the ghoster to go silent for a few hours
            if member["post_streak_silence"]:
                lo, hi = member["post_streak_silence"]
                blackout_minutes = random.randint(lo, hi)
                silent_until[member["name"]] = current_time + timedelta(minutes=blackout_minutes)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(messages))
    print(f"Generated {len(messages)} messages : {output_path}")
       

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 chat.py <vocabulary.txt>")
        sys.exit(1)
    out = sys.argv[2] if len(sys.argv) > 2 else "chat.txt"
    generate_chat(sys.argv[1], out)