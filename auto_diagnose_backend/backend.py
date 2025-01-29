from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
from fpdf import FPDF
import io
import os

# Define the path to the font file (Ensure the font file is available)
FONT_PATH = r"fonts\DejaVuSans.ttf"  # Raw string prevents escape interpretation
FONT_PATH_BOLD = r"fonts\DejaVuSans-Bold.ttf"

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the frontend

# Load translated questions
with open("questions/questions.json", "r", encoding="utf-8") as f:
    questions_data = json.load(f)

# Function to get questions by language
def get_questions_by_language(lang):
    if lang not in ["en", "pt"]:
        lang = "en"  # Default to English if unsupported language is requested
    return [{**q, "category": q["category"][lang], "text": q["text"][lang],
             "options": [{"text": opt["text"][lang], "score": opt["score"], "recommendation": opt["recommendation"][lang]} for opt in q["options"]]}
            for q in questions_data]

# Function to generate recommendations based on category scores
def generate_recommendations(category_scores, category_max_scores, lang="en"):
    weak_categories = [
        category for category, score in category_scores.items()
        if (score / category_max_scores[category]) < 0.5
    ]

    if weak_categories:
        return (f"Foque-se em fortalecer as seguintes áreas: {', '.join(weak_categories)}." if lang == "pt" 
                else f"Focus on strengthening key areas: {', '.join(weak_categories)}."), weak_categories
    return ("Bom trabalho! Nenhuma fraqueza detectada." if lang == "pt" else "Good job! No major weaknesses detected."), []

# Endpoint to fetch questions (supports language selection)
@app.route("/api/questions", methods=["GET"])
def get_questions():
    lang = request.args.get("lang", "en")  # Default to English if not specified
    return jsonify(get_questions_by_language(lang))

# Endpoint to process answers and calculate score (supports language selection)
@app.route("/api/submit", methods=["POST"])
def submit_answers():
    data = request.json
    lang = request.args.get("lang", "en")  # Get language from request

    if not data or "answers" not in data:
        return jsonify({"error": "Invalid input"}), 400

    questions = get_questions_by_language(lang)
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

    # Generate recommendations based on score and category
    recommendations, weak_areas = generate_recommendations(category_scores, category_max_scores, lang)

    return jsonify({
        "percentage_score": round(percentage_score, 2),
        "category_scores": category_scores,
        "category_max_scores": category_max_scores,
        "recommendations": recommendations
    })



