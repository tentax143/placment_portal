from django.shortcuts import render , get_object_or_404
from django.conf import settings
from django.db.models import Count
from .forms import FacultyForm
from .models import Company , Willingness , ApplicationStudent , Placement , Trainer , TrainingCompanyDetails , TrainingCompanyDept , FeedbackDetails
from django.http import JsonResponse
from .decorators import admin_required , admin_specific_role_required

@admin_required
# @admin_specific_role_required(['ALL'])
def analytics_dashboard(request):
    whom = request.session.get('whom')
    return render(request,'admin/analytics_dashboard.html' , {'whom': whom})

# @admin_required
# def filter_dashboard(request):
#     whom = request.session.get('whom')
#     dept = request.session.get('dept')

#     print(whom, dept)
    
#     # Predefined list of departments
#     predefined_departments = [
#         ("B.TECH AD", "AD-ARTIFICIAL INTELLIGENCE AND DATA SCIENCE"),
#         ("B.E CIVIL", "CE-CIVIL ENGINEERING"),
#         ("B.TECH CSBS", "CB-COMPUTER SCIENCE AND BUSINESS SYSTEM"),
#         ("B.E CSE", "CS-COMPUTER SCIENCE AND ENGINEERING"),
#         ("B.E EEE", "EE-ELECTRICAL AND ELECTRONICS ENGINEERING"),
#         ("B.E ECE", "EC-ELECTRONICS AND COMMUNICATION ENGINEERING"),
#         ("B.TECH IT", "IT-INFORMATION TECHNOLOGY"),
#         ("B.E MECH", "ME-MECHANICAL ENGINEERING"),
#     ]

#     selected_placement_type = ["Placement Offer", "Internship + Placement Offer"]

#     # Initialize the department count with 0 for each predefined department
#     dept_counts = {dept[0]: 0 for dept in predefined_departments}

#     # Check if batch is provided in the URL parameters
#     batch = request.GET.get('batch')
#     print("BATCH", batch)
#     students_count = 0
#     # If batch is provided
#     if batch:
#         # Filter students by batch
#         students = list(ApplicationStudent.objects.using('rit_cgpatrack').filter(batch=batch).values_list('reg_no', flat=True))
#         students_count = len(students)
#         print("===================================AT BATCH=================================")
#     else:
#         # Get all students if batch is not provided
#         students = list(ApplicationStudent.objects.using('rit_cgpatrack').all().values_list('reg_no', flat=True))
#         students_count = len(students)

#     # Filter placements based on student reg numbers and placement offer types
#     # placements = Placement.objects.filter(student_reg_id__in=students, placement_offer__in=selected_placement_type).distinct()
#     # print(placements)

#     placements = Placement.objects.filter(
#     student_reg_id__in=students,
#     placement_offer__in=selected_placement_type
#     ).values('student_reg_id').distinct()
#     unique_students = []
#     print(placements)
#     for placement in placements:
#         student_reg_no = placement['student_reg_id']
#         unique_students.append(student_reg_no)
#     print(unique_students)


#     placements_count = 0
#     # Count the placements for each department
#     for placement in placements:
#         student_reg_no = placement['student_reg_id']  # Assuming student_regno is the correct field
#         print(student_reg_no)
#         # Fetch the student's department from the ApplicationStudent model
#         try:
#             student = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=student_reg_no)
#             student_department = student.department
#             print(student_department)  # Get the department from the student record
            
#             # Increment the department count
#             for short_name, full_name in predefined_departments:
#                 if short_name == student_department:
#                     dept_counts[short_name] += 1
#                     placements_count +=1
#         except ApplicationStudent.DoesNotExist:
#             print(f"Student with registration number {student_reg_no} not found in ApplicationStudent.")

#     # Total placements count
#     if placements_count !=0 :
#         placement_percentage = (placements_count/students_count) * 100
#     else:
#         placement_percentage = 0

#     placement_percentage = round(placement_percentage , 1)
#     # Prepare the context data to pass to the template
#     context = {
#         'whom': whom,
#         'dept': dept,
#         'dept_counts': dept_counts,
#         'placements_count':placements_count,
#         'placement_percentage':placement_percentage

#     }

#     return render(request, 'admin/filter_dashboard.html', context)

