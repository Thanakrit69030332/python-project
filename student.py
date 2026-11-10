import os
import qrcode

from database import connect_db


def add_student(student_id, student_name, class_name):
    """เพิ่มข้อมูลนักเรียน"""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students
                (student_id, student_name, class_name)
            VALUES (%s, %s, %s)
            """,
            (student_id, student_name, class_name)
        )
        conn.commit()
        return True, "เพิ่มข้อมูลนักเรียนสำเร็จ"

    except Exception as error:
        conn.rollback()
        return False, f"เพิ่มข้อมูลไม่สำเร็จ: {error}"

    finally:
        cursor.close()
        conn.close()


def find_student(student_id):
    """ค้นหานักเรียนจากรหัส"""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT student_id, student_name, class_name
            FROM students
            WHERE student_id = %s
            """,
            (student_id,)
        )
        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def get_all_students():
    """ดึงข้อมูลนักเรียนทั้งหมด"""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT student_id, student_name, class_name
            FROM students
            ORDER BY student_id
            """
        )
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def generate_student_qr(student_id):
    """สร้าง QR Code ที่เก็บเฉพาะรหัสนักเรียน"""
    os.makedirs("qrcodes", exist_ok=True)

    image = qrcode.make(str(student_id))
    file_path = os.path.join(
        "qrcodes", f"{student_id}.png"
    )
    image.save(file_path)

    return file_path
