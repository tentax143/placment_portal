from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Student , Company ,  ApplicationStudent , Willingness , DepartmentEligibility , Trainer , TrainingCompanyDetails,Placement,Placement_User,Role
from django.http import JsonResponse
from .forms import PlacementForm
import json
from .decorators import student_required, staff_required

def get_whom(request):
    whom = request.session.get('whom')
    return whom

@student_required
def student_dashboard(request):
    student_id = request.session.get('student_id')
    ffg = request.session.get('whom')
    print("ghg", ffg)

    if not student_id:
        return redirect('login')

    try:
        student = Student.objects.get(student_regno=student_id)
        print(student, "working login")

        student_detailed = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=student_id)
        batch = student_detailed.batch  # or `.batch` depending on your model
        print(student_detailed, "dfaaaaaaaaazx")
        print(batch, "dkm")

        # Save batch to session
        request.session['student_batch'] = batch

    except Student.DoesNotExist:
        return redirect('login')

    context = {
        'student': student,
        'student_detailed': student_detailed
    }
    return render(request, 'student/student_dashboard.html', context)


from django.shortcuts import render, redirect
from .forms import ResumeUploadForm
from .models import Student, StudentResume
import os


from django.contrib import messages
from django.shortcuts import redirect, render
import os
from django.conf import settings
from .models import Student, StudentResume

def upload_resume(request):
    # Retrieve `student_regno` from the session
    student_id = request.session.get('student_id')
    print(student_id,"jjbjjjj")
    print(student_id,"jjbjjjj")
    student_regno = Student.objects.get(student_regno=student_id)
    print("Student Reg No:", student_regno)
    if not student_regno:
        messages.error(request, "Student registration number not found.")
        return redirect('upload_resume')  # Redirect to a login or profile page instead
    student = Student.objects.get(student_regno=student_regno)
    if request.method == "POST":
        file_attach = save_uploaded_pdfs(request.FILES, request)
        print(file_attach, "jgagdas")
        Attachment = file_attach.get('resume')
        print(Attachment, "gjyghjg")

        if Attachment:  # Check if Attachment is not None
            resume_path = str(Attachment)
            print(resume_path, "hjfsd")

            # Use the student instance directly
            StudentResume.objects.update_or_create(
                resume_file=resume_path,
                defaults={
                    'student': student,  # Use the student instance here
                },
            )
    return render(request, 'student/resume_update.html', {'student': student})


def placement_form(request):
    print("Hlo")
    print("Entered the Post Space of the Placement Formlllll")
    if request.method == 'POST':
        print("Entered the POST space of the Placement Form")  # Debug: Entered POST request
        
        form = PlacementForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("Form is valid.")  # Debug: Form is valid
            
            # Prepare the placement instance
            placement = form.save(commit=False)
            print("Form cleaned data:", form.cleaned_data)  # Debug: Check cleaned data
            
            # Check if the placement already exists for this student, company, job type, and domain
            existing_placement = Placement.objects.filter(
                student_reg_id=placement.student_reg_id,
                company_id=placement.company_id,
                job_type=placement.job_type,
                job_domain=placement.job_domain
            ).first()

            if existing_placement:
                print("Placement already exists.")  # Debug: Placement already exists
                return JsonResponse({'error': 'Placement already exists for this student, company, and job type.'})

            # Handle rounds logic based on form data
            attended = form.cleaned_data.get('attended')
            passed = form.cleaned_data.get('pass')
            rounds_passed = form.cleaned_data.get('rounds')
            
            # Update round results based on form data
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

            # Save the placement data to the database
            try:
                placement.save()
                print(f"Placement saved: {placement}")  # Confirm placement is saved
                return JsonResponse({'success': 'Placement details added successfully!'})
            except Exception as e:
                print(f"Error saving placement: {e}")  # Error in saving
                return JsonResponse({'error': 'Failed to save placement details'}, status=500)
        else:
            print("Form is not valid.")  # Debug: Form is not valid
            print(form.errors)  # Print form errors to debug
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        # Fetch companies for the dropdown
        # faculty_id = request.session.get('faculty_id')
        # if not faculty_id:
        #     return redirect('staff_login')
        # try:
        #     faculty = Placement_User.objects.get(faculty_id=faculty_id)
        #     faculty_dept = faculty.faculty_dept
        #     print(faculty_dept)  # Get faculty department
            
        # except Placement_User.DoesNotExist:
        #     return redirect('staff_login')
        
        # Filter students by the faculty department
        # Fetch companies for the dropdown
        student_id = request.session.get('student_id')
        
        if not student_id:
            return redirect('student_login')
        
        try:
            # Get student details from ApplicationStudent model
            application_student = Student.objects.get(student_regno=student_id)
            print(application_student)
            # student_dept = application_student.department  # Faculty department if needed
            # print(student_dept)  # Debug output for department
            
            # student = Student.objects.get(student_regno=application_student.reg_no)

        except ApplicationStudent.DoesNotExist:
            return redirect('student_login')
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
        
        
        # Filter students by the faculty department
        # student_id = request.session.get('student_id')
        students = ApplicationStudent.objects.using('rit_cgpatrack').filter(reg_no=student_id)
        student = Student.objects.get(student_regno=student_id)
        willing_companies_ids = list(
            Willingness.objects.filter(student=student).values_list('company_id', flat=True)
        )
        willing_companies_ids = [int(id) for id in willing_companies_ids]
        print("==========================================================")
        print(willing_companies_ids)
        print(student_id)
        companies = Company.objects.all().order_by('-company_id')


        # Get all companies and filter them based on department eligibility
  
        roles = Role.objects.all()  

        return render(request, 'student/placement_form.html', {'students': students, 'companies': companies , 'roles':roles , 'willing_companies_ids':willing_companies_ids})
    

