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

@csrf_exempt
def timetable_gen(request):
    db=MySQLDatabase('time_table_test1',user='root',password='',host='localhost')
    db.connect()

    # data=request.body.decode('utf-8')
    # temp=json.loads(data)
    # term=str(temp['term'])
    term="odd"
    # course=str(temp['course'])
    course="B.E."
    # discipline=str(temp['discipline'])
    discipline="Computer Enginnering"
    # shift=str(temp['shift'])
    shift="morning"

    day_list=[]
    timeslot_list1=[]
    semester_list=[]
    temp_course=TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course).get()
    # print(temp_course.course)
    temp_discipline=TimetableFinalDescipline.select().where(TimetableFinalDescipline.descipline_name==discipline).get()
    # print(temp_discipline.id)
    # temp_course_discipline=TimetableFinalDesciplineCourse.select().where((TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline.id)&(TimetableFinalDesciplineCourse.course==temp_course.id)).get()
    temp_course_discipline=TimetableFinalDesciplineCourse.select().where((TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline.id)&(TimetableFinalDesciplineCourse.course==temp_course.course)).get()
    temp_sem=TimetableFinalSemester.select().where((TimetableFinalSemester.term==term)&(TimetableFinalSemester.descipline_course_table_id==temp_course_discipline.id))
    for sem in temp_sem:
        semester_list.append(str(sem.semester_name))

    temp_day=TimetableFinalDay.select()
    for d in temp_day:
        day_list.append(str(d.day_name))

    temp_timeslot=TimetableFinalTimeslot.select()
    for t in temp_timeslot:
        timeslot_list1.append(str(t.timeslot_name))


    course_dict={}
    discipline_dict={}
    shift_dict={}
    timetable_dict={}
    timeslot_list=[]
    sub_detail={}
    for sem in semester_list:
        temp_sem=TimetableFinalSemester.select().where(TimetableFinalSemester.semester_name==sem).get()
        temp_sub=TimetableFinalSubject.select().where(TimetableFinalSubject.semester_table_id==temp_sem.id)
        subject1={}
        subject_list=[]
        for s in temp_sub:
            temp_sub_scheme=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==s.sub_code).get()
            subject_list.append((s.sub_name,temp_sub_scheme.sub_load,s.sub_code,temp_sub_scheme.sub_practical_class,temp_sub_scheme.sub_theory_class,temp_sub_scheme.sub_tutorial_class))
        subject_list.sort(key=lambda tup:tup[1],reverse=False)
        # print(subject_list)
        list_temp=[]
        for sub in subject_list:
            list_temp.append({'sub_name':sub[0],'sub_code':sub[2],'sub_load':sub[1],'practical_load':sub[3],'theory_load':sub[4],'tutorial_load':sub[5]})
            # subject1[str(s.sub_name)]={'sub_code':s.sub_code,'sub_load':temp_sub_scheme.sub_load,'practical_load':temp_sub_scheme.sub_practical_class,'theory_load':temp_sub_scheme.sub_theory_class,'tutorial_load':temp_sub_scheme.sub_tutorial_class}
        sub_detail[sem]=list_temp

    for sem in semester_list:
        temp1=sub_detail[sem]
        size_of_list=len(temp1)*2
        # print(size_of_list)
        x=len(timeslot_list1)
        timeslot_len=0
        if x>size_of_list:
            timeslot_len=size_of_list
            for t in range(1,timeslot_len+1):
                timeslot_list.append(timeslot_list1[t])
        else:
            timeslot_list=timeslot_list1
        days_dict={}
        sub_lab_counter={}
        day_lab_counter={}
        lab_available={}
        classroom_available={}
        for lab in TimetableFinalLabAvailable.select():
            days_availability={}
            for d in day_list:
                timeslot_availability={}
                for t in timeslot_list:
                    timeslot_availability[t]=1
                days_availability[d]=timeslot_availability
            lab_available[str(lab.lab.lab_name)]=days_availability
        for classroom in TimetableFinalClassroomAvailable.select():
            days_availability={}
            for d in day_list:
                timeslot_availability={}
                for t in timeslot_list:
                    timeslot_availability[t]=1
                days_availability[d]=timeslot_availability
            classroom_available[str(classroom.classroom.classroom_name)]=days_availability
    for sem in semester_list:
        days_dict={}
        for d in day_list:
            faculty_count={}
            subject_count={}
            timeslot_dict={}
            for t in timeslot_list:

    db.close()
    return HttpResponse(json.dumps(classroom_available), content_type="application/json")
