import uuid
import os

def uuid_str():
    return str(uuid.uuid4())

UPLOAD_FOLDER = 'uploads'

def uploads_folder(task_id):
    return os.path.join(UPLOAD_FOLDER, task_id)

def is_valid_uuid(uuid_str):
    try:
        uuid_obj = uuid.UUID(uuid_str, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_str

def read_file(path) -> tuple[str, bool]:
    # return content, is_exist
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read(), True
        except:
            return "", False
    return "", False