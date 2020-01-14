##########################################################################
# Names: Barry Cimring
# Date: Jan 23, 2019
# Description: Classes 'Class','Schedule' for timetable creator
##########################################################################


mandate = [['MPM1','ENG1','SNC1','PPL1O','FSF1','CGC1'],
           ['MPM2','ENG2','SNC2','CHC2','GLC2O/CHV2O'],
           ['MCR3','ENG3'],
           ['ENG4']]

academic_applied = ['P','D','D','D']

electives = [['HIF1O1','GLE1O1','TIJ1O1','ATC1O1','ADA1O1','AVI1O1','AMI1O1','AMV1O1','BTT1O1'],
             ['FSF2O1','FSF2D1','PAF2O1','PPL2O9','HFN2O1','TEJ2O1','TDJ2O1','TGJ2O1','ATC2O1','ADA2O1','AVI2O1','ASM2O1','AMI2O1','AMV2O1','BBI2O1','ICS2O1'],
             ['FSF3U1','PAF3O1','PPL3O1','SBI3U1','SPH3U1','SCH3U1','HPW3C1','HSP3U1','TDJ3M1','TEJ3M1','TFJ3E1','TGJ3M1','TPJ3M1','ATC3M1','ADA3M1','AVI3M1','ASM3M1',
              'AWF3O1','AWQ3M1','AMI3M1','AMV3M1','BAF3M1','BDI3C1','BDP3O1','BMX3E1','CIE3M1','ICS3U1','CGC3O1','IDC3O1','CHW3M1','CLU3M1','HZB3M1','SHAL01','SHAL01'],
             ['ATC4M1','ADA4M1','AVI4M1','ASM4M1','AWF4M1','AWQ4M1','AWF4M1','AMI4M1','AMV4M1','BAT4M1','BBB4M1','BOH4M1','IDC4U2','CIA4U1','ICS4U1','CGR4E1','CGW4U1',
              'CGU4U1','CHY4U1','CLN4U1','HZT4U1','IDC4U1','IDC4U3','EWC4U1','FSF4U1','PAF4O1','PSK4U1','PLF4M1','MDM4U1','MHF4U1','MCV4U1','MHF4U2','MCV4U2','SBI4U1',
              'SPH4U1','SCH4U1','SCH4U2','HFA4U1','HHG4M1','HHS4U1','TDJ4M1','TEJ4M1','TGG4M1','TGJ4M1','TPJ4M1','SHAL01','SHAL01','SHAL01','SHAL01']]

from random import randint
from random import choice
from random import shuffle
from copy import copy
from copy import deepcopy
import time

#######################################################################################################################################
# classroom Class                                                                                                                     #
#######################################################################################################################################

class Classroom(object):
    def __init__(self, subject_types, room):
        self.sub_types = subject_types
        self.sem1 = {1:None, 2:None, 3:None, 4:None, 5:None}
        self.sem2 = {1:None, 2:None, 3:None, 4:None, 5:None}
        
        self.students_sem1 = {1:[], 2:[], 3:[], 4:[], 5:[]}
        self.students_sem2 = {1:[], 2:[], 3:[], 4:[], 5:[]}
        
        self.room = room

    def add_period(self,subject,period):
        if subject in self.sub_types:
            self.per_sub[period] = subject

    def add_teacher(self,teacher,period,semester):
        if semester == 1:
            self.sem1[period].append(teacher)
        if semester == 2:
            self.sem2[period].append(teacher)

    def __str__(self):
        return 'Room: '+self.room
    
#######################################################################################################################################
# BIG SCHEDULE CLASS                                                                                                                  #
#######################################################################################################################################

