import requests
import csv
from bs4 import BeautifulSoup


class Minor:
    def __init__(self, name, URL):
        self.name = name
        self.URL = URL
        self.requirements = []


# following dictionaries are used later
courseAbbreviations = {"sociology": "SOC", "psychology": "PSYCH"}
numbers = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
           'eleven': 11, 'twelve': 12}


# ----------------------------------------------------------------------------------------------------------------------


# Parse sentence of the following structure:
# 'Select x credits in y'
# or 'Select x credits of y courses'
# or 'Select x credits of y-level z courses'
# or 'Select x credits (at least n credits at the m level) in y'
# or 'at least x credits must be at the y level'
# for an example, see: PSYCH, SOC, HDFS, etc.
def parseSentence1(rows, rowModified3, i, minor: Minor):
    flag1 = False
    flag2 = False
    exceptcourse = ''

    for i in range(0, len(rowModified3)):
        if rowModified3[i] == 'Select':
            credits = rowModified3[i + 1]
        if rowModified3[i] == 'in':
            subject = rowModified3[i + 1]
            if subject.lower() in courseAbbreviations.keys():
                subject = courseAbbreviations[subject.lower()]
        if 'in' not in rowModified3:
            if rowModified3[i] == 'courses':
                subject = rowModified3[i - 1]
                if subject.lower() in courseAbbreviations.keys():
                    subject = courseAbbreviations[subject.lower()]
        if rowModified3[i] == 'least':
            credits2 = rowModified3[i + 1]
            flag1 = True
        if rowModified3[i].startswith('level'):
            level = rowModified3[i - 1]
            flag2 = True
        if rowModified3[i].startswith('from'):
            subject = rowModified3[i + 2]
            if 'range' in rowModified3:
                level = rowModified3[i + 3]
                flag2 = True
        if rowModified3[i] == 'except':
            exceptcourse = exceptcourse + "*" + rowModified3[i + 2]

    if flag1 == False and flag2 == False:
        AdditionalClass1 = subject + ".1-499" + exceptcourse + "." + credits
        minor.requirements.append(AdditionalClass1)
    elif flag1 == False and flag2 == True:
        AdditionalClass1 = subject + "." + level + "-499." + credits
        minor.requirements.append(AdditionalClass1)
    elif flag1 == True and flag2 == True:
        AdditionalClass1 = subject + ".1-499." + credits
        minor.requirements.append(AdditionalClass1)

        AdditionalClass2 = subject + "." + level + "-499." + credits2
        minor.requirements.append(AdditionalClass2)

    return i + 1