def filter_dashboard(request):
    whom = request.session.get('whom')
    dept = request.session.get('dept')

    print(whom, dept)
    
    # Predefined list of departments
    predefined_departments = [
        ("B.TECH AD", "AD-ARTIFICIAL INTELLIGENCE AND DATA SCIENCE"),
        ("B.E CIVIL", "CE-CIVIL ENGINEERING"),
        ("B.TECH CSBS", "CB-COMPUTER SCIENCE AND BUSINESS SYSTEM"),
        ("B.E CSE", "CS-COMPUTER SCIENCE AND ENGINEERING"),
        ("B.E EEE", "EE-ELECTRICAL AND ELECTRONICS ENGINEERING"),
        ("B.E ECE", "EC-ELECTRONICS AND COMMUNICATION ENGINEERING"),
        ("B.TECH IT", "IT-INFORMATION TECHNOLOGY"),
        ("B.E MECH", "ME-MECHANICAL ENGINEERING"),
    ]

    selected_placement_type = ["Placement Offer", "Internship + Placement Offer"]

    # Initialize the department count with 0 for each predefined department
    dept_counts = {dept[0]: 0 for dept in predefined_departments}
    
    # Initialize dictionaries for tracking unique students per department and placement counts
    unique_students_by_dept = {dept[0]: {} for dept in predefined_departments}
    placement_counts_by_dept = {dept[0]: {'1': 0, '2': 0, '3': 0} for dept in predefined_departments}

    # Check if batch is provided in the URL parameters
    batch = request.GET.get('batch')
    print("BATCH", batch)
    students_count = 0
    
    # If batch is provided
    if batch:
        # Filter students by batch
        students = list(ApplicationStudent.objects.using('rit_cgpatrack').filter(batch=batch).values_list('reg_no', flat=True))
        students_count = len(students)
        print("===================================AT BATCH=================================")
        
        # Filter placements based on student reg numbers and placement offer types
        placements = Placement.objects.filter(
            student_reg_id__in=students,
            placement_offer__in=selected_placement_type
        ).values('student_reg_id', 'company_id').distinct()

        # Count the placements for each student and department
        student_placement_counts = {}
        for placement in placements:
            student_reg_no = placement['student_reg_id']
            if student_reg_no in student_placement_counts:
                student_placement_counts[student_reg_no] += 1
            else:
                student_placement_counts[student_reg_no] = 1

        # Count placements per department
        for student_reg_no, count in student_placement_counts.items():
            try:
                student = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=student_reg_no)
                student_department = student.department
                print(student_department)

                for short_name, full_name in predefined_departments:
                    if short_name == student_department:
                        # Increment department counts
                        dept_counts[short_name] += 1
                        unique_students_by_dept[short_name][student_reg_no] = count  # Store placement count per student
                        
                        # Classify the student based on their number of placements
                        if count == 1:
                            placement_counts_by_dept[short_name]['1'] += 1
                        elif count == 2:
                            placement_counts_by_dept[short_name]['2'] += 1
                        else:
                            placement_counts_by_dept[short_name]['3'] += 1
            except ApplicationStudent.DoesNotExist:
                print(f"Student with registration number {student_reg_no} not found in ApplicationStudent.")

        # Total placements count
        placements_count = sum(dept_counts.values())
        placement_percentage = (placements_count / students_count * 100) if students_count > 0 else 0
        placement_percentage = round(placement_percentage, 1)

        # Calculate department-specific placement percentages
        dept_percentages = {short_name: 0 for short_name in dept_counts.keys()}
        for short_name in dept_counts.keys():
            if students_count > 0 and dept_counts[short_name] > 0:
                dept_percentages[short_name] = round((dept_counts[short_name] / students_count) * 100, 1)
        print("======================================")
        print(placement_counts_by_dept)
        print("======================================")
        # Prepare the context data to pass to the template
        context = {
            'whom': whom,
            'dept': dept,
            'dept_counts': dept_counts,
            'placements_count': placements_count,
            'placement_percentage': placement_percentage,
            'unique_students_by_dept': {k: list(v.keys()) for k, v in unique_students_by_dept.items()},
            'placement_counts_by_dept': placement_counts_by_dept,  # Add placement count stats per department
            'dept_percentages': dept_percentages,
            'value': "exist",
            'batch':batch
        }

        return render(request, 'admin/filter_dashboard.html', context)

    else:
        # If batch is not provided
        context = {
            'whom': whom,
            'dept': dept,
            'value': "",
        }

        return render(request, 'admin/filter_dashboard.html', context)

   