class Schedule(object):
    def __init__(self):
        sem1 = []
        sem2 = []


    def schedule_classes(self,number_classes,classrooms, all_grades, count = 0,classDataBase = []): # add classes to schedules
        for g in range(len(number_classes)):
            for i in number_classes[g]:
                for j in range(len(number_classes[g][i][1])):
                    if i != 'SHAL01':
                        while True:                                                                 # choose random class, if course in class types
                            students = [all_grades[g][k] for g in range(len(all_grades)) for k in range(len(all_grades[g]))  if [i,j] in all_grades[g][k].courses]
                            randclass, sem, period = self.choose_class(students, [i,j], classrooms)
                            
                            if (i in classrooms[randclass].sub_types) and ((None in classrooms[randclass].sem1.values()) or (None in classrooms[randclass].sem2.values())):
                                if (sem == 1) and (classrooms[randclass].sem1[period] == None) :    # if no ccourse already in that place, add if to classData Base
                                    classrooms[randclass].sem1[period] = [i,j]
                                    classDataBase.append([1,i,period,number_classes[g][i][1][j],j,randclass,classrooms[randclass].room])
                                    count += 1
                                    break
                                                                                                                 
                                if (sem == 2) and (classrooms[randclass].sem2[period] == None) :    # if no ccourse already in that place, add if to classData Base
                                    classrooms[randclass].sem2[period] = [i,j]
                                    classDataBase.append([2,i,period,number_classes[g][i][1][j],j,randclass,classrooms[randclass].room])
                                    count += 1
                                    break

        return classDataBase
    
    def class_sizes(self,number_classes,man_count,classrooms):      # determine class number based of electives
        for i in number_classes:
            class_size = man_count[i]//number_classes[i][0]         # divide class population by number of classes
            remainder = man_count[i]%number_classes[i][0]
            number_classes[i].append([])
            for j in range(number_classes[i][0]):               
                if j == number_classes[i][0] - 1:                   # if the remainder of people is less than
                    remainder = 1
                number_classes[i][1].append(class_size+remainder)
                remainder = 0



    def sort_students(self,classCount,allStudents, classDataBase, classrooms, schedCheck = False, unsort = False):
        yay = 0                                                     # sort students in walls of defense
        boo = 0
        unsortable = []
        for gr in allStudents:
            
            for stdnt in gr:                                        # for each student in grade and year
                if len(stdnt.courses) == 6: stdnt.add_removed()
                if 'SHAL01' in stdnt.courses:
                    stdnt.courses.pop(stdnt.courses.index('SHAL01'))
                    stdnt.tempRemoved.append('SHAL01')
                    stdnt.spare = True
                classes = stdnt.wall1(classDataBase, schedCheck)    # check wall1, add to schedule

                if classes != None:
                    yay += 1
                    update_class_student(stdnt,classes,classDataBase,classrooms)
                    
                else:
                    classes = stdnt.wall2(classDataBase, schedCheck)# check wall2 if wall1 doesnt work 
                    if classes != None:
                        update_class_student(stdnt,classes,classDataBase,classrooms)
                        yay += 1
                        
                    
                    else:
                        if stdnt.spare == None:
                            stdnt.add_removed()

                        classes = stdnt.wall3(classDataBase, schedCheck)# check wall3 if wall2 doesnt work
                        if classes != None:
                            update_class_student(stdnt,classes,classDataBase,classrooms)
                            yay += 1
                            
                        elif unsort == True:
                            classes = stdnt.wall4(classDataBase, schedCheck)    # if student previously unsortable, check wall 4 and wall 5
                            if classes != None:
                                update_class_student(stdnt,classes,classDataBase,classrooms)
                                yay += 1
                                
                            elif len(stdnt.courses) > 7:
                                classes = stdnt.wall5(classDataBase, schedCheck)
                                if classes != None:
                                    update_class_student(stdnt,classes,classDataBase,classrooms)
                                    yay += 1
                                else:
                                    boo += 1
                                    
                        else:                                       # add to boo if never sortable
                            boo += 1
                            unsortable += [stdnt]
                            
                        

                if yay%30 == 0: print(yay,boo)                      # print progess of students that are able to sort and not able to sort
        print(yay,boo)
    
        return allStudents,unsortable

                                                    
    def choose_class(self, students, course, classrooms):   # determine class sechduling
        if course[0][0] == 'M':                             # math class schedules (9, 1-2, 10,2-3, 11,3-5, 12,4,5,1)
            if course[0][3] == '1': ranges = range(1,3)
            elif course[0][3] == '2': ranges = range(2,4)
            elif course[0][3] == '3': ranges = range(3,6)
            elif course[0][3] == '4': ranges = [4,5,1]

        elif course[0][0] == 'E':                           # English class schedules (10, 1-2, 11,2-3, 12,3-5, 9,4,5,1)
            if course[0][3] == '1': ranges = [4,5,1]
            elif course[0][3] == '2': ranges = range(1,3)
            elif course[0][3] == '3': ranges = range(2,4)
            elif course[0][3] == '4': ranges = range(3,6)

        elif course[0][0] == 'S':                           # Science class schedules (10, 1-2, 11,2-3, 12,3-5, 9,4,5,1)
            if course[0][3] == '1': ranges = range(3,6)
            elif course[0][3] == '2': ranges = [4,5,1]
            elif course[0][3] == '3': ranges = range(1,3)
            elif course[0][3] == '4': ranges = range(2,4)

        elif course[0][0] == 'C':                           # geography/history class schedules (10, 1-2, 11,2-3, 12,3-5, 9,4,5,1)
            if course[0][3] == '1': ranges = range(2,4)
            elif course[0][3] == '2': ranges = range(3,6)
            elif course[0][3] == '3': ranges = [4,5,1]
            elif course[0][3] == '4': ranges = range(1,3)
        else:
            ranges = [1,2,3,4,5]
            shuffle(ranges)
        
            
        for classroom in classrooms:                        # return the period and classroom that the course shall be in 
            if course[0] in classroom.sub_types:
                for period in ranges:
                    if (classroom.sem1[period] == None) and (course[0] in classroom.sub_types): 
                        return classrooms.index(classroom), 1, period
                    elif (classroom.sem2[period] == None) and (course[0] in classroom.sub_types):
                        return classrooms.index(classroom), 2, period
                    
        return 

                                                        
    def count_grades(self,all_grades):                      # count the amount of classes in each grade
        man_count = []
        for i in range(len(all_grades)):
            man_count.append(count_classes(all_grades[i],mandate[i],electives[i]))
        return man_count
            
    def number_of_class_per_grade(self,all_grades, counted = False):    # count number of classes per grade with the smaller functions
        gr_cls_num, gr_rem = [], []
        for i in range(len(all_grades)):
            t_cls_num, t_gr_rem = numberOfClasses(all_grades[i], counted)
            gr_cls_num.append(t_cls_num)
            gr_rem.append(t_gr_rem)
        return gr_cls_num, gr_rem

    def add_all_mand_class(self, all_gr_cn, all_gr_r):                  # add mandatody classes with smaller student functions
        for i in range(len(all_gr_cn)):
            all_gr_cn[i],all_gr_r[i] = addMandateClasses(all_gr_cn[i],all_gr_cn[i],mandate[i])
        return all_gr_cn, all_gr_r

    def remove_allGr_classes(self,all_grades,allGr_c):                  # remove classes from the students classes with smaller functions
        for i in range(len(all_grades)):
            allGr_c[i] = remove_classes(all_grades[i],allGr_c[i],i+9)
        return allGr_c

    def add_all_elect_class(self, all_grades, allGr_cn, allGr_r, allGr_c):# add elective classes to student schedule with smaller functions
        for i in range(len(all_grades)):
            allGr_c[i],allGr_cn[i],allGr_r[i] = addElectiveClasses(all_grades[i],allGr_cn[i],allGr_r[i],electives[i],allGr_c[i],i+9)

        return allGr_c,allGr_cn,allGr_r


    def add_teachers(self, classrooms, teacherNames, t_cl, copyt_cl, copyteacherNames):     # add teacher to schdule
        for i in range(1,6):
            for j in classrooms:
                if j.sem1[i] != None:
                    while True:                                                             # if the class is open and teacher can teach the class, add to schdule and teacher schedule
                        if len(copyt_cl[j.sem1[i][0]]) > 0:
                            chosenOne = choice(copyt_cl[j.sem1[i][0]])
                        if teacherNames[copyteacherNames.index(chosenOne)].sem1[i] == None:
                            j.add_teacher(chosenOne,i,1)
                            teacherNames[copyteacherNames.index(chosenOne)].add_class(1,i,(j.sem1[i][0]))
                            copyt_cl[j.sem1[i][0]].remove(chosenOne)
                            break
                        else:
                            j.add_teacher("Null",i,1)
                            break
                copyt_cl = deepcopy(t_cl)
        for i in range(1,6):
            for j in classrooms:
                if j.sem2[i] != None:
                    while True:                                                             # if the class is open and teacher can teach the class, add to schdule and teacher schedule
                        if len(copyt_cl[j.sem2[i][0]]) > 0:
                            chosenOne = choice(copyt_cl[j.sem2[i][0]])
                        if teacherNames[copyteacherNames.index(chosenOne)].sem2[i] == None:
                            j.add_teacher(chosenOne,i,2)
                            teacherNames[copyteacherNames.index(chosenOne)].add_class(2,i,(j.sem2[i][0]))
                            copyt_cl[j.sem2[i][0]].remove(chosenOne)
                            break
                        else:
                            j.add_teacher("Null",i,2)
                            break
                copyt_cl = deepcopy(t_cl)

    def classOptions(self, st, CDB,classrooms):                                     # determine class options for each student
        sem1Count = 0
        sem2Count = 0
        for i in range(1,6):                                                        # count classes per sem
            if st.sem1[i] != None: sem1Count += 1
            if st.sem2[i] != None: sem2Count += 1

        tempCDB = [j for j in CDB if (int(j[1][3])+8) == int(st.grade)]             # create list to find possible class options

        tempCDB,sem1Count,sem2Count = remove_from_CDB(tempCDB,st,sem1Count,sem2Count)
        
        totalBreak = False
        while ((sem1Count < 4) or (sem2Count < 4)) and (sem1Count+sem2Count < 8):   # if sem is less than 4 and a spare is availabe
            for i in tempCDB:
                if i[1] in st.alt:
                    if (i[0] == 1) and (sem1Count < 4):
                        sem1Count += 1
                        update_class_student(st,[i],CDB,classrooms)                 # add class to schedule if in alternates of student
                    if (i[0] == 2) and (sem2Count < 4):
                        sem2Count += 1
                        update_class_student(st,[i],CDB,classrooms)                 # add class to schedule if in alternates of student
                    if (sem1Count == 4) and (sem2Count == 4):
                        break

                if (tempCDB.index(i)) == (len(tempCDB)-1):
                    totalBreak = True
                    break
                
            if (sem1Count >= 4) and (sem2Count >= 4):                               # if schedule is full, break loop
                break
            if totalBreak == True:
                break

        tempCDB,sem1Count,sem2Count = remove_from_CDB(tempCDB,st,sem1Count,sem2Count)

        st.options = [[i[0],i[1],i[2],i[6]] for i in tempCDB]
        
