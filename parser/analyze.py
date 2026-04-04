import re 
from datetime import datetime, timedelta
import emoji 
def total_messages():
    f=open("chat.txt")
    x=0 
    for line in f: 
        x=x+1 
    return x 
count=total_messages()
print(count)
# counting emojis into word count too 
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
print(f"word count is {r}")

def night_owl():
    f=open("chat.txt")
    counts_msgs_night = {
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
        time=words[1]
        hour=int(time.split(":")[0])
        if hour==0 or hour==1 or hour==2 or hour==3: 
            counts_msgs_night[words[3][:-1]]= counts_msgs_night[words[3][:-1]]+1 
    return counts_msgs_night
list=night_owl()
print(f"the night owl is {list}")


# any msg during the first 10 mins after the msg is sent is considered a direct reply
def ghost():
    f=open("chat.txt")
    ghosted_counts = {
        "Aryan" : 0,
        "Akshit" : 0 ,
        "Yash" : 0,
        "Shreya" : 0, 
        "Dev" : 0,
        "Kavya" : 0, 
        "Joshmitha" : 0,
        "Tanvi" : 0
    }
    msg_counts={
        "Aryan" : 0,
        "Akshit" : 0 ,
        "Yash" : 0,
        "Shreya" : 0, 
        "Dev" : 0,
        "Kavya" : 0, 
        "Joshmitha" : 0,
        "Tanvi" : 0
    }
    time_span=10
    prev_sender=None
    prev_hour=None 
    prev_minute=None 
    for line in f: 
        words=line.strip().split()
        sender=words[3][:-1]
        msg_counts[sender]=msg_counts[sender]+1 
        time=words[1]
        hour=int(time.split(":")[0])
        minute=int(time.split(":")[1])
        if prev_sender is not None: 
            time_diff= (hour*60+minute)-(prev_hour*60+prev_minute)
            if time_diff>time_span:
                ghosted_counts[prev_sender]=ghosted_counts[prev_sender]+1
        prev_sender=sender 
        prev_hour=hour 
        prev_minute=minute 
    return ghosted_counts,msg_counts
ghosted, msg = ghost()
for person in msg:
    if msg[person] > 0:
        percentage = (ghosted[person] / msg[person]) * 100
        print(f"{person}: ghosted {ghosted[person]}/{msg[person]} = {percentage:.2f}%")

# a person is considered conversation starter if their msg is the first one after an hour of no msgs
def conversation_starter():
    f=open("chat.txt")
    starter_counts = {
        "Aryan" : 0,
        "Akshit" : 0 ,
        "Yash" : 0,
        "Shreya" : 0, 
        "Dev" : 0,
        "Kavya" : 0, 
        "Joshmitha" : 0,
        "Tanvi" : 0
    }
    prev_hour=None
    prev_minute=None 
    for line in f:
        words=line.strip().split()
        time=words[1]
        sender=words[3][:-1]
        hour=int(time.split(":")[0])
        minute=int(time.split(":")[1])
        if prev_hour is not None: 
            time_diff= (hour*60+minute)-(prev_hour*60+prev_minute)
            if time_diff>120:
                starter_counts[sender]=starter_counts[sender]+1
        prev_hour=hour
        prev_minute=minute 
    return starter_counts
starts=conversation_starter()
print(f"the conversation starter is {starts}")

def most_used_emoji():
    f=open("chat.txt")
    emoji_counts = {}
    for line in f:
        words=line.strip().split()
        for word in words:
            if emoji.is_emoji(word):
                if word not in emoji_counts:
                    emoji_counts[word]=0
                emoji_counts[word]=emoji_counts[word]+1
    return emoji_counts

emoji_counts=most_used_emoji()
sorted_emojis=sorted(emoji_counts.items(), key=lambda x:x[1], reverse=True)
print(f"most used emojis are {sorted_emojis[:5]}")

# busiest day is the single day with the most messages 
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
print(f"the busiest day is: {busyday}")
