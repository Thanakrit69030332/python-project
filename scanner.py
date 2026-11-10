from flask import Flask, jsonify, render_template, request

from attendance import check_in_student
from report import get_today_attendance


def create_app():
    """สร้าง Flask application"""
    app = Flask(__name__)

    @app.route("/checkin")
    def checkin_page():
        return render_template("checkin.html")

    @app.route("/api/checkin", methods=["POST"])
    def api_checkin():
        data = request.get_json(silent=True) or {}
        student_id = data.get("student_id", "")

        if not isinstance(student_id, str):
            return jsonify({
                "success": False,
                "message": "รูปแบบรหัสนักเรียนไม่ถูกต้อง"
            }), 400

        success, message = check_in_student(student_id)

        return jsonify({
            "success": success,
            "message": message
        }), 200 if success else 400

    @app.route("/api/attendance")
    def api_attendance():
        try:
            records = get_today_attendance()

            for record in records:
                record["attendance_date"] = str(
                    record["attendance_date"]
                )
                record["checkin_time"] = str(
                    record["checkin_time"]
                )

            return jsonify(records)

        except Exception:
            app.logger.exception("Failed to load attendance")
            return jsonify({
                "error": "ไม่สามารถโหลดรายงานได้"
            }), 500

    return app
