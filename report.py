
from database import connect_db


def get_today_attendance():
    """ดึงรายชื่อผู้เข้าเรียนของวันนี้"""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                s.student_id,
                s.student_name,
                s.class_name,
                a.attendance_date,
                a.checkin_time,
                a.status
            FROM attendance AS a
            JOIN students AS s
                ON a.student_id = s.student_id
            WHERE a.attendance_date = CURDATE()
            ORDER BY a.checkin_time
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_attendance_summary():
    """สรุปจำนวนผู้มาเรียนวันนี้"""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM students)
                    AS total_students,
                (SELECT COUNT(*)
                 FROM attendance
                 WHERE attendance_date = CURDATE())
                    AS present_students
            """
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

