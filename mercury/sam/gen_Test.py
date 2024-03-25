
from generate_template import make_functions_group, make_yaml_return_str, make_yaml_start_str


def generate_template(env="Prod"):
    
    start_str = make_yaml_start_str(env=env)

    functions_str = ""
    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete"],
        tablename="User",
        table_id="", # it is str.lower(tablename) + "_id"
        code_base_path="User/USER_LAMBDAS",
        http_base_path="",
        env=env,
        extra_funcs=[]
    )

    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete"],
        tablename="Student",
        table_id="", # it is str.lower(tablename) + "_id"
        code_base_path="User/Student/STUDENT_LAMBDAS",
        http_base_path="/user/{user_id}",
        env=env,
        extra_funcs=[
            ("GetAllStudentsOfClass", "/course/{course_id}/students"),
            ("GetAllStudentsOfSection", "/course/{course_id}/section/{section_id}/students")
        ]
    )

    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete"],
        tablename="Staff",
        table_id="", # it is str.lower(tablename) + "_id"
        code_base_path="User/Staff/STAFF_LAMBDAS",
        http_base_path="/user/{user_id}",
        env=env,
        extra_funcs=[
            ("GetAllStaffOfDepartment", "/university/{university_id}/school/{school_id}/department/{department_id}/staff"),
            ("GetAllStaffOfClass", "/course/{course_id}/staff")
        ]
    )

    
    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete"],
        tablename="University",
        table_id="",
        code_base_path="University/UNIVERSITY_LAMBDAS",
        http_base_path="",
        env=env,
        extra_funcs=[

        ]     
    )

    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete"],
        tablename="School",
        table_id="",
        code_base_path="University/School/SCHOOL_LAMBDAS",
        http_base_path="/university/{university_id}",
        env=env,
        extra_funcs=[
            ("GetAllSchoolsOfUniversity", "/university/{university_id}/school") 
        ]     
    )

    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete"],
        tablename="Department",
        table_id="",
        code_base_path="University/School/Department/DEPARTMENT_LAMBDAS",
        http_base_path="/university/{university_id}/school/{school_id}",
        env=env,
        extra_funcs=[
            ("GetAllDepartmentsOfSchool", "/university/{university_id}/school/{school_id}/department") 
        ]     
    )
    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete"],
        tablename="Course",
        table_id="",
        code_base_path="Course/COURSE_LAMBDAS",
        http_base_path="",
        env=env,
        extra_funcs=[
            ("GetAllCoursesOfDepartment", "/university/{university_id}/school/{school_id}/department/{department_id}/courses"),
            ("GetAllCoursesOfSchool", "/university/{university_id}/school/{school_id}/courses"),
            ("GetAllCoursesOfUser", "/user/{user_id}/courses")        
        ]     
    )
    
    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete"],
        tablename="Section",
        table_id="",
        code_base_path="Course/Section/SECTION_LAMBDAS",
        http_base_path="course/{course_id}",
        env=env,
        extra_funcs=[
            ("GetAllSectionsOfCourse", "course/{course_id}/sections")       
        ]     
    )

    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete"],
        tablename="Assignment",
        table_id="",
        code_base_path="Course/Material/Assignment/ASSIGNMENT_LAMBDAS",
        http_base_path="course/{course_id}/material/assignment",
        env=env,
        extra_funcs=[
            ("GetAllAssignmentsOfClass", "course/{course_id}/material/assignment")       
        ]     
    )

    functions_str += "\n\n" + make_functions_group(
        actions=[], # We use OfAssignment in the Folders so its easier to use the extra funcs
        tablename="Submission",
        table_id="",
        code_base_path="Course/Material/Assignment/Submission/SUBMISSION_LAMBDAS",
        http_base_path="course/{course_id}/material/assignment/{assignment_id}/submission",
        env=env,
        extra_funcs=[
            ("GetAllSubmissionsOfAssignment",           "course/{course_id}/material/assignment/{assignment_id}/submission"),
            ("GetASubmissionOfAssignment",              "course/{course_id}/material/assignment/{assignment_id}/submission/{submission_id}"),   
            ("CreateSubmissionOfAssignment",            "course/{course_id}/material/assignment/{assignment_id}/submission"),
            ("ModifySubmissionOfAssignment",            "course/{course_id}/material/assignment/{assignment_id}/submission/{submission_id}"),
            ("DeleteSubmissionOfAssignment",            "course/{course_id}/material/assignment/{assignment_id}/submission/{submission_id}"),    
        ]     
    )

    functions_str += "\n\n" + make_functions_group(
        actions=[], # We use LectureSlides in the Folders so its easier to use the extra funcs
        tablename="Lecture",
        table_id="",
        code_base_path="Course/Material/Lecture/LECTURE_LAMBDAS",
        http_base_path="course/{course_id}/material/lecture",
        env=env,
        extra_funcs=[
            ("GetAllLectureSlidesOfClass", "course/{course_id}/material/lecture"),
            ("GetALectureSlides", "course/{course_id}/material/lecture/{lecture_id}"),   
            ("CreateLectureSlides", "course/{course_id}/material/lecture"),      
            ("ModifyLectureSlides", "course/{course_id}/material/lecture/{lecture_id}"),  
            ("DeleteLectureSlides", "course/{course_id}/material/lecture/{lecture_id}"),  
        ]     
    )


    functions_str += "\n\n" + make_functions_group(
        actions=["GetA","Create","Modify","Delete", "Upload"],
        tablename="Document",
        table_id="",
        code_base_path="Course/Document/DOCUMENT_LAMBDAS",
        http_base_path="course/{course_id}/document",
        env=env,
        extra_funcs=[
            ("GetAllDocuments", "course/{course_id}/document")       
        ]     
    )



    return_str = make_yaml_return_str(env=env)

    with open("/Users/haydenrothman/Desktop/TheBoard/Dashboard-all-in-one-main/Dashboard-All-In-One/api/DashboardDataAPISAM/template.yaml", "w") as text_file:
        text_file.write(start_str)
        text_file.write(functions_str)
        text_file.write(return_str)



generate_template(env="Dev")
