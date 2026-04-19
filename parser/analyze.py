from datetime import datetime
import emoji
import json
import sys

MEMBERS = ["Aryan", "Akshit", "Yash", "Shreya", "Dev", "Kavya", "Joshmitha", "Tanvi"]

CHAT_FILE = sys.argv[1] if len(sys.argv) > 1 else "chat.txt"

# -----------------------------------------------stat 1 -----------------------------------------------------------------
# here we are fining the total no of messages
def total_messages():
    f=open(CHAT_FILE, encoding='utf-8')
    counts = {
        "Aryan" : 0,
        "Akshit" : 0 ,
        "Yash" : 0,
        "Shreya" : 0, 
        "Dev" : 0,
        "Kavya" : 0, 
        "Joshmitha" : 0,
        "Tanvi" : 0
    }
    for line in f:
        words=line.strip().split()
        if len(words) < 4:
            continue
        name=words[3][:-1]
        if name in counts:
            counts[name]=counts[name]+1
    return counts

# -----------------------------------------------stat 2 -----------------------------------------------------------------
# word count including the emoji (counting emoji as word)
def word_count():
    f=open(CHAT_FILE, encoding='utf-8')
    count=0
    val=0
    counts = {
        "Aryan" : 0,
        "Akshit" : 0 ,
        "Yash" : 0,
        "Shreya" : 0, 
        "Dev" : 0,
        "Kavya" : 0, 
        "Joshmitha" : 0,
        "Tanvi" : 0
    }
    for line in f:
        words=line.strip().split()
        if len(words) < 4:
            continue
        count=len(words)-4
        name=words[3][:-1]
        if name in counts:
            counts[name]= counts[name]+count
    return counts
r=word_count()
# print(f"word count is {r}")

# -----------------------------------------------stat 3 -----------------------------------------------------------------
# person who is active at night time (12am–4am)
def night_owl():
    f = open(CHAT_FILE, encoding='utf-8')
    counts_msgs_night = {
        "Aryan": 0,
        "Akshit": 0,
        "Yash": 0,
        "Shreya": 0,
        "Dev": 0,
        "Kavya": 0,
        "Joshmitha": 0,
        "Tanvi": 0
    }
    for line in f:
        words = line.strip().split()
        if len(words) < 4:
            continue
        time = words[1]
        try:
            hour = int(time.split(":")[0])
        except:
            continue
        if 0 <= hour < 4:
            name = words[3][:-1]
            if name in counts_msgs_night:
                counts_msgs_night[name] = counts_msgs_night[name] + 1
    f.close()
    return counts_msgs_night
list=night_owl()
# print(f"the night owl is {list}")

# -----------------------------------------------stat 4 -----------------------------------------------------------------
def ghost():
    f = open(CHAT_FILE, encoding='utf-8')
    # A message is "ghosted" if the next message from someone else arrives 10+ min later.
    # Definition: direct reply = next message from a different person within 10 minutes.
    ghosted_counts = {n: 0 for n in MEMBERS}
    msg_counts = {n: 0 for n in MEMBERS}
    time_span = 10  # minutes
    prev_sender = None
    prev_dt = None
    for line in f:
        words = line.strip().split()
        if len(words) < 4:
            continue
        sender = words[3][:-1]
        if sender not in MEMBERS:
            continue
        msg_counts[sender] += 1
        try:
            dt = datetime.strptime(f"{words[0][:-1]} {words[1]}", "%d/%m/%y %H:%M")
        except:
            continue
        if prev_sender is not None and sender != prev_sender:
            time_diff = (dt - prev_dt).total_seconds() / 60
            if time_diff > time_span:
                ghosted_counts[prev_sender] += 1
        prev_sender = sender
        prev_dt = dt
    f.close()
    return ghosted_counts, msg_counts
ghosted, msg = ghost()
for person in msg:
    if msg[person] > 0:
        percentage = (ghosted[person] / msg[person]) * 100
        # print(f"{person}: ghosted {ghosted[person]}/{msg[person]} = {percentage:.2f}%")

# -----------------------------------------------stat 5 -----------------------------------------------------------------

