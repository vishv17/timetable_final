from django.db import models

class descipline(models.Model):
    descipline_name=models.CharField(max_length=200)

class course(models.Model):
    course_id=models.IntegerField(primary_key=True)
    course_name=models.CharField(max_length=200)

class descipline_course(models.Model):
    descipline_table_id=models.ForeignKey('descipline',on_delete=models.CASCADE)
    course_id=models.ForeignKey('course',db_column='course_id',on_delete=models.CASCADE)

class day(models.Model):
    day_name=models.CharField(max_length=200)

class timeslot(models.Model):
    timeslot_name=models.CharField(max_length=200)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE)

class lab(models.Model):
    lab_id=models.IntegerField(primary_key=True)
    lab_name=models.CharField(max_length=200)

class classroom(models.Model):
    classroom_id=models.IntegerField(primary_key=True)
    classroom_name=models.CharField(max_length=200)

class lab_available(models.Model):
    lab_id=models.ForeignKey('lab',db_column='lab_id',on_delete=models.CASCADE)
    timeslot_id=models.ForeignKey('timeslot',on_delete=models.CASCADE)
    availability=models.BooleanField(default=True)

class classroom_available(models.Model):
    classroom_id=models.ForeignKey('classroom',db_column='classroom_id',on_delete=models.CASCADE)
    timeslot_id=models.ForeignKey('timeslot',on_delete=models.CASCADE)
    availability=models.BooleanField(default=True)

class semester(models.Model):
    semester_name=models.CharField(max_length=200)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE)
    descipline_course_table_id=models.ForeignKey('descipline_course',on_delete=models.CASCADE)

class subject_no_student(models.Model):
    sub_code=models.ForeignKey('subject',db_column='sub_code',on_delete=models.CASCADE)
    no_batch=models.IntegerField()

class shift(models.Model):
    shift_name=models.CharField(max_length=200)
    shift_time=models.CharField(max_length=200)

class semester_classroom(models.Model):
    semester_table_id=models.ForeignKey('semester',on_delete=models.CASCADE)
    classroom_id=models.ForeignKey('classroom',db_column='classroom_id',on_delete=models.CASCADE)

class semester_lab(models.Model):
    semester_table_id=models.ForeignKey('semester',on_delete=models.CASCADE)
    lab_id=models.ForeignKey('lab',db_column='lab_id',on_delete=models.CASCADE)

class subject_batch(models.Model):
    subject_code=models.ForeignKey('subject',db_column='sub_code',on_delete=models.CASCADE)
    batch_name=models.CharField()

class semester_batch(models.Model):
    semester_table_id=models.ForeignKey('semester',on_delete=models.CASCADE)
    no_batches=models.IntegerField()

class subject(models.Model):
    semester_table_id=models.ForeignKey('semester',on_delete=models.CASCADE)
    sub_code=models.IntegerField(primary_key=True)
    sub_name=models.CharField(max_length=200)
    descipline_course_table_id=models.ForeignKey('descipline_course',on_delete=models.CASCADE)
    is_elective=models.BooleanField(default=False)

class subject_scheme(models.Model):
    sub_code=models.ForeignKey('subject',db_column='sub_code',on_delete=models.CASCADE)
    sub_load=models.ImageField()
    sub_theory_class=models.IntegerField()
    sub_practical_class=models.IntegerField()
    sub_practical_class=models.IntegerField()

class faculty(models.Model):
    faculty_id=models.IntegerField(primary_key=True)
    faculty_name=models.CharField(max_length=200)
    position=models.IntegerField()
    work_load=models.IntegerField()
    descipline_course_table_id=models.ForeignKey('descipline_course',on_delete=models.CASCADE)

class faculty_subject(models.Model):
    faculty_id=models.ForeignKey('faculty',db_column='faculty_id',on_delete=models.CASCADE)
    sub_code=models.ForeignKey('subject',db_column='subject',on_delete=models.CASCADE)

class timeslot_day(models.Model):
    day_id=models.ForeignKey('day',on_delete=models.CASCADE)
    timeslot_table_id=models.ForeignKey('timeslot',on_delete=models.CASCADE)
    resource_type=models.BooleanField()
    resource_id=models.IntegerField()
    faculty_subject_table_id=models.ForeignKey('faculty_subject',on_delete=models.CASCADE)
    semester_table_id=models.ForeignKey('semester',on-on_delete=models.CASCADE)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE)