from django.http import JsonResponse
from .models import Placement, ApplicationStudent

def placement_statistics(request):
    # Predefined list of departments
    predefined_departments = [
        ("B.TECH AD", "AD-ARTIFICIAL INTELLIGENCE AND DATA SCIENCE"),
        ("B.E CIVIL", "CE-CIVIL ENGINEERING"),
        ("B.TECH CSBS", "CB-COMPUTER SCIENCE AND BUSINESS SYSTEM"),
        ("B.E CSE", "CS-COMPUTER SCIENCE AND ENGINEERING"),
        ("B.E EEE", "EE-ELECTRICAL AND ELECTRONICS ENGINEERING"),
        ("B.E ECE", "EC-ELECTRONICS AND COMMUNICATION ENGINEERING"),
        ("B.TECH IT", "IT-INFORMATION TECHNOLOGY"),
        ("B.E MECH", "ME-MECHANICAL ENGINEERING"),
    ]

    selected_placement_type = ["Placement Offer", "Internship + Placement Offer"]

    # Initialize the department count with 0 for each predefined department
    dept_counts = {dept[0]: 0 for dept in predefined_departments}

    # Check if batch is provided in the URL parameters
    batch = request.GET.get('batch')

    # If batch is provided
    if batch:
        # Filter students by batch
        students = ApplicationStudent.objects.filter(batch=batch).values_list('reg_no', flat=True)
    else:
        # Get all students if batch is not provided
        students = ApplicationStudent.objects.all().values_list('reg_no', flat=True)

    # Filter placements based on student reg numbers and placement offer types
    placements = Placement.objects.filter(student_regno__in=students, placement_offer__in=selected_placement_type)

    # Count the placements for each department
    for placement in placements:
        student_reg_no = placement.student_regno  # Assuming student_regno is the correct field

        # Fetch the student's department from the ApplicationStudent model
        try:
            student = ApplicationStudent.objects.get(reg_no=student_reg_no)
            student_department = student.department  # Get the department from the student record
            
            # Increment the department count
            for short_name, full_name in predefined_departments:
                if full_name == student_department:
                    dept_counts[short_name] += 1
        except ApplicationStudent.DoesNotExist:
            print(f"Student with registration number {student_reg_no} not found in ApplicationStudent.")

    # Total placements count
    placements_count = placements.count()

    # Prepare context data to pass to the template
    context = {
        'dept_counts': dept_counts,
        'placements_count': placements_count,
    }

    return JsonResponse(context)


from django.db.models import Count
from core.models import Willingness, ApplicationStudent, Company , Role



@admin_required
def placement_dashboard(request):
    whom = request.session.get('whom')
    dept = request.session.get('dept')
    roles = Role.objects.all()
    context = {
        'whom': whom,
        'dept': dept,
        'roles':roles
    }
    return render(request, 'admin/placement_dashboard.html',context)


@admin_required
def willingness_dashboard(request):
    whom = request.session.get('whom')
    dept = request.session.get('dept')
    roles = Role.objects.all()

    context = {
        'whom': whom,
        'dept': dept,
        'roles':roles
    }
    return render(request, 'admin/willingness_dashboard.html',context)



# ==============-=-=-=-=-=-=-======================================================================-=-=-
from django.http import JsonResponse
from .models import Placement, ApplicationStudent, Company

from django.http import JsonResponse
from django.shortcuts import render
from .models import Placement, ApplicationStudent, Company

