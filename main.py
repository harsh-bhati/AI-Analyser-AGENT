import os
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------
# Task 1 — Extract Text From PDF
# ------------------------------

def extract_pdf_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text


# ------------------------------
# Task 2 — Summarize the Act
# ------------------------------

def summarize_text(text):
    prompt = f"""
You are a legal analysis assistant.

Summarize the following Act in **5–10 bullet points** focusing on:
- Purpose
- Key definitions
- Eligibility
- Obligations
- Enforcement

Act Content:
{text[:25000]}  # keep within limits
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    # message_text = response.choices[0].message.content
    # print(message_text)

    return response.choices[0].message.content


# -------------------------------------------
# Task 3 — Extract Key Legislative Sections
# -------------------------------------------

def extract_sections(full_text):
    prompt = f"""
You MUST respond ONLY with valid JSON. No markdown formatting.

Extract:

{{
 "definitions": "",
 "obligations": "",
 "responsibilities": "",
 "eligibility": "",
 "payments": "",
 "penalties": "",
 "record_keeping": ""
}}

Use ONLY the act text below:

ACT TEXT:
{full_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    # print(response)
    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {"error": "Invalid JSON returned from model"}


# -------------------------------------------
# Task 4 — Apply Rule Checks
# -------------------------------------------


def apply_rule_checks(sections, full_text):
    rules = [
        "Act must define key terms",
        "Act must specify eligibility criteria",
        "Act must specify responsibilities of the administering authority",
        "Act must include enforcement or penalties",
        "Act must include payment calculation or entitlement structure",
        "Act must include record-keeping or reporting requirements"
    ]
    
    results = []

    for rule in rules:
        prompt = f"""
You are a legislative compliance checker.

Your task: Determine whether the following rule is satisfied by the Act text.

RULE:
{rule}

ACT TEXT:
{full_text[:25000]}

Provide a JSON response ONLY in this format:

{{
 "rule": "",
 "status": "pass" or "fail",
 "evidence": "quote exact lines from the Act proving your answer",
 "confidence": 0-100
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            result_json = json.loads(response.choices[0].message.content)
        except:
            result_json = {
                "rule": rule,
                "status": "fail",
                "evidence": "LLM returned invalid JSON",
                "confidence": 20
            }

        results.append(result_json)

    return results


# ------------------------------
# MAIN PIPELINE
# ------------------------------

if __name__ == "__main__":
    pdf_path = "ukpga_20250022_en.pdf"

    print("\nExtracting PDF...")
    full_text = extract_pdf_text(pdf_path)

    print("\nSummarizing...")
    summary = summarize_text(full_text)

    print("\nExtracting sections...")
    sections = extract_sections(full_text)

    print("\nRunning rule checks...")
    rules_output = apply_rule_checks(sections, full_text)

    final_output = {
        "summary": summary,
        "sections": sections,
        "rule_checks": rules_output
    }

    # Write to JSON file
    with open("final_output.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    print("\nDone! JSON saved as final_output.json")
