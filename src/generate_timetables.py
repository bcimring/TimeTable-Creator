##########################################################################
# Names: Barry Cimring
# Date: Jan 23, 2019
# Description: Main for timetable creator
##########################################################################

from random import randint
from random import choice
from random import shuffle
from copy import copy
from copy import deepcopy
import time

from objects.Person_Student_and_Teacher_Class import*
from objects.Classroom_Schedule_Class import*

#######################################################################################################################################
# GENERAL VARIABLES AND LOADING FROM TXT FILE                                                                                         #
#######################################################################################################################################

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

# Open files to save student's elective and alternate choices
name_file = open('input_data/stuName_num_gr_data.txt','w')
mand_file = open('input_data/stuMand_data.txt','w')
elect_file = open('input_data/stuElect_data.txt','w')
alt_file = open('input_data/stuAlt_data.txt','w')

# generate elective and alternate courses to sort afterwards
for i in range(4):
    for j in range(300):
        mandatory = [(mandate[i][k] + academic_applied[randint(0,3)]) if len(mandate[i][k])== 4  else mandate[i][k] for k in range(len(mandate[i]))]
        
        elective = []
        for k in range(8-len(mandatory)):
            course = electives[i][randint(0,len(electives[i])-1)]
            while course in elective:
                course = electives[i][randint(0,len(electives[i])-1)]
            elective.append(course)

        alternates = []
        for k in range(2):
            course = electives[i][randint(0,len(electives[i])-1)]
            while (course in alternates) or (course in elective):
                course = electives[i][randint(0,len(electives[i])-1)]
            alternates.append(course)


        name_file.write('name '+'0'*(6-len(str(i*300+j)))+str(i*300+j)+' '+str(i+9)+'\n')
        for mand in mandatory:
            mand_file.write(mand+' ')
        for elect in elective:
            elect_file.write(elect+' ')
        for alt in alternates:
            alt_file.write(alt+' ')
        mand_file.write('\n')
        elect_file.write('\n')
        alt_file.write('\n')
        
name_file.close()
mand_file.close()
elect_file.close()
alt_file.close()



#######################################################################################################################################
# GENERAL FUNCTIONS                                                                                                                   #
#######################################################################################################################################

def countSpares(print_data = True):     # count every spare in
    k = 9
    for grade in all_grades:            # each students schedule and
        spareCOUNT = {}                 # adds them to dictionary that adds amount
        for i in range(11):
            spareCOUNT[i] = 0
            
        for st in grade:
            count = 0
            for i in st.sem1:
                if st.sem1[i] == None:
                    count+= 1
            for j in st.sem2:
                if st.sem2[j] == None:
                    count += 1
            spareCOUNT[count] += 1
            
        if print_data: 
            print(k, ": ", spareCOUNT)
        k+=1

def classAccuracy(all_grades):                  # function counts accuracy at which 
    dic = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0} # each student recieves their selected classes
    for grade in all_grades:
        for st in grade:
            clssLst = []
            for i in range(1,6):
                if st.sem1[i] != None:
                    clssLst.append(st.sem1[i][0])
                if st.sem2[i] != None:
                    clssLst.append(st.sem2[i][0])
            count = 0
            for i in clssLst:
                if i in st.courses:
                    
                    count += 1
            if st.spare == True and count < 8: count += 1
            dic[count] += 1
    return dic

def findSmallClasses():                                 # find the number of classses 
    count = 0                                           # with less than 11 students
    for clss in classrooms:
        for i in range(1,6):
            if ((clss.sem1[i] != None)):
                if 0 < len(clss.students_sem1[i]) < 11:
                    count += len(clss.students_sem1[i])
                    
            if ((clss.sem2[i] != None)):
                if 0 < len(clss.students_sem2[i]) < 11:
                    count += len(clss.students_sem2[i])
    return count

def printClass(classrooms):                             # print all the classrooms and their schdule
    for clss in classrooms:
        print(clss.room,'\nSem 1',clss.sem1,'\nSem 2',clss.sem2,'\n')