def filter_table_view(request):
    # Initialize filter variables
    department = request.GET.get('department', '')
    batch = request.GET.get('batch', '')
    company = request.GET.get('company', '')
    placement_type = request.GET.get('placement_type', '')
    company_type = request.GET.get('company_type', '')
    job_type = request.GET.get('job_type', '')
    job_domain = request.GET.get('job_domain', '')

    # Step 1: Fetch students based on department and batch filters
    student_query = ApplicationStudent.objects.using('rit_cgpatrack').all()

    # Filter students by department if provided
    if department:
        student_query = student_query.filter(department=department)
        student_reg_ids = list(student_query.values_list('reg_no', flat=True))
        placement_data_count = Placement.objects.filter(student_reg_id__in=student_reg_ids)
        placement_data_core_count = placement_data_count.filter(job_domain="Core").count()
        placement_data_non_core_count = placement_data_count.filter(job_domain="Non - Core").count()

    # Filter students by batch if provided
    if batch:
        student_query = student_query.filter(batch=batch)
    # Extract student registration numbers that match the filters
    student_reg_ids = list(student_query.values_list('reg_no', flat=True))
    # Step 2: Fetch Placement data based on the filtered student registration numbers
    placement_data = Placement.objects.filter(student_reg_id__in=student_reg_ids)
  

    # Step 3: Further filter placements based on company if provided
    if company:
        placement_data = placement_data.filter(company_id=company)

    # Further filter placements by placement type if provided
    if placement_type:
        placement_data = placement_data.filter(placement_offer=placement_type)
    
    if job_type:
        placement_data = placement_data.filter(job_type=job_type)
    
    if company_type:
        placement_data = placement_data.filter(company_type=company_type)
    
    if job_domain:
        placement_data = placement_data.filter(job_domain=job_domain)

    # Create a mapping for quick lookup of students
    students = ApplicationStudent.objects.using('rit_cgpatrack').filter(reg_no__in=student_reg_ids)
    student_map = {student.reg_no: student for student in students}
   

    # Step 4: Combine data for the response
    data = []
    for placement in placement_data:
        student = placement.student_reg_id
        app_student = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=student)
      
        if student:
            data.append({
                'reg_no': app_student.reg_no,
                'student_name': app_student.student_name,
                'dept': app_student.department,
                'batch': app_student.batch,
                'cgpa': app_student.cgpa,
                'company': placement.company_id.company_name,
                'placement_type': placement.placement_offer,
                'rounds_passed': sum([bool(placement.round1), bool(placement.round2), bool(placement.round3), bool(placement.round4)]),
                'stipend_or_ctc': placement.stipend or placement.ctc,
                'contact_number': app_student.contact_number,  # Placeholder for contact number
                'job_role' :placement.job_type
            })
    


    # Return JSON response for AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'data': data ,  'placement_data_core_count' :placement_data_core_count,
                'placement_data_non_core_count':placement_data_non_core_count})

    # If not an AJAX request, render the default template
    return render(request, 'company_table.html', {'data': data})



from django.http import JsonResponse
from django.shortcuts import render
from .models import Company, Student, Willingness, ApplicationStudent

def willingness_table_view(request):
    # Initialize filter variables
    department = request.GET.get('department', '')
    batch = request.GET.get('batch', '')
    company_id = request.GET.get('company', '')


    # Step 1: Fetch students based on department and batch filters
    student_query = ApplicationStudent.objects.using('rit_cgpatrack').all()

    # Filter students by department if provided
    print(department)

    if department == "All":
        department = ""
    if department:
        student_query = student_query.filter(department=department)

    # Filter students by batch if provided
    if batch:
        student_query = student_query.filter(batch=batch)

    # Extract student registration numbers that match the filters
    student_reg_ids = list(student_query.values_list('reg_no', flat=True))

    # Step 2: If no department is specified, fetch all willingness data
    if not department:
        willingness_data = Willingness.objects.all()  # Get all willingness records
    else:
        # Fetch Willingness data based on the filtered student registration numbers
        willingness_data = Willingness.objects.filter(student__student_regno__in=student_reg_ids)

    # Step 3: Further filter willingness data based on company if provided
    if company_id:
        willingness_data = willingness_data.filter(company_id=company_id)

    # Step 4: Combine data for the response
    data = []
    for willingness in willingness_data:
        try:
            student = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=willingness.student.student_regno)  # Get ApplicationStudent
        except Exception as e:
            # Print the exception type and message
            print(f"Exception occurred: {type(e).__name__}: {e}")
            # Print a full traceback for more details
            print("Traceback details:")
            # traceback.print_exc()
        company = willingness.company
        data.append({
            'reg_no': student.reg_no,
            'student_name': student.student_name,  # This exists in ApplicationStudent
            'dept': student.department,             # This exists in ApplicationStudent
            'batch': student.batch,
            'company': company.company_name,
            'stipend_or_ctc': company.company_ctc,  # You can adjust this based on your needs
            'job_role': company.company_role,               # This exists in ApplicationStudent
            'cgpa': student.cgpa,
            'sslc' : student.sslc,
            'hsc'  : student.hsc, # This exists in ApplicationStudent
            'history_of_arrear': student.history_of_arrear,
            'bag_of_log' : student.bag_of_log ,
            'diploma'     : student.diploma ,  # This exists in ApplicationStudent
              # You can adjust this based on your needs
            'contact_number': student.contact_number,  # Placeholder for contact number
        })

    # Return JSON response for AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'data': data})

    # If not an AJAX request, render the default template
    return render(request, 'company_table.html', {'data': data})



