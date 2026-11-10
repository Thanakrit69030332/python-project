from datetime import datetime

from database import connect_db
from student import find_student


def check_in_student(student_id):
    """ตรวจสอบนักเรียนและบันทึกการเข้าเรียน"""

    student_id = str(student_id).strip()

    if not student_id:
        return False, "กรุณาระบุรหัสนักเรียน"

    try:
        student = find_student(student_id)

        if student is None:
            return False, "ไม่พบรหัสนักเรียนในระบบ"

        conn = connect_db()
        cursor = conn.cursor()

        try:
            now = datetime.now()

            cursor.execute(
                """
                INSERT INTO attendance
                    (student_id, attendance_date,
                     checkin_time, status)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    student_id,
                    now.date(),
                    now.time().replace(microsecond=0),
                    "มาเรียน"
                )
            )

            conn.commit()

            return True, (
                f"เช็กชื่อสำเร็จ: {student['student_name']} "
                f"เวลา {now.strftime('%H:%M:%S')}"
            )

        except Exception as error:
            conn.rollback()

            # รหัส 1062 หมายถึงข้อมูลซ้ำใน MySQL
            if getattr(error, "errno", None) == 1062:
                return False, "นักเรียนคนนี้เช็กชื่อวันนี้แล้ว"

            return False, f"บันทึกข้อมูลไม่สำเร็จ: {error}"

        finally:
            cursor.close()
            conn.close()

    except Exception as error:
        return False, f"ไม่สามารถเชื่อมต่อฐานข้อมูล: {error}"
