#Note: For this file to work you need to install several dependency libraries.
#This can be done by opening command line and typing in the following instructions:
#pip install PyMuPDF
import fitz
import copy


def GetMinorCertificateRequirements(filename):
    file = open(filename,"r")
    readfile = file.read().split("\n")
    #print(readfile)
    d2Array = []
    for i in readfile:
        if i == "":
            continue
        readline = i.split(",")
        j = 0
        while j != len(readline):
            if readline[j] == '""' or len(readline[j]) == 0:
                del readline[j]
            else:
                readline[j] = readline[j]
                j += 1
        d2Array.append(readline)
    return d2Array

def GetStudentCourses(filename):
    StudentDict = {}
    
    #Citation for extracting text from PDF file: https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file/63518022#63518022
    with fitz.open(filename) as doc:
        records = ""
        for page in doc:
            records += page.get_text()
    
    records = records.split("\n")
    #print(records)
    for i in range(0,len(records)-1):
        #print(records[i])
        #print(ord(records[i][0]))
        #print(ord(records[i][-1]))
        
        if ord(records[i][-1]) == 32 and ord(records[i+1][0]) == 32 and len(records[i]) > 1 and len(records[i+1]) > 1:
            try:
                k = False
                r = True
                key = records[i].strip() + " " + records[i+1][1:].strip()
                #Citation for checking if string contains number: https://www.geeksforgeeks.org/python-check-if-string-contains-any-number/
                if not any(char.isdigit() for char in records[i+1][1:].strip()):
                    key += "100"
                    k = True
                if key in StudentDict and int(float(records[i+4])) > 0:
                    StudentDict[key] = str(StudentDict[key]) + "," + str(int(float(records[i+4])))
                    r = False
                elif int(float(records[i+4])) > 0:
                    StudentDict[key] = str(int(float(records[i+4])))
                if records[i].strip() in StudentDict and int(float(records[i+4])) > 0 and r:
                    StudentDict[records[i].strip()] = StudentDict[records[i].strip()] + "," + records[i+1][1:].strip()
                elif int(float(records[i+4])) > 0 and r:
                    StudentDict[records[i].strip()] = records[i+1][1:].strip()
                if k:
                    StudentDict[records[i].strip()] += "100"
            except:
                print(records[i])
                print(records[i+1])
    return StudentDict

def GetStudentCoursesDebug(filename):
    StudentDict = {}

    records = open(filename,"r").read().split("\n")
    #print(records)
    #print(len(records))
    for i in range(0,len(records)):
        if records[i] == "":
            continue
        try:
            split_records = records[i].split(",")
            #print(split_records)
            k = False
            r = True
            key = split_records[0].strip()
            #Citation for checking if string contains number: https://www.geeksforgeeks.org/python-check-if-string-contains-any-number/
            if not any(char.isdigit() for char in key):
                key += "100"
                k = True
            if key in StudentDict and int(split_records[1]) > 0:
                StudentDict[key] = str(StudentDict[key]) + "," + str(int(split_records[1]))
                r = False
            elif int(split_records[1]) > 0:
                StudentDict[key] = str(int(split_records[1]))
            
            if split_records[0].split(" ")[0] in StudentDict and int(split_records[1]) > 0 and r:
                StudentDict[split_records[0].split(" ")[0]] = StudentDict[split_records[0].split(" ")[0]] + "," + split_records[0].split(" ")[1].strip()
            elif int(split_records[1]) > 0 and r:
                StudentDict[split_records[0].split(" ")[0]] = split_records[0].split(" ")[1].strip()

            if k:
                StudentDict[records[i].strip()] += "100"
            
            
                
        except Exception as e:
            print(e)
            print(records[i])
    return StudentDict
        