def load_teacher_data():                                # open teacher data classes and put teachers into a list
    teacherClasses = open('input_data/teacher_subject_data.txt','r')
    teacherClass = [line[:-1] for line in teacherClasses.readlines()]
    teacherClasses.close()

    for i in range(len(teacherClass)):
        teacherClass[i] = teacherClass[i].split()

    teacherNameList = open('input_data/teacher_name_data.txt','r')
    teacherNames = [line[:-1] for line in teacherNameList.readlines()]
    copyteacherNames = copy(teacherNames)
    teacherNameList.close()
    t_cl = {}

    for i in range(len(teacherNames)):
        for j in teacherClass[i]:
            if j in t_cl:
                t_cl[j].append(teacherNames[i])
            else:
                t_cl[j] = [teacherNames[i]]
    copyt_cl = deepcopy(t_cl)

    for i in range(len(teacherNames)):
        teacherNames[i] = Teacher(teacherNames[i],teacherClass[i])

    return teacherNames, t_cl, copyt_cl, copyteacherNames   # return list of teachers and copy for sorting


                        
#######################################################################################################################################
# MAIN                                                                                                                                #
#######################################################################################################################################

# load student elective data from text files
name_file = open('input_data/stuName_num_gr_data.txt','r')
mand_file = open('input_data/stuMand_data.txt','r')
elect_file = open('input_data/stuElect_data.txt','r')
alt_file = open('input_data/stuAlt_data.txt','r')

# put text files into lists to create student instances
allStuName_num_gr = [name_file.readline()[:-1].split() for i in range(1200)]
allStuMand_course = [mand_file.readline()[:-1].split() for i in range(1200)]
allStuElect_course = [elect_file.readline()[:-1].split() for i in range(1200)]
allStuAlt_course = [alt_file.readline()[:-1].split() for i in range(1200)]

# load room data from text files + create room instances
room_data = open('input_data/classroom_data.txt','r')

rooms = [line[:-1] for line in room_data.readlines()]

subject_data = open('input_data/classroom_subject_data.txt','r')
subjects = [line[:-1].split(' ') for line in subject_data.readlines()]

classrooms = [Classroom(subjects[i],rooms[i]) for i in range(len(rooms))]


#--------------  create list for all student objects of all grades --------------#
grade_9s  = [Student(allStuName_num_gr[i][0],allStuName_num_gr[i][1],allStuName_num_gr[i][2],allStuMand_course[i],allStuElect_course[i],allStuAlt_course[i]) for i in range(300)]
grade_10s = [Student(allStuName_num_gr[i][0],allStuName_num_gr[i][1],allStuName_num_gr[i][2],allStuMand_course[i],allStuElect_course[i],allStuAlt_course[i]) for i in range(300,600)]
grade_11s = [Student(allStuName_num_gr[i][0],allStuName_num_gr[i][1],allStuName_num_gr[i][2],allStuMand_course[i],allStuElect_course[i],allStuAlt_course[i]) for i in range(600,900)]
grade_12s = [Student(allStuName_num_gr[i][0],allStuName_num_gr[i][1],allStuName_num_gr[i][2],allStuMand_course[i],allStuElect_course[i],allStuAlt_course[i]) for i in range(900,1200)]

all_grades = [grade_9s,grade_10s,grade_11s,grade_12s]
BigSchedule = Schedule()

  
#----------------------- count up all the elective courses from every student in each grade -----------------------#
allGr_c = BigSchedule.count_grades(all_grades)

#-------------- determine the number of classes, and how many kids remain that must change a courses --------------#
allGr_cn, allGr_r = BigSchedule.number_of_class_per_grade(allGr_c)

#----------------------  determine if there is a 20 person remainder, then make a class for the 20 ----------------#
allGr_cn, allGr_r = BigSchedule.add_all_mand_class( allGr_cn, allGr_r)

#-------------------------------- change classes of those who are outliers ----------------------------------------#
allGr_c = BigSchedule.remove_allGr_classes(all_grades,allGr_c)

#----------------------------------- add new electives to those who were removed ----------------------------------#
allGr_c, allGr_cn, allGr_r = BigSchedule.add_all_elect_class(all_grades, allGr_cn, allGr_r, allGr_c)


#-----AGAIN----------- count up all the elective courses from every student in each grade -----------------------#
allGr_c = BigSchedule.count_grades(all_grades)

#-----AGAIN---- determine the number of classes, and how many kids remain that must change a courses --------------#

