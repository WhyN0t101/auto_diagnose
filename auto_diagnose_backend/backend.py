from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the frontend

# Load questions from JSON
with open("questions.json") as f:
    questions = json.load(f)

# Endpoint to fetch questions
@app.route("/api/questions", methods=["GET"])
def get_questions():
    return jsonify(questions)

# Endpoint to process answers and calculate score
@app.route("/api/submit", methods=["POST"])
def submit_answers():
    data = request.json  # Expecting {"answers": [...]}

    if not data or "answers" not in data:
        return jsonify({"error": "Invalid input"}), 400

    answers = data["answers"]
    if len(answers) != len(questions):
        return jsonify({"error": "Incomplete answers"}), 400

    total_score = 0
    category_scores = {}
    category_max_scores = {}
    max_score = 0

    # Calculate total score, category scores, and max score
    for i, user_answer in enumerate(answers):
        question = questions[i]
        category = question["category"]

        # Initialize category scores
        if category not in category_scores:
            category_scores[category] = 0
            category_max_scores[category] = 0

        max_question_score = max(option["score"] for option in question["options"])
        category_max_scores[category] += max_question_score
        max_score += max_question_score

        # Add user score for the category
        for option in question["options"]:
            if option["text"] == user_answer:
                total_score += option["score"]
                category_scores[category] += option["score"]
                break

    # Calculate percentage score
    percentage_score = (total_score / max_score) * 100 if max_score > 0 else 0

    # Generate recommendations based on score
    recommendations = generate_recommendations(total_score)

    return jsonify({
        "percentage_score": round(percentage_score, 2),
        "category_scores": category_scores,
        "category_max_scores": category_max_scores,
        "recommendations": recommendations
    })

# Function to generate recommendations based on score
def generate_recommendations(score):
    if score >= 400:
        return "Excellent! Your cybersecurity posture is strong. Maintain current practices."
    elif 300 <= score < 400:
        return "Good job, but there’s room for improvement in specific areas."
    elif 200 <= score < 300:
        return "Fair. Focus on strengthening key areas like access control and incident response."
    else:
        return "Poor. Consider immediate improvements in policies, training, and technology."

if __name__ == "__main__":
    app.run(debug=True)
