from faker import Faker
import random
from .models import *


fake = Faker()

def seed_db(n=50) ->None:
    try:
        for i in range(n):

            departments_obj = Department.objects.all()
            rand_ind = random.randint(0,(len(departments_obj)-1))
            student_id = f'STU-0{random.randint(100,999)}'
            department = departments_obj[rand_ind]
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(20,30)
            student_address = fake.address()

            student_id_obj = StudentId.objects.create(student_id = student_id)

            student_obj = Student.objects.create(
                department  =department,
                student_id = student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,

            )
    except Exception as e:
        print(e)


def marks_s(n):
    try:
        stud_obj = Student.objects.all()
        for student in stud_obj:
            subj = Subject.objects.all()
            for subject in subj:
                SubjectMarks.objects.create(
                    student= student,
                    subject = subject,
                    marks = random.randint(35,100)
                )
    except Exception as e:
        print(e)
