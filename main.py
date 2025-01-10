from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader
import os

# Configure Cloudinary credentials
cloudinary.config(
    cloud_name="dzv3xgdso",
    api_key="995211288265947",
    api_secret="0bJX7uz7v58psFHaP3qT6pukUyQ"
)

app = Flask(__name__)

# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Get the image URL sent from the frontend
        image_url = request.json['imageUrl']
        
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(image_url, folder="media", use_filename=True, unique_filename=False, upload_preset="joyboy")
        
        # Extract the URL from Cloudinary response
        cloudinary_url = response.get('url')
        
        return jsonify({
            'status': 'success',
            'message': 'Image uploaded successfully!',
            'imageUrl': cloudinary_url
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
