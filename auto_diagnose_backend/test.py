import requests
import random

# Base URL of your API
BASE_URL = "http://127.0.0.1:5000"

# Fetch the questions
def fetch_questions():
    response = requests.get(f"{BASE_URL}/api/questions")
    if response.status_code == 200:
        print("Questions fetched successfully!")
        return response.json()
    else:
        print("Error fetching questions:", response.status_code, response.text)
        return None

# Simulate answering all questions with random answers
def submit_answers(questions):
    # Generate random answers
    answers = [random.choice(question["options"])["text"] for question in questions]

    # Submit the answers
    response = requests.post(
        f"{BASE_URL}/api/submit",
        json={"answers": answers}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n=== Test Completed Successfully! ===")
        print(f"Overall Percentage Score: {result['percentage_score']}%")
        print("Category Breakdown:")
        for category, score in result["category_scores"].items():
            max_score = result["category_max_scores"][category]
            print(f"  {category}: {score}/{max_score}")
        print("\nRecommendations:", result["recommendations"])
    else:
        print("\nError submitting answers:", response.status_code, response.text)

# Run the test
if __name__ == "__main__":
    questions = fetch_questions()
    if questions:
        print(f"\nFetched {len(questions)} questions. Running the test...\n")
        submit_answers(questions)
