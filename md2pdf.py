import pypandoc
import os

CJKFONT = 'Songti SC Regular'

def md2pdf(md_file, pdf_file, working_dir):
    # add
    pypandoc.convert_file(md_file, 'pdf', outputfile=pdf_file,
                        cworkdir=working_dir,
                        extra_args=[
                                '--pdf-engine=xelatex', 
                                '--variable', f'CJKmainfont={CJKFONT}',
                                '--variable', 'CJKoptions=AutoFakeBold',
                        ])
