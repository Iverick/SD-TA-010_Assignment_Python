import csv
from datetime import date

def main():
    assessmentResultsPath = "input_files/Assessment_Results.csv"
    industryCertPath = "input_files/Industry_Cert_Results.csv"
    outputFolder = "output_files"
    '''
    assessmentResults supposed to have this structure:
    {studentName: {'grades': {courseName: 'PASS/FAIL'}, 'cloudCert': 'PASS', 'optionCert': 'PASS', 'overallScore': 'PASS'}, ...}
    '''
    assessmentResults = {}

    # NOTE: Remove from the final build
    # readAssessmentResults(assessmentResultsPath, assessmentResults)
    # readIndustryCerts(industryCertPath, assessmentResults)
    # calculateOverallScore(assessmentResults)
    # # For every student generate an output txt file
    # for studentName in assessmentResults:
    #     generateTxtResult(assessmentResults[studentName], studentName, outputFolder)


    try:
        readAssessmentResults(assessmentResultsPath, assessmentResults)
        readIndustryCerts(industryCertPath, assessmentResults)
        calculateOverallScore(assessmentResults)
        # For every student generate an output txt file
        for studentName in assessmentResults:
            generateTxtResult(assessmentResults[studentName], studentName, outputFolder)
        print("Generated all reports!")
    except Exception as e:
        print("Error in program execution: ", e)
    finally:
        print("Program finished!")


'''
Reads data from assessmentResults file with provided path and stores them into a assessmentResults dict

return updated assessmentResults
'''
def readAssessmentResults(filePath, assessmentResults):
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
    rows = []
    # Open an input file and transform each line into a list
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            rows.append(line)

    # I need to get student name and list of scores for every student
    for row in rows[2:]:
        studentGrades = {}
        # skip empty rows
        if not row[0]:
            continue

        studentName = row[0].strip()
        for i in range(len(courseNames)):
            # convert each grade into PASS or FAIL and store it to the corresponding courseName
            courseName = courseNames[i]
            grade = row [i + 1]
            studentGrades[courseName] = 'PASS' if int(grade) >= PASS_MARK else 'FAIL'

        assessmentResults[studentName] = {
            'grades': studentGrades,
            'cloudCert': None,
            'optionCert': None,
            'overallScore': None
        }
    return assessmentResults


'''
Reads data from Industry_Cert file with provided path and updates corresponding 'cloudCert' and 'optionCert' values in assessmentResults

returns assessmentResults dict
'''
def readIndustryCerts(filePath, assessmentResults):
    rows = []
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            rows.append(line)

    # Read rows from the file
    # Name is the first col, cloudCert date is the second, optionCert is a one of the following columns
    for row in rows[2:]:
        name = row[0]
        studentResults = assessmentResults[name]
        cloudCert = 'PASS' if hasPassedCert(row[1]) else 'FAIL'
        optionCert = 'FAIL'
        for col in row[2:]:
            if hasPassedCert(col):
                optionCert = 'PASS'
                break

        studentResults['cloudCert'] = cloudCert
        studentResults['optionCert'] = optionCert
    return assessmentResults


'''
Method loops through all provided assessment scores for every student in assessmentResults dict and uses their values to calculate overallScore 
'''
def calculateOverallScore(assessmentResults):
    for studentName in assessmentResults:
        studentGrades = assessmentResults[studentName]
        # Overall scores is 'PASS' only when every assessment result is 'PASS'
        if 'FAIL' in studentGrades['grades'].values() or studentGrades['cloudCert'] == 'FAIL' or studentGrades['optionCert'] == 'FAIL':
            studentGrades['overallScore'] = 'FAIL'
        else:
            studentGrades['overallScore'] = 'PASS'
    return assessmentResults


'''
Method formats student results data in a readable way, adds data into an output file and saves the file in the output folder
'''
def generateTxtResult(studentResults, name, outputFolder):
    generationDate = date.today().strftime("%d/%m/%Y")

    lines = []
    lines.append("=" * 90)
    lines.append("Summary Results \n")
    lines.append(f"{'Student Name':<65} | {name}")
    lines.append(f"{'Date Generated':<65} | {generationDate}")
    lines.append("=" * 90)
    lines.append("Assessment Results")
    lines.append("-" * 90)

    for moduleName, result in studentResults['grades'].items():
        lines.append(f"{moduleName:<65} | {result}")

    lines.append("=" * 90)
    lines.append("Industry Certification Results")
    lines.append("-" * 90)
    lines.append(f"{'Introduction to Cloud Development':<65} | {studentResults['cloudCert']}")
    lines.append(f"{'Option Certification':<65} | {studentResults['optionCert']}")
    lines.append("=" * 90)
    lines.append(f"{'Overall Result':<65} | {studentResults['overallScore']}")
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

# Launch program execution
main()