def conversation_starter():
    f = open(CHAT_FILE, encoding='utf-8')
    # Counts times a person sent the first message after a 60+ minute silence.
    # Definition: long silence = gap of 60 minutes or more with no messages.
    starter_counts = {n: 0 for n in MEMBERS}
    prev_dt = None
    for line in f:
        words = line.strip().split()
        if len(words) < 4:
            continue
        sender = words[3][:-1]
        if sender not in MEMBERS:
            continue
        try:
            dt = datetime.strptime(f"{words[0][:-1]} {words[1]}", "%d/%m/%y %H:%M")
        except:
            continue
        if prev_dt is not None:
            time_diff = (dt - prev_dt).total_seconds() / 60
            if time_diff >= 60:
                starter_counts[sender] += 1
        prev_dt = dt
    f.close()
    return starter_counts
starts=conversation_starter()
# print(f"the conversation starter is {starts}")

# -----------------------------------------------stat 6 -----------------------------------------------------------------
def most_used_emoji():
    f=open(CHAT_FILE, encoding='utf-8')
    emoji_counts = {
        "Aryan": {},
        "Akshit": {},
        "Yash": {},
        "Shreya": {},
        "Dev": {},
        "Kavya": {},
        "Joshmitha": {},
        "Tanvi": {}
    }
    for line in f:
        words=line.strip().split()
        name=words[3][:-1]
        for word in words[4:]:
            if emoji.is_emoji(word):
                if word not in emoji_counts[name]:
                    emoji_counts[name][word]=0
                emoji_counts[name][word]=emoji_counts[name][word]+1
    result={}
    for name in emoji_counts:
        sorted_emojis=sorted(emoji_counts[name].items(), key=lambda x:x[1], reverse=True)
        result[name]=sorted_emojis[:3]
    return result
top_emojis=most_used_emoji()
# print(f"most used emojis are {top_emojis}")

# -----------------------------------------------stat 7 --------------------------------------------------------------
def busiest_day():
    f=open(CHAT_FILE, encoding='utf-8')
    count={}
    for line in f: 
        words=line.strip().split()
        date=words[0][:-1]
        if date not in count:
            count[date]=0
        count[date]=count[date]+1
    sorted_counts=sorted(count.items(), key=lambda x:x[1], reverse=True)
    return sorted_counts[0]
busyday=busiest_day()
# print(f"the busiest day is: {busyday}")

# -----------------------------------------------stat 8 -----------------------------------------------------------------
def longest_silence():
    f=open(CHAT_FILE, encoding='utf-8')
    prev_dt=None
    max_gap=0
    gap_start=None
    gap_end=None
    for line in f:
        words=line.strip().split()
        if len(words) < 4:
            continue
        dt=datetime.strptime(f"{words[0][:-1]} {words[1]}", "%d/%m/%y %H:%M")
        if prev_dt is not None:
            diff=(dt-prev_dt).total_seconds()
            if diff>max_gap:
                max_gap=diff
                gap_start=prev_dt
                gap_end=dt
        prev_dt=dt
    hours=round(max_gap/3600, 2)
    return {"hours": hours, "days": round(hours/24, 2), "start": gap_start.strftime("%d/%m/%y %H:%M"), "end": gap_end.strftime("%d/%m/%y %H:%M")}
silence=longest_silence()
# print(f"the longest silence is {silence}")

# -----------------------------------------------stat 9 ----------------------------------------------------------------------
# only counts if next message is from someone else within 60 min
def avg_response_time():
    f=open(CHAT_FILE, encoding='utf-8')
    times={
        "Aryan": [],
        "Akshit": [],
        "Yash": [],
        "Shreya": [],
        "Dev": [],
        "Kavya": [],
        "Joshmitha": [],
        "Tanvi": []
    }
    prev_sender=None
    prev_dt=None
    for line in f:
        words=line.strip().split()
        if len(words) < 4:
            continue
        sender=words[3][:-1]
        dt=datetime.strptime(f"{words[0][:-1]} {words[1]}", "%d/%m/%y %H:%M")
        if prev_sender is not None and sender != prev_sender:
            gap=(dt-prev_dt).total_seconds()/60
            if gap<=60:
                times[prev_sender].append(gap)
        prev_sender=sender
        prev_dt=dt
    result={}
    for name in times:
        t=sorted(times[name])
        if t:
            mid=len(t)//2
            result[name]=round((t[mid-1]+t[mid])/2 if len(t)%2==0 else t[mid], 2)
        else:
            result[name]=None
    return result
response=avg_response_time()
# print(f"avg response time is {response}")

