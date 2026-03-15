import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

with open("index.html", "r", encoding="utf-8") as f:
    current_html = f.read()

instruction = os.environ.get("ISSUE_BODY", "")
title = os.environ.get("ISSUE_TITLE", "")

prompt = f"""Tu es un expert développeur web. Modifie ce fichier HTML selon les instructions.

INSTRUCTIONS : {title} — {instruction}

RÈGLES :
- Retourne UNIQUEMENT le HTML complet modifié
- Ne change rien d'autre que ce qui est demandé
- Garde le même style et la même structure

HTML ACTUEL :
{current_html}"""

response = model.generate_content(prompt)
new_html = response.text

if new_html.startswith("```html"):
    new_html = new_html[7:]
if new_html.startswith("```"):
    new_html = new_html[3:]
if new_html.endswith("```"):
    new_html = new_html[:-3]
new_html = new_html.strip()

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("index.html mis a jour !")