# ==============-=-=-=-=-=-=-======================================================================-=-=-



def all_company(request):
    # Predefined list of departments
    predefined_departments = [
        ("B.TECH AD", "AD-ARTIFICIAL INTELLIGENCE AND DATA SCIENCE"),
        ("B.E CIVIL", "CE-CIVIL ENGINEERING"),
        ("B.TECH CSBS", "CB-COMPUTER SCIENCE AND BUSINESS SYSTEM"),
        ("B.E CSE", "CS-COMPUTER SCIENCE AND ENGINEERING"),
        ("B.E EEE", "EE-ELECTRICAL AND ELECTRONICS ENGINEERING"),
        ("B.E ECE", "EC-ELECTRONICS AND COMMUNICATION ENGINEERING"),
        ("B.TECH IT", "IT-INFORMATION TECHNOLOGY"),
        ("B.E MECH", "ME-MECHANICAL ENGINEERING"),
    ]

    # Get all companies ordered by company_id in descending order
    companies = Company.objects.all().order_by('-company_id')



    # Initialize a list to hold the company details along with willingness count by department
    company_willingness = []

    for company in companies:
        # Get all students who have shown willingness for this company
        willingness_students = Willingness.objects.filter(company=company).values_list('student_id', flat=True)

        # Convert to a list to use in the next query
        willingness_student_ids = list(willingness_students)



        # Initialize the department count with 0 for each predefined department
        dept_counts = {dept[0]: 0 for dept in predefined_departments}

        # Only proceed if there are students who showed willingness
        if willingness_student_ids:
            # Get the department of each student who showed willingness and count them
            willing_students = ApplicationStudent.objects.using('rit_cgpatrack').filter(reg_no__in=willingness_student_ids)



            # Count departments
            for student in willing_students:
                if student.department in dept_counts:
                    dept_counts[student.department] += 1

        # Append the company and its willingness count per department to the list
        company_willingness.append({
            'company': company,
            'dept_counts': dept_counts,
        })

    # Render the list of companies with their department-wise willingness counts
    return render(request, 'all_company.html', {
        'company_willingness': company_willingness,
        'predefined_departments': predefined_departments,
    })


def company_details(request, company_id):
    # Use `company_id` instead of `id`
    company = get_object_or_404(Company, company_id=company_id)
        
    
    # Prepare response data
    response_data = {
        'company_name': company.company_name,
        'company_location': company.company_location,
        'company_role': company.company_role,
        'company_skill': company.company_skill,
        'company_eligibility': company.company_eligibility,
        'company_description': company.company_description,
        'company_last_date': company.company_last_date,
    }
    
    return JsonResponse(response_data)

@admin_required
def add_staff(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST) 
     
        if form.is_valid():
          
            form.save()  # Save the data and image
            return render(request,'auth/success.html')  # Redirect to a success page
    else:
        form = FacultyForm()
        dept = request.session.get('dept')

    
    return render(request, 'admin/add_staff.html', {'form': form  , 'dept':dept})



def get_companies(request):
    # Fetch all companies
    companies = Company.objects.all().values('company_id', 'company_name')  # Adjust field names as necessary

    # Convert to a list of dictionaries
    company_list = list(companies)
 
    # Return as JSON response
    return JsonResponse({'companies': company_list})

def get_trainer_companies(request):
    # Fetch all companies
    department = request.GET.get('department', '')

    if department:
        # Get the companies that are eligible for the selected department
        eligible_companies = TrainingCompanyDept.objects.filter(department=department).select_related('trainer_company')
        
        # Prepare the response data with company details
        company_list = [{
            'training_company_id': company.trainer_company.training_company_id,
            'company_name': company.trainer_company.company_name
        } for company in eligible_companies]

        return JsonResponse({'companies': company_list})
    
    return JsonResponse({'companies': []})




   

 # Ensure to import your models

