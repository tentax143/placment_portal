from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages

from .models import Company, Willingness , ApplicationStudent ,Placement,Placement_User , DepartmentEligibility , TrainingCompanyDetails , Role
from .forms import  CompanyForm , NewStudent , PlacementForm

from django.http import JsonResponse

from .decorators import student_required, staff_required , specific_role_required , admin_required


@staff_required
def staff_dashboard(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('staff_login')
    try:
        faculty =  Placement_User.objects.get(faculty_id=faculty_id)
        faculty_dept = faculty.faculty_dept
        if(faculty_dept == "All"):
            faculty_dept = "ADMINISTRATION"
        elif(faculty_dept == "Others"):
            faculty_dept = "Placement Cell"
        else:
            faculty_dept = faculty.faculty_dept
        context = {
        'faculty': faculty,
        'faculty_dept': faculty_dept,
    }
    
    except Placement_User.DoesNotExist:
        return redirect('staff_login')

    
    # Pass the student data to the template
    return render(request, 'staff/staff_dashboard.html', context)




@staff_required
@specific_role_required(['Placement Cell Staff', 'Placement Coordinator' , 'JA','Student Placement Coordinator'])
def add_company(request):
    roles = Role.objects.all()
    company_list = Company.objects.all().values_list('company_name', flat=True).distinct()

    # AJAX request handling
    if 'academic_year' in request.GET:
        academic_year = request.GET.get('academic_year')
        if academic_year:
            companies = Company.objects.filter(company_academic_year=academic_year)
            company_names = list(companies.values_list('company_name', flat=True))
            return JsonResponse({'company_names': company_names})
        return JsonResponse({'company_names': []})

    # Form submission handling
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            # Save the many-to-many data for the form
            form.save_m2m()
            messages.success(request, 'Company added successfully!')
            return redirect('staff_dashboard')
        else:
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'staff/add_company.html', {
                'form': form,
                'roles': roles,
                'company_list': company_list
            })
    else:
        form = CompanyForm()

    return render(request, 'staff/add_company.html', {
        'form': form,
        'roles': roles,
        'company_list': company_list
    })



from .models import Company

