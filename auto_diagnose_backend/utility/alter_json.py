import json
import asyncio
from googletrans import Translator

# Initialize the Google Translator
translator = Translator()

# Load the original questions.json file
with open("questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)

# Function to translate text asynchronously
async def translate_text(text, dest="pt"):
    try:
        translation = await translator.translate(text, src="en", dest=dest)
        return translation.text
    except Exception as e:
        print(f"⚠️ Translation failed for '{text}': {e}")
        return text  # Return original if translation fails

# Function to translate all questions
async def translate_questions():
    tasks = []
    
    for question in questions:
        tasks.append(translate_text(question["category"], dest="pt"))
        tasks.append(translate_text(question["text"], dest="pt"))

        for option in question["options"]:
            tasks.append(translate_text(option["text"], dest="pt"))
            tasks.append(translate_text(option["recommendation"], dest="pt"))
    
    translations = await asyncio.gather(*tasks)

    index = 0
    for question in questions:
        question["category"] = {"en": question["category"], "pt": translations[index]}; index += 1
        question["text"] = {"en": question["text"], "pt": translations[index]}; index += 1

        for option in question["options"]:
            option["text"] = {"en": option["text"], "pt": translations[index]}; index += 1
            option["recommendation"] = {"en": option["recommendation"], "pt": translations[index]}; index += 1

    # Save the translated JSON file
    with open("questions_translated.json", "w", encoding="utf-8") as file:
        json.dump(questions, file, indent=4, ensure_ascii=False)

    print("✅ Translation complete! File saved as 'questions_translated.json'.")

# Run the translation asynchronously
asyncio.run(translate_questions())
