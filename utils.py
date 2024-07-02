import uuid
import os

def uuid_str():
    return str(uuid.uuid4())

UPLOAD_FOLDER = 'uploads'

def uploads_folder(task_id):
    return os.path.join(UPLOAD_FOLDER, task_id)