# def placement_form(request):
#     print("Entered the Post Space of the Placement Form")
#     if request.method == 'POST':
#         print("Entered the Post Space of the Placement Form (POST)")
#         form = PlacementForm(request.POST, request.FILES)

#         if form.is_valid():
#             print("Form is valid.")
#             placement = form.save(commit=False)
#             print("Form cleaned data:", form.cleaned_data)  # Debug: Check cleaned data

#             # Ensure we have the correct Student instance
#             placement_student = placement.student_reg_id  # This is the ApplicationStudent instance
#             print(f"Placement Student instance: {placement_student}")  # Debug: Ensure correct Student instance
            
#             # Check if placement already exists
#             existing_placement = Placement.objects.filter(
#                 student_reg_id=placement.student_reg_id,
#                 company_id=placement.company_id,
#                 job_type=placement.job_type,
#                 job_domain=placement.job_domain
#             ).exists()

#             if existing_placement:
#                 print("Placement already exists.")
#                 return JsonResponse({'error': 'Placement already exists for this student, company, and job type.'})

#             # Handle rounds logic based on form data
#             attended = form.cleaned_data.get('attended')
#             passed = form.cleaned_data.get('pass')
#             rounds_passed = form.cleaned_data.get('rounds')

#             if attended == 'No' or passed == 'No':
#                 placement.round1 = 'Fail'
#                 placement.round2 = 'Fail'
#                 placement.round3 = 'Fail'
#                 placement.round4 = 'Fail'
#             else:
#                 if rounds_passed == 'Round 1':
#                     placement.round1 = 'Pass'
#                     placement.round2 = 'Fail'
#                     placement.round3 = 'Fail'
#                     placement.round4 = 'Fail'
#                 elif rounds_passed == 'Round 2':
#                     placement.round1 = 'Pass'
#                     placement.round2 = 'Pass'
#                     placement.round3 = 'Fail'
#                     placement.round4 = 'Fail'
#                 elif rounds_passed == 'Round 3':
#                     placement.round1 = 'Pass'
#                     placement.round2 = 'Pass'
#                     placement.round3 = 'Pass'
#                     placement.round4 = 'Fail'
#                 elif rounds_passed == 'Round 4':
#                     placement.round1 = 'Pass'
#                     placement.round2 = 'Pass'
#                     placement.round3 = 'Pass'
#                     placement.round4 = 'Pass'
#                 else:
#                     placement.round1 = rounds_passed
#                     placement.round2 = 'EE'
#                     placement.round3 = 'EE'
#                     placement.round4 = 'EE'

#             try:
#                 placement.save()
#                 print(f"Placement saved: {placement}")  # Confirm placement is saved
#                 return JsonResponse({'success': 'Placement details added successfully!'})
#             except Exception as e:
#                 print(f"Error saving placement: {e}")
#                 return JsonResponse({'error': 'Failed to save placement details'}, status=500)

#         else:
#             print("Form is not valid.")
#             print(form.errors)  # Print form errors to debug
#             return JsonResponse({'error': 'Invalid form data'}, status=400)

#     else:
#         # Fetch student info from session
#         student_id = request.session.get('student_id')