# -----------------------------------------------stat 10 -----------------------------------------------------------------
def hype_person():
    f=open(CHAT_FILE, encoding='utf-8')
    times={
        "Aryan": [],
        "Akshit": [],
        "Yash": [],
        "Shreya": [],
        "Dev": [],
        "Kavya": [],
        "Joshmitha": [],
        "Tanvi": []
    }
    prev_sender=None
    prev_dt=None
    for line in f:
        words=line.strip().split()
        if len(words) < 4:
            continue
        sender=words[3][:-1]
        dt=datetime.strptime(f"{words[0][:-1]} {words[1]}", "%d/%m/%y %H:%M")
        if prev_sender is not None and sender != prev_sender:
            gap=(dt-prev_dt).total_seconds()/60
            if gap<=60:
                times[sender].append(gap)
        prev_sender=sender
        prev_dt=dt
    avgs={}
    for name in times:
        t=times[name]
        avgs[name]=round(sum(t)/len(t), 2) if t else None
    return avgs
hype=hype_person()
# print(f"the hype person is {hype}")

# -----------------------------------------------stat 11 ----------------------------------------------------------------------
# if no one replies within 60 min after your message, you get 1 kill point
def conversation_killer():
    kill_counts={
        "Aryan": 0,
        "Akshit": 0,
        "Yash": 0,
        "Shreya": 0,
        "Dev": 0,
        "Kavya": 0,
        "Joshmitha": 0,
        "Tanvi": 0
    }
    msg_counts={
        "Aryan": 0,
        "Akshit": 0,
        "Yash": 0,
        "Shreya": 0,
        "Dev": 0,
        "Kavya": 0,
        "Joshmitha": 0,
        "Tanvi": 0
    }
    lines=open(CHAT_FILE, encoding='utf-8').readlines()
    for i in range(len(lines)):
        words=lines[i].strip().split()
        if len(words) < 4:
            continue
        sender=words[3][:-1]
        msg_counts[sender]=msg_counts[sender]+1
        dt=datetime.strptime(f"{words[0][:-1]} {words[1]}", "%d/%m/%y %H:%M")
        if i+1 < len(lines):
            nxt=lines[i+1].strip().split()
            next_dt=datetime.strptime(f"{nxt[0][:-1]} {nxt[1]}", "%d/%m/%y %H:%M")
            gap=(next_dt-dt).total_seconds()/60
            if gap>=60:
                kill_counts[sender]=kill_counts[sender]+1
        else:
            kill_counts[sender]=kill_counts[sender]+1
    per_person={}
    for name in MEMBERS:
        total=msg_counts[name]
        kills=kill_counts[name]
        per_person[name]={"kills": kills, "total": total, "score": round((kills/total)*100, 2) if total>0 else 0.0}
    return per_person
killer=conversation_killer()
# print(f"the conversation killer is {killer}")



# -----------------------------------------------ghoster score -----------------------------------------------------------------
# Measures burst-then-vanish behaviour: high std-dev of gaps between your own consecutive messages.
# Someone who sends 5 msgs in 30s then goes silent for 3h scores very high; someone active all day scores low.
def ghoster_score():
    from datetime import datetime
    import math
    lines = open(CHAT_FILE, encoding='utf-8').readlines()
    own_gaps = {n: [] for n in MEMBERS}   # gaps (minutes) between consecutive messages by same person

    prev_sender = None
    prev_dt = None
    for line in lines:
        words = line.strip().split()
        if len(words) < 4:
            continue
        sender = words[3][:-1]
        if sender not in MEMBERS:
            prev_sender = sender
            prev_dt = None
            continue
        dt = datetime.strptime(f"{words[0][:-1]} {words[1]}", "%d/%m/%y %H:%M")
        if prev_sender == sender and prev_dt is not None:
            gap = (dt - prev_dt).total_seconds() / 60
            own_gaps[sender].append(gap)
        prev_sender = sender
        prev_dt = dt

    scores = {}
    for name in MEMBERS:
        gaps = own_gaps[name]
        if len(gaps) < 5:
            scores[name] = 0.0
            continue
        mean = sum(gaps) / len(gaps)
        variance = sum((g - mean) ** 2 for g in gaps) / len(gaps)
        scores[name] = round(math.sqrt(variance), 2)   # std-dev in minutes — higher = more bursty/ghosty
    return scores

def overall_emoji_count():
    f=open(CHAT_FILE, encoding='utf-8')
    emoji_counts={}
    for line in f: 
        emojis=[c for c in line if c in emoji.EMOJI_DATA]
        for e in emojis:
            emoji_counts[e]=emoji_counts.get(e,0)+1 
    f.close()
    sorted_emojis=sorted(emoji_counts.items(),key=lambda x:x[1], reverse=True) 
    return sorted_emojis


