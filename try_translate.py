import gpts
import utils as u
import os.path as path
import env

f = u.uploads_folder('6aa4d053-5306-4ccf-a881-f068fc6377ff')
input_file = path.join(f, 'output', 'output.md')
output_file = path.join(f, 'output', 'output.translated.md')
gpts._translate_md(input_file, 'Chinese (Simplified)', output_file, True)