allGr_cn, allGr_r = BigSchedule.number_of_class_per_grade(allGr_c,True)

#_-------------- find all class sizes ----------------------------------------------- #
for i in range(len(allGr_cn)):
    BigSchedule.class_sizes(allGr_cn[i],allGr_c[i],classrooms)

# -------------- put courses into classroom schedule -------------------------------- #
classDataBase = BigSchedule.schedule_classes(allGr_cn,classrooms,all_grades)

# -------------- sort students into each class -------------------------------------- #
print("Hello! This is program which generates accurate electives and mandatory courses for a modelled high school of 1200 students. \nTaking in an input of student elective and alternates, amount of teachers, preferred classes of teachers, classrooms and room numbers,\nand sorts the students into a schedule that is valid depending on their grade and electives.\n\n")
time.sleep(20)

print("Below displays the amount of students (1200 randomly generated) that have been sorted into available classes \nto the LEFT, and those that are unable to be sorted on the RIGHT\n")
all_grades,unsortable = BigSchedule.sort_students(allGr_cn,all_grades, classDataBase,classrooms)
        
countSpares(False)

#######################################################################################
                    # sort_students also in this function
# -------------- correct classes with less than 11 students ------------------------- #

for i in range(2):
    print("\nAfter", i+1 ," time(s) correcting for small and large class sizes, this displays again the amount of \nstudents successfully sorted to the LEFT, and those that are unable to be sorted on the RIGHT")
    repopulate(classrooms,all_grades)
    unsortable,classDataBase = smallClassCorrect(classrooms,all_grades, allGr_cn, BigSchedule, classDataBase)
    repopulate(classrooms,all_grades)
    
#######################################################################################
#Teacher, Period, Semester
#Semester, Period, Subject
teacherNames, t_cl, copyt_cl, copyteacherNames = load_teacher_data()                  # create teacher objects    

BigSchedule.add_teachers(classrooms, teacherNames, t_cl, copyt_cl, copyteacherNames)  # add teachers to class 

largeClassCorrect(all_grades,classrooms)
       
#######################################################################################
# ------------ correct students that have more than 4 course/sem -------------------- #
#######################################################################################
for grade in all_grades:                                
    spareCOUNT = {}
    for i in range(11):
        spareCOUNT[i] = 0
        
    for st in grade:
        count = 0
        classesIn = []
        for i in st.sem1:
            if st.sem1[i] == None:
                count+= 1
            else:
                classesIn.append(st.sem1)
        for j in st.sem2:
            if st.sem2[j] == None:
                count += 1
            else:
                classesIn.append(st.sem1)                                              # creates a dictionary with numbers of certain class sizes
        
        if (count == 0) or (count == 1) or ([classesIn.count(i) for i in classesIn].count(2) > 0):
            st.correctOverloading(classrooms)                                          # corrects overloaded classrooms
        
        spareCOUNT[count] += 1
    
########################################################################################

for i in unsortable:
    if (i.sem1 != {1:None,2:None,3:None,4:None,5:None}) and (i.sem2 != {1:None,2:None,3:None,4:None,5:None}):
        unsortable.pop(unsortable.index(i))
Nothing,unsortable = BigSchedule.sort_students(allGr_cn,[unsortable], classDataBase,classrooms,True,True)

#######################################################################################
# ------------ correct students that have more than 4 course/sem -------------------- #
#######################################################################################
        
for grade in all_grades:                               
    spareCOUNT = {}
    for i in range(11):
        spareCOUNT[i] = 0
    for st in grade:
        count = 0
        for i in st.sem1:
            if st.sem1[i] == None:
                count+= 1
        for j in st.sem2:
            if st.sem2[j] == None:                                                    # creates a dictionary with numbers of certain class sizes
                count += 1
        if (count == 0) or (count == 1):
            st.correctOverloading(classrooms)                                         # corrects overloaded classrooms
        
        spareCOUNT[count] += 1
    
########################################################################################
#                   DISPLAY CLASS/STUDENT/SCHEDULE DATA IN SCHEDULE                    #
########################################################################################

#################################################################
# give class options to students and add splitclasses
#################################################################

repopulate(classrooms,all_grades)

