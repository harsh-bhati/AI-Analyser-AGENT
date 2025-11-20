# AI-Analyser-AGENT
**AI-powered Legislative Document Analyzer** — Upload a PDF of an Act and automatically generate a structured legal summary, extract statutory elements (definitions, eligibility, obligations, penalties, etc.), and evaluate compliance with predefined rule checks.
Built with **Python, Streamlit, PyPDF2, OpenAI GPT-4o-mini**, and includes a complete JSON output pipeline.


This is an end-to-end AI tool that analyzes legal Acts from PDF files and produces:

- ✅ A clean **summary** (purpose, definitions, eligibility, obligations, enforcement, etc.)
- ✅ Structured **legislative section extraction** (definitions, responsibilities, payments, penalties, etc.)
- ✅ Automated **rule-based compliance checks**
- ✅ A final **JSON output** containing all results
- ✅ A **Streamlit UI** to upload PDFs, view JSON responses, and download results

Built using:
- `Python 3`
- `Streamlit`
- `PyPDF2`
- `OpenAI GPT-4o-mini`
- `dotenv`

---

## 🚀 Features

### 🔹 1. Extracts Text From Any PDF
Uses **PyPDF2** to parse and extract readable text from legislative PDFs.

### 🔹 2. AI-Generated Legal Summary
Summarizes key sections of the Act into 5–10 bullet points:
- Purpose  
- Key definitions  
- Eligibility  
- Obligations  
- Enforcement  

### 🔹 3. JSON Legislative Structure Extraction
The AI extracts structured fields:

```json
{
  "definitions": {},
  "obligations": {},
  "responsibilities": {},
  "eligibility": {},
  "payments": {},
  "penalties": {},
  "record_keeping": {}
}
````

### 🔹 4. Rule-Based Compliance Analysis

Checks if required legal fields exist and provides:

* pass / fail
* evidence
* confidence score

### 🔹 5. Streamlit Web App

Upload a PDF → get instant structured JSON → download the final output.

---

## 📂 Project Structure

```
│── main.py                # Main pipeline for extraction + AI analysis
│── streamlit_app.py       # Streamlit UI
│── final_output.json      # Auto-generated output (after running app)
│── requirements.txt
│── .env                   # Stores API key
```

---

## 🧰 Installation

### 1. Clone the repository

```bash
git clone https://github.com/harsh-bhati/AI-Analsyer-AGENT.git
cd AI-Analsyer-AGENT
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv/Scripts/activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

## 🧠 Usage from CLI

Run the full pipeline:

```terminal
python main.py
```

This will generate:

```
final_output.json
```

---

## 🖥️ Running the Streamlit UI

```terminal
streamlit run streamlit_app.py
```

The UI will allow you to:

* Upload PDF
* Run full analysis
* Preview structured JSON
* Download the JSON

---

## 📸 UI Screenshot

---

## 📌 Example Output Format

```json
{
  "summary": "…",
  "sections": {
      "definitions": {},
      "eligibility": {},
      "payments": {}
  },
  "rule_checks": [
      {
          "rule": "Act must define key terms",
          "status": "pass",
          "confidence": 95
      }
  ]
}
```
