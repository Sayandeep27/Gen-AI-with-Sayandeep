import streamlit as st
import PyPDF2
import os

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBpijVSmuqyt5qelKWaPKpd-Ys30wTd37w"

# Gemini LLM initialization
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)

# Output parser
parser = StrOutputParser()

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["resume_text", "job_description"],
    template="""
You are a professional resume evaluator.
Compare the following RESUME and JOB DESCRIPTION.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Give the following output:
1. Percentage match between resume and job description (only number, no % sign).
2. List the key skills or qualifications missing from the resume.
Respond in this format:
Match: <percent>
Missing Topics: <comma-separated list>
"""
)

# Chain
chain: RunnableSequence = prompt_template | llm | parser


# Resume PDF text extractor
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Streamlit UI
st.set_page_config(page_title="Resume vs JD Matcher", layout="centered")

st.title("📄 Resume & 🧾 Job Description Matcher")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description here", height=200)

if st.button("Match Now"):
    if uploaded_file is None or not job_description.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = chain.invoke({
                "resume_text": resume_text,
                "job_description": job_description
            })

            # Parse result
            try:
                match_line, missing_line = result.split("\n")
                match_percent = match_line.split(":")[1].strip()
                missing_topics = missing_line.split(":")[1].strip()

                st.success(f"✅ Match Score: {match_percent}%")
                st.markdown(f"### 🔍 Missing Topics:\n- " + "\n- ".join(missing_topics.split(',')))
            except:
                st.error("Error parsing response. Please try again.")
