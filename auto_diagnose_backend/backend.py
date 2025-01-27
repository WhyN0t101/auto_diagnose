from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
from fpdf import FPDF
import io

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
    data = request.json

    if not data or "answers" not in data:
        return jsonify({"error": "Invalid input"}), 400

    answers = data["answers"]
    if len(answers) != len(questions):
        return jsonify({"error": "Incomplete answers"}), 400

    total_score = 0
    category_scores = {}
    category_max_scores = {}
    max_score = 0

    for i, user_answer in enumerate(answers):
        question = questions[i]
        category = question["category"]

        if category not in category_scores:
            category_scores[category] = 0
            category_max_scores[category] = 0

        max_question_score = max(option["score"] for option in question["options"])
        category_max_scores[category] += max_question_score
        max_score += max_question_score

        for option in question["options"]:
            if option["text"] == user_answer:
                total_score += option["score"]
                category_scores[category] += option["score"]
                break

    percentage_score = (total_score / max_score) * 100 if max_score > 0 else 0
    recommendations = generate_recommendations(total_score)

    return jsonify({
        "percentage_score": round(percentage_score, 2),
        "category_scores": category_scores,
        "category_max_scores": category_max_scores,
        "recommendations": recommendations,
    })

@app.route("/api/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json

    if not data or "answers" not in data or "category_scores" not in data or "recommendations" not in data:
        return jsonify({"error": "Invalid input"}), 400

    answers = data["answers"]
    category_scores = data["category_scores"]
    category_max_scores = data.get("category_max_scores", {})
    recommendations = data["recommendations"]

    # Create a PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Cybersecurity Diagnostic Report", ln=True, align="C")
    pdf.ln(10)

    # Total Score
    total_score = sum(category_scores.values())
    max_total_score = sum(category_max_scores.values())
    percentage_score = (total_score / max_total_score) * 100 if max_total_score > 0 else 0

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt=f"Total Score: {total_score}/{max_total_score} ({round(percentage_score, 2)}%)", ln=True)
    pdf.ln(10)

    # Recommendations
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Recommendations:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, recommendations)
    pdf.ln(10)

    # Category Scores
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Category Scores:", ln=True)
    pdf.set_font("Arial", size=12)
    for category, score in category_scores.items():
        max_score = category_max_scores.get(category, "N/A")
        pdf.cell(200, 10, txt=f"{category}: {score}/{max_score}", ln=True)
    pdf.ln(10)

    # Detailed Answers
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Detailed Answers:", ln=True)
    pdf.set_font("Arial", size=12)
    for idx, answer in enumerate(answers):
        pdf.cell(200, 10, txt=f"Q{idx + 1}: {answer}", ln=True)

    # Save the PDF to a BytesIO stream
    pdf_output = io.BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))  # Output PDF as string and write to BytesIO
    pdf_output.seek(0)

    return send_file(
        pdf_output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="diagnostic_report.pdf",
    )

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
