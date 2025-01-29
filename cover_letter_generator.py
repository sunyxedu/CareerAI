import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import date
from rating_system import analyze_resume

def generate_cover_letter(resume_scores, company_name, highlights, job_link=None):
    """
    Generate a cover letter based on resume analysis and company details.
    
    Args:
        resume_scores (dict): Resume section scores from rating system
        company_name (str): Name of the company
        highlights (list): Key highlights from resume analysis
        job_link (str, optional): Link to job posting
    
    Returns:
        str: Generated cover letter
    """
    try:
        # Load OpenAI API key
        load_dotenv()
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Extract key strengths from resume scores
        strengths = []
        for section, items in resume_scores.items():
            if isinstance(items, list):
                top_items = sorted(items, key=lambda x: x['score'], reverse=True)[:2]
                for item in top_items:
                    if item['score'] >= 7:  # Only include high-scoring items
                        strengths.append(f"{item['name']} from {section}")

        # Create prompt for GPT
        prompt = f"""Write a professional cover letter with the following details:
        Company: {company_name}
        Key Strengths: {', '.join(strengths)}
        Key Highlights: {', '.join(highlights)}
        
        The letter should:
        1. Be formal and professional
        2. Highlight the candidate's relevant strengths and achievements
        3. Incorporate 2-3 key highlights naturally into the letter
        4. Show genuine enthusiasm for {company_name}
        5. Include today's date ({date.today().strftime('%B %d, %Y')})
        6. Be around 300-400 words
        7. Have a clear structure with opening, body paragraphs, and closing
        8. Connect the highlights to potential value for the company
        
        Make the letter engaging but not overly aggressive.
        """
        
        if job_link:
            prompt += f"\nPlease also consider the job posting at: {job_link}"

        # Generate cover letter using GPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        cover_letter = response.choices[0].message.content
        
        return cover_letter

    except Exception as e:
        print(f"Error generating cover letter: {e}")
        return None

def test_cover_letter_generation():
    # Get resume scores from rating system
    pdf_path = "/Users/yuxuan/Documents/CareerAI/Resume.pdf"
    try:
        overall_score, section_scores, highlights, weaknesses = analyze_resume(pdf_path)
        
        # Test data
        company_name = "Copper.co"
        job_link = "https://bit.ly/40wPQvb"

        # Generate cover letter using actual resume analysis
        cover_letter = generate_cover_letter(
            resume_scores=section_scores,
            company_name=company_name,
            highlights=highlights,
            job_link=job_link
        )
        
        # Assertions
        assert cover_letter is not None, "Cover letter should not be None"
        assert len(cover_letter) > 0, "Cover letter should not be empty"
        assert company_name in cover_letter, "Cover letter should mention company name"
        
        # Print the generated cover letter
        print("\nGenerated Cover Letter:")
        print("=" * 50)
        print(cover_letter)
        print("=" * 50)
        
    except Exception as e:
        print(f"Error in test: {e}")

if __name__ == "__main__":
    test_cover_letter_generation()
