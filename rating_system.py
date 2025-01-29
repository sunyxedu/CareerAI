import os
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
from io import BytesIO
import json
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px

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

def analyze_resume(pdf_file_path: str):
    """
    Upload a PDF resume for analysis using function calling.
    Returns the overall score, section scores, and feedback.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    with open(pdf_file_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()
    
    # Extract and truncate text from PDF
    text_content = extract_text_from_pdf(pdf_content)
    truncated_text = truncate_text(text_content)

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
                "required": ["overall_score", "section_scores", "highlights", "weaknesses"]
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a resume analysis expert."},
            {"role": "user", "content": f"Please analyze this resume and provide detailed scoring for each section: {truncated_text}"}
        ],
        functions=functions,
        function_call={"name": "analyze_resume"}
    )

    function_args = response.choices[0].message.function_call.arguments
    data = eval(function_args)
    
    overall_score = data["overall_score"]
    section_scores = data["section_scores"]
    highlights = data["highlights"]
    weaknesses = data["weaknesses"]

    return overall_score, section_scores, highlights, weaknesses

if __name__ == "__main__":
    pdf_path = "/Users/yuxuan/Documents/CareerAI/Resume.pdf"
    try:
        overall_score, section_scores, highlights, weaknesses = analyze_resume(pdf_path)
        print(f"\nOverall Resume Score: {overall_score}/10")
        
        print("\nDetailed Section Scores:")
        
        print("\nProjects:")
        for project in section_scores["projects"]:
            print(f"- {project['name']}: {project['score']}/10")
            
        print("\nAwards:")
        for award in section_scores["awards"]:
            print(f"- {award['name']}: {award['score']}/10")
            
        print("\nEducation:")
        for edu in section_scores["education"]:
            print(f"- {edu['name']}: {edu['score']}/10")
            
        print("\nWork Experience:")
        for exp in section_scores["work_experience"]:
            print(f"- {exp['name']}: {exp['score']}/10")
            
        print("\nSkills and Interests:")
        for skill in section_scores["skills_interests"]:
            print(f"- {skill['name']}: {skill['score']}/10")
        
        print("\nHighlights:", *highlights, sep="\n- ")
        print("\nAreas for Improvement:", *weaknesses, sep="\n- ")
        
        # Calculate average scores for each section
        avg_scores = {
            'Projects': sum(p['score'] for p in section_scores['projects'])/len(section_scores['projects']),
            'Awards': sum(a['score'] for a in section_scores['awards'])/len(section_scores['awards']),
            'Education': sum(e['score'] for e in section_scores['education'])/len(section_scores['education']),
            'Work Experience': sum(w['score'] for w in section_scores['work_experience'])/len(section_scores['work_experience']),
            'Skills & Interests': sum(s['score'] for s in section_scores['skills_interests'])/len(section_scores['skills_interests'])
        }
        
        # Create radar chart using plotly
        categories = list(avg_scores.keys())
        values = list(avg_scores.values())
        
        # Create subplot with radar chart and scatter plots
        fig = sp.make_subplots(rows=3, cols=2, 
                             specs=[[{'type': 'polar'}, {'type': 'xy'}],
                                   [{'type': 'xy'}, {'type': 'xy'}],
                                   [{'type': 'xy'}, {'type': 'xy'}]],
                             subplot_titles=('Overall Analysis', 'Projects', 'Awards', 
                                          'Education', 'Work Experience', 'Skills & Interests'))

        # Add radar chart
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Resume Scores'
        ), row=1, col=1)

        # Add scatter plots for each section
        sections = {
            'projects': (1, 2),
            'awards': (2, 1),
            'education': (2, 2),
            'work_experience': (3, 1),
            'skills_interests': (3, 2)
        }

        for section, (row, col) in sections.items():
            items = section_scores[section]
            names = [item['name'] for item in items]
            scores = [item['score'] for item in items]
            avg = sum(scores) / len(scores)
            
            # Add scatter plot
            fig.add_trace(go.Scatter(
                x=list(range(len(scores))),
                y=scores,
                mode='markers+lines',
                name=section.replace('_', ' ').title(),
                text=names,
                hovertemplate='%{text}<br>Score: %{y}'
            ), row=row, col=col)
            
            # Add average line
            fig.add_trace(go.Scatter(
                x=[0, len(scores)-1],
                y=[avg, avg],
                mode='lines',
                line=dict(dash='dash'),
                name=f'Average ({avg:.1f})'
            ), row=row, col=col)

        # Update layout
        fig.update_layout(
            height=1200,
            showlegend=False,
            title_text='Resume Analysis Dashboard',
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            )
        )

        # Update axes for scatter plots
        for i in range(1, 6):
            row = (i + 1) // 2
            col = 2 if i % 2 == 1 else 1
            if i > 0:  # Skip the polar plot
                fig.update_yaxes(title_text='Score', range=[0, 10], row=row, col=col)
                fig.update_xaxes(title_text='Items', row=row, col=col)

        fig.show()
        
    except Exception as e:
        print("Error occurred:", e)
