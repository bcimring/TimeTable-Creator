##########################################################################
# Names: Barry Cimring
# Date: Jan 23, 2019
# Description: Classes 'Person','Student','Teacher' for timetable creator
##########################################################################

from random import randint
from random import choice
from random import shuffle
from copy import copy
from copy import deepcopy
import time

#######################################################################################################################################
# PERSON CLASS                                                                                                                        #
#######################################################################################################################################

class Person(object):                                           # Person class 
    def __init__(self, name = '', number = 0):                  # master class to student and teacher
        self.name = name
        self.number = number
        self.sem1 = {}
        self.sem2 = {}

    def __str__(self):                                          # string method for name and number
        return str(self.name)+' with number '+str(self.number)


#######################################################################################################################################
# SUDENT CLASS                                                                                                                        #
#######################################################################################################################################

class Student(object):
    def __init__(self, name, stuNumber, grade, mandates, electives, alternates):
        Person.__init__(self, name = '', number = 0)
        self.name = name
        self.num = stuNumber
        self.grade = grade

        self.mandate = mandates
        self.elect = electives
        self.alt = alternates
        self.spare = None
        self.tempRemoved = []
        self.options = None

        self.courses = self.mandate+self.elect
        self.classes = []
        
        self.sem1 = {1:None, 2:None, 3:None, 4:None, 5:None}
        self.sem2 = {1:None, 2:None, 3:None, 4:None, 5:None}

    def __str__(self):
        return 'Student '+self.num+' with mandatory courses: '+str(self.mandate)+'; elective courses: '+str(self.elect)+'; and alternates: '+str(self.alt)
    
    def addCourse(self,course):
        self.courses.append(course)

    def drop_course(self,course):
        self.courses.pop(self.courses.index(course))

    def swapCourse(self,course,newCourse):
        self.courses[self.courses.index(course)] = newCourse
    
    def schedule_course(self,course,period,sem):
        if sem == 1:
            self.sem1[period] = course
        elif sem == 2:
            self.sem2[period] = course
    
    def add_alternate(self,man_count,course,grade):                                 # add alternate course if student changes
        
        self.drop_course(course)
        self.addCourse(self.alt.pop(0))
        
        man_count[course] -= 1
        if len(self.alt) == 0:
            course = electives[grade-9][randint(0,len(electives[grade-9])-1)]       # choose course from list of electives
            while (course not in man_count) or (course in self.courses):            # if not already an elective of student
                course = electives[grade-9][randint(0,len(electives[grade-9])-1)]   # add to its course
            self.alt.append(course)
        
        man_count[self.alt[0]] += 1
        
        return man_count
                
    def wall1(self, CDB, checkRest = False, break3 = False, break4 = False, break5 = False, break6 = False, break7 = False): # first line of defense in sorting
        attempt = []
        if len(self.courses) == 7: break7 = True
        if len(self.courses) == 6: break6 = True
        if len(self.courses) == 5: break5 = True
        if len(self.courses) == 4: break4 = True
        if len(self.courses) == 3: break3 = True
        
        tempCDB = [i for i in CDB if i[1] in self.courses]
            
        for clss1 in tempCDB:
            if ((clss1[1] == self.courses[-1])) and (self.schedCheck(attempt + [clss1], checkRest)):         # take class from schedule, add to attemp list, check if valid in students schedule
                attempt.append(clss1)
                
                for clss2 in tempCDB:
                    if ((clss2[1] == self.courses[-2]))  and (self.schedCheck(attempt + [clss2], checkRest)):# take another clsas from schedule, check if valid, and so on until all electives are fulfilled
                        attempt.append(clss2)
                        for clss3 in tempCDB:
                            if ((clss3[1] == self.courses[-3]))  and (self.schedCheck(attempt + [clss3], checkRest)):
                                attempt.append(clss3)
                                if break3: return attempt
                                
                                for clss4 in tempCDB:
                                    if ((clss4[1] == self.courses[-4]))  and (self.schedCheck(attempt + [clss4], checkRest)):
                                        attempt.append(clss4)
                                        if break4: return attempt
                                        
                                        for clss5 in tempCDB:
                                            if ((clss5[1] == self.courses[-5]))  and (self.schedCheck(attempt + [clss5], checkRest)):
                                                attempt.append(clss5)
                                                if break5: return attempt
                                                
                                                for clss6 in tempCDB:
                                                    if ((clss6[1] == self.courses[-6]))  and (self.schedCheck(attempt + [clss6], checkRest)):
                                                        attempt.append(clss6)
                                                        if break6: return attempt
                                                        
                                                        for clss7 in tempCDB:
                                                            if ((clss7[1] == self.courses[-7]))  and (self.schedCheck(attempt + [clss7], checkRest)):
                                                                attempt.append(clss7)
                                                                if break7: return attempt
                                                                
                                                                for clss8 in tempCDB:
                                                                    if ((clss8[1] == self.courses[-8]))  and (self.schedCheck(attempt + [clss8], checkRest)):
                                                                        attempt.append(clss8)
                                                                        if self.schedCheck(attempt, checkRest):
                                                                            return attempt                  # return the list of classes this student will be taking
                                                                        attempt.pop()                       # if course invalid, pop it from list and choose another
                                                                attempt.pop()
                                                        attempt.pop()
                                                attempt.pop()
                                        attempt.pop()
                                attempt.pop()
                        attempt.pop()
                attempt.pop()

    def wall2(self,CDB, checkRest = False):         # 2nd, 3rd, 4th, and 5th line of defence
        attempt = []                                # temporarily removes a course from elevtices
        for i in range(len(self.courses)):          # sees if a schedule can be made if this course is removed
            tempRemove = self.courses.pop(i)        # make the schedule with the remaining courses
            attempt = self.wall1(CDB,checkRest)
            if attempt != None:
                self.tempRemoved.append(tempRemove)
                return attempt
            self.courses.insert(i,tempRemove)

            
    def wall3(self,CDB, checkRest = False):
        attempt = []                                # temporarily removes a course from elevtices
        for i in range(len(self.courses)):          # sees if a schedule can be made if this course is removed
            tempRemove = self.courses.pop(i)        # make the schedule with the remaining courses
            attempt = self.wall2(CDB,checkRest)
            if attempt != None:
                self.tempRemoved.append(tempRemove)
                return attempt
            self.courses.insert(i,tempRemove)

    def wall4(self,CDB, checkRest = False):
        attempt = []                                # temporarily removes a course from elevtices
        for i in range(len(self.courses)):          # sees if a schedule can be made if this course is removed
            tempRemove = self.courses.pop(i)        # make the schedule with the remaining courses
            attempt = self.wall3(CDB,checkRest)
            if attempt != None:
                self.tempRemoved.append(tempRemove)
                return attempt
            self.courses.insert(i,tempRemove)

    def wall5(self,CDB, checkRest = False):
        attempt = []                                # temporarily removes a course from elevtices
        for i in range(len(self.courses)):          # sees if a schedule can be made if this course is removed
            tempRemove = self.courses.pop(i)        # make the schedule with the remaining courses
            attempt = self.wall4(CDB,checkRest)
            if attempt != None:
                self.tempRemoved.append(tempRemove)
                return attempt
            self.courses.insert(i,tempRemove)

    def schedCheck(self,attempt, checkRest = False):        # checks if a students schedule is valid
        sem1 = [clss for clss in attempt if clss[0] == 1]
        sem2 = [clss for clss in attempt if clss[0] == 2]
        if (len(sem1) == 5) or (len(sem2) == 5):            # if five courses per semester, invalid
            return False

        if not checkRest:                                   # if class size > 30, invalid
            for i in attempt:
                if i[3] < -8:
                    return False
        else:
            for i in attempt:
                if i[3] < -15:
                    return False
                
        for i in range(len(attempt)):                       # if duplicate courses or classes, invalid
            for j in range(len(attempt)):
                if i != j:
                    if ((attempt[i][0] == attempt[j][0]) and (attempt[i][2] == attempt[j][2])) or (attempt[i][1] == attempt[j][1]):
                        return False
        return True                                         # otherwise, valid
    
    def add_removed(self):                                  # re-add the temporary removed courses from 2,3,4,5 walls 
        for k in range(len(self.tempRemoved)):
            if (self.tempRemoved[k] not in self.courses):
                self.courses.append(self.tempRemoved[k])
        self.tempRemoved = []

    def correctOverloading(self,classrooms):                # some courses are duplicates in the schedule
        sem1 = [self.sem1[clss] for clss in self.sem1 if self.sem1[clss] != None]
        sem2 = [self.sem2[clss] for clss in self.sem2 if self.sem2[clss] != None]

        for i in self.sem1:                                 # remove the duplicates in sem 1
            for j in self.sem1:
                if (j != i) and (self.sem1[j] != None) and (self.sem1[i] != None):
                    if self.sem1[j][0][:4] == self.sem1[i][0][:4]:
                        self.sem1[j] = None
                        break
                    
            for j in self.sem2:                             # remove the duplicates in sem1 which are in sem 2
                if (self.sem2[j] != None) and (self.sem1[i] != None):
                    if self.sem2[j][0][:4] == self.sem1[i][0][:4]:
                        if (len(sem1) > 4):
                            self.sem1[i] = None
                            break
                        elif (len(sem2) > 4):
                            self.sem2[j] = None
                            break

        for i in self.sem2:                                 # remove the duplicates in sem 2
            for j in self.sem2:
                if j != i and (self.sem2[j] != None) and (self.sem2[i] != None):
                    if self.sem2[j][0][:4] == self.sem2[i][0][:4]:
                        self.sem2[j] = None
                        break

        if (len(sem1) == 5) and (len(sem2) == 4):           # remove an extra course in sem 1 that is not recquired
            for i in range(len(sem1)):
                if sem1[i][0] in self.alt:
                    st.sem1[i] = None
                    for k in classrooms:
                        if k.room == self.sem1[i][2]:       # remove student from that class
                            k.students_sem1[i].pop(k.students_sem1[i].index(self))
                    break
            self.sem1[3] = None
            
        if (len(sem1) == 4) and (len(sem2) == 5):           # remove an extra course in sem 2 that is not recquired
            for i in range(len(sem2)):
                if sem2[i][0] in self.alt:
                    st.sem2[i] = None
                    for k in classrooms:
                        if k.room == self.sem2[i][2]:       # remove student from that class
                            k.students_sem2[i].pop(k.students_sem2[i].index(self))
                    break
            self.sem2[3] = None