total_msgs       = total_messages()
words            = word_count()
owls             = night_owl()
ghosted, msg_cnt = ghost()
starters         = conversation_starter()
top_emojis       = most_used_emoji()
busy             = busiest_day()
silence          = longest_silence()
response         = avg_response_time()
hype             = hype_person()
killer           = conversation_killer()
ghoster          = ghoster_score()
overall_emojis = overall_emoji_count()

# ghost_pct = (ghosted / msg_cnt) * 100
ghost_pct = {}
for person in MEMBERS:
    if msg_cnt[person] > 0:
        ghost_pct[person] = round((ghosted[person] / msg_cnt[person]) * 100, 2)
    else:
        ghost_pct[person] = 0.0

# -----------------------------------------------derived / pre-computed fields for JS ---------------------------------

# sorted arrays (JS no longer needs to sort at render time)
total_msgs_sorted   = sorted(total_msgs.items(),   key=lambda x: x[1], reverse=True)
word_count_sorted   = sorted(words.items(),         key=lambda x: x[1], reverse=True)
night_owl_sorted    = sorted(owls.items(),          key=lambda x: x[1], reverse=True)
ghost_pct_sorted    = sorted(ghost_pct.items(),     key=lambda x: x[1], reverse=True)
starters_sorted     = sorted(starters.items(),      key=lambda x: x[1], reverse=True)
hype_sorted         = sorted([(k, v) for k, v in hype.items() if v is not None], key=lambda x: x[1])
killer_sorted       = sorted(killer.items(),        key=lambda x: x[1]["score"], reverse=True)

# bar chart percentages (JS no longer needs to compute val/max*100)
_max_msgs   = total_msgs_sorted[0][1]
_max_words  = word_count_sorted[0][1]
_max_owls   = night_owl_sorted[0][1]
_max_ghost  = ghost_pct_sorted[0][1]
_max_starts = starters_sorted[0][1]
_max_hype   = hype_sorted[-1][1]

total_msgs_pct  = {n: round((v / _max_msgs)   * 100, 1) for n, v in total_msgs.items()}
word_count_pct  = {n: round((v / _max_words)  * 100, 1) for n, v in words.items()}
night_owl_pct   = {n: round((v / _max_owls)   * 100, 1) if _max_owls > 0 else 0.0 for n, v in owls.items()}
ghost_pct_pct   = {n: round((v / _max_ghost)  * 100, 1) if _max_ghost > 0 else 0.0 for n, v in ghost_pct.items()}
starters_pct    = {n: round((v / _max_starts) * 100, 1) if _max_starts > 0 else 0.0 for n, v in starters.items()}
hype_pct        = {n: round((v / _max_hype)   * 100, 1) for n, v in hype.items() if v is not None}

# avg response time normalization for bubble sizing (norm 0-1, and pixel size 68-112)
_resp_vals  = [v for v in response.values() if v is not None]
_resp_min   = min(_resp_vals) if _resp_vals else 0
_resp_max   = max(_resp_vals) if _resp_vals else 1
response_normalized = {}
response_bubble_size = {}
for name, val in response.items():
    if val is not None:
        norm = (val - _resp_min) / (_resp_max - _resp_min + 0.01)
        response_normalized[name]   = round(norm, 4)
        response_bubble_size[name]  = round(68 + norm * 44)
    else:
        response_normalized[name]   = None
        response_bubble_size[name]  = None

# words per message
words_per_message = {
    n: round(words[n] / total_msgs[n], 1) if total_msgs[n] > 0 else 0
    for n in MEMBERS
}

# active member threshold (30% of max messages) used for hype/personality logic
active_member_threshold = round(_max_msgs * 0.3)

# personality labels — mirrors getPersonality() logic in app.js exactly
_max_night    = max(owls.values())
_max_wpm      = max(words_per_message.values())
_max_starts_v = max(starters.values())
_max_ghost_v  = max(ghost_pct.values())
_max_killer_v = max(v["score"] for v in killer.values())
_max_ghoster_v = max(ghoster.values())
_min_msgs_v   = min(total_msgs.values())
_active_hype  = [(n, v) for n, v in hype.items() if v is not None and total_msgs[n] >= active_member_threshold]
_min_hype_v   = min(v for _, v in _active_hype) if _active_hype else None

_min_wpm = min(words_per_message.values())

