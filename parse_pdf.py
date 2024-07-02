from gptpdf import parse_pdf
import sys
import utils as u
import os

task_id = sys.argv[1]
api_key = sys.argv[2]
base_url = sys.argv[3]
gpt_worker = int(sys.argv[4])

# filepath
file_path = u.uploads_folder(task_id)
input_file = os.path.join(file_path, 'input.pdf')
output_dir = os.path.join(file_path, 'output')

print('TaskID:', task_id)

parse_pdf(input_file, api_key=api_key, base_url=base_url, output_dir=output_dir, gpt_worker=gpt_worker, verbose=True)