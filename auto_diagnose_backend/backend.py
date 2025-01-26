from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the frontend

# Load questions from JSON file
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

    # Calculate the score
    for i, user_answer in enumerate(answers):
        question = questions[i]
        for option in question["options"]:
            if option["text"] == user_answer:
                total_score += option["score"]
                break

    # Generate recommendations based on score
    recommendations = generate_recommendations(total_score)

    return jsonify({
        "score": total_score,
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
