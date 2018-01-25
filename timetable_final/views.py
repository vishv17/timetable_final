from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import View
from django import views
from rest_framework import serializers
import MySQLdb,json,operator,random
from collections import OrderedDict
from operator import itemgetter
from peewee import *
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from time_table_models1 import TimetableFinalCourse,TimetableFinalDescipline,TimetableFinalDesciplineCourse,TimetableFinalClassroom,TimetableFinalShift,TimetableFinalTimeslot,TimetableFinalClassroomAvailable,TimetableFinalDay,TimetableFinalFaculty,TimetableFinalSemester,TimetableFinalSubject,TimetableFinalFacultySubject,TimetableFinalLab,TimetableFinalLabAvailable,TimetableFinalSemesterBatch,TimetableFinalSemesterClassroom,TimetableFinalSemesterLab,TimetableFinalSubjectBatch,TimetableFinalSubjectNoStudent,TimetableFinalSubjectScheme,TimetableFinalTimeslotDay
from .models import descipline,course,descipline_course,day,timeslot,lab,classroom,lab_available,classroom_available,semester,subject_no_student,shift,semester_classroom,semester_lab,subject_batch,semester_batch,subject,subject_scheme,faculty,faculty_subject,timeslot_day

def timetable_gen(request):
    db=MySQLDatabase('time_table_test1',user='root',password='',host='localhost')
    db.connect()

    data=request.body.decode('utf-8')
    temp=json.loads(data)
    # term=str(temp['term'])
    term="odd"
    course=str(temp['course'])
    discipline=str(temp['discipline'])
    shift=str(temp['shift'])

    day_list=[]
    timeslot_list=[]

    if term=="odd":
        semester_list=[1,3,5,7]
    else:
        semester_list=[2,4,6,8]

    temp_day=TimetableFinalDay.select()
    for d in temp_day:
        day_list.append(str(d.day_name))

    temp_timeslot=TimetableFinalTimeslot.select()
    for t in temp_timeslot:
        timeslot_list.append(str(t.timeslot_name))


    course_dict={}
    discipline_dict={}
    shift_dict={}
    timetable_dict={}

    sub_detail={}
    for sem in semester_list:
        temp_sem=TimetableFinalSemester.select().where(TimetableFinalSemester.semester_name)
