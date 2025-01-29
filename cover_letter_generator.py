import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import date
import csv

def read_personal_info_from_csv(name):
    """
    Read personal information from the CSV file.
    
    Args:
        name (str): Name of the person (used in CSV filename)
    
    Returns:
        dict: Personal information including name, email, and phone
    """
    filename = f'resume_analysis_{name.lower().replace(" ", "_")}.csv'
    personal_info = {}
    
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'Personal Info':
                    personal_info[row[1].lower()] = row[3]
        return personal_info
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def generate_cover_letter(name, company_name, highlights, job_link=None):
    """
    Generate a cover letter based on personal info and company details.
    
    Args:
        name (str): Full name of the applicant
        company_name (str): Name of the company
        highlights (list): Key highlights from resume
        job_link (str, optional): Link to job posting
    
    Returns:
        str: Generated cover letter
    """
    try:
        # Load OpenAI API key
        load_dotenv()
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Get personal info from CSV
        personal_info = read_personal_info_from_csv(name)
        
        # print(personal_info['name'], personal_info['email'], personal_info['phone'])
        
        if not personal_info:
            raise Exception("Could not read personal information from CSV")

        # Create prompt for GPT
        prompt = f"""Write a professional cover letter with the following details:
        Company: {company_name}
        Job Seeker's Name: {personal_info['name']}
        Job Seeker's Email: {personal_info['email']}
        Job Seeker's Phone: {personal_info['phone']}
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
    # Test data
    name = "Yuxuan Sun"  # This should match the name used in CSV filename
    company_name = "Copper.co"
    highlights = [
        "Strong experience in Python development",
        "Machine learning expertise",
        "Previous internship at tech companies"
    ]
    job_link = "https://bit.ly/40wPQvb"

    # Generate cover letter
    cover_letter = generate_cover_letter(
        name=name,
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

if __name__ == "__main__":
    test_cover_letter_generation()
