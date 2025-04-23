from django import forms
from .models import Student
from .models import Company , Placement
    

from django import forms
from .models import Company

from django import forms
from .models import Company, DepartmentEligibility  # Assuming DepartmentEligibility is the related model

class CompanyForm(forms.ModelForm):
    company_opening_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    company_last_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    company_ctc = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g., 5 from django import forms
from .models import Student
from .models import Company , Placement
    

from django import forms
from .models import Company

from django import forms
from .models import Company, DepartmentEligibility  # Assuming DepartmentEligibility is the related model

class CompanyForm(forms.ModelForm):
    company_opening_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    company_last_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    company_ctc = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g., 5 LPA'}))
    company_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True)

    # Custom field for selecting multiple departments (this will be handled in a related model)
    company_eligibility_dept = forms.MultipleChoiceField(
        choices=[
            ('B.TECH AD', 'AD - Artificial Intelligence and Data Science'),
            ('B.E CIVIL', 'CE - Civil Engineering'),
            ('B.TECH CSBS', 'CB - Computer Science and Business System'),
            ('B.E CSE', 'CS - Computer Science and Engineering'),
            ('B.E EEE', 'EE - Electrical and Electronics Engineering'),
            ('B.E ECE', 'EC - Electronics and Communication Engineering'),
            ('B.TECH IT', 'IT - Information Technology'),
            ('B.E MECH', 'ME - Mechanical Engineering')
        ],
        widget=forms.SelectMultiple(attrs={'style': 'height: 100px; width: 100%;'}),
        required=True
    )

    class Meta:
        model = Company
        fields = [
            'company_name', 'company_role', 'company_location', 'company_skill',
            'company_eligibility','company_eligibility_hsc' ,'company_eligibility_sslc','company_eligibility_diploma','no_standing_arrear','history_of_arrear', 'company_academic_year', 'company_opening_date',
            'company_last_date', 'company_ctc', 'company_image', 'company_description'
        ]


    def save(self, commit=True):
        company = super().save(commit=commit)
        print("inside the commit")
        # Clear old entries before adding new ones
        print("commit -->" , commit)
        if commit:
            print("if commit" , commit)
            DepartmentEligibility.objects.filter(company=company).delete()

            # Save each selected department
            for dept in self.cleaned_data.get('company_eligibility_dept'):
                DepartmentEligibility.objects.create(company=company, department=dept)

        return company

from django import forms
from .models import Placement , Placement_User

class PlacementForm(forms.ModelForm):
    rounds = forms.CharField(required=False)
    class Meta:
        model = Placement
        fields = ['student_reg_id', 'company_id', 'attended', 'round1', 'round2', 'round3', 'round4', 'placement_offer','job_domain','job_type','company_type', 'ctc', 'offer_letter' , 'company_location','stipend']

    def __init__(self, *args, **kwargs):
        super(PlacementForm, self).__init__(*args, **kwargs)
        self.fields['student_reg_id'].required = False
        self.fields['company_id'].required = False
        self.fields['attended'].required = False
        self.fields['round1'].required = False
        self.fields['round2'].required = False
        self.fields['round3'].required = False
        self.fields['round4'].required = False
        self.fields['job_type'].required = False
        self.fields['job_domain'].required = False
        self.fields['placement_offer'].required = False
        self.fields['company_type'].required = False
        self.fields['ctc'].required = False
        self.fields['offer_letter'].required = False
        self.fields['company_location'].required = False
        self.fields['stipend'].required = False

        

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Placement_User
        fields = ['faculty_id', 'faculty_name','faculty_role' ,'faculty_dept', 'faculty_email']
        widgets = {
            'faculty_dept': forms.Select(choices=[
                ('B.Tech AD', 'B.Tech AD'),
                ('B.Tech IT', 'B.Tech IT'),
                ('B.Tech CSBS', 'B.Tech CSBS'),
                ('B.E CSE', 'B.E CSE'),
                ('B.E Civil', 'B.E Civil'),
                ('B.E EEE', 'B.E EEE'),
                ('B.E ECE', 'B.E ECE'),
                ('B.E Mech', 'B.E Mech'),
                ('Others','Others'),
                ('All','All'),
            ]) , 
            'faculty_role': forms.Select(choices=[
                ('Placement Cell Staff', 'Placement Cell Staff'),
                ('Placement Coordinator', 'Placement Coordinator'),
                ('Student Placement Coordinator', 'Student Placement Coordinator'),
                ('JA', 'JA'),
                ('HOD', 'HOD'),
                ('ALL', 'Principal'),
                ('ALL', 'Vice Principal'),
                ('ALL', 'GM'),
            ])
        }


class NewStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_regno', 'student_dob']
       




# forms.py
from django import forms
from .models import Student

class StudentLoginForm(forms.Form):
    regno = forms.CharField(label='Registration Number', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)

class StudentFirstLoginForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['student_dob', 'student_password']
        widgets = {
            'student_password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('student_password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')



from .models import Placement_User

class StaffLoginForm(forms.Form):
    faculty_id = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class StaffFirstLoginForm(forms.Form):
    faculty_name = forms.CharField(max_length=100)
    faculty_email = forms.EmailField()
    faculty_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('faculty_password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class Student_form(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        # exclude = ["cgpa"]


               





from .models import TrainingCompanyDetails , TrainingCompanyDept


class TrainerCompanyForm(forms.ModelForm):
    company_opening_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    company_last_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    # Custom field for selecting multiple departments
    company_eligibility_dept = forms.MultipleChoiceField(
        choices=[
            ('B.TECH AD', 'AD - Artificial Intelligence and Data Science'),
            ('B.E CIVIL', 'CE - Civil Engineering'),
            ('B.TECH CSBS', 'CB - Computer Science and Business System'),
            ('B.E CSE', 'CS - Computer Science and Engineering'),
            ('B.E EEE', 'EE - Electrical and Electronics Engineering'),
            ('B.E ECE', 'EC - Electronics and Communication Engineering'),
            ('B.TECH IT', 'IT - Information Technology'),
            ('B.E MECH', 'ME - Mechanical Engineering')
        ],
        widget=forms.SelectMultiple(attrs={'style': 'height: 100px; width: 100%;'}),
        required=True
    )

    class Meta:
        model = TrainingCompanyDetails
        fields = [
            'company_name', 'company_address', 'company_place',
            'company_email', 'company_academic_year', 'company_opening_date',
            'company_last_date'  # Removed topics and trainer fields
        ]

    def save(self, commit=True):
        trainer_company = super().save(commit=commit)

        if commit:
            # Clear old entries before adding new ones
            TrainingCompanyDept.objects.filter(trainer_company=trainer_company).delete()

            # Save each selected department
            for dept in self.cleaned_data.get('company_eligibility_dept'):
                TrainingCompanyDept.objects.create(trainer_company=trainer_company, department=dept)

        return trainer_company


from .models import Trainer

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['company', 'trainer_name', 'trainer_gender', 'topics', 'description']
        
    # Customizing the fields for the form
    company = forms.ModelChoiceField(
        queryset=TrainingCompanyDetails.objects.all(),
        empty_label="Select Company",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    trainer_gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


from django import forms

class SignupForm(forms.ModelForm):
    class Meta:
        model = Placement_User
        fields = ['faculty_id', 'faculty_name', 'faculty_dept', 'faculty_role', 'faculty_email', 'faculty_password']
        widgets = {
            'faculty_password': forms.PasswordInput(),  # To hide the password input
        }



from .models import FeedbackDetails


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackDetails
        fields = [
            'trainer',  # Use 'trainer' instead of 'trainer_id'
            'course_content',
            'lecture_sessions',
            'practical_sessions',
            'interactive_sessions',
            'course_material',
            'usefulness',
            'knowledge_improvement',
            'timely_communication',
            'overall_arrangement',
            'content_relevance',
            'resource_person',
            'liked_topic',
            'specific_feedback',
        ]


from .models import Experience

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['student', 'company', 'round1_details', 'round2_details', 'round3_details', 'round4_details']
        widgets = {
            'round1_details': forms.Textarea(attrs={'rows': 3}),
            'round2_details': forms.Textarea(attrs={'rows': 3}),
            'round3_details': forms.Textarea(attrs={'rows': 3}),
            'round4_details': forms.Textarea(attrs={'rows': 3}),
        }


from .models import Role

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name']
        labels = {
            'role_name': 'Role Name',
        }

from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'link', 'experience', 'salary', 'location', 'description', 'post_date', 'image_link', 'date_of_post']


from django import forms
from .models import StudentResume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = StudentResume
        fields = ['resume_file']
LPA'}))
    company_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True)

    # Update company_role to handle multiple selections
    company_role = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )

    # Custom field for selecting multiple departments
    company_eligibility_dept = forms.MultipleChoiceField(
        choices=[
            ('B.TECH AD', 'AD - Artificial Intelligence and Data Science'),
            ('B.E CIVIL', 'CE - Civil Engineering'),
            ('B.TECH CSBS', 'CB - Computer Science and Business System'),
            ('B.E CSE', 'CS - Computer Science and Engineering'),
            ('B.E EEE', 'EE - Electrical and Electronics Engineering'),
            ('B.E ECE', 'EC - Electronics and Communication Engineering'),
            ('B.TECH IT', 'IT - Information Technology'),
            ('B.E MECH', 'ME - Mechanical Engineering')
        ],
        widget=forms.SelectMultiple(attrs={'style': 'height: 100px; width: 100%;'}),
        required=True
    )

    class Meta:
        model = Company
        fields = [
            'company_name', 'company_role', 'company_location', 'company_skill',
            'company_eligibility','company_eligibility_hsc' ,'company_eligibility_sslc','company_eligibility_diploma','no_standing_arrear','history_of_arrear', 'company_academic_year', 'company_opening_date',
            'company_last_date', 'company_ctc', 'company_image', 'company_description'
        ]

    def save(self, commit=True):
        company = super().save(commit=commit)
        if commit:
            DepartmentEligibility.objects.filter(company=company).delete()
            for dept in self.cleaned_data.get('company_eligibility_dept'):
                DepartmentEligibility.objects.create(company=company, department=dept)
        return company

