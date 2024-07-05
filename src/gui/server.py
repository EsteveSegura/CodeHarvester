import os
import sys
from utils.output_supressor import DisablePrint
from flask import Flask, Response, request, json
from flask_cors import CORS, cross_origin
import file_manipulation.file_operations as fo
import file_manipulation.tree_generator as tg

store = {}

def get_static_folder_path():
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller env
        base_dir = sys._MEIPASS
        static_folder_path = os.path.join(base_dir, 'static')
    else:
        # Python3 env
        base_dir = os.path.dirname(os.path.abspath(__file__))
        static_folder_path = os.path.join(base_dir, '..', '..', 'static')
    return static_folder_path

def launch_server(structure_file_json, directory, port):
    static_folder_path = get_static_folder_path()
    app = Flask(__name__, static_folder=static_folder_path)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    store['structure_file_json'] = structure_file_json
    store['directory'] = directory

    @app.route('/')
    @cross_origin()
    def home():
        index_html_path = os.path.join(static_folder_path, 'index.html')
        with open(index_html_path, 'r') as html_file:
            html_content = html_file.read()

        return Response(html_content, mimetype='text/html')

    @app.route('/api/v1/structure')
    def structure():
        return store['structure_file_json']

    @app.route('/api/v1/terminal', methods=['POST'])
    @cross_origin()
    def terminal():
        data = request.get_json()

        print(data['paths'])
        dir = store['directory']

        include_files = [os.path.relpath(os.path.join(dir, f), dir) for f in data['paths']]
        files = fo.find_included_files(dir, include_files)
        tree_text = tg.print_tree_included(dir, include_files)
        markdown = fo.generate_markdown(files)
        
        output_content = markdown + '\n\n' + tree_text
        
        return json.dumps({'response': output_content})
    
    with DisablePrint():
        app.run(port=port, debug=False)
