"""
URL configuration for placement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from core import views , views_login , views_admin , views_staff , views_student, gemini
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Main URLS
    path("admin_of_django/", admin.site.urls),
    path('', views.index, name="index"),

    #Login URLS
    path('auth/student_login/', views_login.student_login, name='student_login'),
    path('auth/student_first_login/<str:regno>/', views_login.first_login, name='first_login'),
    path('auth/staff_login/', views_login.staff_login, name='staff_login'),
    path('auth/staff_first_login/<str:faculty_id>/', views_login.first_staff_login, name='first_staff_login'),

    #Logout URLS
    path('logout/', views.logout, name='logout'),

    #ADMIN URLS
    path('admin/add_staff' ,  views_admin.add_staff , name="add_staff"),
    path('admin/analytics_dashboard', views_admin.analytics_dashboard, name="analytics_dashboard"),
    path('company', views_admin.all_company, name="admin_company"),
    path('admin/filter_dashboard', views_admin.filter_dashboard, name="filter_dashboard"),

    path('admin/company/<int:company_id>/', views_admin.company_details, name='admin_company_details'),
    path('get-companies/', views_admin.get_companies, name='get_companies'),
    path('get-trainer-companies/', views_admin.get_trainer_companies, name='get_trainer_companies'),
    path('filter_company_count/', views_admin.filter_company_count, name='filter_company_count'),
    path('admin/placement_dashboard', views_admin.placement_dashboard, name="placement_dashboard"),
      path('admin/willingness_dashboard', views_admin.willingness_dashboard, name="willingness_dashboard"),
    path('admin/filter_table_view/', views_admin.filter_table_view, name='filter_table_view'), # URL for the all_company view
        path('admin/willingness_table_view/', views_admin.willingness_table_view, name='willingness_table_view'), # URL for the all_company view

    path('admin/update-faculty-password/', views_admin.update_faculty_password, name='update_faculty_password'),

    path('admin/training_dashboard', views_admin.training_dashboard, name="training_dashboard"),
    path('admin/filter_trainer_table_view/', views_admin.filter_trainer_table_view, name='filter_trainer_table_view'), # URL for the all_company view
    path('admin/trainer_list_view', views_admin.trainer_list_view, name="trainer_list_view"),
    path('feedback/<int:trainer_id>/', views_admin.get_feedback_for_trainer, name='feedback_for_trainer'),



    #STAFF URLS
    path('staff/staff_dashboard', views_staff.staff_dashboard, name="staff_dashboard"),
    # path('staff/company', views_staff.all_company, name="staff_company"),
    # path('staff/company/<int:company_id>/', views_staff.company_details, name='company_details'),
    # path('staff/add_role', views_staff.add_role , name='addrole'),
        path('add-role/', views_staff.add_role, name='add_role'),

    path('staff/add_company' ,  views_staff.add_company , name="add_company"),
    path('get-companies-by-batch/', views_staff.fetch_companies_by_academic_year, name='fetch_companies_by_academic_year'),
    path('staff/willingness_dashboard', views_staff.willingness_dashboard_staff, name="willingness_dashboard_staff"),
    path('staff/job_opening' ,  views_staff.job_list , name="job_opening"),
    path('job_recommendations' ,  gemini.main_offer , name="job_recommendations"),
    # path('staff/resume_download' ,  views_staff.resume_download , name="resume_download"),
    path('staff/add_training_details' ,  views_staff.add_training_details , name="add_training_details"),
    path('staff/add-student/', views_staff.add_student, name='add_student'),
     path('staff/change_password/', views_staff.change_password, name='change_password'),
     path('staff/import-student/', views_staff.import_students, name='import_student'),
       path('download_student_template/', views_staff.download_student_template, name='download_student_template'),
    path('staff/placement_form/', views_staff.placement_form, name='placement'),
    path('fetch_companies/<str:student_reg_id>/', views_staff.fetch_companies, name='fetch_companies'),
    path('staff/add_trainer/', views_staff.add_trainer, name='add_trainer'),
    path('add-trainer/', views_staff.add_trainer, name='add_trainer'),

    path('main_offer/', gemini.main_offer, name='main_offer'),




    #STUDENT URLS
    path('student/dashboard/', views_student.student_dashboard, name='student_dashboard'),
    path('student/upload_resume/', views_student.upload_resume, name='upload_resume'),
    path('student/all_company', views_student.all_company, name="student_company"),
    path('student/company/<int:company_id>/', views_student.company_details, name='company_details'),
    path('student/submit_willingness/', views_student.submit_willingness, name='submit_willingness'),
    path('student/wishlist', views_student.Wishlist, name="wishlist"),
    path('student/view_training', views_student.view_training, name="view_training"),
    path('student/placement_form/', views_student.placement_form, name='placement_student'),
    path('student/training_company/<int:trainer_id>/', views_student.training_company, name='training_company'),
    path('feedback/submit/', views_student.feedback_view, name='feedback_submit'),  # Endpoint for submitting feedback
    path('student/interview_exp', views_student.interview_exp, name="interview_exp"),
     path('student/show_exp', views_student.show_exp, name="show_exp"),
     path('submit-experience/', views_student.submit_experience, name='submit_experience'),
     path('get-experience/<int:company_id>/', views_student.get_experience, name='get_experience'),


    path('signup/', views_login.signup, name='staff_signup'),
     path('download/manual/', views_login.download_manual, name='download_manual'),



    #UNKNOWN URLS
    path('download/', views.download_excel, name='download_excel'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)