#         if not student_id:
#             return redirect('student_login')

#         try:
#             # Get student details from ApplicationStudent model
#             application_student = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=student_id)
#             student_dept = application_student.department  # Faculty department if needed
#             print(f"Student Department: {student_dept}")  # Debug output for department

#             # Now fetch the correct Student object
#             student = Student.objects.get(student_regno=application_student.reg_no)  # Query for Student using reg_no from ApplicationStudent

#         except ApplicationStudent.DoesNotExist:
#             return redirect('student_login')
#         except Student.DoesNotExist:
#             return JsonResponse({'error': 'Student not found'}, status=404)

#         # Get all willing companies for this student
#         willing_companies_ids = list(
#             Willingness.objects.filter(student=student).values_list('company_id', flat=True)
#         )
#         willing_companies_ids = [int(id) for id in willing_companies_ids]

#         # Get all companies available for placements
#         companies = Company.objects.all().order_by('-company_id')

#         # Get roles (assuming a Role model exists)
#         roles = Role.objects.all()

#         # Render placement form page with necessary context data
#         return render(request, 'student/placement_form.html', {
#             'student': student,
#             'companies': companies,
#             'roles': roles,
#             'willing_companies_ids': willing_companies_ids
#         })



def save_uploaded_pdfs(file_dict,request):
    student_id = request.session.get('student_id')

    profile_images_directory = os.path.join('media', 'resume')
    os.makedirs(profile_images_directory, exist_ok=True)

    file_paths = {}
    counter = 1
    for field_name, file_obj in file_dict.items():
        base_file_name = f'{student_id}.pdf'
        file_path = os.path.join(profile_images_directory, base_file_name)
        print(file_path)
# Check if the file already exists, if yes, append a number
        if os.path.exists(file_path):
            # If file exists, modify the file name with a counter
            new_file_name = f'{student_id}.pdf'
            file_path = os.path.join(profile_images_directory, new_file_name)
            print(file_path)
            


        with open(file_path, 'wb') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        file_paths[field_name] = file_path
        print(file_paths[field_name],"jjhjiiijiii")
    return file_paths

# def all_company(request):
#     # Get all companies ordered by company_id in descending order
#     student_id = request.session.get('student_id')
#     if not student_id:
#         return redirect('login')

#     try:
#         student = Student.objects.get(student_regno=student_id)

#         # Fetch the student's department
#         student_department = student.department  # Assuming you have a department field in Student

#         # Get willing companies ids for the student
#         willing_companies_ids = list(
#             Willingness.objects.filter(student=student).values_list('company_id', flat=True)
#         )
#         willing_companies_ids = [int(id) for id in willing_companies_ids]

#         # Get all companies and filter them based on department eligibility
#         companies = Company.objects.all().order_by('-company_id')

#         eligible_companies = []
#         for company in companies:
#             # Check if the student is eligible for this company
#             if DepartmentEligibility.objects.filter(company=company, department=student_department).exists():
#                 eligible_companies.append(company)

#     except Student.DoesNotExist:
#         return redirect('login')

#     context = {
#         'companies': companies, # Pass the eligible companies to the context
#         'student': student,
#         'willing_companies_ids': willing_companies_ids,
#     }
#     return render(request, 'student/all_company.html', context)

@student_required
def all_company(request):
    student_regno = request.session.get('student_id')
    if not student_regno:
        return redirect('login')

    student = get_object_or_404(Student, student_regno=student_regno)

    willing_companies_ids = list(
        Willingness.objects
                   .filter(student=student)
                   .values_list('company_id', flat=True)
    )

    student_batch = request.session.get('student_batch')  # e.g., "2022-26"

    if student_batch:
        try:
            start, end = student_batch.split('-')
            if len(end) == 2:
                student_batch = f"{start}-{start[:2]}{end}"  # → "2022-2026"
                print("Formatted batch:", student_batch)
        except Exception as e:
            print("Batch formatting failed:", e)
            # Optionally set student_batch to None or fallback value
            student_batch = None

    if student_batch:
        companies = Company.objects.filter(
            company_academic_year=student_batch
        ).order_by('-company_id')
    else:
        companies = Company.objects.all().order_by('-company_id')

    context = {
        'companies': companies,
        'student': student,
        'willing_companies_ids': willing_companies_ids,
    }
    return render(request, 'student/all_company.html', context)




