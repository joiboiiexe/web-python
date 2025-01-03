from flask import Blueprint, request, render_template, flash, redirect, url_for
from app.utils import upload_to_cloudinary

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "images" not in request.files:
            flash("No file part")
            return redirect(request.url)

        uploaded_files = request.files.getlist("images")
        image_urls = []

        for file in uploaded_files:
            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)

            # Upload to Cloudinary
            upload_result = upload_to_cloudinary(file)
            if upload_result:
                image_urls.append(upload_result)

        flash("Images uploaded successfully!")
        return render_template("index.html", image_urls=image_urls)

    return render_template("index.html", image_urls=[])
