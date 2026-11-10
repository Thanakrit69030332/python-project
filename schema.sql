
CREATE DATABASE IF NOT EXISTS student_attendance
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE student_attendance;

CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(20) PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    class_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    attendance_date DATE NOT NULL,
    checkin_time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'มาเรียน',

    CONSTRAINT fk_attendance_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id),

    CONSTRAINT unique_student_daily
        UNIQUE (student_id, attendance_date)
);

INSERT IGNORE INTO students
    (student_id, student_name, class_name)
VALUES
    ('65001', 'สมชาย ใจดี', 'ม.1/1'),
    ('65002', 'สมหญิง รักเรียน', 'ม.1/1'),
    ('65003', 'สมศักดิ์ ตั้งใจ', 'ม.1/2');


