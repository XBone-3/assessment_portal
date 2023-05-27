from enum import Enum


class Options(Enum):
    ADD = "A"
    SEARCH = "S"
    INSERT = "I"
    QUIT = "Q"
    YES = "Y"
    NO = "N"


def file_availability_check():
    try:
        students = open(f"{students_text}", "a")
        assessments = open(f"{assessments_text}", "a")
    except Exception as e:
        print(f"file does not exist or problem while creating files: {e}")
        return False
    finally:
        students.close()
        assessments.close()
    return True


def add_student(students, student_info):
    with open(f"{students_text}", "r") as existing_students:
        students_list = existing_students.readlines()
        for student in students_list:
            s_id = student.split("\t")[0]
            if s_id == student_id:
                print("Student already exists in the database")
                return 0
    students.write('\t'.join(student_info.values()) + '\n')
    print("The details of the students you entered are as follows:")
    for key, value in student_info.items():
        print(f"{key} : {value}")
    print(f"The record has been successfully added to the {students_text} file.")
    return 1


def insert_marks(assessments, student_id):
    with open(f"{students_text}", "r") as existing_students:
        students_list = existing_students.readlines()
        student_ids = []
        for student in students_list:
            s_id = student.split("\t")[0]
            student_ids.append(s_id)
        if student_id not in student_ids:
            return 0
    while True:
        subject_code = input(f"{common_request_string} subject code: ")
        assessment_number = input(f"{common_request_string} assessment number: ")
        marks = input(f"{common_request_string} marks: ")
        assessment_info = {
            "subject_code": subject_code,
            "assessment_number": assessment_number,
            "marks": marks,
        }
        assessments.write(student_id + '\t' + '\t'.join(assessment_info.values()) + '\n')
        print("The details of the student you entered are as follows:")
        for key, value in assessment_info.items():
            print(f"{key} : {value}")
        print(f"The record has been successfully added to the {assessments_text} file.")
        new_record = input(
            "Do you want to enter marks for another assessment (Y/N)?\n= "
        )
        if Options(new_record.capitalize()) == Options.NO:
            break
    return 1


def search_marks(students, assessments, student_id):
    student_list = students.readlines()
    assessments_list = assessments.readlines()
    student_info = dict()
    assessments_info = list()
    for student in student_list:
        s_id = student.split("\t")[0]
        if s_id == student_id:
            student_info["Student ID"] = s_id
            student_info["Student Name"] = student.split("\t")[1]
            student_info["Course"] = student.split("\t")[2].split('\n')[0]
    if len(student_info.keys()) == 0:
        return student_info, assessments_info
    for assessment in assessments_list:
        assessment_split = assessment.split("\t")
        assessment_dict = dict()
        if assessment_split[0] == student_id:
            assessment_dict["Subject Code"] = assessment_split[1]
            assessment_dict["Assessment Number"] = assessment_split[2]
            assessment_dict["Marks"] = assessment_split[3].split('\n')[0]
            assessments_info.append(assessment_dict)
    return student_info, assessments_info


if __name__ == "__main__":
    QUIT = False
    OPTIONS = [
        "Welcome to the student and Assessment management system.",
        "<ADD> Enter A to add details of student.",
        "<INSERT> Enter I to insert assignmentt marks of student.",
        "<SEARCH> Enter S to Search assessment marks for a student.",
        "<QUIT> Enter Q to quit"
    ]
    common_request_string = "Please enter the"
    students_text = "students.txt"
    assessments_text = "assessments.txt"
    assessment_number = "Assessment Number"
    subject_code = "Subject Code"
    available = file_availability_check()
    if available:
        while not QUIT:
            print("=" * (len(max(OPTIONS)) + 5))
            for option in OPTIONS:
                print(option)
            print("=" * (len(max(OPTIONS)) + 5))
            user_input = input("Enter operation: ")
            if Options(user_input.capitalize()) == Options.QUIT:
                QUIT = True
                print("Thank You!")
            elif Options(user_input.capitalize()) == Options.ADD:
                while True:
                    student_id = input(f"{common_request_string} student ID: ")
                    student_name = input(f"{common_request_string} student name: ")
                    course = input(f"{common_request_string} course: ")
                    print("Thank You!")
                    student_info = {
                        "student_id": student_id,
                        "student_name": student_name,
                        "course": course,
                    }
                    with open(f"{students_text}", "a") as students:
                        status = add_student(students, student_info)
                    new_record = input(
                        "Do you want to enter details for another student (Y/N)?\n= "
                    )
                    if Options(new_record.capitalize()) == Options.NO:
                        break
            elif Options(user_input.capitalize()) == Options.INSERT:
                student_id = input(f"{common_request_string} student ID: ")
                with open(f"{assessments_text}", "a") as assessments:
                    status = insert_marks(assessments, student_id)
            elif Options(user_input.capitalize()) == Options.SEARCH:
                while True:
                    student_id = input(f"{common_request_string} student ID: ")
                    with open(f"{students_text}", "r") as students, open(f"{assessments_text}", "r") as assessments:
                        student_info, assessments_info = search_marks(students, assessments, student_id)
                    for key, value in student_info.items():
                        print(f"{key} : {value}")
                    print("Subject Code\tAssessment Number\tMarks")
                    for item in assessments_info:
                        print(
                            item[subject_code]
                            + " " * (len(subject_code) - len(item[subject_code]))
                            + "\t"
                            + item[assessment_number]
                            + " "
                            * (len(assessment_number) - len(item[assessment_number]))
                            + "\t"
                            + item["Marks"]
                        )
                    new_search = input(
                        "Do you want to search assessment marks for another student (Y/N)?\n= "
                    )
                    if Options(new_search.capitalize()) == Options.NO:
                        break
            else:
                print("Please provide input for available operation")
