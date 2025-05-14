from app.services.student_service import StudentService
import app.models.attendance
import app.models.grade
import app.models.subject
import app.models.student

#StudentService.add_student("Michał", "Tomaszewski", "21370420690")
print(StudentService.get_student(4))
StudentService.edit_student(4, "El Roberto", "Lewandowski", "21212121212")
print(StudentService.get_student(4))
