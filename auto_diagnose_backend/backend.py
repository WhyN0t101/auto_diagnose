from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
from fpdf import FPDF
import io
import os

# Obtém o diretório base do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "fonts")

# Caminhos completos das fontes
FONT_PATH = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_PATH_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
IMAGE_DIR = os.path.join(BASE_DIR, "images")


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

TOOL_RECOMMENDATIONS = {
    "Access Control": ["Okta", "Microsoft Entra ID (Azure AD)"],
    "Data Protection": ["VeraCrypt", "BitLocker"],
    "Employee Awareness and Training": ["KnowBe4", "Infosec IQ"],
    "Governance and Policies": ["NIST Cybersecurity Framework", "CIS Controls"],
    "Incident Response and Recovery": ["Splunk SOAR", "IBM Resilient"],
    "Network Security": ["Snort", "Wireshark"],
    "Third-Party Risk Management": ["OneTrust", "Prevalent"],
}
# PDF Class
class PDF(FPDF):
    def footer(self):
        """ Add page numbers on all pages except cover. """
        self.set_y(-15)
        self.set_font("DejaVu", size=10)
        if self.page_no() > 1:
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

# Function to get questions by language
def get_questions_by_language(lang):
    if lang not in ["en", "pt"]:
        lang = "en"  # Default to English if unsupported language is requested
    return [{**q, "category": q["category"][lang], "text": q["text"][lang],
             "options": [{"text": opt["text"][lang], "score": opt["score"], "recommendation": opt["recommendation"][lang]} for opt in q["options"]]}
            for q in questions_data]

# Recommended cybersecurity tools based on categories
TOOL_RECOMMENDATIONS = {
    "Access Control": ["Okta", "Microsoft Entra ID (Azure AD)"],
    "Data Protection": ["VeraCrypt", "BitLocker"],
    "Employee Awareness and Training": ["KnowBe4", "Infosec IQ"],
    "Governance and Policies": ["NIST Cybersecurity Framework", "CIS Controls"],
    "Incident Response and Recovery": ["Splunk SOAR", "IBM Resilient"],
    "Network Security": ["Snort", "Wireshark"],
    "Third-Party Risk Management": ["OneTrust", "Prevalent"],
}

CATEGORY_MAPPING = {
    "governança e políticas": "Governance and Policies",
    "proteção de dados": "Data Protection",
    "controle de acesso": "Access Control",
    "treinamento e conscientização de funcionários": "Employee Awareness and Training",
    "resposta e recuperação de incidentes": "Incident Response and Recovery",
    "segurança de rede": "Network Security",
    "gestão de risco de terceiros": "Third-Party Risk Management",
}


