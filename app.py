from werkzeug.utils import secure_filename
import uuid
from utils.enhancer import enhance_image
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part"
        
        file = request.files['image']
        if file.filename == '':
            return "No selected file"
        
        # Sanitize filename
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]  # short random ID

        # Generate safe filenames
        original_filename = f"{unique_id}_{filename}"
        enhanced_filename = f"enhanced_{original_filename}"

        # Paths
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        enhanced_path = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_filename)

        # Save & enhance
        file.save(filepath)
        enhance_image(filepath, enhanced_path)

        # Redirect
        return redirect(url_for('result', filename=original_filename, enhanced=enhanced_filename))

    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    enhanced = request.args.get('enhanced')
    return render_template('result.html', filename=filename, enhanced=enhanced)

if __name__ == '__main__':
    app.run(debug=True)