class Minor:
    def __init__(self,name,completion,fullrequirements,completedrequirements,failedrequirements):
        self.name = name
        self.completion = completion
        self.fullrequirements = fullrequirements
        self.completedrequirements = completedrequirements
        self.failedrequirements = failedrequirements
        
    def __eq__(self,other):
        if self.completion == completion:
            return True
        return False
    
    def __lt__(self,other):
        if self.completion < other.completion:
            return True
        return False
    
    def __gt__(self,other):
        if self.completion > other.completion:
            return True
        return False
        
    



def delcourse(StudentCourseTable,RemovedCourse):
    rc = RemovedCourse.strip().split(" ")
    tdata = StudentCourseTable[RemovedCourse].split(",")
    if len(tdata) > 0:
        del tdata[0]
    if len(tdata) > 0:
        StudentCourseTable[RemovedCourse] = ",".join(tdata)
    else:
        del StudentCourseTable[RemovedCourse]
        tdata = StudentCourseTable[rc[0]].split(",")
        i = 0
        while i < len(tdata):
            if tdata[i] == rc[1]:
                del tdata[i]
            else:
                i += 1
        StudentCourseTable[rc[0]] = ",".join(tdata)
        return StudentCourseTable

def getcoursecredits(StudentCourseTable,Course):
    c = StudentCourseTable[Course].split(",")
    return int(c[0])
        
    
        


d2Array = GetMinorCertificateRequirements("MinorCertificateRequirements.csv")
StudentCourseTable = GetStudentCoursesDebug("Test.txt")
#StudentCourseTable = GetStudentCourses("SSR_TSRPT.pdf")

#Useful for debug of student/requirements reports
print(d2Array)
print()
print(StudentCourseTable)