@app.route("/api/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json
    lang = request.args.get("lang", "en")  # Support language selection

    # Load questions
    questions = get_questions_by_language(lang)

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

    # Identify weak categories
    weak_categories = [
        category.strip().lower() for category, percentage in category_percentages.items() if percentage < 50
    ]
    weak_categories_english = [CATEGORY_MAPPING.get(cat, cat) for cat in weak_categories]


    # Extract recommendations based on answers
    extracted_recommendations = {}
    for idx, answer in enumerate(answers):
        if idx < len(questions):  # Ensure index is within range
            question_text = questions[idx]["text"]
            category = questions[idx]["category"]
            
            # Find the corresponding recommendation in the selected language
            recommendation = next(
                (opt["recommendation"] for opt in questions[idx]["options"] if opt["text"] == answer),
                "No specific recommendation" if lang == "en" else "Sem recomendação específica"
            )

            if category not in extracted_recommendations:
                extracted_recommendations[category] = []
            extracted_recommendations[category].append(f"• {recommendation}")

    # Filter suggested tools based on weak categories
    suggested_tools = {
        cat: TOOL_RECOMMENDATIONS.get(cat, []) for cat in weak_categories_english
    }

    # ✅ Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ✅ Load Fonts
    try:
        pdf.add_font("DejaVu", "", os.path.abspath(FONT_PATH), uni=True)
        pdf.add_font("DejaVu", "B", os.path.abspath(FONT_PATH_BOLD), uni=True)
    except Exception as e:
        print(f"🚨 Error loading fonts: {e}")
        raise

    pdf.set_font("DejaVu", "", 12)

    # ✅ **Front Page**
    pdf.add_page()
    pdf.image(os.path.join(IMAGE_DIR, "background.png"), x=0, y=0, w=210, h=297)

    pdf.set_font("DejaVu", "B", size=22)  # Reduced font size to fit within width
    pdf.set_y(80)  # Adjust position

    # ✅ Use `multi_cell()` to avoid overflow
    pdf.multi_cell(190, 10, txt="Cybersecurity Diagnostic Report" if lang == "en" else "Relatório de Diagnóstico de Cibersegurança",
                align="C")

    pdf.set_y(120)
    pdf.set_font("DejaVu", size=14)
    pdf.cell(0, 10, txt="Report Date: 2025", ln=True, align="C")

    # ✅ Centering the logo properly
    pdf.image(os.path.join(IMAGE_DIR, "logo_hq.png"), x=(210-50)/2, y=180, w=50)

    pdf.image(os.path.join(IMAGE_DIR, "logo_hq.png"), x=80, y=180, w=50)

    # ✅ Add Category Breakdown
    pdf.add_page()
    pdf.set_font("DejaVu", "B", size=18)
    pdf.cell(0, 10, txt="Category Breakdown" if lang == "en" else "Desempenho por Categoria", ln=True)
    pdf.ln(5)

    pdf.set_font("DejaVu", size=12)
    for category, score in category_scores.items():
        max_cat_score = category_max_scores.get(category, "N/A")
        pdf.cell(200, 10, txt=f"{category}: {score}/{max_cat_score} ({round(category_percentages[category], 2)}%)", ln=True)

    pdf.ln(10)

    # ✅ **Recommendations**
    pdf.add_page()
    pdf.set_font("DejaVu", "B", size=18)
    pdf.cell(0, 10, txt="Recommendations" if lang == "en" else "Recomendações", ln=True)
    pdf.ln(5)

    pdf.set_font("DejaVu", size=12)
    for category, recs in extracted_recommendations.items():
        pdf.set_font("DejaVu", style="B", size=14)
        pdf.cell(0, 10, txt=category, ln=True)
        pdf.ln(5)

        pdf.set_font("DejaVu", size=12)
        for rec in recs:
            pdf.multi_cell(0, 8, rec)
            pdf.ln(3)

    pdf.ln(10)

    REVERSE_CATEGORY_MAPPING = {v: k for k, v in CATEGORY_MAPPING.items()}

    if suggested_tools and any(tools for tools in suggested_tools.values()):  # Ensure at least one tool exists
        pdf.add_page()
        pdf.set_font("DejaVu", "B", size=18)
        pdf.cell(0, 10, txt="Suggested Tools for Improvement" if lang == "en" else "Ferramentas Recomendadas", ln=True)
        pdf.ln(5)

        pdf.set_font("DejaVu", size=12)
        for category, tools in suggested_tools.items():
            # Se a linguagem for PT, converte os nomes das categorias para português
            category_display = REVERSE_CATEGORY_MAPPING.get(category, category) if lang == "pt" else category

            if tools:  # Ensure there are tools before printing
                pdf.set_font("DejaVu", "B", size=14)
                pdf.cell(0, 10, txt=category_display, ln=True)
                pdf.ln(3)
                pdf.set_font("DejaVu", size=12)
                for tool in tools:
                    pdf.cell(0, 8, txt=f"• {tool}", ln=True)
                pdf.ln(5)

    # ✅ Save PDF and Send Response
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest="S").encode("latin1", "ignore")
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    print("✅ Weak Categories:", weak_categories_english)
    print("🔍 Suggested Tools Mapping:", suggested_tools)



    return send_file(
        pdf_output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="cybersecurity_diagnostic_report.pdf" if lang == "en" else "diagnostico_ciberseguranca.pdf",
    )

if __name__ == "__main__":
    app.run(debug=True)