# Parse sentence of the following structure:
# 'In addition to the x credits of coursework listed, students may choose any y (z credits) of the following:'
def parseSentence2(rows, rowModified3, i, minor: Minor):
    for x in rowModified3:
        if x.lower() in numbers.keys():
            numberOfCourses = numbers[x.lower()]

    RequiredClasses = str(numberOfCourses)

    k = i + 1
    while k < len(rows):
        rowModified4 = str(rows[k]).split('"')
        if "courselistcomment" in rowModified4:
            break

        rowModified5 = str(rows[k]).split()

        flagx = False  # if flagx == True, that means the structure of the HTML code includes 'title'

        for j in range(len(rowModified5)):
            if rowModified5[j].startswith('title'):
                flagx = True

                coursePrefix = rowModified5[j].split('"')[1]
                courseNumber = rowModified5[j + 1].split('"')[0]

                flag1 = False
                for char in courseNumber:
                    if char == '/':
                        flag1 = True

                if flag1 == False:

                    flag2 = False
                    for char in coursePrefix:
                        if char == '/':
                            flag2 = True

                    if flag2 == False:
                        courseName = coursePrefix + ' ' + courseNumber
                        break
                    else:
                        coursePrefixes = coursePrefix.split('/')
                        coursePrefix1 = coursePrefixes[0]
                        coursePrefix2 = coursePrefixes[1]
                        courseName = coursePrefix1 + ' ' + courseNumber + '/' + coursePrefix2 + ' ' + courseNumber
                        break

                else:
                    course1Prefix = rowModified5[j].split('"')[1]
                    course1Number = rowModified5[j + 1].split('/')[0]
                    course2Prefix = rowModified5[j + 1].split('/')[1]
                    course2Number = rowModified5[j + 2].split('"')[0]
                    courseName = course1Prefix + ' ' + course1Number + '/' + course2Prefix + ' ' + course2Number
                    break

        if flagx == False:
            coursePrefix = rowModified5[4].split('>')[1]
            courseNumber = rowModified5[5].split('<')[0]

            flag1 = False
            for char in courseNumber:
                if char == '/':
                    flag1 = True

            if flag1 == False:

                flag2 = False
                for char in coursePrefix:
                    if char == '/':
                        flag2 = True

                if flag2 == False:
                    courseName = coursePrefix + ' ' + courseNumber
                else:
                    coursePrefixes = coursePrefix.split('/')
                    coursePrefix1 = coursePrefixes[0]
                    coursePrefix2 = coursePrefixes[1]
                    courseName = coursePrefix1 + ' ' + courseNumber + '/' + coursePrefix2 + ' ' + courseNumber

            else:
                course1Prefix = rowModified5[j].split('"')[1]
                course1Number = rowModified5[j + 1].split('/')[0]
                course2Prefix = rowModified5[j + 1].split('/')[1]
                course2Number = rowModified5[j + 2].split('"')[0]
                courseName = course1Prefix + ' ' + course1Number + '/' + course2Prefix + ' ' + course2Number

        if k == i + 1:
            RequiredClasses = RequiredClasses + "." + courseName
        else:
            RequiredClasses = RequiredClasses + "*" + courseName

        k = k + 1

    minor.requirements.append(RequiredClasses)
    return k


# Parse sentence of the following structure:
# 'Select x credits of the following:'
def parseSentence3(rows, rowModified3, i, minor: Minor):
    if rowModified3[1].lower() not in numbers.keys():
        numberOfCredits = int(rowModified3[1])
    else:
        numberOfCreditsString = rowModified3[1].lower()
        numberOfCredits = numbers[numberOfCreditsString]

    RequiredClasses = "(" + str(numberOfCredits) + ")"

    k = i + 1
    while k < len(rows):
        rowModified4 = str(rows[k]).split('"')
        if "courselistcomment" in rowModified4 or "courselistcomment commentindent" in rowModified4:
            break

        rowModified5 = str(rows[k]).split()

        flagx = False       # if flagx == True, that means the structure of the HTML code includes 'title'

        for j in range(len(rowModified5)):
            if rowModified5[j].startswith('title'):
                flagx = True

                coursePrefix = rowModified5[j].split('"')[1]
                courseNumber = rowModified5[j + 1].split('"')[0]

                flag = False
                for char in coursePrefix:
                    if char == '/':
                        flag = True

                if flag == False:
                    courseName = coursePrefix + ' ' + courseNumber
                    break

                else:
                    coursePrefixes = coursePrefix.split('/')
                    coursePrefix1 = coursePrefixes[0]
                    coursePrefix2 = coursePrefixes[1]
                    courseName = coursePrefix1 + ' ' + courseNumber + '/' + coursePrefix2 + ' ' + courseNumber
                    break

        if flagx == False:
            coursePrefix = rowModified5[4].split('>')[1]
            courseNumber = rowModified5[5].split('<')[0]

            flag = False
            for char in coursePrefix:
                if char == '/':
                    flag = True

            if flag == False:
                courseName = coursePrefix + ' ' + courseNumber

            else:
                coursePrefixes = coursePrefix.split('/')
                coursePrefix1 = coursePrefixes[0]
                coursePrefix2 = coursePrefixes[1]
                courseName = coursePrefix1 + ' ' + courseNumber + '/' + coursePrefix2 + ' ' + courseNumber


        if k == i + 1:
            RequiredClasses = RequiredClasses + "." + courseName
        else:
            RequiredClasses = RequiredClasses + "*" + courseName

        k = k + 1

    minor.requirements.append(RequiredClasses)
    return k