# total emojis sent per person (sum of their top_emojis counts)
_emoji_totals = {n: sum(c for _, c in top_emojis[n]) for n in MEMBERS}
_max_emoji_total = max(_emoji_totals.values())

_personality_map = {
    "Chatterbox":          {"label": "The Chatterbox",           "emoji": "💬"},
    "DryTexter":           {"label": "The Dry Texter",           "emoji": "🪨"},
    "NightOwl":            {"label": "The Night Owl",            "emoji": "🦉"},
    "EmojiQueen":          {"label": "Emoji Queen",              "emoji": "👑"},
    "HypePerson":          {"label": "The Hype Person",          "emoji": "⚡"},
    "EssayWriter":         {"label": "The Essay Writer",         "emoji": "📝"},
    "ConversationStarter": {"label": "The Conversation Starter", "emoji": "🚀"},
    "Ghost":               {"label": "The Ghoster",              "emoji": "👻"},
    "Killer":              {"label": "The Killer",               "emoji": "💀"},
    "Lurker":              {"label": "The Lurker",               "emoji": "👁️"},
    "Regular":             {"label": "The Regular",              "emoji": "😎"},
}

# returns a list so dual-personality members (Tanvi) can have two badges
def _get_personality(name):
    labels = []
    if total_msgs[name] == _max_msgs:
        labels.append(_personality_map["Chatterbox"])
    if words_per_message[name] == _min_wpm:
        labels.append(_personality_map["DryTexter"])
    if owls[name] == _max_night:
        labels.append(_personality_map["NightOwl"])
    if _emoji_totals[name] == _max_emoji_total:
        labels.append(_personality_map["EmojiQueen"])
    if (hype[name] is not None and total_msgs[name] >= active_member_threshold
            and _min_hype_v is not None and abs(hype[name] - _min_hype_v) < 0.001):
        labels.append(_personality_map["HypePerson"])
    if words_per_message[name] == _max_wpm:
        labels.append(_personality_map["EssayWriter"])
    if starters[name] == _max_starts_v:
        labels.append(_personality_map["ConversationStarter"])
    if ghoster[name] == _max_ghoster_v:
        labels.append(_personality_map["Ghost"])
    if total_msgs[name] == _min_msgs_v:
        labels.append(_personality_map["Lurker"])
    if killer[name]["score"] == _max_killer_v:
        labels.append(_personality_map["Killer"])
    return labels if labels else [_personality_map["Regular"]]

personality = {name: _get_personality(name) for name in MEMBERS}

# ranks (1-based) for each stat used in profile cards
def _ranks(d, reverse=True):
    sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=reverse)
    return {name: i + 1 for i, (name, _) in enumerate(sorted_items)}

total_msgs_rank  = _ranks(total_msgs)
word_count_rank  = _ranks(words)

data = {

    "total_messages_group": sum(total_msgs.values()),
    "stats": {
        "total_messages":       total_msgs,
        "word_count":           words,
        "night_owl":            owls,
        "ghost": {
            "ghosted_counts":   ghosted,
            "msg_counts":       msg_cnt,
            "ghost_percentage": ghost_pct,
        },
        "conversation_starter": starters,
        "most_used_emoji":      top_emojis,
        "overall_emojis":       overall_emojis,
        "busiest_day":          busy,
        "longest_silence":      silence,
        "avg_response_time":    response,
        "hype_person":          hype,
        "conversation_killer":  killer,
    },

    # ---- pre-computed fields ----
    "derived": {
        "sorted": {
            "total_messages":        total_msgs_sorted,
            "word_count":            word_count_sorted,
            "night_owl":             night_owl_sorted,
            "ghost_percentage":      ghost_pct_sorted,
            "conversation_starter":  starters_sorted,
            "hype_person":           hype_sorted,
            "conversation_killer":   killer_sorted,
        },
        "pct": {
            "total_messages":        total_msgs_pct,
            "word_count":            word_count_pct,
            "night_owl":             night_owl_pct,
            "ghost_percentage":      ghost_pct_pct,
            "conversation_starter":  starters_pct,
            "hype_person":           hype_pct,
        },
        "words_per_message":         words_per_message,
        "active_member_threshold":   active_member_threshold,
        "personality":               personality,
        "ranks": {
            "total_messages":        total_msgs_rank,
            "word_count":            word_count_rank,
        },
        "response_normalized":       response_normalized,
        "response_bubble_size":      response_bubble_size,
    }
}


with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("stats saved to web/data.json")