# CAN BE ALTERED BELOW
        sem1 = [self.sem1[clss] for clss in self.sem1 if self.sem1[clss] != None]
        sem2 = [self.sem2[clss] for clss in self.sem2 if self.sem2[clss] != None]
        if (len(sem1) == 5) and (len(sem2) == 5):
            for k in classrooms:
                if k.room == self.sem1[3][2]:
                        k.students_sem1[3].pop(k.students_sem1[3].index(self.num))
                if k.room == self.sem2[3][2]:
                    k.students_sem2[3].pop(k.students_sem2[3].index(self.num))
                    
            self.sem1[3],self.sem2[3] = None,None


#######################################################################################################################################
# TEACHER      CLASS                                                                                                                  #
#######################################################################################################################################


class Teacher(Person):                                      # teacher class, used for adding teacher to classes
    def __init__(self, name, subjects):
        Person.__init__(self, name = '', number = 0)
        self.name= name
        self.subjects = subjects
        self.sem1 = {1:None, 2:None, 3:None, 4:None, 5:None}
        self.sem2 = {1:None, 2:None, 3:None, 4:None, 5:None}

    def __str__(self):
        return self.name+" "+str(self.subjects)

    def add_class(self,semester, period, subject):          # add teachers to classes
        if semester == 1:
            self.sem1[period] = subject
        if semester == 2:
            self.sem2[period] = subject

