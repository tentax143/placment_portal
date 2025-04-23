import fitz  # PyMuPDF
import pytesseract
import cv2
import numpy as np
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import mysql.connector
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Company, ApplicationStudent, Willingness, DepartmentEligibility, Trainer, TrainingCompanyDetails
from django.http import JsonResponse
import json
from .decorators import student_required, staff_required
from .models import Job

# Set up Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Configure Google Generative AI
GOOGLE_API_KEY = "AIzaSyA8gQ3tl41pzCFCfauXLu6yv7YHqEp0W3g"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.85,
    top_p=0.95,
    top_k=1,
    max_output_tokens=8000
)

def is_valid_file(file_path):
    """Check if the file has a valid extension (PDF or DOCX)."""
    valid_extensions = ('.pdf', '.docx')
    return file_path.lower().endswith(valid_extensions)

def pdf_to_images(pdf_path):
    """Convert PDF pages to images and return a list of images."""
    if not is_valid_file(pdf_path):
        raise ValueError("File must be a PDF or DOCX.")

    doc = fitz.open(pdf_path)
    images = []
    for i in range(len(doc)):
        page = doc.load_page(i)  
        pix = page.get_pixmap()  
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, -1) 
        images.append(img) 

    return images 

def preprocess_image(img):
    """Convert an image to grayscale and zoom for better OCR accuracy.""" 
    gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    zoomed = cv2.resize(gray, None, fx=4.1667, fy=4.1667)
    return zoomed

def perform_ocr_on_images(images):
    """Perform OCR on a list of images and return extracted text.""" 
    extracted_text = []
    for img in images:
        processed_img = preprocess_image(img)
        text = pytesseract.image_to_string(processed_img)
        extracted_text.append(text)
    return extracted_text

def correction(text):
    """Use Gemini to correct and improve the extracted text."""
    prompt_template = """
    You have received a resume extracted using OCR. Please correct any mistakes in English and dont give extra things...just what said.. Here is the text:

    {text}
    """

    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    generated_content = chain.invoke({"text": text})

    return generated_content.content

def recommend_jobs(generated_content, jobs):
    """Generate job recommendations based on the extracted content and job list."""
    job_info = [f"{job['title']} - {job['link']}" for job in jobs]  # Create a list of job titles with links

    prompt_template = """
    Based on the following resume content, suggest most relevant job titles and links from the provided list. Prioritize jobs that closely align with the candidate's skills, experiences, and career goals.
    **Resume Content:**
    {content}

    **Available Jobs:**
    {jobs}

    **Task:**
    1. **Identify Key Skills and Experiences:** Analyze the resume to extract the most relevant skills, technical proficiencies, and professional experiences.
    2. **Match to Job Requirements:** Compare these extracted skills and experiences to the job descriptions in the provided list.
    3. **Prioritize Recommendations:** Rank the matched jobs based on the degree of overlap between the candidate's qualifications and the job requirements. 

    **Output Format:**
    Template :
    * Title : link

    **Constraints:**
    **Response only the jobs with 
    * **Limit to 20 Recommendations:** Provide a maximum of 20 highly relevant job recommendations.
    * **Avoid Overlapping Recommendations:** Ensure that the recommended jobs are distinct and don't have significant overlap in terms of required skills or experience.
    *** Only recommend the job in the output format defined dont add other texts..
    *** If exception no job given then Tell only "No Jobs were found.."
    """

    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    job_recommendations = chain.invoke({"content": generated_content, "jobs": "\n".join(job_info)})

    # Optionally, parse the response to ensure it's limited to 20 jobs
    matched_jobs = job_recommendations.content.splitlines()
    limited_jobs = matched_jobs[:20]  # Limit to 20 jobs

    return "\n".join(limited_jobs)