@app.route("/api/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json
    lang = request.args.get("lang", "en")  # Support language selection

    # Validate input
    if not data or "answers" not in data or "category_scores" not in data or "category_max_scores" not in data or "recommendations" not in data:
        return jsonify({"error": "Invalid input"}), 400

    answers = data["answers"]
    category_scores = data["category_scores"]
    category_max_scores = data["category_max_scores"]
    recommendations = data["recommendations"]

        # Calculate category percentages
    category_percentages = {
        category: (score / category_max_scores[category]) * 100 if category_max_scores[category] > 0 else 0
        for category, score in category_scores.items()
    }
    # Calculate overall score
    total_score = sum(category_scores.values())
    max_score = sum(category_max_scores.values())
    percentage_score = (total_score / max_score) * 100 if max_score > 0 else 0
    # Identify categories below 50%
    weak_categories = [category for category, percentage in category_percentages.items() if percentage < 50]

    # Suggested tools based on category scores (English and Portuguese versions)
    tool_recommendations_en = {
        "Access Control": ["Okta", "Microsoft Entra ID (Azure AD)"],
        "Data Protection": ["VeraCrypt", "BitLocker"],
        "Employee Awareness and Training": ["KnowBe4", "Infosec IQ"],
        "Governance and Policies": ["NIST Cybersecurity Framework", "CIS Controls"],
        "Incident Response and Recovery": ["Splunk SOAR", "IBM Resilient"],
        "Network Security": ["Snort", "Wireshark"],
        "Third-Party Risk Management": ["OneTrust", "Prevalent"]
    }

    tool_recommendations_pt = {
        "Controlo de Acessos": ["Okta", "Microsoft Entra ID (Azure AD)"],
        "Proteção de Dados": ["VeraCrypt", "BitLocker"],
        "Consciencialização e Formação dos Funcionários": ["KnowBe4", "Infosec IQ"],
        "Governança e Políticas": ["NIST Cybersecurity Framework", "CIS Controls"],
        "Resposta a Incidentes e Recuperação": ["Splunk SOAR", "IBM Resilient"],
        "Segurança de Rede": ["Snort", "Wireshark"],
        "Gestão de Riscos de Terceiros": ["OneTrust", "Prevalent"]
    }

    # Determine which tool recommendation set to use based on language
    tool_recommendations = tool_recommendations_en if lang == "en" else tool_recommendations_pt

    # Filter and select recommended tools for weak categories
    category_tool_recommendations = {
        category: tool_recommendations.get(category, [])[:2]
        for category in weak_categories if category in tool_recommendations
    }

    title = "Cybersecurity Diagnostic Report" if lang == "en" else "Relatório de Diagnóstico de Cibersegurança"
    # ✅ Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ✅ Ensure font exists before adding it
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)  # Normal font
    pdf.add_font("DejaVu", "B", FONT_PATH_BOLD, uni=True)  # Bold version
    pdf.set_font("DejaVu", "", 12)  # Use DejaVu font


    pdf.set_font("DejaVu", style="B", size=16)
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)

    # ✅ Add Overall Score
    pdf.set_font("DejaVu", style="B", size=14)
    pdf.cell(0, 10, txt="Overall Score:" if lang == "en" else "Pontuação Geral:", ln=True)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 10, txt=f"{total_score}/{max_score} ({round(percentage_score, 2)}%)", ln=True)
    pdf.ln(10)

    # ✅ Add Category Scores
    pdf.set_font("DejaVu", style="B", size=14)
    pdf.cell(0, 10, txt="Category Breakdown:" if lang == "en" else "Desempenho por Categoria:", ln=True)
    pdf.ln(5)
    
    pdf.set_font("DejaVu", size=12)
    for category, score in category_scores.items():
        max_cat_score = category_max_scores.get(category, "N/A")
        pdf.cell(200, 10, txt=f"{category}: {score}/{max_cat_score} ({round(category_percentages[category], 2)}%)", ln=True)

    pdf.ln(10)

    # ✅ Add Recommendations
    pdf.set_font("DejaVu", style="B", size=14)
    pdf.cell(0, 10, txt="Recommendations:" if lang == "en" else "Recomendações:", ln=True)
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, recommendations)
    pdf.ln(10)

    # **Only Add Suggested Tools if Any Exist**
    if category_tool_recommendations:
        pdf.set_font("DejaVu", style="B", size=14)
        pdf.cell(200, 10, txt="Suggested Tools for Improvement:", ln=True)
        pdf.set_font("DejaVu", size=12)
        for category, tools in category_tool_recommendations.items():
            pdf.multi_cell(0, 10, f"{category}: {', '.join(tools)}")
        pdf.ln(10)
        
    pdf.set_font("DejaVu", style="B", size=14)
    pdf.cell(0, 10, txt="Answers Summary:" if lang == "en" else "Respostas Escolhidas:", ln=True)
    pdf.ln(5)

    pdf.set_font("DejaVu", size=12)
    for idx, answer in enumerate(answers):
        pdf.multi_cell(0, 10, f"Q{idx + 1}: {answer}")
        pdf.ln(2)

    

    # ✅ Ensure proper encoding and output
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest="S").encode("latin1", "ignore")  # Use "ignore" to remove problematic chars
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)


    return send_file(
        pdf_output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="cybersecurity_diagnostic_report.pdf" if lang == "en" else "diagnostico_ciberseguranca.pdf",
    )
if __name__ == "__main__":
    app.run(debug=True)


'''
    # ✅ Add Answers
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Detailed Answers:" if lang == "en" else "Respostas Detalhadas:", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    for idx, answer in enumerate(answers):
        question_text = questions_data[idx]["text"][lang]  # Get question text in the selected language

        # Find the corresponding recommendation in the selected language
        recommendation = next(
            (opt["recommendation"][lang] for opt in questions_data[idx]["options"] if opt["text"][lang] == answer),
            "No specific recommendation" if lang == "en" else "Sem recomendação específica"
        )
        
        # Add question, answer, and recommendation to PDF
        pdf.multi_cell(0, 10, f"Q{idx + 1}: {question_text}\n"
                            f"{'Answer' if lang == 'en' else 'Resposta'}: {answer}\n"
                            f"{'Recommendation' if lang == 'en' else 'Recomendação'}: {recommendation}")
        pdf.ln(5) 
'''