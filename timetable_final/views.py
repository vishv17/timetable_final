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
    term="even"
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


    faculty_detail={}
    for temp_course in TimetableFinalCourse.select():
        temp_discipline_dict={}
        for temp_discipline in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==temp_course.course):
            temp_sem_dict={}
            for temp_sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==temp_discipline.id):
                temp_sub_dict={}
                for temp_sub in TimetableFinalSubject.select().where(TimetableFinalSubject.semester_table_id==temp_sem.id):
                    temp_fac_list=[]
                    for temp_fac in TimetableFinalFacultySubject.select().where(TimetableFinalFacultySubject.sub_code==temp_sub.sub_code):
                         temp_fac_list.append([temp_fac.faculty,str(temp_fac.faculty.faculty_name,temp_fac.position,temp_fac.work_load)])
                    temp_sub_dict[str(temp_sub.sub_name)]=temp_fac_list
                temp_sem_dict[str(temp_sem.semester_name)]=temp_sub_dict
            temp_discipline_dict[str(temp_discipline.descipline_table_id.descipline_name)]=temp_sem_dict
        faculty_detail[str(temp_course.course_name)]=temp_discipline_dict

    sub_fac_detail={}
    for temp_course in TimetableFinalCourse.select():
        temp_discipline_dict={}
        for temp_discipline in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==temp_course.course):
            temp_sem_dict={}
            for temp_sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==temp_discipline.id):
                temp_sub_dict={}
                for temp_sub in TimetableFinalSubject.select().where(TimetableFinalSubject.semester_table_id==temp_sem.id):
                    temp_fac_list=[]
                    for temp_fac in TimetableFinalFacultySubject.select().where(TimetableFinalFacultySubject.sub_code==temp_sub.sub_code):
                        temp_fac_list.append((temp_fac.faculty.faculty,temp_fac.faculty.position,temp_fac.faculty.faculty_name,temp_fac.faculty.work_load))
                    temp_fac_list.sort(key=lambda tup:tup[1],reverse=True)
                    temp_i=0
                    temp_fac_dict={}
                    for temp_fac_2 in temp_fac_list:
                        temp_fac_dict[temp_i]={
                                                'id':temp_fac_2[0],
                                                'name':temp_fac_2[2],
                                                'position':temp_fac_2[1],
                                                'work_load':temp_fac_2[3]
                                                }
                        temp_i+=1
                    temp_sub_dict[str(temp_sub.sub_code)]={
                                                            'sub_code':temp_sub.sub_code,
                                                            'sub_name':temp_sub.sub_name,
                                                            'is_elective':temp_sub.is_elective,
                                                            'faculty':temp_fac_dict
                                                            }

                temp_sem_dict[str(temp_sem.semester_name)]=temp_sub_dict
            temp_discipline_dict[str(temp_discipline.descipline_table_id.descipline_name)]=temp_sem_dict
        sub_fac_detail[str(temp_course.course_name)]=temp_discipline_dict



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
############## Below Code is for classroom/lab_day_timeslot_wise availability of classrooms and labs################
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
##############################################################################################################


##### Below code is for day_timeslot_wise availability of lab and classrooms ######
        # lab_available={}
        # for d in day_list:
        #     timeslot_availability={}
        #     for t in timeslot_list:
        #         temp1={}
        #         for lab in TimetableFinalLabAvailable.select():
        #             temp1[str(lab.lab.lab_name)]=1
        #         timeslot_availability[t]=temp1
        #     lab_available[d]=timeslot_availability
        # classroom_available={}
        # for d in day_list:
        #     timeslot_availability={}
        #     for t in timeslot_list:
        #         temp1={}
        #         for classroom in TimetableFinalClassroomAvailable.select():
        #             temp1[str(classroom.classroom.classroom_name)]=1
        #         timeslot_availability[t]=temp1
        #     classroom_available[d]=timeslot_availability