def filter_company_count(request):
    # Debugging print statement
 

    # Predefined list of departments
    predefined_departments = [
        ("B.TECH AD", "AD-ARTIFICIAL INTELLIGENCE AND DATA SCIENCE"),
        ("B.E CIVIL", "CE-CIVIL ENGINEERING"),
        ("B.TECH CSBS", "CB-COMPUTER SCIENCE AND BUSINESS SYSTEM"),
        ("B.E CSE", "CS-COMPUTER SCIENCE AND ENGINEERING"),
        ("B.E EEE", "EE-ELECTRICAL AND ELECTRONICS ENGINEERING"),
        ("B.E ECE", "EC-ELECTRONICS AND COMMUNICATION ENGINEERING"),
        ("B.TECH IT", "IT-INFORMATION TECHNOLOGY"),
        ("B.E MECH", "ME-MECHANICAL ENGINEERING"),
    ]

    # Get the selected company and placement type from the request
    selected_company_id = request.GET.get('company_id')
    selected_placement_type = request.GET.get('placement_type')
    print(selected_placement_type)

    # Initialize a list to hold the company details along with willingness count by department
    company_willingness = []

    # Fetch the company ID
    company = Company.objects.filter(company_id=selected_company_id).values('company_id').first()
    company_id = company['company_id'] if company else None

    # Initialize the department count with 0 for each predefined department
    dept_counts = {dept[0]: 0 for dept in predefined_departments}
    print(company_id)
    # Get all placements for the selected company and placement type
    placements = Placement.objects.filter(company_id=company_id, placement_offer=selected_placement_type)
    print(placements)

    # Count departments based on placements
    # Count departments based on placements
    for placement in placements:
    # Get the student's registration number from the placement record
        student_reg_no = placement.student_reg_id# This assumes student_reg_id is the foreign key

    # Fetch the student's department from the ApplicationStudent model in the 'rit_cgpatrack' database
        try:
            student = ApplicationStudent.objects.using('rit_cgpatrack').get(reg_no=student_reg_no)
            student_department = student.department  # Get the department from the student record
        
        # Increment the department count
            if student_department in dept_counts:
                dept_counts[student_department] += 1
        except ApplicationStudent.DoesNotExist:
            print(f"Student with registration number {student_reg_no} not found in ApplicationStudent.")


    # Append the company and its willingness count per department to the list
    company_willingness.append({
        'company': company_id if company_id else "Unknown Company",  # Handle if company is not found
        'dept_counts': dept_counts,
    })

    # Return a JSON response with the company willingness counts
    return JsonResponse({'company_willingness': company_willingness})



@admin_required
def training_dashboard(request):
    whom = request.session.get('whom')
    dept = request.session.get('dept')
    context = {
        'whom': whom,
        'dept': dept,
    }
    return render(request, 'admin/trainer_dashboard.html' , context)






def filter_trainer_table_view(request):
    # Initialize filter variables from request
    department = request.GET.get('department', '')
    batch = request.GET.get('batch', '')
    company = request.GET.get('company', '')

    # Step 1: Initialize the trainer query
    trainer_query = Trainer.objects.all()

    # Step 2: Filter trainers by department if provided
    if department:
        trainer_query = trainer_query.filter(company__eligibility_departments__department=department)

    # Step 3: Filter trainers by batch if provided
    if batch:
        trainer_query = trainer_query.filter(company__company_academic_year=batch)

    # Step 4: Filter trainers by company if provided
    if company:
        trainer_query = trainer_query.filter(company__training_company_id=int(company))


    # Prepare the response data
    data = []
    for trainer in trainer_query:
        # Get the list of departments for the trainer's company
        departments = trainer.company.eligibility_departments.all()
        department_list = ', '.join([dept.department for dept in departments])
        
        # Append the trainer details to the data list
        data.append({
            'trainer_name': trainer.trainer_name,
            'dept': department_list,
            'batch': trainer.company.company_academic_year,
            'company': trainer.company.company_name,
            'topics': trainer.topics,
            'gender': trainer.trainer_gender,
            'start_date': trainer.company.company_opening_date,
            'end_date': trainer.company.company_last_date,
        })

    # Return the data as JSON for the AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'data': data})

    # If not an AJAX request, render a default template (if needed)
    return render(request, 'trainer_table.html', {'data': data})