for i in range(10):
    classDataBase, splitList = smallClass(classDataBase, classrooms, all_grades)        # FINDS SPLIT CLASSES

    for i in splitList:                                                                 # adds split classes to class objects
        i[0] = i[0].split('/')[:2]
        i[0] = i[0][0]+'/'+i[0][1]
        if (i[2] == 1) and (classrooms[i[1]].sem1[i[3]] != None):
            classrooms[i[1]].sem1[i[3]][0] = i[0]
        if (i[2] == 2) and (classrooms[i[1]].sem2[i[3]] != None):
            classrooms[i[1]].sem2[i[3]][0] = i[0]

for grade in all_grades:                                                                # finds option classes for students
    for st in grade:
        BigSchedule.classOptions(st,classDataBase,classrooms)
        
#################################################################
# REMOVE STUDENTS FROM NONE CLASSES


print("\nAmount of spares per grade (from 9-12, including lunches):")
countSpares()

print('\nNumber of classes assigned originally chosen by student:')
print(classAccuracy(all_grades))

print("\nNumber of classes with certain class sizes:")
print(classPopulation(classrooms))


#############################################################################
#                       ADD STUDENT COURSES TO TXT FILES                    #
#############################################################################
                                                                            #
studentData = open('output_data\[AFTER_SORTING]_student_semester_data.txt','w')         #
optionData = open('output_data\[AFTER_SORTING]_student_course_options.txt','w')         #
classroomScheduleData = open('output_data\[AFTER_SORTING]_classrooms_schedule.txt','w')
teacherScheduleData = open('output_data\[AFTER_SORTING]_teacher_semester_data.txt','w')

for gr in all_grades:                                                       #
    for st in gr:                                                           #
        studentData.write(st.num+' '+st.name+' 1 ')    #
        for i in range(1,6):
            if st.sem1[i] != None:
                studentData.write(str(i)+' '+str(st.sem1[i][0])+' '+str(st.sem1[i][2])+' ')
            else:
                studentData.write(str(i)+' SHAL-01 0000 ')
        studentData.write(' 2 ')
        for i in range(1,6):
            if st.sem2[i] != None:
                studentData.write(str(i)+' '+str(st.sem2[i][0])+' '+str(st.sem2[i][2])+' ')
            else:
                studentData.write(str(i)+' SHAL-01 0000 ')
        studentData.write('\n')

        if st.options != None:
            for i in st.options:
                optionData.write(str(i[0])+' '+str(i[2])+' '+str(i[1])+' '+str(i[3])+' ')            
        optionData.write('\n')

for clss in classrooms:
    classroomScheduleData.write(str(clss.room)+' 1 ')
    for i in range(1,6):
        if clss.sem1[i] != None:
            classroomScheduleData.write(str(i)+' '+str(clss.sem1[i][0])+' '+str(clss.sem1[i][1])+' '+str(clss.sem1[i][2])+' ')
        else:
            classroomScheduleData.write(str(i)+' None 0 None ')

    classroomScheduleData.write('2 ')
    for i in range(1,6):
        if clss.sem2[i] != None:
            classroomScheduleData.write(str(i)+' '+str(clss.sem2[i][0])+' '+str(clss.sem2[i][1])+' '+str(clss.sem2[i][2])+' ')
        else:
            classroomScheduleData.write(str(i)+' None 0 None ')

    classroomScheduleData.write('\n')

for te in teacherNames:                                                          
    teacherScheduleData.write(te.name+' 1 ')    
    for i in range(1,6):
        if te.sem1[i] != None:
            teacherScheduleData.write(str(i)+' '+str(te.sem1[i])+' ')
        else:
            teacherScheduleData.write(str(i)+' SHAL-01 0000 ')
    teacherScheduleData.write(' 2 ')
    for i in range(1,6):
        if te.sem2[i] != None:
            teacherScheduleData.write(str(i)+' '+str(te.sem2[i])+' ')
        else:
            teacherScheduleData.write(str(i)+' SHAL-01 0000 ')
    teacherScheduleData.write('\n')

teacherScheduleData.close()
classroomScheduleData.close()
optionData.close()
studentData.close()                                                         #

print("\n\nAll of the data regarding the schedules of the students, teachers, and classrooms can now be found in the local directory in text files.")
                                                                            #
#############################################################################
