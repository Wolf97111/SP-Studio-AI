from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with open("index.html", "r", encoding="utf-8") as f:
    current_html = f.read()

instruction = os.environ.get("ISSUE_BODY", "")
title = os.environ.get("ISSUE_TITLE", "")

prompt = f"""Tu es expert HTML/CSS/JS. Modifie ce fichier selon ces instructions UNIQUEMENT :

TITRE: {title}
DETAILS: {instruction}

REGLES ABSOLUES:
- Retourne UNIQUEMENT le code HTML complet
- Ne modifie que ce qui est demande
- Conserve tout le reste identique

HTML:
{current_html}"""

response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=prompt
)

new_html = response.text
for tag in ["```html", "```"]:
    if new_html.startswith(tag):
        new_html = new_html[len(tag):]
if new_html.endswith("```"):
    new_html = new_html[:-3]
new_html = new_html.strip()

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("OK!")
