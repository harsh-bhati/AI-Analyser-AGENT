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


def apply_rule_checks(sections):
    rules = {
        "Act must define key terms": "definitions",
        "Act must specify eligibility criteria": "eligibility",
        "Act must specify responsibilities of the administering authority": "responsibilities",
        "Act must include enforcement or penalties": "penalties",
        "Act must include payment calculation or entitlement structure": "payments",
        "Act must include record-keeping or reporting requirements": "record_keeping",
    }

    results = []

    for rule, field in rules.items():
        content = sections.get(field)
        # print(content)
        # Convert dict to plain string if needed
        if isinstance(content, dict):
            text = " ".join(content.values())
        else:
            text = str(content or "")

        # Simple pass/fail based on length
        if len(text.strip()) > 10:
            status = "pass"
            evidence = text[:180] + "..."
            confidence = 95
        else:
            status = "fail"
            evidence = ""
            confidence = 40

        results.append({
            "rule": rule,
            "status": status,
            "evidence": evidence,
            "confidence": confidence
        })

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
    rules_output = apply_rule_checks(sections)

    final_output = {
        "summary": summary,
        "sections": sections,
        "rule_checks": rules_output
    }

    # Write to JSON file
    with open("final_output.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    print("\nDone! JSON saved as final_output.json")