def trainer_list_view(request):
    trainers = Trainer.objects.all()  # Get all trainers
    return render(request, 'admin/trainer_list.html', {'trainers': trainers})


def feedback_details_view(request, trainer_id):
    print("AT FEEDBACK RESPONSE     ")
    feedbacks = FeedbackDetails.objects.filter(trainer=trainer_id)
    feedback_data = feedbacks.values()  # Get all feedback as a list of dictionaries
    return JsonResponse(list(feedback_data), safe=False)


from django.db.models import Avg
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' before importing pyplot

import matplotlib.pyplot as plt
import numpy as np
from django.http import JsonResponse
from django.db.models import Avg
from .models import FeedbackDetails
from io import BytesIO
import base64

def get_feedback_for_trainer(request, trainer_id):
    # Get feedback for the selected trainer
    feedbacks = FeedbackDetails.objects.filter(trainer_id=trainer_id)
    print("Came into feed back form")
    # Aggregate feedback counts
    if not feedbacks.exists():
        return JsonResponse({"error": "No feedback found for this trainer"}, status=404)

    print("Came into feed back form")

    # Calculate averages
    course_content_count = feedbacks.aggregate(Avg('course_content'))['course_content__avg']
    lecture_sessions_count = feedbacks.aggregate(Avg('lecture_sessions'))['lecture_sessions__avg']
    practical_sessions_count = feedbacks.aggregate(Avg('practical_sessions'))['practical_sessions__avg']
    interactive_sessions_count = feedbacks.aggregate(Avg('interactive_sessions'))['interactive_sessions__avg']
    course_material_count = feedbacks.aggregate(Avg('course_material'))['course_material__avg']
    usefulness_count = feedbacks.aggregate(Avg('usefulness'))['usefulness__avg']
    timely_communication_count = feedbacks.aggregate(Avg('timely_communication'))['timely_communication__avg']
    overall_arrangement_count = feedbacks.aggregate(Avg('overall_arrangement'))['overall_arrangement__avg']

    print("Came into feed back form")
    # Data for chart
    data = {
        'Course Content': course_content_count,
        'Lecture Sessions': lecture_sessions_count,
        'Practical Sessions': practical_sessions_count,
        'Interactive Sessions': interactive_sessions_count,
        'Course Material': course_material_count,
        'Usefulness': usefulness_count,
        'Timely Communication': timely_communication_count,
        'Overall Arrangement': overall_arrangement_count,
    }
    print("Came into feed back form")
    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is a circle.
    print("123Came into feed back form")
    # Save to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    print("Came into feed back form")
    # Encode the image to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)  # Close the figure to free memory
    print("123Came into feed back form")
    # Render the image in an HTML img tag
    return JsonResponse({"image": f"data:image/png;base64,{image_base64}"})

from django.shortcuts import render, redirect
from django.contrib import messages
from hashlib import sha256
from .models import Placement_User
from django.contrib.messages import get_messages


def encrypt_password(password):
    """Encrypt the password using SHA-256."""
    return sha256(password.encode()).hexdigest()

def update_faculty_password(request):
    if request.method == 'GET':
        get_messages(request)  
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')  # Get the faculty ID
        new_password = request.POST.get('faculty_password')  # Get the new password

        # Encrypt the new password
        encrypted_password = encrypt_password(new_password)

        # Get department from session
        session_dept = request.session.get('dept', None)  # Assuming faculty_dept is stored in session

        # Update password for the specified faculty member
        try:
            faculty_member = Placement_User.objects.get(faculty_id=faculty_id)  # Get the faculty member by ID
            
            # Check if session department is "ALL" or matches the faculty's department
            if session_dept == "ALL" or session_dept == faculty_member.faculty_dept:
                faculty_member.faculty_password = encrypted_password  # Update the password
                faculty_member.save()  # Save the changes
                messages.success(request, 'Password updated successfully for faculty')
            else:
                messages.error(request, 'You do not have permission to update this faculty member.')

        except Placement_User.DoesNotExist:
            messages.error(request, 'Faculty ID not found.')

        return redirect('update_faculty_password')  # Redirect to the update password view

    return render(request, 'admin/change_password.html')  # Render the form if GET