def count_classes(students,mandate,electives, counted = False):                     # count the number of classes each elective should have
    man_count = {}
    for i in mandate:
        if len(i) < 5:
            man_count[i+"P"] = 0
            man_count[i+"D"] = 0            
        else:
            man_count[i] = 0
            
    for i in electives:
        man_count[i] = 0
        
    for i in man_count:                                         # add the electives up of each student
        for j in range(len(students)):
            if i in students[j].courses:
                man_count[i] += 1

    for st in students:                                         # make the spare attribute True if its in the student electives
        if 'SHAL01' in st.courses:
            st.spare == True
            
    return man_count

def remove_classes(students,man_count,grade):                   # Remove classes if the elective is less than 15 people 
    remove = []
    for i in man_count:
        if man_count[i] < 15:
            remove.append(i)
            
    for i in remove:                                            # remove it from student courses, add an alternate to courses
        for j in range(len(students)):
            if i in students[j].courses:
                man_count = students[j].add_alternate(man_count,i,grade)
        del man_count[i]
        
    return man_count


def numberOfClasses(man_count,counted = False):
    number_classes = {}
    remain = {}
    
    for i in man_count:
        number_classes[i] = (man_count[i]//15)
        remain[i] = (man_count[i]%15)
        if (counted == True) and (number_classes[i]*10 >= remain[i]):
            remain[i] = 0
        number_classes[i] = [number_classes[i]]
        
    return number_classes,remain

def addMandateClasses(number_classes, remain, mandate):
    for mand_course in mandate:
        for course in remain:
            if ((mand_course+'D' == course) and (remain[course][0] != 0)):
                number_classes[course][0] += 1
                remain[course][0] = 0
                
            if ((mand_course+'P' == course) and (remain[course][0] != 0)):
                number_classes[course][0] += 1
                remain[course][0] = 0

    return number_classes,remain

def addElectiveClasses(students, number_classes, remain, electives, man_count, grade):
    for i in remain:
        for j in range(len(electives)):
            if electives[j] in i:
                if remain[i][0] >= 20:
                    number_classes[i] += 1
                    remain[i] = 0
                elif remain[i][0] < number_classes[i][0]*5:
                    teey = 0
                    
                else:
                    counter = 0
                    for k in range(len(students)):
                        if (i in students[k].courses) and (counter <= remain[i][0]):
                            man_count = students[k].add_alternate(man_count,i, grade)
                            counter += 1
                        if counter == remain[i]:
                            break
                            
    return man_count,number_classes,remain

def update_class_student(stdnt,classes,CDB,classrooms):                             # update the classes of the student
    for clss in classes:
        
        CDB[CDB.index(clss)][3] -= 1
        if clss[0] == 1:
            stdnt.sem1[clss[2]] = [clss[1],clss[4],classrooms[clss[5]].room]        # add sem to schedule, and class number to student list
            classrooms[clss[5]].students_sem1[clss[2]].append(stdnt.num)
        elif clss[0] == 2:
            stdnt.sem2[clss[2]] = [clss[1],clss[4],classrooms[clss[5]].room]        # add sem to schedule, and class number to student list
            classrooms[clss[5]].students_sem2[clss[2]].append(stdnt.num)

    return CDB, classrooms

def choose_sem(count):
    return choice([1,2])

def add_class_to_students(course,students,period,sem, classNum):                    # insert class to student schedule
    for student in students:
        student.schedule_course([course,classNum],period,sem)
        student.drop_course([course,classNum])

def smallClassCorrect(classrooms,all_grades, allGr_cn, BigSchedule, classDataBase): # correct small class numbers
    to_remove = []
    count = 0
                                                                                    # Removing class from classroom schedule
    for clss in classrooms:
        for i in range(1,6):
            if (clss.sem1[i] != None) and (len(clss.students_sem1[i]) < 11):        # if class has less than 11 people
                while len(clss.students_sem1[i]) != 0:                              # remoeve all of the students and
                    if clss.sem1[i][0] == all_grades[int(clss.students_sem1[i][0])//300][int(clss.students_sem1[i][0])%300].sem1[i][0]:
                        to_remove.append([all_grades[int(clss.students_sem1[i][0])//300][int(clss.students_sem1[i][0])%300],clss.sem1[i]])
                    clss.students_sem1[i].pop(clss.students_sem1[i].index(clss.students_sem1[i][0]))
                clss.sem1[i] = None
                for j in classDataBase:
                    if (j[0] == 1) and (j[2] == i) and (j[1] == clss.sem2[i]) and (j[6] == clss.room):
                        classDataBase.pop(classDataBase.index(j))
                        
            if (clss.sem2[i] != None) and (len(clss.students_sem2[i]) < 11):        # if class has less than 11 people
                while len(clss.students_sem2[i]) != 0:                              # remoeve all of the students and
                    if clss.sem2[i][0] == all_grades[int(clss.students_sem2[i][0])//300][int(clss.students_sem2[i][0])%300].sem2[i][0]:
                        to_remove.append([all_grades[int(clss.students_sem2[i][0])//300][int(clss.students_sem2[i][0])%300],clss.sem2[i]])
                    clss.students_sem2[i].pop(clss.students_sem2[i].index(clss.students_sem2[i][0]))
                clss.sem2[i] = None
                for j in classDataBase:
                    if (j[0] == 2) and (j[2] == i) and (j[1] == clss.sem2[i]) and (j[6] == clss.room):
                        classDataBase.pop(classDataBase.index(j))
                    
                
    for i in range(len(to_remove)):                                                     # create new schedule for students that classes were removed from
        to_remove[i][0].sem1,to_remove[i][0].sem2 = {1:None, 2:None, 3:None, 4:None, 5:None},{1:None, 2:None, 3:None, 4:None, 5:None}
        to_remove[i][0].add_removed()    
    all_grades,unsortable = BigSchedule.sort_students(allGr_cn,[[i[0] for i in to_remove]],classDataBase, classrooms, True, True)

    return unsortable,classDataBase

def classPopulation(classrooms):                                                        # count the number of students in each class
    clssCount = {}
    for i in range(11,37):                                                              # generate dictionary
        clssCount[i] = 0
    for clss in classrooms:
        for i in range(1, 6):
            if clss.sem1[i] != None:
                while len(clss.students_sem1[i]) < 11: clss.students_sem1[i].append(clss.students_sem1[i][0])
                clssCount[len(clss.students_sem1[i])] += 1
            if clss.sem2[i] != None:
                while len(clss.students_sem2[i]) < 11: clss.students_sem2[i].append(clss.students_sem2[i][0])
                clssCount[len(clss.students_sem2[i])] += 1
    return clssCount

def largeClassCorrect(all_grades,classrooms):                                           # correct the large classes                                  
    for clss in classrooms:
        for i in range(1,6):
            if len(clss.students_sem1[i]) > 33:                                         # if class is greater than 33 students

                break1 = False
                if len(clss.students_sem1[i]) > 33:
                    for clss2 in classrooms:                                            # split it into two classes
                        if (clss.sem1[i][0] in clss2.sub_types) and (clss2.sem1[i] == None):
                            clss2.sem1[i] = [clss.sem1[i][0],str(clss.sem1[i][1])+'B','Null']
                            
                            count = 0                                                   # remove half the students from the original, add them to the new one
                            pop = len(clss.students_sem1[i])//2                         # add students to new class if room teaches the same subject

                            for st in all_grades[int(clss2.sem1[i][0][3])-1]:           # add half of students from class 1 to class 2
                                if count > pop:
                                    break1 = True
                                    break
                                if (st.sem1[i] != None) and (st.num in clss.students_sem1[i]):# if classes is the same
                                    st.sem1[i][2] = clss2.room
                                    clss2.students_sem1[i].append(clss.students_sem1[i].pop(clss.students_sem1[i].index(st.num)))
                                    count += 1

                        if break1 == True:
                            break                                                       # break from loop after all changes made

                                                                                    # same as above just for semester 1
            if len(clss.students_sem2[i]) > 33:                                         # if class is greater than 33 students

                break1 = False
                if len(clss.students_sem2[i]) > 33:
                    for clss2 in classrooms:                                            # split it into two classes
                        if (clss.sem2[i][0] in clss2.sub_types) and (clss2.sem2[i] == None):
                            clss2.sem2[i] = [clss.sem2[i][0],str(clss.sem2[i][1])+'B','Null']
                            
                            count = 0                                                   # remove half the students from the original, add them to the new one
                            pop = len(clss.students_sem2[i])//2                         # add students to new class if room teaches the same subject

                            for st in all_grades[int(clss2.sem2[i][0][3])-1]:           # add half of students from class 1 to class 2
                                if count > pop:
                                    break1 = True
                                    break
                                if (st.sem2[i] != None) and (st.num in clss.students_sem2[i]):# if classes is the same
                                    st.sem2[i][2] = clss2.room
                                    clss2.students_sem2[i].append(clss.students_sem2[i].pop(clss.students_sem2[i].index(st.num)))
                                    count += 1
                        if break1 == True:
                            break 


def remove_from_CDB(tempCDB,st,sem1Count,sem2Count):                # remove classes from classDataBase for temporary purposes
    if sem1Count == 4:
        for j in range(len(tempCDB)-1,-1,-1):                       # if full sem1, remove all sem1
            if tempCDB[j][0] == 1:
                tempCDB.pop(j)
              
    if sem2Count == 4:                                              # if full sem2, remove all sem2
        for j in range(len(tempCDB)-1,-1,-1):
            if tempCDB[j][0] == 2:
                tempCDB.pop(j)
    

    for i in range(1,6):
        if st.sem1[i] != None:                                      # if already in schedule, remove
            for j in range(len(tempCDB)-1,-1,-1):
                if ((tempCDB[j][0] == 1) and (i == tempCDB[j][2])) or (tempCDB[j][1] in st.courses):
                    tempCDB.pop(j)

    for i in range(1,6):
        if st.sem2[i] != None:                                      # if already in schedule, remove
            for j in range(len(tempCDB)-1,-1,-1):
                if ((tempCDB[j][0] == 2) and (i == tempCDB[j][2])) or (tempCDB[j][1] in st.courses):
                    tempCDB.pop(j)

    
    if (sem1Count == 4) and (sem2Count < 4) and (st.spare == True):# re add sem1 and sem2 course counts
        sem2Count += 1
    elif (sem2Count == 4) and (sem1Count < 4) and (st.spare == True):
        sem1Count += 1
    

    return tempCDB,sem1Count,sem2Count

def repopulate(classrooms,all_grades):                      # re adjust class populations 
    for clss in classrooms:                                 # after resorting
        for i in range(1,6):
            clss.students_sem1[i] = []
            clss.students_sem2[i] = []

    for grade in all_grades:
        for st in grade:
            for i in range(1,6):
                if st.sem1[i] != None:
                    for j in classrooms:
                        if j.sem1[i] != None:
                            if (j.room == st.sem1[i][2]) and (j.sem1[i][0] == st.sem1[i][0]):
                                j.students_sem1[i].append(st.num)
                                break

                if st.sem2[i] != None:
                    for j in classrooms:
                        if j.sem2[i] != None:
                            if (j.room == st.sem2[i][2]) and (j.sem2[i][0] == st.sem2[i][0]):
                                j.students_sem2[i].append(st.num)
                                break
    
    for clss in classrooms:                                 # remove studentts from classes they're not in 
        for i in range(1,6):
            if (clss.students_sem1[i] == None) and (len(clss.students_sem1[i]) > 0):
                for st in all_grades[int(clss.students_sem1[i][0])//300]:
                    if st.num in clss.students_sem1[i]:
                        st.sem1[i] = None
                clss.students_sem1[i] = []                  # make classes empty that are None
                        
            if (clss.students_sem2[i] == None) and (len(clss.students_sem2[i]) > 0):
                for st in all_grades[int(clss.students_sem2[i][0])//300]:
                    if st.num in clss.students_sem2[i]:
                        st.sem2[i] = None
                clss.students_sem2[i] = []
                
            if clss.students_sem1[i] == []:
                clss.sem1[i] = None
            if clss.students_sem2[i] == []:
                clss.sem2[i] = None

def smallClass(classDataBase, classrooms, all_grades, splitList = []):
    for clss in classrooms:                                                         # check all classes
        for i in range(1,6):
            if (0 < len(clss.students_sem1[i]) < 15) and (clss.sem1[i] != None):    # if ther population is low
                addition1 = False
                for clss2 in classrooms:
                    if clss2.sem1[i] != None:                                       # check another class, if popultion also low
                        if (clss2.sem1[i][0] == clss.sem1[i][0]) and (clss2.sem1[i][1] != clss.sem1[i][1]) and (len(clss2.students_sem1[i]) < 36 - len(clss.students_sem1[i])):
                            for num in clss.students_sem1[i]:
                                clss2.students_sem1[i].append(num)                  # merge the two classes
                                all_grades[int(num)//300][int(num)%300].sem1[i][2] = clss2.room
                            clss.sem1[i] = None
                            
                            for j in classDataBase:
                                if (j[0] == 1) and (j[2] == i) and (j[1] == clss.sem1[i]) and (j[6] == clss.room):
                                    classDataBase.pop(classDataBase.index(j))
                            addition1 = True
                            break
    
                if addition1 == False:
                    for clss2 in classrooms:                                        # if cannot merge small classes
                        if clss2.sem1[i] != None:
                            if (clss2.sem1[i][0][:2] == clss.sem1[i][0][:2]) and (len(clss2.sem1[i][0]) <= 6) and (abs(int(clss2.sem1[i][0][3]) - int(clss.sem1[i][0][3])) == 1) and (len(clss2.students_sem1[i]) < 36 - len(clss.students_sem1[i])):
                                clss2.sem1[i][0] = clss2.sem1[i][0]+'/'+clss.sem1[i][0]
                                
                                for num in clss.students_sem1[i]:                   # make a split class
                                    clss2.students_sem1[i].append(num)
                                    all_grades[int(num)//300][int(num)%300].sem1[i][2] = clss2.room
                                    
                                for j in classDataBase:                             # merge the two classes
                                    if (j[0] == 1) and (j[2] == i) and (j[1] == clss.sem2[i]) and (j[6] == clss.room):
                                        classDataBase.pop(classDataBase.index(j))
                                        
                                splitList.append([clss2.sem1[i][0]+'/'+clss.sem1[i][0],classrooms.index(clss2),1,i])
                                clss.sem1[i] = None
                                break

            if (0 < len(clss.students_sem2[i]) < 15) and (clss.sem2[i] != None):
                addition2 = False
                for clss2 in classrooms:                                            # check all classes
                    if clss2.sem2[i] != None:
                        if (clss2.sem2[i][0] == clss.sem2[i][0]) and (clss2.sem2[i][1] != clss.sem2[i][1]) and (len(clss2.students_sem2[i]) < 36 - len(clss.students_sem2[i])):
                            for num in clss.students_sem2[i]:
                                clss2.students_sem2[i].append(num)                  # if small population of both classes
                                all_grades[int(num)//300][int(num)%300].sem2[i][2] = clss2.room
                                
                            for j in classDataBase:                                 # merge classes
                                if (j[0] == 2) and (j[2] == i) and (j[1] == clss.sem2[i]) and (j[6] == clss.room):
                                    classDataBase.pop(classDataBase.index(j))
                                    
                            clss.sem2[i] = None
                            addition2 = True
                            break

                if addition2 == False:
                    for clss2 in classrooms:
                        if clss2.sem2[i] != None:                                   # if cannot merge small classes
                            if (clss2.sem2[i][0][:3] == clss.sem2[i][0][:3]) and (len(clss2.sem2[i][0]) <= 6) and (abs(int(clss2.sem2[i][0][3]) - int(clss.sem2[i][0][3])) == 1) and (len(clss2.students_sem2[i]) < 36 - len(clss.students_sem2[i])):
                                clss2.sem2[i][0] = clss2.sem2[i][0]+'/'+clss.sem2[i][0]
                                
                                for num in clss.students_sem2[i]:                   # try to make split
                                    clss2.students_sem2[i].append(num)
                                    all_grades[int(num)//300][int(num)%300].sem2[i][2] = clss2.room
                                    
                                for j in classDataBase:                             # merge two classes
                                    if (j[0] == 2) and (j[2] == i) and (j[1] == clss.sem2[i]) and (j[6] == clss.room):
                                        classDataBase.pop(classDataBase.index(j))
                                        
                                splitList.append([clss2.sem2[i][0]+'/'+clss.sem2[i][0],classrooms.index(clss2),2,i])
                                clss.sem2[i] = None
                                break
    return classDataBase, splitList
