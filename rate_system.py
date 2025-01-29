import os
from xai import Grok
from dotenv import load_dotenv
import PyPDF2
from io import BytesIO

load_dotenv()

def extract_text_from_pdf(pdf_content):
    """Extract text from PDF content."""
    pdf_file = BytesIO(pdf_content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def truncate_text(text, max_chars=50000):
    """Truncate text to a maximum number of characters."""
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text

def upload_and_analyze_resume(pdf_file_path: str):
    """
    Upload a PDF resume for analysis using function calling.
    Returns the score, highlights, and weaknesses.
    """
    client = Grok(api_key=os.environ.get("GROK_API_KEY"))

    with open(pdf_file_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()
    
    # Extract and truncate text from PDF
    text_content = extract_text_from_pdf(pdf_content)
    truncated_text = truncate_text(text_content)

    functions = [
        {
            "name": "analyze_resume",
            "description": "Analyze a resume and provide scoring and feedback",
            "parameters": {
                "type": "object",
                "properties": {
                    "score": {
                        "type": "integer",
                        "description": "Score out of 10 for the resume"
                    },
                    "highlights": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Key strengths identified in the resume"
                    },
                    "weaknesses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Areas for improvement in the resume"
                    }
                },
                "required": ["score", "highlights", "weaknesses"]
            }
        }
    ]

    response = client.chat.create(
        model="grok-1",
        messages=[
            {"role": "system", "content": "You are a resume analysis expert."},
            {"role": "user", "content": f"Please analyze this resume: {truncated_text}"}
        ],
        functions=functions,
        function_call={"name": "analyze_resume"}
    )

    function_args = response.choices[0].message.function_call.arguments
    data = eval(function_args)
    
    score = data["score"]
    highlights = data["highlights"]
    weaknesses = data["weaknesses"]

    return score, highlights, weaknesses

if __name__ == "__main__":
    pdf_path = "/Users/yuxuan/Documents/CareerAI/Resume.pdf"
    try:
        score, highlights, weaknesses = upload_and_analyze_resume(pdf_path)
        print(f"Resume Score: {score}/10")
        print("\nHighlights:", *highlights, sep="\n- ")
        print("\nAreas for Improvement:", *weaknesses, sep="\n- ")
        
    except Exception as e:
        print("Error occurred:", e)
