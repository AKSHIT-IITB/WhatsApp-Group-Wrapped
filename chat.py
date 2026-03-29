import random
import numpy as np
from datetime import datetime, timedelta
import sys, os

def load_vocabulary(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    words = [w.strip() for w in content.split(',') if w.strip()]
    return words

EMOJIS = ['😂','😂😂','🥀','🥺','🤣','😭','😭💀','🤡','🥲','😢','👍','👍👍']

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
    },
]

