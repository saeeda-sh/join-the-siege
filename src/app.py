from flask import request, jsonify

from src.tasks import flask_app, classify_file_task


ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "txt", "xlsx", "docx", "csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@flask_app.route("/classify_file", methods=["POST"])
def classify_file_route() -> dict[str, object]:
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_bytes = file.read()
    filename = file.filename

    task = classify_file_task.delay(file_bytes, filename)

    return jsonify({"task_id": task.id}), 200


@flask_app.route("/get_classification_result/<task_id>", methods=["GET"])
def get_classification_result(task_id) -> dict[str, object]:
    task = classify_file_task.AsyncResult(task_id)

    if task.state == "PENDING":
        return jsonify({"status": "processing"}), 202
    elif task.state == "SUCCESS":
        return jsonify({"file_class": task.result}), 200
    elif task.state == "FAILURE":
        return jsonify({"status": "failed", "error": str(task.info)}), 500


if __name__ == "__main__":
    flask_app.run(debug=True)
