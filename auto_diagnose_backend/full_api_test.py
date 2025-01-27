import requests
import random

BASE_URL = "http://127.0.0.1:5000"  # Replace with the actual base URL of your API

# Test sample answers based on the provided question set
def generate_sample_answers(questions):
    answers = []
    for question in questions:
        random_option = random.choice(question["options"])  # Randomly select an answer
        answers.append(random_option["text"])
    return answers

# Test questions endpoint
def test_get_questions():
    print("Testing /api/questions endpoint...")
    response = requests.get(f"{BASE_URL}/api/questions")
    if response.status_code == 200:
        questions = response.json()
        print(f"Successfully fetched {len(questions)} questions.")
        return questions
    else:
        print(f"Failed to fetch questions. Status code: {response.status_code}")
        print("Response:", response.text)
        return None

# Test submit answers endpoint
def test_submit_answers(questions, answers):
    print("Testing /api/submit endpoint...")
    payload = {"answers": answers}
    response = requests.post(f"{BASE_URL}/api/submit", json=payload)
    if response.status_code == 200:
        result = response.json()
        print("Successfully calculated scores and recommendations.")
        print("Percentage Score:", result["percentage_score"])
        print("Category Scores:", result["category_scores"])
        print("Recommendations:", result["recommendations"])
        return result
    else:
        print(f"Failed to submit answers. Status code: {response.status_code}")
        print("Response:", response.text)
        return None

# Test generate PDF endpoint
def test_generate_pdf(answers, category_scores, category_max_scores, recommendations):
    print("Testing /api/generate-pdf endpoint...")
    payload = {
        "answers": answers,
        "category_scores": category_scores,
        "category_max_scores": category_max_scores,
        "recommendations": recommendations,
    }
    response = requests.post(f"{BASE_URL}/api/generate-pdf", json=payload, stream=True)
    if response.status_code == 200:
        with open("test_diagnostic_report.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)
        print("PDF successfully generated and saved as 'test_diagnostic_report.pdf'.")
    else:
        print(f"Failed to generate PDF. Status code: {response.status_code}")
        print("Response:", response.text)

# Main function to execute tests
if __name__ == "__main__":
    # Step 1: Fetch questions
    questions = test_get_questions()
    if not questions:
        exit("Failed to fetch questions. Exiting...")

    # Step 2: Generate sample answers
    sample_answers = generate_sample_answers(questions)
    print("Sample Answers:", sample_answers)

    # Step 3: Submit answers and calculate scores
    result = test_submit_answers(questions, sample_answers)
    if not result:
        exit("Failed to submit answers. Exiting...")

    # Step 4: Generate PDF report
    test_generate_pdf(
        answers=sample_answers,
        category_scores=result["category_scores"],
        category_max_scores=result["category_max_scores"],
        recommendations=result["recommendations"],
    )