# Parse sentence of the following structure:
# 'Select x of the following:'
# 'Select x courses from the following list:'
def parseSentence4(rows, rowModified3, i, minor: Minor):
    if rowModified3[1].lower() not in numbers.keys():
        numberOfCourses = int(rowModified3[1])
    else:
        numberOfCoursesString = rowModified3[1].lower()
        numberOfCourses = numbers[numberOfCoursesString]

    RequiredClasses = str(numberOfCourses)

    k = i + 1
    while k < len(rows):
        rowModified4 = str(rows[k]).split('"')
        if "courselistcomment" in rowModified4:
            break

        rowModified5 = str(rows[k]).split()

        flagx = False           # if flagx == True, that means the structure of the HTML code includes 'title'

        for j in range(len(rowModified5)):
            if rowModified5[j].startswith('title'):
                flagx = True

                coursePrefix = rowModified5[j].split('"')[1]
                courseNumber = rowModified5[j + 1].split('"')[0]

                flag = False
                for char in coursePrefix:
                    if char == '/':
                        flag = True

                if flag == False:
                    courseName = coursePrefix + ' ' + courseNumber
                    break

                else:
                    coursePrefixes = coursePrefix.split('/')
                    coursePrefix1 = coursePrefixes[0]
                    coursePrefix2 = coursePrefixes[1]
                    courseName = coursePrefix1 + ' ' + courseNumber + '/' + coursePrefix2 + ' ' + courseNumber
                    break

        if flagx == False:
            coursePrefix = rowModified5[4].split('>')[1]
            courseNumber = rowModified5[5].split('<')[0]

            flag = False
            for char in coursePrefix:
                if char == '/':
                    flag = True

            if flag == False:
                courseName = coursePrefix + ' ' + courseNumber

            else:
                coursePrefixes = coursePrefix.split('/')
                coursePrefix1 = coursePrefixes[0]
                coursePrefix2 = coursePrefixes[1]
                courseName = coursePrefix1 + ' ' + courseNumber + '/' + coursePrefix2 + ' ' + courseNumber

        if k == i + 1:
            RequiredClasses = RequiredClasses + "." + courseName
        else:
            RequiredClasses = RequiredClasses + "*" + courseName

        k = k + 1

    minor.requirements.append(RequiredClasses)
    return k


# Parse sentence of the following structure:
# 'Select x credits from any y course except z'
# 'Select x credits from the y z-x-range'
# for an example, see: ANTH minor
def parseSentence5(rows, rowModified3, i, minor: Minor):
    flag1 = False
    exceptCourseNumber = ''

    for i in range(0, len(rowModified3)):
        if rowModified3[i] == 'Select':
            credits = rowModified3[i + 1]
        if rowModified3[i].startswith('from'):
            subject = rowModified3[i + 2]
            if 'range' in rowModified3:
                lowerLevel = rowModified3[i + 3]
                upperLevel = rowModified3[i + 4]
                flag1 = True
        if rowModified3[i] == 'except':
            exceptCourse = str(rows[i]).split('"')[13]
            exceptCourseNumber = "*" + exceptCourse.split()[1]

    if flag1 == False:
        AdditionalClass1 = subject + ".1-499" + exceptCourseNumber + "." + credits
        minor.requirements.append(AdditionalClass1)
    elif flag1 == True:
        AdditionalClass1 = subject + "." + lowerLevel + "-" + upperLevel + "." + credits
        minor.requirements.append(AdditionalClass1)

    return i + 1


# ----------------------------------------------------------------------------------------------------------------------


