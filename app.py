
from flask import Flask, request, render_template, Response, send_file, send_from_directory
import os
import markdown
from markupsafe import Markup
from markdown_utils import ImagePrefixExtension

from archive import archive
import utils as u
import env
import threading
import gptpdf
import datetime
import gpts

app = Flask(__name__)

os.makedirs(u.UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

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
        threading.Thread(target=run_gptpdf, args=(task_id, '')).start()
        return task_id, 200

@app.route('/task/<path:task_id>/status')
def task_status(task_id):
    if not u.is_valid_uuid(task_id):
        return "illegal task id", 400
    file_path = u.uploads_folder(task_id)
    wip_flag = os.path.join(file_path, 'WIP')
    wip_content, exist = u.read_file(wip_flag)
    if exist:
        return wip_content, 200
    output_md = os.path.join(file_path, "output", "output.md")
    if os.path.exists(output_md):
        return "finished", 200
    return "not found", 404

@app.route('/task/<path:task_id>')
def md_render(task_id):
    if not u.is_valid_uuid(task_id):
        return "illegal task id", 400
    file_path = u.uploads_folder(task_id)
    wip_flag = os.path.join(file_path, 'WIP')
    wip_content, exist = u.read_file(wip_flag)
    if exist:
        return render_template('task_wip.html', started_at=wip_content, filename=task_id)
    # 读取 Markdown 文件并转换为 HTML
    output_dir = os.path.join(file_path, "output")
    file_path = os.path.join(output_dir, "output.md")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            html_content = markdown.markdown(content, extensions=[ImagePrefixExtension(prefix= "/"+output_dir)])
            return render_template('task.html', content=Markup(html_content), filename=task_id)
    else:
        return "Task not found", 404

@app.route('/uploads/<path:filename>')
def file_server(filename):
    if '..' in filename:
        return "illegal path", 400
    if not filename.endswith('.png'):
        return "illegal file type", 400
    filename = filename.strip('/')
    strs = filename.split('/')
    if not u.is_valid_uuid(strs[0]):
        return "illegal task id", 400
    return send_from_directory(u.UPLOAD_FOLDER, filename)

@app.route('/md/<path:task_id>')
def md_format(task_id):
    if not u.is_valid_uuid(task_id):
        return "illegal task id", 400
    file_path = os.path.join(u.uploads_folder(task_id), "output", "output.md",)
    return send_file(file_path, mimetype='text/markdown', as_attachment=True, download_name=task_id+'.md')

@app.route('/zip/<path:task_id>')
def zip_format(task_id):
    if not u.is_valid_uuid(task_id):
        return "illegal task id", 400
    file_path = os.path.join(u.uploads_folder(task_id), "archive.zip",)
    print(file_path)
    return send_file(file_path, mimetype='application/x-zip', as_attachment=True, download_name=task_id+'.zip')

def run_gptpdf(task_id, translate_to=''):
    print('Running TaskID:', task_id)
    file_path = u.uploads_folder(task_id)
    wip_flag = os.path.join(file_path, 'WIP')
    
    u.write_file(wip_flag, datetime.datetime.now().isoformat())
    
    with open(wip_flag, 'w', encoding='utf-8') as file:
        file.write(str(datetime.datetime.now().isoformat()))
    # mock_run_gptpdf(task_id)
    input_file = os.path.join(file_path, 'input.pdf')
    output_dir = os.path.join(file_path, 'output')
    gptpdf.parse_pdf(input_file, api_key=env.OpenAI_Key, base_url=env.OpenAI_BaseUrl, output_dir=output_dir, gpt_worker=env.MaxThread, verbose=True, model=env.Model)
    translate_md(task_id, translate_to)
    archive(task_id)
    os.remove(wip_flag)
    print('Finished TaskID:', task_id)

def translate_md(task_id, translate_to):
    if translate_to == '':
        return
    print('Translating TaskID:', task_id)
    file_path = u.uploads_folder(task_id)
    wip_flag = os.path.join(file_path, 'TRANSLATE')
    
    u.write_file(wip_flag, datetime.datetime.now().isoformat())
    
    output_dir = os.path.join(file_path, 'output')
    input_file = os.path.join(output_dir, 'output.md')
    output_file = os.path.join(output_dir, 'output.translated.md')
    gpts.translate_md(
        input_file=input_file, 
        output_file=output_file,
        target_lang='Chinese (Simplified)',
        verbose=True)
    archive(task_id)
    os.remove(wip_flag)
    print('Translated TaskID:', task_id)

if __name__ == '__main__':
    app.run(host=env.Host, port=env.Port, debug=False)
