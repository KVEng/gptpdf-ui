
from flask import Flask, request, render_template, Response, send_file, send_from_directory
import os
import subprocess
import base64
import markdown
from markupsafe import Markup
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
from archive import archive
import utils as u
import xml.etree.ElementTree as ElementTree
import re

app = Flask(__name__)

os.makedirs(u.UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', pdf_files=get_all_pdf_names(u.UPLOAD_FOLDER))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        task_id = u.uuid_str()
        upload_dir = u.uploads_folder(task_id)
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, 'input.pdf')
        file.save(filepath)
        return Response(run_gptpdf(task_id), content_type='text/event-stream')

@app.route('/files/<path:task_id>')
def md_render(task_id):
    # 读取 Markdown 文件并转换为 HTML
    output_dir = os.path.join(u.uploads_folder(task_id), "output")
    file_path = os.path.join(output_dir, "output.md")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            html_content = markdown.markdown(content, extensions=[ImagePrefixExtension(prefix= "/"+output_dir)])
            return render_template('file.html', content=Markup(html_content), filename=task_id)
    else:
        return "File not found", 404

@app.route('/uploads/<path:filename>')
def file_server(filename):
    return send_from_directory(u.UPLOAD_FOLDER, filename)

@app.route('/md/<path:task_id>')
def md_format(task_id):
    file_path = os.path.join(u.uploads_folder(task_id), "output", "output.md",)
    return send_file(file_path, mimetype='text/markdown', as_attachment=True, download_name=task_id+'.md')

@app.route('/zip/<path:task_id>')
def zip_format(task_id):
    file_path = os.path.join(u.uploads_folder(task_id), "output", "archive.zip",)
    return send_file(file_path, mimetype='application/x-zip', as_attachment=True, download_name=task_id+'.zip')

def run_gptpdf(task_id):
    process = subprocess.Popen(['python', 'parse_pdf.py', task_id, os.environ['OPENAI_API_KEY'], os.environ['OPENAI_BASE_URL'], '4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):
        line_str = line.decode('utf-8')
        match = re.match(r'!\[.*\]\((.*)\)', line_str)  # Match any image path format
        if match:
            image_path = match.group(1)
            full_image_path = os.path.join(u.uploads_folder(task_id), 'output', image_path)
            if os.path.exists(full_image_path):
                with open(full_image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    base64_image = f"data:image/png;base64,{encoded_string}"
                    line_str = f"![]({base64_image})"
        yield f'data: {line_str}\n\n'
    process.stdout.close()
    process.wait()
    archive(task_id)

def get_all_pdf_names(directory):
    """
    获取目录下所有的 PDF 文件名称列表
    :param directory: 目标目录
    :return: PDF 文件名称列表
    """
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(file)
    return pdf_files

class ImagePrefixExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'prefix': ['', 'Prefix for image paths']
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        IMAGE_LINK_RE = r'!\[(.*?)\]\((.*?)\)'
        md.inlinePatterns.register(ImagePrefixInlineProcessor(IMAGE_LINK_RE, self.getConfigs()), 'image_prefix', 175)

class ImagePrefixInlineProcessor(InlineProcessor):
    def __init__(self, pattern, config):
        super().__init__(pattern)
        self.config = config

    def handleMatch(self, m, data):
        if m:
            alt = m.group(1)
            src = m.group(2)
            src = self.config['prefix'] + "/" + src
            el = ElementTree.Element("img")
            el.set('src', src)
            el.set('alt', alt)
            return el, m.start(0), m.end(0)
        return None, None, None



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