def fetch_companies_by_academic_year(request):
    try:
        academic_year = request.GET.get('academic_year')
        
        # Check if the academic year is provided
        if not academic_year:
            return JsonResponse({'error': 'Academic year not provided'}, status=400)
        
        # Fetch companies based on the academic year
        companies = Company.objects.filter(company_academic_year=academic_year)
        
        # Format companies as a list of dictionaries for JSON response
        company_data = [
            {
                'company_id': company.company_id,
                'company_name': company.company_name,
                'company_location': company.company_location,
                'company_role': company.company_role
            }
            for company in companies
        ]
        print(company_data)
        return JsonResponse({'company_names': company_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


import difflib

from .forms import RoleForm
def add_role(request):
    if request.method == 'POST':
        role_name = request.POST.get('role_name').strip()

        if not role_name:
            return JsonResponse({'error': 'Role name is required.'})

        # Normalize role_name to lowercase and strip trailing 's' if it exists
        normalized_role_name = role_name.lower().rstrip('s')

        # Check for similar roles in the database
        existing_roles = Role.objects.values_list('role_name', flat=True)
        similar_roles = [role for role in existing_roles if difflib.SequenceMatcher(None, role.lower(), normalized_role_name).ratio() > 0.8]

        if similar_roles:
            return JsonResponse({'error': f'A similar role already exists: {", ".join(similar_roles)}'})

        # Create the Role object if no similar roles were found
        role, created = Role.objects.get_or_create(role_name=role_name)

        if created:
            return JsonResponse({'success': 'Role added successfully.'})
        else:
            return JsonResponse({'error': 'Role already exists.'})

    else:

        return render(request, 'staff/add_role.html')



@staff_required
@specific_role_required(['JA'])
def add_student(request):
    if request.method == 'POST':
        form = NewStudent(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'auth/success.html')  # Create a success page
    else:
        form = NewStudent()
    return render(request, 'staff/add_student.html', {'form': form})


@staff_required
@specific_role_required(['JA','STUDENT'])
def placement_form(request):
    print("Entered the Post Space of the Placement Formlllll")
    if request.method == 'POST':
        print("Entered the Post Space of the Placement Form")
        form = PlacementForm(request.POST, request.FILES)
        if form.is_valid():
            placement = form.save(commit=False)
            
            existing_placement = Placement.objects.filter(
            student_reg_id=placement.student_reg_id,
            company_id=placement.company_id,
            job_type=placement.job_type,
            job_domain=placement.job_domain
            ).first()

            if existing_placement:
                return JsonResponse({'error': 'Placement already exists for this student, company, and job type.'})

            # Handle rounds logic based on form data
            if form.cleaned_data.get('attended') == 'No':
                placement.round1 = 'Fail'
                placement.round2 = 'Fail'
                placement.round3 = 'Fail'
                placement.round4 = 'Fail'
            elif form.cleaned_data.get('pass') == 'No':
                placement.round1 = 'Fail'
                placement.round2 = 'Fail'
                placement.round3 = 'Fail'
                placement.round4 = 'Fail'
            else:
                rounds_passed = form.cleaned_data.get('rounds')
                if rounds_passed == 'Round 1':
                    placement.round1 = 'Pass'
                    placement.round2 = 'Fail'
                    placement.round3 = 'Fail'
                    placement.round4 = 'Fail'
                elif rounds_passed == 'Round 2':
                    placement.round1 = 'Pass'
                    placement.round2 = 'Pass'
                    placement.round3 = 'Fail'
                    placement.round4 = 'Fail'
                elif rounds_passed == 'Round 3':
                    placement.round1 = 'Pass'
                    placement.round2 = 'Pass'
                    placement.round3 = 'Pass'
                    placement.round4 = 'Fail'
                elif rounds_passed == 'Round 4':
                    placement.round1 = 'Pass'
                    placement.round2 = 'Pass'
                    placement.round3 = 'Pass'
                    placement.round4 = 'Pass'
                else:
                    placement.round1 = rounds_passed
                    placement.round2 = 'EE'
                    placement.round3 = 'EE'
                    placement.round4 = 'EE'

            placement.save()
            return JsonResponse({'success': 'Placement details added successfully!'})
        else:
            print(form.errors)
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        # Fetch companies for the dropdown
        faculty_id = request.session.get('faculty_id')
        if not faculty_id:
            return redirect('staff_login')
        try:
            faculty = Placement_User.objects.get(faculty_id=faculty_id)
            faculty_dept = faculty.faculty_dept
            print(faculty_dept)  # Get faculty department
            
        except Placement_User.DoesNotExist:
            return redirect('staff_login')
        
        # Filter students by the faculty department
        students = ApplicationStudent.objects.using('rit_cgpatrack').filter(department=faculty_dept)
        companies = Company.objects.all()
        roles = Role.objects.all()

        return render(request, 'staff/placement_form.html', {'students': students, 'companies': companies , 'roles':roles})

    
from django.http import JsonResponse


@staff_required
def fetch_companies(request, student_reg_id):
    try:
        print("Fetch Companies")
        print(student_reg_id)
        # Fetch the student's department from ApplicationStudent model
        student = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=student_reg_id)
        print(student)
        student_department = student.department
        print(student_department)

        # Query to find companies the student gave willingness for
        willingness_entries = Willingness.objects.filter(student=student_reg_id)
        print(willingness_entries)

        companies = []
        for entry in willingness_entries:
            company = entry.company  # Get the company associated with the willingness entry

            # Check if the company is eligible for the student's department
            eligible_departments = DepartmentEligibility.objects.filter(company=company, department=student_department)

            # Only add the company to the list if the student's department is eligible
            if eligible_departments.exists():
                companies.append({
                    'company_id': company.company_id,
                    'company_name': company.company_name,
                    'company_location': company.company_location
                })

        return JsonResponse({'companies': companies})
    except ApplicationStudent.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)










from .forms import TrainerCompanyForm

def add_training_details(request):
    if request.method == 'POST':
        form = TrainerCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_training_details')  # Change to your desired redirect URL or view name
    else:
        form = TrainerCompanyForm()

    return render(request, 'staff/add_training_details.html', {'form': form})  # Change to your actual template name


