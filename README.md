# Cybersecurity Diagnostic Tool

This project provides a tool to evaluate an organization's cybersecurity posture. It consists of a **frontend** built with Vue.js and a **backend** built with Flask. The tool allows users to answer diagnostic questions and receive a cybersecurity score along with recommendations for improvement.

---

## **Project Structure**

```plaintext
project-root/
├── auto_diagnose_backend/     # Backend (Flask API)
├── auto_diagnose_frontend/    # Frontend (Vue.js)
└── .gitignore                 # Git ignore file
```

---

## **Requirements**

### **Backend Requirements**
- Python 3.9+
- Flask 2.2.2
- flask-cors 3.0.10

### **Frontend Requirements**
- Node.js 16+
- npm 7+ (comes with Node.js)
- Vue 3
- TailwindCSS 3

---

## **Installation**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/WhyN0t101/auto_diagnose.git
cd auto_diagnose
```

---

### **Step 2: Backend Setup**
1. Navigate to the backend folder:
   ```bash
   cd auto_diagnose_backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On macOS/Linux
   source venv/bin/activate
   # On Windows
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install flask
   ```
4. Run the Flask server:
   ```bash
   python backend.py
   ```

   The backend will be accessible at `http://127.0.0.1:5000`.

---

### **Step 3: Frontend Setup**
1. Navigate to the frontend folder:
   ```bash
   cd ../auto_diagnose_frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be accessible at `http://127.0.0.1:5173`.

---

## **Usage**

1. Access the frontend by navigating to `http://127.0.0.1:5173` in your browser.
2. Click on **Start Diagnostic** to begin the cybersecurity assessment.
3. Answer the questions and submit your answers.
4. Review your score and recommendations for improvement.

---

## **Endpoints**

### **Backend API**
#### `GET /api/questions`
- **Description**: Fetches the list of diagnostic questions.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "text": "Does your organization have a cybersecurity policy?",
      "options": [
        { "text": "Yes" },
        { "text": "No" },
        { "text": "Partially" }
      ]
    }
  ]
  ```

#### `POST /api/submit`
- **Description**: Submits the answers and calculates the score.
- **Request Body**:
  ```json
  {
    "answers": ["Yes", "No", "Partially"]
  }
  ```
- **Response**:
  ```json
  {
    "score": 85,
    "recommendations": "Focus on implementing endpoint security solutions."
  }
  ```

---

## **Technologies Used**
- **Frontend**: Vue 3, TailwindCSS, Axios
- **Backend**: Flask, Flask-CORS
- **Build Tools**: Vite.js for Vue.js development

---


## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contact**
For inquiries or contributions, contact **[Your Name]** at **[Your Email]**.
