import os
from flask import Flask, render_template, jsonify, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from random import randint

UPLOAD_FOLDER = 'input'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__,
            static_folder="../frontend/dist/static",
            template_folder="../frontend/dist")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/send-file', methods=['POST'])
def save_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            response = {'error': 'No file detected'}
            return jsonify(response)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            response = {'error': 'No file detected'}
            return jsonify(response)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'OK': 'saved'})

        return jsonify({'error': 'not allowed'})

    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/api/get/<path:filename>')
def get_picture(filename):
    if allowed_file(filename) and os.path.isfile(filename):
        return send_file(
            '../input/' + filename,
            mimetype='image/gif'
        )
    else:
        return jsonify({'error': 'not such file'})


if __name__ == '__main__':
    app.run(
        debug=True,
        threaded=True,
        port=8080,
        host='0.0.0.0'
    )