##########################################################################################





    for sem in semester_list:
        temp_semester=TimetableFinalSemester.select().where(TimetableFinalSemester.semester_name==sem).get()
        subject_list=[]
        for sub in TimetableFinalSubject.select().where(TimetableFinalSubject.semester_table_id==temp_semester.id):
            subject_list.append({'sub_code':sub.sub_code,'sub_name':str(sub.sub_name),'is_elective':sub.is_elective})
        days_dict={}
        lab_counter={}
        for d in day_list:
            faculty_count={}
            subject_count={}
            timeslot_dict={}
            # below flag is checking of whether current day and current semester having lab or not and if previous day same time slot not having lab
            flag1=1
            for t in timeslot_list:

                # if lab_count[sem]>0:
                #     flag1=1
                # else:
                #     flag1=0
                lab_flag=0
                if flag1==0:
                    for lab in TimetableFinalSemesterLab.select().where(TimetableFinalSemesterLab.semester_table_id==temp_semester.id):
                        if lab_available[str(lab.lab.lab_name)][d][t]==1:
                            flag=0
                            if len(days_dict)>0:
                                b=days_dict.keys().pop()
                                temp_timeslot_dict=days_dict[b]
                                info=temp_tiemslot_dict[t]
                                if info['lab']==1:
                                    flag1=1
                                    break
                                else:
                                    # no_batch=TimetableFinalSemesterBatch.select().where(TimetableFinalSemesterBatch.semester_table_id==temp_semester.id).get()
                                    no_batch=TimetableFinalSemesterBatch.get(TimetableFinalSemesterBatch.semester_table_id==temp_semester.id).no_batches
                                    # print(no_batch)
                                    elective_sub_list=[]
                                    for sub1 in subject_list:
                                        if sub1['is_elective']==1:
                                            elective_sub_list.append(sub1)
                                    # print(elective_sub_list)
                                    el_sub_batch_info=[]
                                    for sub2 in elective_sub_list:
                                        s_info=TimetableFinalSubject.select().where(TimetableFinalSubject.sub_name==str(sub2['sub_name'])).get()
                                        # s_info=TimetableFinalSubject.get(TimetableFinalSubject.sub_name==str(sub2['sub_name'])).sub_code
                                        # no_batch_sub=TimetableFinalSubjectNoStudent.select().where(TimetableFinalSubjectNoStudent.sub_code==s_info.sub_code).get()
                                        no_batch_sub=TimetableFinalSubjectNoStudent.get(TimetableFinalSubjectNoStudent.sub_code==s_info.sub_code).no_batch
                                        sub2['no_batch']=no_batch_sub
                                        el_sub_batch_info.append(sub2)

                                    sub=random.choice(subject_list)
                                    # if sub['is_elective']==1:
                                    #     counter=0
                                    #     while counter<=no_batch:
                                    #         for sub2 in elective_sub_list:
                                    #             sub_no_batch=sub2['no_batch']
                                    #             temp1={}
                                    #             for c in range(1,sub_no_batch+1):
                                    # else:
                                    #     pass
                            else:
                                # no_batch=TimetableFinalSemesterBatch.get(TimetableFinalSemesterBatch.semester_table_id==temp_semester.id).no_batches
                                # print(no_batch,sem)
                                pass
                        else:
                            pass
                elif flag1==1:
                    elective_sub_list=[]
                    for sub1 in subject_list:
                        if sub1['is_elective']==1:
                            elective_sub_list.append(sub1)
                    # print(elective_sub_list)
                    sub_batch_info=[]
                    for sub2 in elective_sub_list:
                        s_info=TimetableFinalSubject.select().where(TimetableFinalSubject.sub_name==str(sub2['sub_name'])).get()
                        no_batch_sub=TimetableFinalSubjectNoStudent.select().where(TimetableFinalSubjectNoStudent.sub_code==s_info.sub_code).get()
                        print(no_batch_sub.no_batch)
                    for classroom in TimetableFinalSemesterClassroom.select().where(TimetableFinalSemesterClassroom.semester_table_id==temp_semester.id):
                        temp_sub=random.choice(subject_list)
                        sub=temp_sub['sub_name']
                        if temp_sub['is_elective']==1:
                            pass
    db.close()
    return HttpResponse(json.dumps(sub_fac_detail), content_type="application/json")
