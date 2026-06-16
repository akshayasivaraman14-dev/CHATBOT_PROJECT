import json

with open("data/faq.json", "r", encoding="utf-8") as f:
    FAQ_DATA = json.load(f)

def search_faq(question):
    question = question.lower().strip()

    for key, answer in FAQ_DATA.items():
        if key in question:
            return answer

    return None