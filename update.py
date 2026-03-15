from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

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

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

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

print("OK!")
