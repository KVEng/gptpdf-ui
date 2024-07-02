import shutil as sh

def archive(task_id : str):
    sh.make_archive(f'./uploads/{task_id}/archive', 'zip', f'./uploads/{task_id}/output')
