import streamlit as st
import json
from main import extract_pdf_text, summarize_text, extract_sections, apply_rule_checks

st.title("📘 Universal Credit Act Analyzer")
st.write("Upload a PDF and get structured JSON output (summary + sections + rule checks).")

uploaded_pdf = st.file_uploader("Upload Universal Credit Act PDF", type=["pdf"])

if uploaded_pdf:
    st.success("PDF uploaded successfully!")

    # ---- Extract PDF Text ----
    st.info("Extracting text from PDF...")
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_pdf.read())

    full_text = extract_pdf_text("temp.pdf")

    # ---- Summarize ----
    st.info("Generating summary...")
    summary = summarize_text(full_text)

    # ---- Extract Sections ----
    st.info("Extracting legislative sections...")
    sections = extract_sections(full_text)
    # print(sections)
    # ---- Rule Checks ----
    st.info("Running rule checks...")
    rules_output = apply_rule_checks(sections)

    # Combine final output
    final_output = {
        "summary": summary,
        "sections": sections,
        "rule_checks": rules_output
    }

    st.success("JSON generated successfully!")

    # ---- Display JSON ----
    st.subheader("📦 Final JSON Output")
    st.json(final_output)

    # ---- Download Button ----
    json_str = json.dumps(final_output, indent=4, ensure_ascii=False)
    st.download_button(
        label="⬇️ Download JSON",
        data=json_str,
        file_name="final_output.json",
        mime="application/json"
    )
