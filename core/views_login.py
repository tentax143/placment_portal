
from django.shortcuts import render, redirect
from django.conf import settings
from .models import  Student , Placement_User
from .forms import StudentLoginForm, StaffLoginForm, StaffFirstLoginForm,StudentLoginForm, StudentFirstLoginForm 
import hashlib

def encrypt_password(raw_password):
    return hashlib.sha256(raw_password.encode()).hexdigest()



#LOGINS :
def student_login(request):
    if request.method == 'POST':
        print("1OIII")
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            print("2OIII")
            regno = form.cleaned_data['regno']
            password = form.cleaned_data['password']
            try:
                student = Student.objects.get(student_regno=regno)
                print(student,"fhsukfhsdf")
                if student.student_password != 'nan' and student.student_password :
                    if student.student_password == encrypt_password(password):

                        #WHOM
                        request.session['whom'] = "STUDENT"

                        request.session['student_id'] = regno

                        return redirect('student_dashboard')
                    else:
                        form.add_error('password', 'Incorrect password.')
                else:
                    return redirect('first_login', regno=regno)
            except Student.DoesNotExist:
                form.add_error('regno', 'Unauthorized')
    else:
        form = StudentLoginForm()

    return render(request, 'auth/student_login.html')

def first_login(request, regno):
    print("djsfijfdsij")
    try:
        student = Student.objects.get(student_regno=regno)
        print(student,"wreskdjf")
    except Student.DoesNotExist:
        return redirect('student_login')

    if request.method == 'POST':
        form = StudentFirstLoginForm(request.POST, instance=student)
        
        if form.is_valid():
            user=form.save(commit=False)
            user.student_password = encrypt_password(user.student_password)
            user.save()
            return redirect('student_login')
    else:
        form = StudentFirstLoginForm()

    return render(request, 'auth/first_login.html', {'form': form, 'regno': regno})

def staff_login(request):
    if request.method == 'POST':
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            faculty_id = form.cleaned_data['faculty_id']
            password = form.cleaned_data['password']
            try:
                faculty = Placement_User.objects.get(faculty_id=faculty_id)
                
                if faculty.faculty_password:
                    if faculty.faculty_password == encrypt_password(password):
                        if faculty.faculty_role == "ALL" or faculty.faculty_role == "HOD":
                            request.session['whom'] = "ADMIN"
                            request.session['role'] = faculty.faculty_role
                            request.session['dept'] = faculty.faculty_dept
                            request.session['name'] = faculty.faculty_name
                            request.session['faculty_id'] = faculty_id
                            print("During auth , the Role , is " , faculty.faculty_role)
                            return redirect('filter_dashboard')
                        else:
                            request.session['whom'] = "STAFF"
                            
                        request.session['role'] = faculty.faculty_role
                        request.session['dept'] = faculty.faculty_dept
                        request.session['faculty_id'] = faculty_id
                        return redirect('staff_dashboard')
                    else:
                        form.add_error('password', 'Incorrect password.')
                else:
                    return redirect('first_staff_login' , faculty_id)
            except Placement_User.DoesNotExist:
                form.add_error('faculty_id', 'Unauthorized')
    else:
        form = StaffLoginForm()
    return render(request, 'auth/staff_login.html')

def first_staff_login(request, faculty_id):
    try:
        faculty = Placement_User.objects.get(faculty_id=faculty_id)
    except Placement_User.DoesNotExist:
        return redirect('staff_login')

    if request.method == 'POST':
        form = StaffFirstLoginForm(request.POST)
        if form.is_valid():
            faculty_name = form.cleaned_data['faculty_name']
            faculty_email = form.cleaned_data['faculty_email']
            if faculty.faculty_name == faculty_name and faculty.faculty_email == faculty_email:
                faculty.faculty_password = encrypt_password(form.cleaned_data['faculty_password'])
                faculty.save()
                return redirect('staff_login')
            else:
                form.add_error(None, 'Name or email does not match our records.')
    else:
        form = StaffFirstLoginForm()

    return render(request, 'auth/first_staff_login.html', {'form': form, 'faculty_id': faculty_id})


from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Encrypt the password before saving
            faculty_password = encrypt_password(form.cleaned_data['faculty_password'])
            faculty = form.save(commit=False)  # Create the object but don't save it to the DB yet
            faculty.faculty_password = faculty_password  # Set the encrypted password
            faculty.save()  # Now save it to the DB
            return redirect('staff_login')  # Redirect after successful signup
    else:
        form = SignupForm()

    return render(request, 'auth/signup.html', {'form': form})
    

from django.http import FileResponse
from django.conf import settings
import os

def download_manual(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'manuals', 'manual.pdf')
    print("=======================================================================")
    print(file_path)
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')