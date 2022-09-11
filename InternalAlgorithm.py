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
                if len([int(i) for i in records[i+1][1:].strip().split() if i.isdigit()]) == 0:
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
for minor in d2Array:
    StudentCourseTableCopy = copy.deepcopy(StudentCourseTable)
    MinorRequirements = []
    name = minor[0]
    requirementcount = len(minor) - 1
    failedcount = 0
    for r in range(1,len(minor)):
        requirement = minor[r]
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
                
        #Will work on later
##        elif len(split_requirement) == 2:
##            required_coursenumber = int(split_requirement[0])
##            required_courses = split_requirement[1].split("*")
##            iterator = 0
##            while iterator < len(required_courses) and required_coursenumber > 0:
##                try:
##
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
                    
                 
            

    completion = (requirementcount-failedcount) / requirementcount
    MinorArray.append(Minor(name,completion,MinorRequirements))
print()
MinorArray.sort(reverse=True)
for certificate in MinorArray:
    print(certificate.name + " Completion Rate: " + str(certificate.completion * 100) + "%")
    if len(certificate.requirements) > 0:
        print("Remaining Requirements: " + str(certificate.requirements))
    print()
    