MinorArray = []
#Note: For all student/minor requirements, it will *only* count the requirement as fufilled if the student course is identical to the one in the requirement.
#For example, CAS 100A, CAS 100B and CAS 100C will not count for the purposes of fufilling a CAS 100 class.
for minor in d2Array:
    
    StudentCourseTableCopy = copy.deepcopy(StudentCourseTable)
    #print(StudentCourseTableCopy)
    MinorRequirements = []
    name = minor[0]
    requirementcount = len(minor) - 1
    failedcount = 0
    DuplicateCourses = {}
    ChoiceCourses = {}
    DuplicatesNeeded = {}
    requirementiterator = 0
    completedrequirements = []
    fullrequirements = []
    
    newminor = []
    print(name)

    #Gets full requirements from minor
    for m in range(1,len(minor)):
        split_i = minor[m].split(".")
        for i in range(0,len(split_i)):
            split_i[i] = split_i[i].strip()
        if len(split_i) == 1:
            fullrequirements.append(split_i[0])
            
        elif len(split_i) == 2:
            if split_i[0][0] == "(" or split_i[0][-1] == ")":
                split_i[0] = split_i[0][1:-1]
                cc = "credit"
            else:
                cc = "course"
            if int(split_i[0]) > 1:
                cc += "s"
                
            fullrequirements.append(split_i[0] + " " + cc + " from (" + str(split_i[1].split("*"))[1:-1] + ")")

        elif len(split_i) == 3:
            fullrequirements.append(split_i[2] + " credits from " + split_i[0] + " " + split_i[1] + "-level classes or higher")

    #Tests whether minor/certificate has duplicate courses in "choose any X of Y" requirements, and if so puts them in a special duplicate course list
    for m in minor:
        split_i = m.split(".")
        for i in range(0,len(split_i)):
            split_i[i] = split_i[i].strip()
        if len(split_i) == 2:
            requirementsplit = split_i[1].split("*")
            iterator = 0
            #print(m)
            #This may or may not be wrong, will need to test
            while iterator < len(requirementsplit):
                
                
                c = requirementsplit[iterator].split("/")
                for i in range(0,len(c)):
                    c[i] = c[i].strip()
                #print(c[0])
                #There are two cases that need to be tackled for each requirement: One where only a single course can be used to fufill a sub-requirement, and one where multiple courses can be used to fufuill a sub-requirement.
                #The block of code below deals with the first case.
                if len(c) == 1:
                    if c[0] not in ChoiceCourses:
                        ChoiceCourses[c[0]] = str(requirementiterator)
                        
                    elif c[0] not in DuplicateCourses:
                        #print(c[0])
                        
                        DuplicateCourses[c[0]] = ChoiceCourses[c[0]] + "," + str(requirementiterator)
                        del requirementsplit[iterator]

                        #The way the code is set up, the first time a duplicate course is found, it is not recognized as duplicate, and is therefore not expunged from the requirements section.
                        #This would mean that that course can be "double counted".
                        #As such, this block of code below manually goes back and expunges that first duplicate course from the requirement it came from.
                        #This code shows up a total of twice, once here and once in the second case.  Both of them are more or less identical, and as such it might be best to convert this block of code into a function in the future.
                        backchange = newminor[int(ChoiceCourses[c[0]])].split(".")
                        split_backchange = backchange[1].split("*")
                        j = 0
                        while j < len(split_backchange):
                            split_j = split_backchange[j].split("/")
                            i = 0
                            while i < len(split_j):
                                if split_j[i] == c[0]:
                                    del split_j[i]
                                else:
                                    i += 1
                            if len(split_j) > 0:
                                split_backchange[j] = "/".join(split_j)
                            else:
                                del split_backchange[j]
                                iterator -= 1
                            j += 1
                        newminor[int(ChoiceCourses[c[0]])] = backchange[0] + "." + "*".join(split_backchange)
                        #print(newminor[int(ChoiceCourses[c[0]])])
                        
                        
                    else:
                        DuplicateCourses[c[0]] = DuplicateCourses[c[0]] + "," + str(requirementiterator)
                        del requirementsplit[iterator]
                #This block of code deals with the second case.
                else:
                    ccopy = copy.deepcopy(c)
                    #print(c[0])
                    #print(c[1])
                    AppendChoice1 = False
                    AppendChoice2 = False
                    jterator = 0
                    #print(c)
                    #print(ccopy)
                    while jterator < len(c):
                        
                        if c[jterator] not in ChoiceCourses.keys():
                            ChoiceCourses[c[jterator]] = str(requirementiterator)
                        elif c[jterator] not in DuplicateCourses.keys():
                            #This block of code deals with any courses that are both duplicates and have multiple courses eligible for fufilling sub-requirements.
                            #This block of code shows up twice, once here and once in the block of code where the course is already in DuplicateCourses.
                            DuplicateCourses[c[jterator]] = ChoiceCourses[c[jterator]] + "," + str(requirementiterator)
                            dupec = []
                            for i in ccopy:
                                #print(i)
                                if i == c[jterator]:
                                    continue
                                if i in DuplicateCourses.keys():
                                    dupec.append(i)
                                else:
                                    DuplicateCourses[c[jterator]] += "*" + i
                            #This deals with the relevant duplicate courses, and adjusts their split so that duplicate courses (that they now know are duplicate but did not at the time of initialization) is correctly placed.
                            if len(dupec) > 0:
                                DuplicateCourses[c[jterator]] += "/"
                                for i in range(0,len(dupec)):
                                    DuplicateCourses[c[jterator]] += idupec[i]
                                    if i != len(dupec) - 1:
                                        DuplicateCourses[c[jterator]] += "*"
                                    duperesult = DuplicateCourses[idupec[i]].split(",")
                                    dupersplits = duperestult[-1].split("/")
                                    dupersplits[1] += "*" + c[jterator]
                                    dupersplita = duplersplits[0].split("*")
                                    kterator = 0
                                    while kterator < len(dupersplita):
                                        if dupersplita[kterator] == c[jterator]:
                                            del dupersplita[kterator]
                                        else:
                                            kterator += 1
                                    dupersplits[0] = "*".join(dupersplita)
                                    duperesult[-1] = "/".join(dupersplits)
                                    DuplicateCourses[idupec[i]] = ",".join(duperesult)
                                        

                            #This is the second time the requirement rewriting codeblock shows up.
                            backchange = newminor[int(ChoiceCourses[c[jterator]])].split(".")
                            split_backchange = backchange[1].split("*")
                            #print(backchange)
                            j = 0
                            while j < len(split_backchange):
                                split_j = split_backchange[j].split("/")
                                i = 0
                                while i < len(split_j):
                                    if split_j[i] == c[jterator]:
                                        del split_j[i]
                                        dupec = DuplicateCourses[c[jterator]].split(",")
                                        dupec[0] = dupec[0] + "*" + "*".join(split_j)
                                        DuplicateCourses[c[jterator]] = ",".join(dupec)
                                    else:
                                        i += 1
                                if len(split_j) > 0:
                                    split_backchange[j] = "/".join(split_j)
                                else:
                                    del split_backchange[j]
                                    iterator -= 1
                                j += 1
                            newminor[int(ChoiceCourses[c[jterator]])] = backchange[0] + "." + "*".join(split_backchange)
                            del c[jterator]
                            jterator -= 1
                            #print(newminor[int(ChoiceCourses[c[0]])])
                        else:
                            DuplicateCourses[c[jterator]] = DuplicateCourses[c[jterator]] + "," + str(requirementiterator)
                            for i in ccopy:
                                dupec = []
                                if i == c[jterator]:
                                    continue
                                if i in DuplicateCourses.keys():
                                    dupec.append(i)
                                else:
                                    DuplicateCourses[c[jterator]] += "*" + i
                            #This deals with the relevant duplicate courses, and adjusts their split so that duplicate courses (that they now know are duplicate but did not at the time of initialization) is correctly placed.
                            if len(dupec) > 0:
                                DuplicateCourses[c[jterator]] += "/"
                                for i in range(0,len(dupec)):
                                    DuplicateCourses[c[jterator]] += idupec[i]
                                    if i != len(dupec) - 1:
                                        DuplicateCourses[c[jterator]] += "*"
                                        
                                    duperesult = DuplicateCourses[idupec[i]].split(",")
                                    dupersplits = duperestult[-1].split("/")
                                    dupersplits[1] += "*" + c[jterator]
                                    dupersplita = duplersplits[0].split("*")
                                    
                                    kterator = 0
                                    while kterator < len(dupersplita):
                                        if dupersplita[kterator] == c[jterator]:
                                            del dupersplita[kterator]
                                        else:
                                            kterator += 1
                                            
                                    dupersplits[0] = "*".join(dupersplita)
                                    duperesult[-1] = "/".join(dupersplits)
                                    DuplicateCourses[idupec[i]] = ",".join(duperesult)
                            del c[jterator]
                            jterator -= 1
                        jterator += 1


                    requirementsplit[iterator] = "/".join(c)

                        
                iterator += 1
            newminor.append(split_i[0] + "." + "*".join(requirementsplit))
            #print(newminor[-1])
                                            
        else:
            newminor.append(m)
        requirementiterator += 1
    #print(newminor)
    #print(list(ChoiceCourses.keys()))
    #print(list(DuplicateCourses.keys()))
    #Deletes all duplicate courses that the student does not have, as they are useless for the purposes of calculating whether a minor is elegible
    #Also makes a copy of the original duplicate course list that has all the unused courses.
    #This is so said unused courses can be retrieved for the purposes of failed requirement course calculation
    #print(DuplicateCourses)
    DuplicateCoursesUnused = copy.deepcopy(DuplicateCourses)
    for i in DuplicateCoursesUnused.keys():
        try:
            DuplicateCourses[i] = StudentCourseTableCopy[i] + "," + DuplicateCourses[i]
        except:
            del DuplicateCourses[i]
    #print(DuplicateCourses)
    for i in DuplicateCourses.keys():
        del DuplicateCoursesUnused[i]
        StudentCourseTableCopy = delcourse(StudentCourseTableCopy,i)
        
                             
    for r in range(1,len(newminor)):
        fufilledcourse = []
        requirement = newminor[r]
        split_requirement = requirement.split(".")
        if len(split_requirement) == 1:
            try:
                StudentCourseTableCopy = delcourse(StudentCourseTableCopy,requirement)
                completionrequirements.append(requirement)
            except Exception as e:
                failedcount += 1
                MinorRequirements.append(requirement)
                
        #Note: This should only be triggered in certificates.  Triggering case 2 and case 3 in the same minor/certificate may cause double counting (working on fixing this).
        #May or may not need to be fixed
        elif len(split_requirement) == 2:
            
            if split_requirement[0][0] == "(" and split_requirement[0][-1] == ")":
                required_coursenumber = int(split_requirement[0][1:-1])
                credit = True
                debug = True
                #print(DuplicateCourses)
            else:
                required_coursenumber = int(split_requirement[0])
                credit = False
                debug = False
            required_courses = split_requirement[1].split("*")
            if debug:
                print(required_courses)
                print(len(required_courses))
                
            iterator = 0
            while iterator < len(required_courses) and required_coursenumber > 0:
                print(required_courses[iterator])
                print(iterator)
                print(len(required_courses))
                if required_courses[iterator] == "":
                    print("delete " + required_courses[iterator])
                    del required_courses[iterator]
                    continue
                rc = required_courses[iterator].split("/")
                c = 0
                d = False
                currentcourse = ""
                for i in rc:
                    if i not in DuplicateCourses:
                        if i in StudentCourseTableCopy.keys():
                            if getcoursecredits(StudentCourseTableCopy,i) > c:
                                c = getcoursecredits(StudentCourseTableCopy,i)
                                currentcourse = i
                            c = max(c,getcoursecredits(StudentCourseTableCopy,i))
                            d = True
                            
                            
                            
                            #print(i)
                if d:
                    if credit:
                        required_coursenumber -= c
                    else:
                        required_coursenumber -= 1
                    StudentCourseTableCopy = delcourse(StudentCourseTableCopy,currentcourse)
                    fufilledcourse.append([currentcourse,c])
                    del required_courses[iterator]
                else:
                    iterator += 1
            if required_coursenumber > 0:
                DuplicatesNeeded[r] = str(required_coursenumber) + "," + str(credit)
            else:
                sstring = str(fullrequirements[r-1]) + ": Fulfilled by ("
                for i in fufilledcourse:
                    if credit:
                        sstring += str(i[1]) + "-credit course " + i[0]
                    else:
                        sstring += i[0]
                    if i != fufilledcourse[-1]:
                        sstring += ", "
                sstring += ")"
                completedrequirements.append(sstring)
            
                    
                    
        #Note: this should only occur in minors.  Triggering case 2 and case 3 in the same minor/certificate may cause double counting (working on fixing this).
        elif len(split_requirement) == 3:
            field = split_requirement[0]
            numcredits = split_requirement[2]
            try:
                #Citation for extracting numbers from string: https://www.geeksforgeeks.org/python-extract-numbers-from-string/
                fieldcoursennumbers = [int(course) for course in StudentCourseTableCopy[field].split() if course.isdigit()]
                print(fieldcoursenumbers)
                fieldcourses = StudentCourseTableCopy[field].split(",")
                print(fieldcourses)
                for course in range(0,len(fieldcoursenumbers)):
                    if numcredits <= 0:
                        break
                    if fieldcoursenumbers[course] > split_requirement[1]:
                        tdata = StudentCourseTableCopy[fieldcourses[course]].split(",")
                        i = 0
                        while i < len(tdata) and numcredits > 0:
                            numcredits -= int(tdata[i])
                        fufilledcourse.append([fieldcourses[course],int(tdata[i])])
                if numcredits > 0:
                    failedcount += 1
                    MinorRequirements.append(str(numcredits) + " credits from " + field + " " + split_requirement[1] + "-level classes or higher")
                else:
                    sstring = str(fullrequirements[r-1]) + ": Fulfilled by ("
                for i in fufilledcourse:
                    sstring += str(i[1]) + "-credit course " + i[0]
                    if i != fufilledcourse[-1]:
                        sstring += ", "
                sstring += ")"
                completedrequirements.append(sstring)
            except:
                failedcount += 1
                MinorRequirements.append(str(numcredits) + " credits from " + field + " " + split_requirement[1] + "-level classes or higher")

    #print(name)
    #print(DuplicatesNeeded)
    #print(DuplicateCourses)
    DuplicateCheck = True
    while len(DuplicatesNeeded) > 0 and len(DuplicateCourses) > 0:
        #This absolute nonsense of a code block serves to (attempt to) solve the problem of placing the correct duplicate courses in the optimal course requirements such that the minor/certificate will be correctly verified as complete.
        #The first part of this is to test to see whether there are any duplicate courses that are only applicable for a single requirement, and if so allocating that to said requirement.
        #Ideally this will cause a cascading effect where the allocation of single requirement duplicate courses creates more single requirement duplicate courses as more and more requirements are fulfilled.
        if DuplicateCheck:
            DuplicateCheck = False
            DuplicateCoursesDelete = {}
            for keys in DuplicateCourses.keys():
                r = DuplicateCourses[keys].split(",")
                c = int(r[0])
                del r[0]
                #print(r)
                iterator = 0
                while iterator < len(r):
                    r[iterator].split("*")
                    if int(r[iterator].split("*")[0]) not in DuplicatesNeeded.keys():
                        del r[iterator]
                    else:
                        iterator += 1
                if len(r) <= 1:
                    if len(r) == 0:
                        DuplicateCoursesDelete[keys] = ""
                    else:
                        requirementlist = DuplicatesNeeded[int(r[0].split("*")[0])].split(",")
                        if requirementlist[1] == "True":
                            cr = 0
                            for i in r[0].split("/")[0].split("*")[1:]:
                                try:
                                    cr = max(cr,StudentCourseTableCopy[i])
                                except:
                                    dummy = 'dummy'
                            c -= cr
                            requirementlist[0] = str(int(requirementlist[0]) - c)
                        else:
                            requirementlist[0] = str(int(requirementlist[0]) - 1)
                        if int(requirementlist[0]) > 0:
                            DuplicatesNeeded[int(r[0])] = ",".join(requirementlist)
                        else:
                            DuplicateCheck = True
                            del DuplicatesNeeded[int(r[0].split("*")[0])]
                        DuplicateCoursesDelete[keys] = ""

            for keys in DuplicateCoursesDelete.keys():
                del DuplicateCourses[keys]
        else:
            #This is the block of code that deals with placing the correct duplicate courses in the optimal course requirements such that the minor/certificate will be correctly verified as complete.
            #This is very much a difficult problem, possibly impossible, and as such here I have made a placeholder algorithm that just takes the first duplicate course and places it in the first requirement available to it.
            #I'm not even gonna pretend that this is optimal, will fix later probably
            k = list(DuplicateCourses.keys())[0]
            r = DuplicateCourses[k].split(",")
            c = int(r[0])
            #print(r[1])
            requirementlist = DuplicatesNeeded[int(r[1].split("*")[0])].split(",")
            if requirementlist[1] == "True":
                cr = 0
                for i in r[0].split("/")[0].split("*")[1:]:
                    try:
                        cr = max(cr,StudentCourseTableCopy[i])
                    except:
                        dummy = 'dummy'
                c -= cr
                requirementlist[0] = str(int(requirementlist[0]) - c)
            else:
                requirementlist[0] = str(int(requirementlist[0]) - 1)
            if int(requirementlist[0]) > 0:
                DuplicatesNeeded[r[1].split("*")[0]] = ",".join(requirementlist)
            else:
                DuplicateCheck = True
                del DuplicatesNeeded[int(r[1].split("*")[0])]
            del DuplicateCourses[k]
    #print(DuplicatesNeeded)
    #print(DuplicateCourses)
    if len(DuplicatesNeeded) > 0:
        for requirements in DuplicatesNeeded.keys():
            numbers = DuplicatesNeeded[requirements].split(",")
            for h in DuplicateCoursesUnused.keys():
                j = DuplicateCoursesUnused[h].split(",")
                
                #print(j)
                for k in j:
                    m = k.split("*")
                    #print(m)
                    if int(m[0]) == requirements:
                        if len(m) > 1:
                            #Deletes "loose" requirement (X part of "X/Y" where Y is a duplicate and X is either duplicate or not)
                            backchange = newminor[requirements].split(".")
                            split_backchange = backchange[1].split("*")
                            j = 0
                            while j < len(split_backchange):
                                split_j = split_backchange[j].split("/")
                                #print(split_j)
                                i = 0
                                while i < len(split_j):
                                    if split_j[i] in m[1:]:
                                        del split_j[i]
                                    else:
                                        i += 1
                                if len(split_j) > 0:
                                    split_backchange[j] = "/".join(split_j)
                                else:
                                    del split_backchange[j]
                                j += 1
                            newminor[requirements] = backchange[0] + "." + "*".join(split_backchange)

                            #Appends "loose" requirement back to correct "X/Y" pair to maintain stability
                            #print("End")
                            #print(m)
                            n = ""
                            for i in range(1,len(m)):
                                n += "/" + m[i]
                            if numbers[1] == "True":
                                search = h+n
                                search = search.split("/")
                                ma = 0
                                cma = ""
                                for i in search:
                                    try:
                                        if int(StudentCourseTableCopy[i].split(",")[0]) > ma:
                                            ma = int(StudentCourseTableCopy[i].split(",")[0])
                                            cma = i
                                    except:
                                        dummy = "dummy"
                                if i != "":
                                    n += " {currently fufilled by " + str(ma) + "-credit course " + cma + "}"
                            #print(n)
                        else:
                            n = ""
                        newminor[requirements] += "*" + h + n
                        break
                
            if numbers[1] == "True":
                cc = "credit"
            else:
                cc = "course"
            if int(numbers[0]) > 1:
                cc += "s"
            failedcount += 1
            r = newminor[requirements].split(".")[1].split("*")
            i = 0
            while i < len(r):
                if r[i] == "":
                    del r[i]
                else:
                    i += 1
            newminor[requirements] = newminor[requirements].split(".")[0] + "." + "*".join(r)
            #print(newminor[requirements])
                
            #print(numbers[0])
            #print(newminor)
            #MinorRequirements.append(numbers[0] + " " + cc + " from (" + str(newminor[requirements].split("."))[1:-1] + ")")
            MinorRequirements.append(numbers[0] + " " + cc + " from (" + str(str(newminor[requirements].split(".")[1]).split("*"))[1:-1] + ")")
            
            
            
            
        
            
                    
                 
            

    completion = (requirementcount-failedcount) / requirementcount
    MinorArray.append(Minor(name,completion,fullrequirements,completedrequirements,MinorRequirements))
print()
MinorArray.sort(reverse=True)
for certificate in MinorArray:
    print(certificate.name + " Completion Rate: " + str(certificate.completion * 100) + "%")
    print()
    print("Full Requirements: " + str(list(certificate.fullrequirements)))
    print()
    if len(certificate.completedrequirements) > 0:
        print("Completed Requirements: " + str(list(certificate.completedrequirements)))
        print()
    if len(certificate.failedrequirements) > 0:
        print("Remaining Requirements: " + str(list(certificate.failedrequirements)))
        print()

        #Doesn't work how I want it to, I'd have to directly go into the requirements and edit the relevant 2. ones
        #print(str(list(s for s in sorted(certificate.requirements))))

    print()
    