from .forms import TrainerForm

def add_trainer(request):
    # Fetch all existing training companies


    if request.method == 'POST':
        form = TrainerForm(request.POST)
        print("0========-=-==========================")
        if form.is_valid():
            form.save()
            return redirect('add_trainer') 
        else:
            # Display form errors
            print(form.errors)  # Print form errors to the console for debugging
            messages.error(request, 'There was an error adding the company. Please check the form.') 
    else:
        form = TrainerForm()
    training_companies = TrainingCompanyDetails.objects.all()
    print(training_companies)
    return render(request, 'staff/add_trainer.html', {
        'form': form,
        'training_companies': training_companies  # Pass companies to the template
    })




import pandas as pd
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Student

def import_students(request):
    if request.method == 'POST':
        excel_file = request.FILES['file']
        
        # Read the Excel file using pandas
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            messages.error(request, f'Error reading Excel file: {str(e)}')
            return redirect('add_student')

        # Verify if the required columns are present
        required_columns = ['student_regno', 'student_dob']
        if not all(column in df.columns for column in required_columns):
            messages.error(request, 'The uploaded file does not match the required format.')
            return redirect('add_student')

        # Replace NaN values with None and convert appropriate columns to correct data types
        df = df.where(pd.notnull(df), None)
        df['student_regno'] = df['student_regno'].astype(str)  # Ensure regno is treated as a string

        # Loop through each row in the DataFrame and update or create Student records
        for index, row in df.iterrows():
            student_regno = row['student_regno']
            student_dob = row['student_dob']
            
            # Add or update student record
            student, created = Student.objects.update_or_create(
                student_regno=student_regno,
                defaults={
                    'student_dob': student_dob
                }
            )

        messages.success(request, 'Students imported successfully!')
        return redirect('add_student')
    else:
          return render(request, 'staff/import_student.html')


import pandas as pd
from django.http import HttpResponse
import io

def download_student_template(request):
    # Define the column names for the template
    columns = ['student_regno', 'student_dob']

    # Create an empty DataFrame with those column names
    df = pd.DataFrame(columns=columns)

    # Create a BytesIO buffer to write the Excel data to
    buffer = io.BytesIO()

    # Use pandas to write the DataFrame to the buffer as an Excel file
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    # Set the position back to the start of the buffer
    buffer.seek(0)

    # Prepare the HTTP response to send the file
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_template.xlsx'

    return response



    from django.shortcuts import render, redirect
from django.contrib import messages
from hashlib import sha256
from .models import Student

import hashlib

def encrypt_password(raw_password):
    return hashlib.sha256(raw_password.encode()).hexdigest()


@staff_required
@specific_role_required(['JA'])
def change_password(request):
    if request.method == 'POST':
        student_regno = request.POST.get('student_regno')
        student_password = request.POST.get('student_password')

        # Encrypt the password using SHA-256
        encrypted_password = encrypt_password(student_password)

        # Retrieve the student record by registration number
        student = get_object_or_404(Student, student_regno=student_regno)

        # Update only the password
        student.student_password = encrypted_password
        student.save()

        messages.success(request, 'Password changed successfully!')
        return redirect('change_password')  # Redirect to the change password view

    return render(request, 'staff/change_password.html')  # Render the form again if GET



from .models import Job
from django.shortcuts import render

def job_list(request):
    # Query the Job model to get all records
    jobs = Job.objects.all()  # Fetch all job records

    # Pass the jobs data to the template
    return render(request, 'staff/job_opening.html', {'jobs': jobs})

def job_recommendations(request):
# Query the Job model to get all records
    jobs = Job.objects.all()  # Fetch all job records

    # Pass the jobs data to the template
    return render(request, 'staff/job_opening.html', {'jobs': jobs})

@staff_required
@specific_role_required(['Placement Coordinator','JA','Student Placement Coordinator'])
def willingness_dashboard_staff(request):
    whom = request.session.get('whom')
    dept = request.session.get('dept')
    roles = Role.objects.all()

    context = {
        'whom': whom,
        'dept': dept,
        'roles':roles
    }
    return render(request, 'staff/willingness_dashboard.html',context)