# The following function parses minor's/certificate's webpage and stores their requirements
def parseRequirements(minor: Minor):
    # opening the webpage
    page = requests.get(minor.URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # extracting the table of requirements from the webpage
    table = soup.find("table", {"class": "sc_courselist"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')        # rows includes all the contents of the requirements table

    # going through each line of the table one by one
    i = 1
    while i < len(rows):
        rowModified1 = str(rows[i]).split('"')

        # The following block of code parses 'courselistcomments'
        # which are basic sentences describing requirements of a minor/certificate
        if 'courselistcomment' in rowModified1:
            # rowModified2 - extracting the sentence
            rowModified2 = str(rows[i]).split('>')[3].split('<')[0]

            # getting rid of unwanted characters
            for char in rowModified2:
                if char in "?.!/;:":
                    rowModified2 = rowModified2.replace(char, '')
                if char == '-':
                    rowModified2 = rowModified2.replace(char, ' ')

            rowModified3 = rowModified2.split()

            # Parse sentence of the following structure:
            # 'Select x credits in y'
            # or 'Select x credits of y courses'
            # or 'Select x credits of y-level z courses'
            # or 'Select x credits (at least n credits at the m level) in y'
            # or 'at least x credits must be at the y level'
            # for an example, see: PSYCH, SOC, HDFS, etc.
            if ('in' in rowModified3) or ('of' in rowModified3 and 'courses' in rowModified3):
                k = parseSentence1(rows, rowModified3, i, minor)
                i = k

            # Parse sentence of the following structure:
            # 'In addition to the x credits of coursework listed, students may choose any y (z credits) of the following:'
            elif ('addition' in rowModified3) and ('following' in rowModified3):
                k = parseSentence2(rows, rowModified3, i, minor)
                i = k

            # Parse sentence of the following structure:
            # 'Select x credits of the following:'
            elif ('credits' in rowModified3) and ('following' in rowModified3):
                k = parseSentence3(rows, rowModified3, i, minor)
                i = k

            # Parse sentence of the following structure:
            # 'Select x of the following:'
            # 'Select x courses from the following list:'
            elif ('Select' in rowModified3) and ('following' in rowModified3):
                k = parseSentence4(rows, rowModified3, i, minor)
                i = k

            # Parse sentence of the following structure:
            # 'Select x credits from any y course except z'
            # 'Select x credits from the y z-range'
            # for an example, see: ANTH minor
            elif ('Select' in rowModified3) and ('from' in rowModified3):
                k = parseSentence5(rows, rowModified3, i, minor)
                i = k

        else:
            rowModified2 = str(rows[i]).split()

            # The following block of code parses two lines of the list at the same time, when
            # the lines are connected to each other using 'or'
            if (i < len(rows) - 2):
                nextRow = str(rows[i + 1]).split('"')
                if nextRow[1].startswith('orclass'):

                    flagx = False           # If flagx == True, that means the HTML structure of the sentence includes 'title'

                    for j in range(len(rowModified2)):
                        if rowModified2[j].startswith('title'):
                            flagx = True

                            course1Prefix = rowModified2[j].split('"')[1]
                            course1Number = rowModified2[j + 1].split('"')[0]

                            flag = False
                            for char in course1Prefix:
                                if char == '/':
                                    flag = True

                            if flag == False:
                                course1Name = course1Prefix + ' ' + course1Number
                                break

                            else:
                                coursePrefixes = course1Prefix.split('/')
                                coursePrefix1 = coursePrefixes[0]
                                coursePrefix2 = coursePrefixes[1]
                                course1Name = coursePrefix1 + ' ' + course1Number + '/' + coursePrefix2 + ' ' + course1Number
                                break

                    if flagx == False:
                        course1Prefix = rowModified2[4].split('>')[1]
                        course1Number = rowModified2[5].split('<')[0]

                        flag = False
                        for char in course1Prefix:
                            if char == '/':
                                flag = True

                        if flag == False:
                            course1Name = course1Prefix + ' ' + course1Number

                        else:
                            coursePrefixes = course1Prefix.split('/')
                            coursePrefix1 = coursePrefixes[0]
                            coursePrefix2 = coursePrefixes[1]
                            course1Name = coursePrefix1 + ' ' + course1Number + '/' + coursePrefix2 + ' ' + course1Number

                    nextRowModified = str(rows[i + 1]).split()


                    flagx = False       # If flagx == True, that means the HTML structure of the sentence includes 'title'

                    for m in range(len(nextRowModified)):
                        if nextRowModified[m].startswith('title'):
                            flagx = True

                            course2Prefix = nextRowModified[m].split('"')[1]
                            course2Number = nextRowModified[m + 1].split('"')[0]

                            flag = False
                            for char in course2Prefix:
                                if char == '/':
                                    flag = True

                            if flag == False:
                                course2Name = course2Prefix + ' ' + course2Number
                                break

                            else:
                                coursePrefixes = course2Prefix.split('/')
                                coursePrefix1 = coursePrefixes[0]
                                coursePrefix2 = coursePrefixes[1]
                                course2Name = coursePrefix1 + ' ' + course2Number + '/' + coursePrefix2 + ' ' + course2Number
                                break

                    if flagx == False:
                        course2Prefix = nextRowModified[4].split('>')[1]
                        course2Number = nextRowModified[5].split('<')[0]

                        flag = False
                        for char in course2Prefix:
                            if char == '/':
                                flag = True

                        if flag == False:
                            course2Name = course2Prefix + ' ' + course2Number

                        else:
                            coursePrefixes = course2Prefix.split('/')
                            coursePrefix1 = coursePrefixes[0]
                            coursePrefix2 = coursePrefixes[1]
                            course2Name = coursePrefix1 + ' ' + course2Number + '/' + coursePrefix2 + ' ' + course2Number

                    RequiredClass = "1." + course1Name + "*" + course2Name
                    minor.requirements.append(RequiredClass)
                    i = i + 2
                    continue

            # The following block of code parses requirements that are easiest to understand
            # This includes requirements that follow the following structure:
            # 'coursePrefix courseNumber'   example: PSYCH 100
            # 'coursePrefix1/coursePrefix2 courseNumber'   example: PSYCH/SOC 450
            flagx = False       # If flagx == True, that means the HTML structure of the sentence includes 'title'

            for j in range(len(rowModified2)):
                if rowModified2[j].startswith('title'):
                    flagx = True

                    coursePrefix = rowModified2[j].split('"')[1]
                    courseNumber = rowModified2[j + 1].split('"')[0]

                    flag = False
                    for char in coursePrefix:
                        if char == '/':
                            flag = True

                    if flag == False:
                        courseName = coursePrefix + ' ' + courseNumber
                        minor.requirements.append(courseName)
                        break

                    else:
                        coursePrefixes = coursePrefix.split('/')
                        coursePrefix1 = coursePrefixes[0]
                        coursePrefix2 = coursePrefixes[1]
                        courseName = coursePrefix1 + ' ' + courseNumber + '/' + coursePrefix2 + ' ' + courseNumber
                        minor.requirements.append(courseName)
                        break

            # If the requirement is written in a non-conventional way - without 'title'
            if (flagx == False) and ('courselistcomment areasubheader undefined' not in rowModified1) and ('courselistcomment areaheader' not in rowModified1) and ('courselistcomment commentindent' not in rowModified1):
                coursePrefix = rowModified2[4].split('>')[1]
                courseNumber = rowModified2[5].split('<')[0]

                flag = False
                for char in coursePrefix:
                    if char == '/':
                        flag = True

                if flag == False:
                    courseName = coursePrefix + ' ' + courseNumber
                    minor.requirements.append(courseName)

                else:
                    coursePrefixes = coursePrefix.split('/')
                    coursePrefix1 = coursePrefixes[0]
                    coursePrefix2 = coursePrefixes[1]
                    courseName = coursePrefix1 + ' ' + courseNumber + '/' + coursePrefix2 + ' ' + courseNumber
                    minor.requirements.append(courseName)

            i = i + 1


# ----------------------------------------------------------------------------------------------------------------------


# The following function writes all the minors/certificates and their requirements to .csv file
def WriteRequirementsToCSVFile(minorsAndCertificates):
    # create a list that stores all the names and requirements of each minor and certificate
    namesAndRequirements = []

    # parsing the requirements for each minor and certificate
    # using the parseRequirements() function
    for i in range(len(minorsAndCertificates)):
        parseRequirements(minorsAndCertificates[i])

        # adding each minor's and certificate's name and requirements to namesAndRequirements list
        info = []
        info.append(minorsAndCertificates[i].name)
        info.extend(minorsAndCertificates[i].requirements)
        namesAndRequirements.append(info)

    # open the csv file in the write mode
    with open('MinorCertificateRequirements.csv', 'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        # writing contents of namesAndRequirements line by line to the .csv file
        for k in range(len(namesAndRequirements)):
            writer.writerow(namesAndRequirements[k])


# ----------------------------------------------------------------------------------------------------------------------

# Creating objects for each minor and certificate and running the WriteRequirementsToSCVFile() function

minorsAndCertificates = []

PSYCHMinor = Minor("PSYCH Minor", "https://bulletins.psu.edu/undergraduate/colleges/liberal-arts/psychology-minor/#programrequirementstext")
minorsAndCertificates.append(PSYCHMinor)

SOCMinor = Minor("SOC Minor", "https://bulletins.psu.edu/undergraduate/colleges/liberal-arts/sociology-minor/#programrequirementstext")
minorsAndCertificates.append(SOCMinor)

HDFSMinor = Minor("HDFS Minor", "https://bulletins.psu.edu/undergraduate/colleges/health-human-development/human-development-family-studies-minor/#programrequirementstext")
minorsAndCertificates.append(HDFSMinor)

ANTHMinor = Minor("ANTH Minor", "https://bulletins.psu.edu/undergraduate/colleges/liberal-arts/anthropology-minor/#programrequirementstext")
minorsAndCertificates.append(ANTHMinor)

BHCPCertificate = Minor("BHCP Certificate", "https://bulletins.psu.edu/undergraduate/colleges/behrend/behavioral-health-counseling-psychology-certificate/#programrequirementstext")
minorsAndCertificates.append(BHCPCertificate)

CDPCCertificate = Minor("CDPC Certificate", "https://bulletins.psu.edu/undergraduate/colleges/abington/chemical-dependency-prevention-counseling-certificate/#programrequirementstext")
minorsAndCertificates.append(CDPCCertificate)

CDCertificate = Minor("CD Certificate", "https://bulletins.psu.edu/undergraduate/colleges/behrend/child-development-certificate/#programrequirementstext")
minorsAndCertificates.append(CDCertificate)

CYFSCertificate = Minor("CYFS Certificate", "https://bulletins.psu.edu/undergraduate/colleges/health-human-development/children-youth-family-services-certificate/#programrequirementstext")
minorsAndCertificates.append(CYFSCertificate)

# CPPP Certificate ????

DSCertificate = Minor("DS Certificate", "https://bulletins.psu.edu/undergraduate/colleges/liberal-arts/diversity-studies-certificate/#programrequirementstext")
minorsAndCertificates.append(DSCertificate)

MSCertificate = Minor("MS Certificate", "https://bulletins.psu.edu/undergraduate/colleges/arts-architecture/museum-studies-certificate/#programrequirementstext")
minorsAndCertificates.append(MSCertificate)

SGCCCertificate = Minor("SGCC Certificate", "https://bulletins.psu.edu/undergraduate/colleges/liberal-arts/small-group-conflict-collaboration-certificate/#programrequirementstext")
minorsAndCertificates.append(SGCCCertificate)

SJCertificate = Minor("SJ Certificate", "https://bulletins.psu.edu/undergraduate/colleges/berks/social-justice-certificate/#programrequirementstext")
minorsAndCertificates.append(SJCertificate)

TSCertificate = Minor("TS Certificate", "https://bulletins.psu.edu/undergraduate/colleges/behrend/trauma-studies-certificate/#programrequirementstext")
minorsAndCertificates.append(TSCertificate)

YDSJCertificate = Minor("YDSJ Certificate", "https://bulletins.psu.edu/undergraduate/colleges/university-college/youth-development-social-justice-certificate/#programrequirementstext")
minorsAndCertificates.append(YDSJCertificate)


WriteRequirementsToCSVFile(minorsAndCertificates)