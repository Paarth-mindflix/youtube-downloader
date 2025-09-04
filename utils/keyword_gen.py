# utils/keyword_gen.py

import random
# from trending import fetch_google_trends, fetch_news_headlines
from utils.config import Config
import openai

TOPICS = [
    "Indian news anchor", "Bollywood celebrity", "politician", "journalist",
    "TV show host", "actor", "singer", "stand-up comedian", "spokesperson",
]
MODIFIERS = [
    "interview", "talking", "speech", "panel discussion", "face cam",
    "talk show", "debate", "conversation", "press conference", "public speaking"
]
FOCUS = [
    "face", "closeup", "dialogue", "zoomed", "on stage", "sitting interview",
    "live talk", "in person", "reaction", "expression"
]
LANGUAGES = ["Hindi", "Tamil", "Bengali", "Telugu", "Malayalam", "English", 
             "Kannada", "Punjabi", "Gujarati"
]

def random_keyword_combos(n=20):
    keywords = set()
    while len(keywords) < n:
        combo = f"{random.choice(TOPICS)} {random.choice(MODIFIERS)} {random.choice(FOCUS)} {random.choice(LANGUAGES)}"
        keywords.add(combo)
    return list(keywords)

def gpt_keywords(n=10):
    if not Config.OPENAI_API_KEY:
        return []
    openai.api_key = Config.OPENAI_API_KEY
    prompt = f"Generate {n} YouTube search queries likely to return Indian talking-face videos in indian regional languages."
    try:
        res = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        content = res.choices[0].message.content
        print("🧠 GPT Output:\n", content)

        # Only keep lines that look like actual queries
        cleaned_lines = []
        for line in content.split('\n'):
            line = line.strip().strip('"-•1234567890. ').strip()
            if len(line) < 5:
                continue
            if any(keyword in line.lower() for keyword in ["sure", "here", "these queries", "should help"]):
                continue
            cleaned_lines.append(line)

        return cleaned_lines

    except Exception as e:
        print(f"EXCEPTION BABY {e}")
        return []

def generate_keywords(total=30, use_gpt=True):
    keywords = set()
    keywords.update(random_keyword_combos(n=total // 2))
    if use_gpt:
        keywords.update(gpt_keywords(n=total // 2))
    return list(keywords)

# keywords = generate_keywords(use_gpt=False)
# print(keywords)