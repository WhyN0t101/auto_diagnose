import requests
import random

BASE_URL = "http://127.0.0.1:5000"  # Update if needed
LANGUAGES = ["en", "pt"]  # Supported languages

# Function to generate sample answers based on provided questions
def generate_sample_answers(questions):
    return [random.choice(question["options"])["text"] for question in questions]

# Function to fetch questions for a given language
def test_get_questions(lang):
    print(f"\nTesting /api/questions endpoint for language: {lang}...")
    response = requests.get(f"{BASE_URL}/api/questions?lang={lang}")
    
    if response.status_code == 200:
        questions = response.json()
        print(f"Successfully fetched {len(questions)} questions in {lang}.")
        return questions
    else:
        print(f"Failed to fetch questions ({lang}). Status code: {response.status_code}")
        print("Response:", response.text)
        return None

# Function to submit answers and get scores/recommendations
def test_submit_answers(lang, questions, answers):
    print(f"\nTesting /api/submit endpoint for language: {lang}...")
    payload = {"answers": answers}
    response = requests.post(f"{BASE_URL}/api/submit?lang={lang}", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Successfully calculated scores in {lang}.")
        print("Percentage Score:", result["percentage_score"])
        print("Category Scores:", result["category_scores"])
        print("Recommendations:", result["recommendations"])
        return result
    else:
        print(f"Failed to submit answers ({lang}). Status code: {response.status_code}")
        print("Response:", response.text)
        return None

# Function to generate a PDF report
def test_generate_pdf(lang, answers, category_scores, category_max_scores, recommendations):
    print(f"\nTesting /api/generate-pdf endpoint for language: {lang}...")
    payload = {
        "answers": answers,
        "category_scores": category_scores,
        "category_max_scores": category_max_scores,
        "recommendations": recommendations,
    }
    response = requests.post(f"{BASE_URL}/api/generate-pdf?lang={lang}", json=payload, stream=True)
    
    if response.status_code == 200:
        filename = f"test_diagnostic_report_{lang}.pdf"
        with open(filename, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"PDF successfully generated for {lang} and saved as '{filename}'.")
    else:
        print(f"Failed to generate PDF ({lang}). Status code: {response.status_code}")
        print("Response:", response.text)

# Main function to execute tests for both languages
if __name__ == "__main__":
    for lang in LANGUAGES:
        print(f"\nRunning tests for language: {lang.upper()}")

        # Step 1: Fetch questions in the selected language
        questions = test_get_questions(lang)
        if not questions:
            print(f"Skipping tests for {lang} due to failed question retrieval.")
            continue

        # Step 2: Generate sample answers
        sample_answers = generate_sample_answers(questions)
        print(f"Sample Answers ({lang}):", sample_answers)

        # Step 3: Submit answers and get scores
        result = test_submit_answers(lang, questions, sample_answers)
        if not result:
            print(f"Skipping PDF generation for {lang} due to failed answer submission.")
            continue

        # Step 4: Generate the PDF report
        test_generate_pdf(
            lang=lang,
            answers=sample_answers,
            category_scores=result["category_scores"],
            category_max_scores=result["category_max_scores"],
            recommendations=result["recommendations"],
        )

    print("\nAll tests completed!")