@student_required
def company_details(request, company_id):
    # Use `company_id` instead of `id`
    company = get_object_or_404(Company, company_id=company_id)

    # Fetch the student ID from the session
    student_id = request.session.get('student_id')
    print("Details are " , company, student_id)
    if not student_id:
        return JsonResponse({'error': 'Student not logged in'}, status=400)

    # Fetch the student from the main database
    student = get_object_or_404(Student, student_regno=student_id)

    try:
        # Fetch the student academic details from a different database
        application_student = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=student_id)

        # Check eligibility based on CGPA
        is_eligible = application_student.cgpa >= company.company_eligibility

       # Check if hsc value can be converted to a float and is eligible by HSC
        if application_student.hsc:
            try:
                hsc_value = float(application_student.hsc)  # Convert varchar to float
                is_eligible_by_hsc_or_diploma = hsc_value >= company.company_eligibility_hsc
            except ValueError:
                is_eligible_by_hsc_or_diploma = False  # Handle cases where conversion fails
                print("Invalid HSC value, unable to compare eligibility.")

        # Check if diploma value is not 'nan' or 0 and is eligible by diploma
        if application_student.diploma != 'nan' and application_student.diploma != 0:
            try:
                diploma_value = float(application_student.diploma)  # Convert varchar to float
                is_eligible_by_hsc_or_diploma = diploma_value >= company.company_eligibility_diploma
            except ValueError:
                is_eligible_by_hsc_or_diploma = False  # Handle cases where conversion fails
                print("Invalid Diploma value, unable to compare eligibility.")


        is_eligible_by_sslc = application_student.sslc >= company.company_eligibility_sslc

        history_of_arrear = application_student.history_of_arrear <= company.history_of_arrear

        bag_of_logs =  application_student.bag_of_log <= company.no_standing_arrear
        # Check eligibility based on department using DepartmentEligibility model
        is_eligible_by_dept = DepartmentEligibility.objects.filter(
            company=company,
            department=application_student.department
        ).exists()

        # Determine overall eligibility
        eligible = is_eligible and is_eligible_by_dept and is_eligible_by_hsc_or_diploma and is_eligible_by_sslc and history_of_arrear and bag_of_logs
        print(eligible, "blh blah ")

    except ApplicationStudent.DoesNotExist:
        return JsonResponse({'error': 'Student details not found in secondary database'}, status=404)

    # Prepare response data
    response_data = {
        'company_name': company.company_name,
        'company_location': company.company_location,
        'company_role': company.company_role,
        'company_skill': company.company_skill,
        'company_eligibility': company.company_eligibility,
        'company_description': company.company_description,
        'company_last_date': company.company_last_date,
        'is_eligible': eligible
    }
    print(response_data,"sjhfsjh")

    return JsonResponse(response_data)

