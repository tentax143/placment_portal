from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from .models import Job
import os

# Create your views here.
def index(request):
    return render(request,'index.html')

def logout (request):
    request.session.flush()
    return redirect('index')


def download_excel(request):
    # Define the path to the file
    file_path = os.path.join(settings.BASE_DIR,'static\\requred_files', 'sample_student_data.xlsx')
    # Serve the file as an attachment
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='cgpa_formate.xlsx')
    return response



