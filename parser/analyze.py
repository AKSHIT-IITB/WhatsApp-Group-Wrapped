from datetime import datetime
import emoji 
import json 

MEMBERS = ["Aryan", "Akshit", "Yash", "Shreya", "Dev", "Kavya", "Joshmitha", "Tanvi"]

# -----------------------------------------------stat 1 -----------------------------------------------------------------
# here we are fining the total no of messages 
def total_messages():
    f=open("chat.txt")
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
        name=words[3][:-1]
        counts[name]=counts[name]+1
    return counts

# -----------------------------------------------stat 2 -----------------------------------------------------------------
# word countn including the emoji (counting emoji as word)
def word_count():
    f=open("chat.txt")
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
        count=len(words)-4
        name=words[3][:-1]
        counts[name]= counts[name]+count 
    return counts
r=word_count()
# print(f"word count is {r}")

# -----------------------------------------------stat 3 -----------------------------------------------------------------
# perosn who active at night time 
def night_owl():
    f = open("chat.txt")
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
    f = open("chat.txt")
    # counts how many times no one replied to your message within 10 minutes
    ghosted_counts = {
        "Aryan": 0,
        "Akshit": 0,
        "Yash": 0,
        "Shreya": 0,
        "Dev": 0,
        "Kavya": 0,
        "Joshmitha": 0,
        "Tanvi": 0
    }
    # total messages each person sent
    msg_counts = {
        "Aryan": 0,
        "Akshit": 0,
        "Yash": 0,
        "Shreya": 0,
        "Dev": 0,
        "Kavya": 0,
        "Joshmitha": 0,
        "Tanvi": 0
    }
    time_span = 10
    prev_sender = None
    prev_hour = None
    prev_minute = None
    for line in f:
        words = line.strip().split()
        if len(words) < 4:
            continue
        sender = words[3][:-1]
        if sender in msg_counts:
            msg_counts[sender] = msg_counts[sender] + 1
        time = words[1]
        try:
            hour = int(time.split(":")[0])
            minute = int(time.split(":")[1])
        except:
            continue
        if prev_sender is not None:
            time_diff = (hour * 60 + minute) - (prev_hour * 60 + prev_minute)
            if time_diff > time_span and sender != prev_sender:
                if prev_sender in ghosted_counts:
                    ghosted_counts[prev_sender] = ghosted_counts[prev_sender] + 1
        prev_sender = sender
        prev_hour = hour
        prev_minute = minute
    f.close()
    return ghosted_counts, msg_counts
ghosted, msg = ghost()
for person in msg:
    if msg[person] > 0:
        percentage = (ghosted[person] / msg[person]) * 100
        # print(f"{person}: ghosted {ghosted[person]}/{msg[person]} = {percentage:.2f}%")

# -----------------------------------------------stat 5 -----------------------------------------------------------------

def conversation_starter():
    f = open("chat.txt")
    starter_counts = {
        "Aryan": 0,
        "Akshit": 0,
        "Yash": 0,
        "Shreya": 0,
        "Dev": 0,
        "Kavya": 0,
        "Joshmitha": 0,
        "Tanvi": 0
    }
    prev_hour = None
    prev_minute = None
    for line in f:
        words = line.strip().split()
        if len(words) < 4:
            continue
        time = words[1]
        sender = words[3][:-1]
        try:
            hour = int(time.split(":")[0])
            minute = int(time.split(":")[1])
        except:
            continue
        if prev_hour is not None:
            time_diff = (hour * 60 + minute) - (prev_hour * 60 + prev_minute)
            if time_diff >= 60:
                if sender in starter_counts:
                    starter_counts[sender] = starter_counts[sender] + 1
        prev_hour = hour
        prev_minute = minute
    f.close()
    return starter_counts
starts=conversation_starter()
# print(f"the conversation starter is {starts}")

# -----------------------------------------------stat 6 -----------------------------------------------------------------
def most_used_emoji():
    f=open("chat.txt")
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
    f=open("chat.txt")
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
    f=open("chat.txt")
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
    f=open("chat.txt")
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
    f=open("chat.txt")
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
    winner=min((n for n in avgs if avgs[n] is not None), key=lambda n: avgs[n])
    return {"winner": winner, "avg_reply_minutes": avgs[winner], "per_person": avgs}
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
    lines=open("chat.txt").readlines()
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
    winner=max(per_person, key=lambda x: per_person[x]["score"])
    return {"winner": winner, "winner_score": per_person[winner]["score"], "per_person": per_person}
killer=conversation_killer()
# print(f"the conversation killer is {killer}")


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

# ghost_pct = (ghosted / msg_cnt) * 100
ghost_pct = {}
for person in MEMBERS:
    if msg_cnt[person] > 0:
        ghost_pct[person] = round((ghosted[person] / msg_cnt[person]) * 100, 2)
    else:
        ghost_pct[person] = 0.0

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
        "busiest_day":          busy,
        "longest_silence":      silence,
        "avg_response_time":    response,
        "hype_person":          hype,
        "conversation_killer":  killer,
    }
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("stats saved data.json")