from django import forms
from .models import Placement , Placement_User

class PlacementForm(forms.ModelForm):
    rounds = forms.CharField(required=False)
    class Meta:
        model = Placement
        fields = ['student_reg_id', 'company_id', 'attended', 'round1', 'round2', 'round3', 'round4', 'placement_offer','job_domain','job_type','company_type', 'ctc', 'offer_letter' , 'company_location','stipend']

    def __init__(self, *args, **kwargs):
        super(PlacementForm, self).__init__(*args, **kwargs)
        self.fields['student_reg_id'].required = False
        self.fields['company_id'].required = False
        self.fields['attended'].required = False
        self.fields['round1'].required = False
        self.fields['round2'].required = False
        self.fields['round3'].required = False
        self.fields['round4'].required = False
        self.fields['job_type'].required = False
        self.fields['job_domain'].required = False
        self.fields['placement_offer'].required = False
        self.fields['company_type'].required = False
        self.fields['ctc'].required = False
        self.fields['offer_letter'].required = False
        self.fields['company_location'].required = False
        self.fields['stipend'].required = False

        

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Placement_User
        fields = ['faculty_id', 'faculty_name','faculty_role' ,'faculty_dept', 'faculty_email']
        widgets = {
            'faculty_dept': forms.Select(choices=[
                ('B.Tech AD', 'B.Tech AD'),
                ('B.Tech IT', 'B.Tech IT'),
                ('B.Tech CSBS', 'B.Tech CSBS'),
                ('B.E CSE', 'B.E CSE'),
                ('B.E Civil', 'B.E Civil'),
                ('B.E EEE', 'B.E EEE'),
                ('B.E ECE', 'B.E ECE'),
                ('B.E Mech', 'B.E Mech'),
                ('Others','Others'),
                ('All','All'),
            ]) , 
            'faculty_role': forms.Select(choices=[
                ('Placement Cell Staff', 'Placement Cell Staff'),
                ('Placement Coordinator', 'Placement Coordinator'),
                ('Student Placement Coordinator', 'Student Placement Coordinator'),
                ('JA', 'JA'),
                ('HOD', 'HOD'),
                ('ALL', 'Principal'),
                ('ALL', 'Vice Principal'),
                ('ALL', 'GM'),
            ])
        }


class NewStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_regno', 'student_dob']
       




# forms.py
from django import forms
from .models import Student

class StudentLoginForm(forms.Form):
    regno = forms.CharField(label='Registration Number', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)

class StudentFirstLoginForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['student_dob', 'student_password']
        widgets = {
            'student_password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('student_password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')



from .models import Placement_User

class StaffLoginForm(forms.Form):
    faculty_id = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class StaffFirstLoginForm(forms.Form):
    faculty_name = forms.CharField(max_length=100)
    faculty_email = forms.EmailField()
    faculty_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('faculty_password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class Student_form(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        # exclude = ["cgpa"]


               





from .models import TrainingCompanyDetails , TrainingCompanyDept


class TrainerCompanyForm(forms.ModelForm):
    company_opening_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    company_last_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    # Custom field for selecting multiple departments
    company_eligibility_dept = forms.MultipleChoiceField(
        choices=[
            ('B.TECH AD', 'AD - Artificial Intelligence and Data Science'),
            ('B.E CIVIL', 'CE - Civil Engineering'),
            ('B.TECH CSBS', 'CB - Computer Science and Business System'),
            ('B.E CSE', 'CS - Computer Science and Engineering'),
            ('B.E EEE', 'EE - Electrical and Electronics Engineering'),
            ('B.E ECE', 'EC - Electronics and Communication Engineering'),
            ('B.TECH IT', 'IT - Information Technology'),
            ('B.E MECH', 'ME - Mechanical Engineering')
        ],
        widget=forms.SelectMultiple(attrs={'style': 'height: 100px; width: 100%;'}),
        required=True
    )

    class Meta:
        model = TrainingCompanyDetails
        fields = [
            'company_name', 'company_address', 'company_place',
            'company_email', 'company_academic_year', 'company_opening_date',
            'company_last_date'  # Removed topics and trainer fields
        ]

    def save(self, commit=True):
        trainer_company = super().save(commit=commit)

        if commit:
            # Clear old entries before adding new ones
            TrainingCompanyDept.objects.filter(trainer_company=trainer_company).delete()

            # Save each selected department
            for dept in self.cleaned_data.get('company_eligibility_dept'):
                TrainingCompanyDept.objects.create(trainer_company=trainer_company, department=dept)

        return trainer_company


from .models import Trainer

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['company', 'trainer_name', 'trainer_gender', 'topics', 'description']
        
    # Customizing the fields for the form
    company = forms.ModelChoiceField(
        queryset=TrainingCompanyDetails.objects.all(),
        empty_label="Select Company",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    trainer_gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


from django import forms

class SignupForm(forms.ModelForm):
    class Meta:
        model = Placement_User
        fields = ['faculty_id', 'faculty_name', 'faculty_dept', 'faculty_role', 'faculty_email', 'faculty_password']
        widgets = {
            'faculty_password': forms.PasswordInput(),  # To hide the password input
        }



from .models import FeedbackDetails


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackDetails
        fields = [
            'trainer',  # Use 'trainer' instead of 'trainer_id'
            'course_content',
            'lecture_sessions',
            'practical_sessions',
            'interactive_sessions',
            'course_material',
            'usefulness',
            'knowledge_improvement',
            'timely_communication',
            'overall_arrangement',
            'content_relevance',
            'resource_person',
            'liked_topic',
            'specific_feedback',
        ]


from .models import Experience

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['student', 'company', 'round1_details', 'round2_details', 'round3_details', 'round4_details']
        widgets = {
            'round1_details': forms.Textarea(attrs={'rows': 3}),
            'round2_details': forms.Textarea(attrs={'rows': 3}),
            'round3_details': forms.Textarea(attrs={'rows': 3}),
            'round4_details': forms.Textarea(attrs={'rows': 3}),
        }


from .models import Role

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name']
        labels = {
            'role_name': 'Role Name',
        }

from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'link', 'experience', 'salary', 'location', 'description', 'post_date', 'image_link', 'date_of_post']


from django import forms
from .models import StudentResume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = StudentResume
        fields = ['resume_file']
