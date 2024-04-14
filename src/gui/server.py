import os

from flask import Flask, Response, request, json
from flask_cors import CORS, cross_origin

import file_manipulation.file_operations as fo
import file_manipulation.tree_generator as tg

store = {}

def launch_server(structure_file_json, directory):
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    store['structure_file_json'] = structure_file_json
    store['directory'] = directory

    @app.route('/')
    @cross_origin()
    def home():
        with open('./static/index.html', 'r') as html_file:
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
    
    if __name__ == "__main__":
        app.run(host='127.0.0.1', port=4111, debug=False, show_server_banner=False)
