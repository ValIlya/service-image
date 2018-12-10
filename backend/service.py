import os
from flask import Flask, render_template, jsonify, request, send_file, g, Blueprint, make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS
from random import randint

from lib.colorization import init_model, preprocess_image, process_image

UPLOAD_FOLDER = os.path.abspath('input/')
TRANSFORMED_FOLDER = os.path.abspath('output/')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

NET = init_model()

app = Flask(__name__,
            static_folder="../frontend/dist/static",
            template_folder="../frontend/dist")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/send-file', methods=['POST'])
def save_file():
    try:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return make_response(jsonify({'error': 'No file detected'}), 404)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return make_response(jsonify({'error': 'No file detected'}), 404)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                outfilepath = os.path.join(app.config['TRANSFORMED_FOLDER'], filename)
                file.save(filepath)
                preprocess_image(filepath, outfilepath)
                process_image(outfilepath, outfilepath, NET)
                return jsonify({'OK': 'saved'})

            return make_response(jsonify({'error': 'not allowed'}), 404)

    except (AttributeError, KeyError, ValueError) as e:
        return make_response(jsonify({'error': str(e)}), 404)


@app.route('/api/get/<path:filename>')
def get_picture(filename):
    sec_filename = secure_filename(filename)
    transformed = request.args.get('transformed') or False
    if transformed:
        filepath = os.path.join(app.config['TRANSFORMED_FOLDER'], sec_filename)
    else:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], sec_filename)
    if allowed_file(sec_filename) and os.path.isfile(filepath):
        return send_file(
            filepath,
            mimetype='image/gif'
        )
    else:
        return make_response(jsonify({'error': 'not such file'}), 404)


@app.route('/api/gallery')
def get_gallery():
    format_str = '/api/get/{}?transformed=true'
    files = os.listdir(app.config['TRANSFORMED_FOLDER'])
    filtered_files = [format_str.format(f) for f in files if allowed_file(f)]
    return jsonify({'picList': filtered_files})


def create_app():
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['TRANSFORMED_FOLDER'] = TRANSFORMED_FOLDER
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=True,
        threaded=True,
        port=8080,
        host='0.0.0.0'
    )
