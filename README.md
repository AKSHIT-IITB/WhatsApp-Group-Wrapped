# WhatsApp-Group-Wrapped
Course Project - CS108

A browser-based, Spotify Wrapped-style slideshow that visualises social dynamics found in a WhatsApp group chat. Built with Python (chat generator + statistics parser) and JavaScript (front-end).

---

## Project Structure

```
whatsapp-wrapped/
├── generator/chat.py
├── parser/analyze.py
├── web/              (index.html, style.css, app.js)
├── chat.txt
├── data.json
└── vocabulary.txt
```

---

## How to Run

### Step 1 — Generate the chat

```bash
python generator/chat.py vocabulary.txt
```

- Reads `vocabulary.txt` (comma-separated words)
- Outputs `chat.txt` in the format:
  ```
  DD/MM/YY, HH:MM - Sender_Name: Message text
  ```
- Each member has a distinct personality (Chatterbox, Night Owl, Dry Texter, etc.)

### Step 2 — Parse the chat

```bash
python parser/analyze.py chat.txt
```

- Reads `chat.txt`
- Outputs `data.json` with all statistics

## Dependencies

```bash
pip install emoji numpy
```

| Library | Purpose |
|---|---|
| `emoji` | Detecting and counting emojis per person |
| `numpy` | Used in chat.py for weighted random personality simulation |
| `datetime` | Parsing message timestamps |
| `json` | Writing data.json output |

---

## data.json Schema

```json
{
  "total_messages_group": 1500,

  "stats": {

    "total_messages": {
      "Name": 120
    },

    "word_count": {
      "Name": 843
    },

    "night_owl": {
      "Name": 14
    },

    "ghost": {
      "ghosted_counts": {
        "Name": 20
      },
      "msg_counts": {
        "Name": 120
      },
      "ghost_percentage": {
        "Name": 16.67
      }
    },

    "conversation_starter": {
      "Name": 8
    },

    "most_used_emoji": {
      "Name": [["😂", 10], ["🔥", 6], ["💀", 4]]
    },

    "busiest_day": {
      "date": "22/07/24",
      "count": 87
    },

    "longest_silence": {
      "hours": 14.5,
      "days": 0.6,
      "start": "22/07/24 23:10",
      "end": "23/07/24 13:40"
    },

    "avg_response_time": {
      "Name": 4.5
    },

    "hype_person": {
      "Name": 2.3
    },

    "conversation_killer": {
      "Name": {
        "kills": 12,
        "total": 120,
        "score": 10.0
      }
    }

  }
}
```

---

## Stat Definitions

| # | Stat | Definition |
|---|---|---|
| 1 | `total_messages` | Number of messages sent per person |
| 2 | `word_count` | Number of words sent per person (emojis counted as words) |
| 3 | `night_owl` | Messages sent between 12am – 4am per person |
| 4 | `ghost` | How often your message gets no reply within 10 minutes |
| 5 | `conversation_starter` | Times you sent the first message after 60+ min of silence |
| 6 | `most_used_emoji` | Top 3 emojis used by each person |
| 7 | `busiest_day` | Single day with the highest message count |
| 8 | `longest_silence` | Longest continuous gap with no messages at all |
| 9 | `avg_response_time` | Median minutes before someone replies to you (within 60 min window) |
| 10 | `hype_person` | Average minutes each person takes to reply to others (lower = more hype) |
| 11 ⭐ | `conversation_killer` | % of your messages followed by 60+ min of silence — your kill score |

