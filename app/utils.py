import cloudinary
import cloudinary.uploader
from app.config import Config

cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

def upload_to_cloudinary(file):
    try:
        upload_result = cloudinary.uploader.upload(file)
        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None
