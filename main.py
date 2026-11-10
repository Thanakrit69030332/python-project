
import socket
import threading
import tkinter as tk
import webbrowser

from tkinter import ttk, messagebox

from scanner import create_app
from student import add_student, generate_student_qr
from report import get_today_attendance, get_attendance_summary


def get_local_ip():
    """ค้นหา IP ของคอมพิวเตอร์ในเครือข่าย"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("192.0.2.1", 80))
        return sock.getsockname()[0]
    except OSError:
        return "ไม่พบ IP"
    finally:
        sock.close()


def add_student_action():
    """รับข้อมูลจากหน้าจอและเพิ่มนักเรียน"""
    student_id = id_entry.get().strip()
    student_name = name_entry.get().strip()
    class_name = class_entry.get().strip()

    if not student_id or not student_name or not class_name:
        messagebox.showwarning(
            "ข้อมูลไม่ครบ",
            "กรุณากรอกรหัส ชื่อ และห้องเรียน"
        )
        return

    success, message = add_student(
        student_id, student_name, class_name
    )

    if not success:
        messagebox.showerror("เพิ่มนักเรียน", message)
        return

    try:
        qr_path = generate_student_qr(student_id)
        messagebox.showinfo(
            "สำเร็จ",
            f"{message}\nสร้าง QR Code แล้วที่:\n{qr_path}"
        )
    except Exception as error:
        messagebox.showwarning(
            "เพิ่มนักเรียนสำเร็จ",
            f"{message}\nแต่สร้าง QR Code ไม่สำเร็จ: {error}"
        )

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)

    refresh_table()


def refresh_table():
    """โหลดข้อมูลการเข้าเรียนวันนี้มาแสดง"""
    try:
        records = get_today_attendance()
        summary = get_attendance_summary()

        for item in attendance_table.get_children():
            attendance_table.delete(item)

        for record in records:
            attendance_table.insert(
                "",
                tk.END,
                values=(
                    record["student_id"],
                    record["student_name"],
                    record["class_name"],
                    str(record["checkin_time"]),
                    record["status"]
                )
            )

        summary_label.config(
            text=(
                f"มาเรียน {summary['present_students']} คน "
                f"จากนักเรียนทั้งหมด {summary['total_students']} คน"
            )
        )
        status_label.config(text="เชื่อมต่อฐานข้อมูลสำเร็จ")

    except Exception:
        status_label.config(
            text="โหลดข้อมูลไม่ได้ กรุณาตรวจสอบ MySQL"
        )

    root.after(3000, refresh_table)


def open_checkin_page():
    """เปิดหน้าเช็กชื่อบนคอมพิวเตอร์"""
    webbrowser.open("http://127.0.0.1:5000/checkin")


def start_server():
    """เริ่ม Flask ใน Thread แยกจาก Tkinter"""
    app = create_app()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )


# ---------- สร้างหน้าต่างหลัก ----------



root = tk.Tk()
root.title("ระบบเช็กชื่อนักเรียน QR Code")
root.geometry("850x600")

title_label = ttk.Label(
    root,
    text="ระบบเช็กชื่อนักเรียนด้วย QR Code",
    font=("Tahoma", 18, "bold")
)
title_label.pack(pady=12)

form = ttk.LabelFrame(root, text="เพิ่มนักเรียน")
form.pack(fill="x", padx=15, pady=8)

ttk.Label(form, text="รหัสนักเรียน").grid(
    row=0, column=0, padx=5, pady=8
)
id_entry = ttk.Entry(form, width=18)
id_entry.grid(row=0, column=1, padx=5, pady=8)

ttk.Label(form, text="ชื่อ-นามสกุล").grid(
    row=0, column=2, padx=5, pady=8
)
name_entry = ttk.Entry(form, width=24)
name_entry.grid(row=0, column=3, padx=5, pady=8)

ttk.Label(form, text="ห้องเรียน").grid(
    row=1, column=0, padx=5, pady=8
)
class_entry = ttk.Entry(form, width=18)
class_entry.grid(row=1, column=1, padx=5, pady=8)

ttk.Button(
    form,
    text="เพิ่มนักเรียนและสร้าง QR",
    command=add_student_action
).grid(row=1, column=2, columnspan=2, padx=5, pady=8)

button_frame = ttk.Frame(root)
button_frame.pack(fill="x", padx=15, pady=8)

ttk.Button(
    button_frame,
    text="เปิดหน้าเช็กชื่อ",
    command=open_checkin_page
).pack(side="left", padx=5)

ip = get_local_ip()
ttk.Label(
    button_frame,
    text=f"URL สำหรับโทรศัพท์: http://{ip}:5000/checkin"
).pack(side="left", padx=8)

summary_label = ttk.Label(root, text="กำลังโหลดข้อมูล...")
summary_label.pack(pady=5)

columns = (
    "student_id",
    "student_name",
    "class_name",
    "checkin_time",
    "status"
)

attendance_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

headings = {
    "student_id": "รหัสนักเรียน",
    "student_name": "ชื่อ-นามสกุล",
    "class_name": "ห้องเรียน",
    "checkin_time": "เวลาเข้าเรียน",
    "status": "สถานะ"
}


for column in columns:
    attendance_table.heading(
        column, text=headings[column]
    )
    attendance_table.column(column, width=150)

attendance_table.pack(
    fill="both", expand=True, padx=15, pady=8
)

status_label = ttk.Label(root, text="กำลังเริ่มระบบ...")
status_label.pack(pady=5)

# เริ่ม Web Server โดยไม่บล็อกหน้าต่าง Tkinter
threading.Thread(
    target=start_server,
    daemon=True
).start()

root.after(1000, refresh_table)

root.mainloop()

