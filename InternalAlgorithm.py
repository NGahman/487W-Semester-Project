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
            if readline[j] == '""':
                del readline[j]
            else:
                readline[j] = readline[j][1:-1]
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
                key = records[i].strip() + " " + records[i+1][1:].strip()
                #Citation for checking if string contains number: https://www.geeksforgeeks.org/python-check-if-string-contains-any-number/
                if not any(char.isdigit() for char in records[i+1][1:].strip()):
                    key += "100"
                if key in StudentDict and int(float(records[i+4])) > 0:
                    StudentDict[key] = str(StudentDict[key]) + "," + str(int(float(records[i+4])))
                elif int(float(records[i+4])) > 0:
                    StudentDict[key] = str(int(float(records[i+4])))
                if records[i].strip() in StudentDict and int(float(records[i+4])) > 0:
                    StudentDict[records[i].strip()] = StudentDict[records[i].strip()] + "," + records[i+1][1:].strip()
                elif int(float(records[i+4])) > 0:
                    StudentDict[records[i].strip()] = records[i+1][1:].strip()
            except:
                print(records[i])
                print(records[i+1])
    return StudentDict
        
        
class Minor:
    def __init__(self,name,completion,requirements):
        self.name = name
        self.completion = completion
        self.requirements = requirements
        
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
        
    
    
        