@student_required
@csrf_exempt
def submit_willingness(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company_id = data.get('company_id')
            status = data.get('status')
            student_regno = data.get('student_regno')

            # Fetch the Company object
            company = Company.objects.get(pk=company_id)
            student = Student.objects.get(student_regno=student_regno)

            # Check if a Willingness entry already exists
            willingness_entry, created = Willingness.objects.get_or_create(
                company=company,
                student=student,
                defaults={'willingness': status}
            )

            if not created:
                # If it already exists, update the willingness status
                willingness_entry.willingness = status
                willingness_entry.save()

            return JsonResponse({'success': True})
        except Company.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Company not found'})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@student_required
def Wishlist(request):
    application_students = ApplicationStudent.objects.using('rit_cgpatrack').all()

    student_id = request.session.get('student_id')
    student = Student.objects.get(student_regno=student_id)

    # Get companies where the student has given willingness
    willing_companies = Company.objects.filter(
        willingness__student=student,
        willingness__willingness='willing'
    ).distinct()

    context = {
        'willing_companies': willing_companies,
        'application_students': application_students,
    }
    return render(request, 'student/wishlist.html', context)



def view_training(request):
    # Get the student_id from the session
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    # Get all trainers ordered by trainer name in descending order, and include related company info
    trainers = Trainer.objects.all().select_related('company').order_by('-trainer_name')

    # Prepare context data, including the trainers and their associated company information
    context = {
        'trainers': trainers,
    }

    return render(request, 'student/view_training.html', context)



def training_company(request, trainer_id):
    # Get the trainer object or return a 404 error if not found
    trainer = get_object_or_404(Trainer, trainer_id=trainer_id)

    # Get the related company object using the ForeignKey relationship
    company = get_object_or_404(TrainingCompanyDetails, training_company_id=trainer.company.training_company_id)

    # Get the related departments for the company, and create a comma-separated string
    departments = company.eligibility_departments.all()
    department_list = ', '.join([dept.department for dept in departments])

    # Prepare response data, including the department list
    response_data = {
        'trainer_id': trainer.trainer_id,
        'company_name': company.company_name,
        'company_address': company.company_address,
        'company_place': company.company_place,
        'company_email': company.company_email,
        'company_opening_date': company.company_opening_date,
        'company_last_date': company.company_last_date,
        'description': trainer.description,
        'topics': trainer.topics,
        'departments': department_list,  # Added departments as a comma-separated string
    }

    return JsonResponse(response_data)

from .forms import FeedbackForm

def feedback_view(request):
    if request.method == 'POST':
        print("Feed back came ")
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Save the feedback to the database
            return JsonResponse({'status': 'success', 'message': 'Feedback submitted successfully!'})
        else:
            print(form.errors)
            return JsonResponse({'status': 'error', 'message': 'Invalid form data!'})

    return render(request, 'feedback_form.html')




def interview_exp(request):
    application_students = ApplicationStudent.objects.using('rit_cgpatrack').all()

    student_id = request.session.get('student_id')
    student = Student.objects.get(student_regno=student_id)

    # Get companies where the student has been placed
    placed_companies = Company.objects.filter(
        placement__student_reg_id=student
    ).distinct()
    print(placed_companies)

    context = {
        'placed_companies': placed_companies,  # Update context to include placed companies
        'application_students': application_students,
        'student_id':student_id,
    }
    return render(request, 'student/share_experience.html', context)


def show_exp(request):
    application_students = ApplicationStudent.objects.using('rit_cgpatrack').all()

    student_id = request.session.get('student_id')

    placed_companies = Company.objects.all().order_by('-company_id')
    # Get companies where the student has been placed


    context = {
        'placed_companies': placed_companies,  # Update context to include placed companies
        'application_students': application_students,
        'student_id':student_id,
    }
    return render(request, 'student/show_experience.html', context)


from .models import Experience, Student, Company
 # Use with caution, ensure CSRF protection is handled
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

 # Use this for testing; consider CSRF protection for production
def submit_experience(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)

            # Extract values from the parsed JSON
            student_id = data.get('student_id')
            company_id = data.get('company_id')
            round1 = data.get('round1')
            round2 = data.get('round2')
            round3 = data.get('round3')
            round4 = data.get('round4')

            print("Student ID:", student_id)
            print("Company ID:", company_id)

            # Save the experience data to the database
            experience = Experience(
                student_id=student_id,  # Assuming you have a ForeignKey to Student model
                company_id=company_id,  # Assuming you have a ForeignKey to Company model
                round1_details=round1,
                round2_details=round2,
                round3_details=round3,
                round4_details=round4,
            )
            experience.save()

            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)



from django.http import JsonResponse
from django.db.models import OuterRef, Subquery
from .models import Experience, ApplicationStudent  # Make sure to import your models

def get_experience(request, company_id):
    if request.method == 'GET':
        experiences = Experience.objects.filter(company=company_id).values(
            'student__student_regno',  # Fetching student registration number
            'round1_details',
            'round2_details',
            'round3_details',
            'round4_details'
        )

        # Create a list to store the full experience details
        experience_list = []

        for exp in experiences:
            # Get the student registration number
            student_regno = exp['student__student_regno']

            # Fetch the associated ApplicationStudent details
            try:
                app_student = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=student_regno)
                experience_list.append({
                    'student_regno': student_regno,
                    'student_name': app_student.student_name,
                    'department': app_student.department,
                    'cgpa': app_student.cgpa,
                    'batch': app_student.batch,
                    'round1_details': exp['round1_details'],
                    'round2_details': exp['round2_details'],
                    'round3_details': exp['round3_details'],
                    'round4_details': exp['round4_details'],
                })
            except ApplicationStudent.DoesNotExist:
                # Handle case where ApplicationStudent is not found
                experience_list.append({
                    'student_regno': student_regno,
                    'student_name': 'Unknown',
                    'department': 'Unknown',
                    'cgpa': 'Unknown',
                    'batch': 'Unknown',
                    'round1_details': exp['round1_details'],
                    'round2_details': exp['round2_details'],
                    'round3_details': exp['round3_details'],
                    'round4_details': exp['round4_details'],
                })

        return JsonResponse({'status': 'success', 'experiences': experience_list}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
