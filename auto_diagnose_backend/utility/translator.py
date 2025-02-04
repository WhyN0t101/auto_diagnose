import json
import asyncio
from googletrans import Translator

# Initialize Translator
translator = Translator()

async def translate_text(text, src="en", dest="pt"):
    """Translates text asynchronously"""
    translation = await translator.translate(text, src=src, dest=dest)
    return translation.text

async def translate_questions():
    """Loads and translates questions.json"""
    with open("questions.json", "r", encoding="utf-8") as file:
        questions = json.load(file)

    # Translate each question and its options
    for question in questions:
        question["text"] = await translate_text(question["text"])

        # Translate options
        for option in question["options"]:
            option["text"] = await translate_text(option["text"])
            option["recommendation"] = await translate_text(option["recommendation"])

    # Save translated JSON file
    with open("questions_pt.json", "w", encoding="utf-8") as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)

    print("Translation completed! The translated file is saved as 'questions_pt.json'.")

# Run the async translation function
asyncio.run(translate_questions())