d2Array = GetMinorCertificateRequirements("MinorCertificateRequirements.csv")
print(d2Array)
print()
StudentCourseTable = GetStudentCourses("SSR_TSRPT.pdf")
print(StudentCourseTable)
MinorArray = []
#Note: For all student/minor requirements, it will *only* count the requirement as fufilled if the student course is identical to the one in the requirement.
#For example, CAS 100A, CAS 100B and CAS 100C will not count for the purposes of fufilling a CAS 100 class.
for minor in d2Array:
    StudentCourseTableCopy = copy.deepcopy(StudentCourseTable)
    MinorRequirements = []
    name = minor[0]
    requirementcount = len(minor) - 1
    failedcount = 0
    DuplicateCourses = {}
    ChoiceCourses = {}
    DuplicatesNeeded = {}
    requirementiterator = 0
    #Tests whether minor/certificate has duplicate courses in "choose any X of Y" requirements, and if so puts them in a special duplicate course list
    newminor = []
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
                if len(c) == 1:
                    if c[0] not in ChoiceCourses:
                        ChoiceCourses[c[0]] = str(requirementiterator)
                        
                    elif c[0] not in DuplicateCourses:
                        #print(c[0])
                        DuplicateCourses[c[0]] = ChoiceCourses[c[0]] + "," + str(requirementiterator)
                        del requirementsplit[iterator]
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
                elif len(c) == 2:
                    #print(c[0])
                    #print(c[1])
                    AppendChoice1 = False
                    AppendChoice2 = False
                    if c[0] not in ChoiceCourses.keys():
                        ChoiceCourses[c[0]] = str(requirementiterator)
                        AppendChoice1 = True
                    elif c[0] not in DuplicateCourses.keys():
                        DuplicateCourses[c[0]] = ChoiceCourses[c[0]] + "," + str(requirementiterator) + "*" + c[1]
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
                        DuplicateCourses[c[0]] = DuplicateCourses[c[0]] + "," + str(requirementiterator) + "*" + c[1]

                    if c[1] not in ChoiceCourses.keys():
                        ChoiceCourses[c[1]] = str(requirementiterator)
                        AppendChoice2 = True
                    elif c[1] not in DuplicateCourses.keys():
                        DuplicateCourses[c[1]] = ChoiceCourses[c[1]] + "," + str(requirementiterator) + "*" + c[0]
                        backchange = newminor[int(ChoiceCourses[c[1]])].split(".")
                        split_backchange = backchange[1].split("*")
                        j = 0
                        while j < len(split_backchange):
                            split_j = split_backchange[j].split("/")
                            i = 0
                            while i < len(split_j):
                                if split_j[i] == c[1]:
                                    del split_j[i]
                                else:
                                    i += 1
                            if len(split_j) > 0:
                                split_backchange[j] = "/".join(split_j)
                            else:
                                del split_backchange[j]
                                iterator -= 1
                            j += 1
                        newminor[int(ChoiceCourses[c[1]])] = backchange[0] + "." + "*".join(split_backchange)
                        #print(newminor[int(ChoiceCourses[c[1]])])
                    else:
                        DuplicateCourses[c[1]] = DuplicateCourses[c[1]] + "," + str(requirementiterator) + "*" + c[0]

                    #if AppendChoice1 and AppendChoice2:
                    #    print(requirementsplit[iterator])
                    if AppendChoice1 and not AppendChoice2:
                        requirementsplit[iterator] = c[0]
                    elif not AppendChoice1 and AppendChoice2:
                        requirementsplit[iterator] = c[1]
                    elif not AppendChoice1 and not AppendChoice2:
                        del requirementsplit[iterator]
                iterator += 1
            newminor.append(split_i[0] + "." + "*".join(requirementsplit))
            #print(newminor[-1])
                                            
        else:
            newminor.append(m)
        requirementiterator += 1
    #print(list(ChoiceCourses.keys()))
    #print(list(DuplicateCourses.keys()))
    #Deletes all duplicate courses that the student does not have, as they are useless for the purposes of calculating whether a minor is elegible
    #Also makes a copy of the original duplicate course list that has all the unused courses.
    #This is so said unused courses can be retrieved for the purposes of failed requirement course calculation
    DuplicateCoursesUnused = copy.deepcopy(DuplicateCourses)
    for i in DuplicateCoursesUnused.keys():
        try:
            DuplicateCourses[i] = StudentCourseTableCopy[DuplicateCourses[i]] + "," + DuplicateCourses[i]
        except:
            del DuplicateCourses[i]
    for i in DuplicateCourses.keys():
        del DuplicateCoursesUnused[i]
        
                             
    for r in range(1,len(newminor)):
        requirement = newminor[r]
        split_requirement = requirement.split(".")
        if len(split_requirement) == 1:
            try:
                split_course = StudentCourseTableCopy[split_requirement].split(",")
                if len(split_course) == 1:
                    del StudentCourseTableCopy[split_requirement]
                else:
                    del split_course[0]
                    StudentCourseTableCopy[split_requirement] = ",".join(split_course)
            except:
                failedcount += 1
                MinorRequirements.append(requirement)
                
        #Note: This should only be triggered in certificates.  Triggering case 2 and case 3 in the same minor/certificate may cause double counting (working on fixing this).
        #May or may not need to be fixed
        elif len(split_requirement) == 2:
            
            if split_requirement[0][0] == "(" and split_requirement[0][-1] == ")":
                required_coursenumber = int(split_requirement[0][1:-1])
                credit = True
            else:
                required_coursenumber = int(split_requirement[0])
                credit = False
            required_courses = split_requirement[1].split("*")
            iterator = 0
            while iterator < len(required_courses) and required_coursenumber > 0:
                if required_courses[iterator] == "":
                    del required_courses[iterator]
                    continue
                if required_courses[iterator] not in DuplicateCourses:
                    if required_courses[iterator] in StudentCourseTableCopy:
                        del required_courses[iterator]
                        if credit:
                            required_coursenumber -= StudentCourseTableCopy[required_courses[iterator]]
                        else:
                            required_coursenumber -= 1
                iterator += 1
            if required_coursenumber > 0:
                DuplicatesNeeded[r] = str(required_coursenumber) + "," + str(credit)
            
                    
                    
        #Note: this should only occur in minors.  Triggering case 2 and case 3 in the same minor/certificate may cause double counting (working on fixing this).
        elif len(split_requirement) == 3:
            field = split_requirement[0]
            numcredits = split_requirement[2]
            try:
                #Citation for extracting numbers from string: https://www.geeksforgeeks.org/python-extract-numbers-from-string/
                fieldcoursennumbers = [int(course) for course in StudentCourseTableCopy[field].split() if course.isdigit()]
                fieldcourses = StudentCourseTableCopy[field].split(",")
                for course in range(0,len(fieldcoursenumbers)):
                    if numcredits <= 0:
                        break
                    if fieldcoursenumbers[course] > split_requirement[1]:
                        numcredits -= int(StudentCourseTableCopy[fieldcourses[course]])
                if numcredits > 0:
                    failedcount += 1
                    MinorRequirements.append(str(numcredits) + " credits from " + field + " " + split_requirement[1] + "-level classes or higher")
            except:
                failedcount += 1
                MinorRequirements.append(str(numcredits) + " credits from " + field + " " + split_requirement[1] + "-level classes or higher")

    #I'm like 90% sure that this is straight up wrong, will need to test thoroughly
    DuplicateCheck = True
    while len(DuplicatesNeeded) > 0 and len(DuplicateCourses) > 0:
        
        if DuplicateCheck:
            DuplicateCheck = False
            for keys in DuplicateCourses.keys():
                r = DuplicateCourses[keys].split(",")
                c = int(r[0])
                del r[0]
                iterator = 0
                while iterator < len(r):
                    r[iterator].split("*")
                    if r[iterator] not in DuplicatesNeeded.keys():
                        del r[iterator]
                    else:
                        iterator += 1
                if len(r) < 1:
                    if len(r) == 0:
                        del DuplicateCourses[keys]
                    else:
                        requirementlist = DuplicatesNeeded[r[0].split("*")[0]].split(",")
                        if requirementlist[1] == "True":
                            try:
                                c -= StudentCourseTableCopy[r[0].split("*")[1]]
                            except:
                                dummy = 'dummy'
                            requirementlist[0] = str(int(requirementlist[0]) - c)
                        else:
                            requirementlist[0] = str(int(requirementlist[0]) - 1)
                        if int(requirementlist[0]) > 0:
                            DuplicatesNeeded[r[0]] = ",".join(requirementlist)
                        else:
                            DuplicateCheck = False
                            del DuplicatesNeeded[r[0].split("*")[0]]
                        del DuplicateCourses[keys]
        else:
            #I'm not even gonna pretend that this is optimal, will fix later probably
            k = list(DuplicateCourses.keys())[0]
            r = DuplicateCourses[k].split(",")
            c = r[0]
            requirementlist = DuplicatesNeeded[r[1].split("*")[0]].split(",")
            if requirementlist[1] == "True":
                try:
                    c -= StudentCourseTableCopy[r[0].split("*")[1]]
                except:
                    dummy = 'dummy'
                requirementlist[0] = str(int(requirementlist[0]) - c)
            else:
                requirementlist[0] = str(int(requirementlist[0]) - 1)
            if int(requirementlist[0]) > 0:
                DuplicatesNeeded[r[0].split("*")[0]] = ",".join(requirementlist)
            else:
                DuplicateCheck = False
                del DuplicatesNeeded[r[0].split("*")[0]]
            del DuplicateCourses[k]
    if len(DuplicatesNeeded) > 0:
        #print(list(DuplicatesNeeded.keys()))
        #print(list(DuplicateCoursesUnused.values()))
        for requirements in DuplicatesNeeded.keys():
            
            for i in DuplicateCoursesUnused.keys():
                j = DuplicateCoursesUnused[i].split(",")
                for k in j:
                    m = k.split("*")
                    if int(m[0]) == requirements:
                        if len(m) > 1:
                            #Deletes "loose" requirement (part of "X/Y" where Y is a duplicate and X is either duplicate or not)
                            backchange = newminor[requirements].split(".")
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
                                j += 1
                            newminor[requirements] = backchange[0] + "." + "*".join(split_backchange)

                            #Appends "loose" requirement back to correct "X/Y" pair to maintain stability
                            n = "/" + m[1]
                        else:
                            n = ""
                        newminor[requirements] += "*" + i + n
                        break
                
            #Gonna need to figure out how to add duplicated courses
            numbers = DuplicatesNeeded[requirements].split(",")
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
    MinorArray.append(Minor(name,completion,MinorRequirements))
print()
MinorArray.sort(reverse=True)
for certificate in MinorArray:
    print(certificate.name + " Completion Rate: " + str(certificate.completion * 100) + "%")
    if len(certificate.requirements) > 0:
        print("Remaining Requirements: " + str(list(certificate.requirements)))

        #Doesn't work how I want it to, I'd have to directly go into the requirements and edit the relevant 2. ones
        #print(str(list(s for s in sorted(certificate.requirements))))

    print()
    


