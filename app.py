from werkzeug.utils import secure_filename
import uuid
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from utils.enhancer import enhance_image
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for sessions
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to cleanup old files
def cleanup_old_files(folder, age_limit=7 * 24 * 60 * 60):
    current_time = time.time()
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            if current_time - os.path.getctime(file_path) > age_limit:
                os.remove(file_path)
                print(f"Deleted {filename} as it's older than {age_limit / 3600} hours.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        brightness = float(request.form.get('brightness', 2.5))  # Default to 2.5
        if 'image' not in request.files:
            flash("No file part.")
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash("No selected file.")
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash("Unsupported file type. Please upload an image.")
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        original_filename = f"{unique_id}_{filename}"
        enhanced_filename = f"enhanced_{original_filename}"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        enhanced_path = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_filename)

        file.save(filepath)
        enhance_image(filepath, enhanced_path, brightness)

        return redirect(url_for('result', filename=original_filename, enhanced=enhanced_filename))

    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    enhanced = request.args.get('enhanced')
    return render_template('result.html', filename=filename, enhanced=enhanced)

# Cleanup old files on startup
cleanup_old_files(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    app.run(debug=True)
