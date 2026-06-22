import csv

def main():
    assessmentResultsPath = "input_files/Assessment_Results.csv"
    industryCertPath = "input_files/Industry_Cert_Results.csv"
    outputFolder = "output_files"
        
    try:
        assessmentResults = readAssessmentResults(assessmentResultsPath)
        industryCerts = readIndustryCerts(industryCertPath)
        assessmentResults = mergeResults(assessmentResults, industryCerts)
        assessmentResults = calculateOverallScore(assessmentResults)
        # For every student generate an output txt file
        for studentResult in assessmentResults:
            generateTxtResult(studentResult, outputFolder)
    except:
        print("Error in program execution")
    finally:
        print("Generated all reports!")


'''
Reads data from assessmentResults file with provided path and converts them into a list

assessmentResults has the following structure:
[{studentName: {'grades': {'courseName': 'PASS/FAIL'}, 'cloudCert': None, 'optionCert': None}}, ...]
'''
def readAssessmentResults(filePath):
    assessmentResults = []
    PASS_MARK = 50
    courseNames = [
        'SD-TA-001 Software Development and Design Fundamentals',
        'SD-TA-002 Customer Support Provision for the ICT Professional',
        'SD-TA-003 Web Development',
        'SD-TA-004 Software Development Using SQL',
        'SD-TA-005 Data and Cyber Security',
        'SD-TA-006 Install, Configure and Upgrade ICT Software',
        'SD-TA-007 Object Oriented Programming - Python',
        'SD-TA-008 Project Management and Agile Systems of Work',
        'SD-TA-009 Event Driven Programming',
        'SD-TA-010 Procedural Programming - Python',
        'SD-TA-011 Quality Assurance and Software Testing',
        'SD-TA-012 Systems Development'
    ]
    # Open an input file and transform each line into a list
    with open(filePath, newline='') as csvfile:
        rows = csv.reader(csvfile)
        rowsList = list(rows)

    # I need to get student name and list of scores for every student
    for row in rowsList[2:]:
        # skip empty rows
        if not row[0]:
            continue
        studentName = row[0].strip()
        
        studentGrades = {}
        for i in range(len(courseNames)):
            # convert each grade into PASS or FAIL and store it to the corresponding courseName
            courseName = courseNames[i]
            grade = row [i + 1]
            studentGrades[courseName] = 'PASS' if int(grade) >= PASS_MARK else 'FAIL'
        studentResult = {
            studentName: {
                'grades': studentGrades,
                'cloudCert': None,
                'optionCert': None,
                'overallScore': None
            }
        }
        assessmentResults.append(studentResult)
    return assessmentResults


'''
Reads data from Industry_Cert file with provided path and converts them into a dict

assessmentResults has the following structure:
[{studentName: [{'cloudCert': 'PASS/FAIL'}, {'optionCert': 'PASS/FAIL'}]}]
'''
def readIndustryCerts(filePath):
    industryCerts = []
    with open(filePath, newline='') as csvfile:
        rows = csv.reader(csvfile)
        rowsList = list(rows)

    # Read rows from the file
    # Name is the first col, cloudCert date is the second, optionCert is a one of the following columns
    for row in rowsList[2:]:
        name = row[0]
        cloudCert = {
            'cloudCert': 'PASS' if hasPassedCert(row[1]) else 'FAIL'
        }
        optionCert = {'optionCert': 'FAIL'}

        for col in row[2:]:
            if hasPassedCert(col):
                optionCert = {'optionCert': 'PASS'}
                break
            
        studentOutput = {name: [cloudCert, optionCert]}
        industryCerts.append(studentOutput)
    return industryCerts


'''
Merges assessmentResults and industryCert data into a single list.
Uses student as a key for both passed list

returns:
[{studentName: {'grades': {'courseName': 'PASS/FAIL'}, 'cloudCert': Bool, 'optionCert': Bool}}, ...]
'''
def mergeResults(assessmentResults, industryCerts):
    for industryResult in industryCerts:
        name = list(industryResult.keys())[0]
        # For every assessmentResult, update corresponding 'cloudCert' and 'optionCert' values
        for assessmentResult in assessmentResults:
            if name in assessmentResult:
                assessmentResult[name]['cloudCert'] = industryResult[name][0]['cloudCert']
                assessmentResult[name]['optionCert'] = industryResult[name][1]['optionCert']
    return assessmentResults


'''
Method loops through all provided assessment scores in assessmentResults dict and uses their values to calculate overallScore 
'''
def calculateOverallScore(assessmentResults):
    for studentResult in assessmentResults:
        name = list(studentResult.keys())[0]
        student = studentResult[name]
        # Overall scores is 'PASS' only when every assessment result is 'PASS'
        if 'FAIL' in student['grades'].values() or student['cloudCert'] == 'FAIL' or student['optionCert'] == 'FAIL':
            student['overallScore'] = 'FAIL'
        else:
            student['overallScore'] = 'PASS'
    return assessmentResults


'''
Method formats student results data in a readable way, adds data into an output file and saves the file in the output folder
'''
def generateTxtResult(studentResult, outputFolder):
    name = list(studentResult.keys())[0]
    student = studentResult[name]

    lines = []
    lines.append("=" * 90)
    lines.append("Summary Results \n")
    lines.append(f"{'Student Name':<65} | {name}")
    lines.append("=" * 90)
    lines.append("Assessment Results")
    lines.append("-" * 90)

    for moduleName, result in student['grades'].items():
        lines.append(f"{moduleName:<65} | {result}")

    lines.append("=" * 90)
    lines.append("Industry Certification Results")
    lines.append("-" * 90)
    lines.append(f"{'Introduction to Cloud Development':<65} | {student['cloudCert']}")
    lines.append(f"{'Option Certification':<65} | {student['optionCert']}")
    lines.append("=" * 90)
    lines.append(f"{'Overall Result':<65} | {student['overallScore']}")
    lines.append("=" * 90)

    # Create a file add write lines list into it
    fileName = f"{outputFolder}/{name} - Summary of Results.txt"
    with open(fileName, "w") as f:
        f.write("\n".join(lines))

    print(f"Generated: {fileName}")


def hasPassedCert(certResult):
    # Check if passed certResult string is success of failure
    if certResult == 'FAIL' or certResult == '':
        return False
    return True

main()
