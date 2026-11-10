
import mysql.connector


def connect_db():
    """สร้างการเชื่อมต่อกับ MySQL"""
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="A1234",
        database="student_attendance",
        charset="utf8mb4"
    )

