
from django.db import models
from django.utils.timezone import now  # To get the current date and time
import os

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    company_role = models.CharField(max_length=255)
    company_location = models.CharField(max_length=255)
    company_skill = models.CharField(max_length=255)
    company_eligibility = models.FloatField()
    company_eligibility_sslc = models.FloatField( null=True   , blank=True)
    company_eligibility_hsc = models.FloatField( null=True , blank=True)
    company_eligibility_diploma = models.FloatField(null=True , blank=True)
    history_of_arrear =models.FloatField(null=True , blank=True)
    no_standing_arrear = models.FloatField(null=True , blank=True)
    company_academic_year = models.CharField(max_length=150)
    company_opening_date = models.DateField(null=True, blank=True)
    company_last_date = models.DateField(null=True, blank=True)
    company_ctc = models.CharField(max_length=255, null=True, blank=True)
    company_image = models.ImageField(upload_to='company_images/', null=True, blank=True)
    company_description = models.TextField()

    def __str__(self):
        return self.company_name

# This is the related model that stores each department's eligibility for a company
class DepartmentEligibility(models.Model):
    company = models.ForeignKey(Company, related_name='eligibility_departments', on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.department} - {self.company.company_name}"


class Student(models.Model):
    student_regno = models.CharField(max_length=255, primary_key=True)
    student_dob = models.DateField(null=True, blank=True)
    student_password = models.CharField(max_length=100 ,  blank=True, null=True)


    def __str__(self):
        return self.student_regno

class StudentResume(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='')
    resume_text = models.TextField(max_length=100 ,  blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     # Get the file name and extension
    #     if self.resume_file:
    #         # Create a new file name based on student_regno
    #         ext = os.path.splitext(self.resume_file.name)[1]  # Get file extension
    #         self.resume_file.name = f"{self.student.student_regno}{ext}"  # Rename the file
    #     super().save(*args, **kwargs)


class Experience(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    round1_details = models.TextField()
    round2_details = models.TextField()
    round3_details = models.TextField()
    round4_details = models.TextField()
    date_added = models.DateField(default=now)

    def __str__(self):
        return f"{self.student} - {self.company}"

class Willingness(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    willingness = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.student} - {self.company} - {self.willingness}"


class Placement(models.Model):
    student_reg_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_location = models.CharField(max_length=150, blank=True, null=True)
    attended = models.CharField(max_length=3, blank=True, null=True)
    round1 = models.CharField(max_length=5, blank=True, null=True)
    round2 = models.CharField(max_length=5, blank=True, null=True)
    round3 = models.CharField(max_length=5, blank=True, null=True)
    round4 = models.CharField(max_length=5, blank=True, null=True)
    placement_offer = models.CharField(max_length=150, blank=True, null=True)
    job_type = models.CharField(max_length=150, blank=True, null=True)
    job_domain = models.CharField(max_length=150, blank=True, null=True)
    company_type = models.CharField(max_length=150, blank=True, null=True)
    stipend = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ctc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    offer_letter = models.FileField(upload_to='offer_letters/', blank=True, null=True)

    def __str__(self):
        return f"{self.student_reg_id} - {self.company_id} - {self.attended}"

class ApplicationStudent(models.Model):
    reg_no  = models.CharField(max_length=100,primary_key=True)
    student_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    cgpa = models.FloatField()
    batch = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    sslc  = models.FloatField()
    hsc  = models.CharField(max_length=20)
    history_of_arrear = models.FloatField()
    bag_of_log =  models.FloatField()
    diploma  = models.CharField(max_length=20)

# laptop
# defalut_email_id

    # other fields

    class Meta:
        db_table = 'application_student'
        managed = False


class defalut_email_id(models.Model):
    email_id = models.CharField(max_length=100)
    department= models.CharField(max_length=100)

    class Meta:
        db_table = 'application_defalut_email_id'
        managed = False


class Placement_User(models.Model):
      faculty_id  = models.CharField(max_length=100,primary_key=True)
      faculty_name = models.CharField(max_length=100)
      faculty_dept = models.CharField(max_length=100)
      faculty_role = models.CharField(max_length=100)
      faculty_email = models.CharField(max_length=100)
      faculty_password = models.CharField(max_length=100 ,  blank=True, null=True)


class TrainingCompanyDetails(models.Model):
    # Adding a primary key field explicitly, though Django creates an id field automatically
    training_company_id = models.AutoField(primary_key=True)  # This creates an auto-incrementing primary key
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_place = models.CharField(max_length=255)
    company_email = models.EmailField()
    company_academic_year = models.CharField(max_length=150)
    company_opening_date = models.DateField(null=True, blank=True)
    company_last_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.training_company_id}"

class TrainingCompanyDept(models.Model):
    trainer_company = models.ForeignKey(TrainingCompanyDetails, related_name='eligibility_departments', on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.department} - {self.trainer_company.company_name}"


from django.db import models

class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)  # This creates an auto-incrementing primary key
    trainer_name = models.CharField(max_length=255)
    trainer_gender = models.CharField(max_length=10)  # or you can use choices for male/female
    topics = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    company = models.ForeignKey(TrainingCompanyDetails, related_name='trainers', on_delete=models.CASCADE)

    def __str__(self):
        return self.trainer_name


from django.db import models

class FeedbackDetails(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    course_content = models.IntegerField()
    lecture_sessions = models.IntegerField()
    practical_sessions = models.IntegerField()
    interactive_sessions = models.IntegerField()
    course_material = models.IntegerField()
    usefulness = models.IntegerField()
    knowledge_improvement = models.CharField(max_length=10)
    timely_communication = models.IntegerField()
    overall_arrangement = models.IntegerField()
    content_relevance = models.CharField(max_length=3)
    resource_person = models.CharField(max_length=3)
    liked_topic = models.TextField()
    specific_feedback = models.TextField()


class Role(models.Model):
    role_name = models.CharField(max_length=100)

    def __str__(self):
        return self.role_name


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    experience = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    post_date = models.CharField(max_length=100)
    image_link = models.CharField(max_length=255, blank=True, null=True)
    date_of_post = models.DateField()

    def __str__(self):
        return self.title

