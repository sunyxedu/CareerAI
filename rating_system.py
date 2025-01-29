import os
from openai import OpenAI
from dotenv import load_dotenv
import csv
from pdf_parser import parse_pdf
import json
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px

load_dotenv()

def analyze_resume(pdf_file_path: str):
    """
    Upload a PDF resume for analysis using function calling.
    Returns the overall score, section scores, and feedback.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Get text content from PDF
    text_content = parse_pdf(pdf_file_path)

    functions = [
        {
            "name": "analyze_resume",
            "description": "Analyze a resume and provide detailed scoring and feedback",
            "parameters": {
                "type": "object",
                "properties": {
                    "overall_score": {
                        "type": "integer",
                        "description": "Overall score out of 10 for the resume"
                    },
                    "personal_info": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"}
                        }
                    },
                    "section_scores": {
                        "type": "object",
                        "properties": {
                            "projects": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "score": {"type": "integer"},
                                        "feedback": {"type": "string"}
                                    }
                                }
                            },
                            "awards": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "score": {"type": "integer"},
                                        "feedback": {"type": "string"}
                                    }
                                }
                            },
                            "education": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "score": {"type": "integer"},
                                        "feedback": {"type": "string"}
                                    }
                                }
                            },
                            "work_experience": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "score": {"type": "integer"},
                                        "feedback": {"type": "string"}
                                    }
                                }
                            },
                            "skills_interests": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "score": {"type": "integer"},
                                        "feedback": {"type": "string"}
                                    }
                                }
                            }
                        }
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
                "required": ["overall_score", "personal_info", "section_scores", "highlights", "weaknesses"]
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a resume analysis expert."},
            {"role": "user", "content": f"Please analyze this resume and provide detailed scoring for each section: {text_content}"}
        ],
        functions=functions,
        function_call={"name": "analyze_resume"}
    )

    function_args = response.choices[0].message.function_call.arguments
    data = eval(function_args)
    
    overall_score = data["overall_score"]
    personal_info = data["personal_info"]
    section_scores = data["section_scores"]
    highlights = data["highlights"]
    weaknesses = data["weaknesses"]

    # Save results to CSV
    save_results_to_csv(overall_score, personal_info, section_scores, highlights, weaknesses)

    return overall_score, personal_info, section_scores, highlights, weaknesses

def save_results_to_csv(overall_score, personal_info, section_scores, highlights, weaknesses):
    """Save the analysis results to CSV files"""
    # Use name to create unique filenames
    name = personal_info['name'].lower().replace(' ', '_')
    
    # Save main scores
    with open(f'resume_analysis_{name}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'Name', 'Score', 'Feedback'])
        
        # Write personal info
        writer.writerow(['Personal Info', 'Name', '', personal_info['name']])
        writer.writerow(['Personal Info', 'Email', '', personal_info['email']])
        writer.writerow(['Personal Info', 'Phone', '', personal_info['phone']])
        
        # Write overall score
        writer.writerow(['Overall', 'Resume', overall_score, ''])
        
        # Write section scores
        for section, items in section_scores.items():
            for item in items:
                writer.writerow([
                    section.replace('_', ' ').title(),
                    item['name'],
                    item['score'],
                    item['feedback']
                ])
    
    # Save highlights and weaknesses
    with open(f'resume_feedback_{name}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Type', 'Feedback'])
        for highlight in highlights:
            writer.writerow(['Highlight', highlight])
        for weakness in weaknesses:
            writer.writerow(['Weakness', weakness])

if __name__ == "__main__":
    pdf_path = "/Users/yuxuan/Documents/CareerAI/Resume.pdf"
    try:
        overall_score, personal_info, section_scores, highlights, weaknesses = analyze_resume(pdf_path)
        print(f"\nOverall Resume Score: {overall_score}/10")
        print("\nAnalysis results have been saved to CSV files.")
        
    except Exception as e:
        print("Error occurred:", e)