def fetch_jobs_from_database():
    """Fetch job titles, companies, and links from the database based on the date_of_post."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='placement_portal',
            user='root',  
            password=''  
        )

        cursor = connection.cursor()
        
        # Calculate the date 7 days ago from today
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        # SQL query to fetch jobs posted in the last 7 days
        cursor.execute("""
            SELECT title, company, link, date_of_post 
            FROM core_job 
            WHERE date_of_post >= %s
        """, (seven_days_ago,))
        
        jobs = cursor.fetchall()
        
        # Print the sample titles and links of jobs fetched for verification
        for job in jobs:
            print(f"Job Title: {job[0]}, Date Posted: {job[3]}, Link: {job[2]}")
        
        # Return a list of dictionaries with title, company, and link
        return [{'title': job[0], 'company': job[1], 'link': job[2]} for job in jobs]

    except mysql.connector.Error as error:
        print(f"Error fetching jobs from database: {error}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

from django.http import HttpResponse

def main_offer(request):
    """Main function to execute the PDF to OCR process based on student registration number."""
    student_id = request.session.get('student_id')
    if not student_id:
        print("Student ID not found in session.")
        return HttpResponse("Student ID not found.", status=400)  # Return a 400 response

    pdf_path = os.path.join(r'E:/New _Admission_Portal_old/rit_placement/mediaresume', f'{student_id}.pdf')
    if not os.path.exists(pdf_path):
        print(f"File for student ID {student_id} not found.")
        return HttpResponse("File not found.", status=404)  # Return a 404 response

    images = pdf_to_images(pdf_path)
    job_list = fetch_jobs_from_database()

    if images:
        all_improved_texts = []  

        for i, text in enumerate(perform_ocr_on_images(images)):
            improved_text = correction(text)
            all_improved_texts.append(improved_text)
            print(f"Corrected Text for Page {i + 1}:\n{improved_text}\n")  # Print corrected text for each page

        combined_text = "\n".join(all_improved_texts)
        recommendations = recommend_jobs(combined_text, job_list)

# Initialize an empty dictionary for job recommendations
        job_dict = {}

        # Check if recommendations is a string and not empty
        if isinstance(recommendations, str) and recommendations.strip():
            # Process the recommendations string
            for line in recommendations.strip().split('\n'):
                # Remove leading asterisk and spaces
                line = line.lstrip('* ').strip()
                # Split the line by the colon to separate job name and link
                if ' : ' in line:
                    job_name, job_link = line.split(' : ', 1)
                    # Clean the job name by removing leading/trailing asterisks
                    job_name = job_name.replace('**', '').strip()
                    job_dict[job_name] = job_link.strip()
        job_data=[]
        for key,value in job_dict.items():
            
            job_data.append(Job.objects.filter(link=value).first())
        # recommend_job_link=list(Job.objects.filter(link__in=job_data))
        # print(recommend_job_link,"working!!!!!!!!")
        for key in job_data:
            if key != None:
                print(key.company)

        # Check if the dictionary is still empty and print relevant info
        if not job_dict:
            print("No job recommendations found. Recommendations output was:")
            print(recommendations)
        else:
            print("Job Recommendations:\n", job_dict)  # Print job recommendations
        # table_html = '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">'
        # # table_html += f'{% extends "base.html" %}'
        # table_html += '<center style="color:blue;"><h3>RECOMMENDED JOBS BASED ON YOUR PROFILE(GENERATED BY AI)</h3></center>'
        # table_html += '<tr style="background:blue; color:white;"><th>Title</th><th>Company</th><th>Salary</th><th>Location</th><th>Apply Link</th></tr>'

        # # Add rows for each dictionary entry
        # for key in job_data:
        #     print(key,"keyess")
        #     if key != None:
        #         print(key.company,"oioiooi")
        #         table_html += f"""<tr>
        #         <td>{key.title}</td>
        #         <td>{key.company}</td>
        #         <td>{key.salary}</td>
        #         <td>{key.location}</td>
        #         <td><a href="{key.link}">Apply</a></td>
        #         </tr>"""

        # # Close the table tag
        # table_html += '</table>'

        # Return the HTML response with content type as 'text/html'
        # return HttpResponse(table_html, content_type='text/html')


    return render(request, 'job_recommendation.html', {'jobs': job_data})  # Return a response if no images were processed

if __name__ == "__main__":
    # Assuming this script is run in an environment where the Django request object is available.
    # In an actual Django setup, you would trigger the main function from a view or similar.
    # For testing, you might create a mock request object or call the function with a specific student ID in a Django view.
    main_offer(request)  # Call the main function with the request object
