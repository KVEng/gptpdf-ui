import shutil as sh

def archive(task_id : str):
    sh.make_archive(f'./uploads/{task_id}/archive', 'zip', f'./uploads/{task_id}/output')
    
archive('26b63b23-91fb-448e-90fb-18048748ba47')