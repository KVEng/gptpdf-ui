import pypandoc

CJKFONT = 'Songti SC Regular'

def md2pdf(md_file, pdf_file):
    # add
    pypandoc.convert_file(md_file, 'pdf', outputfile=pdf_file,
                        extra_args=[
                                '--pdf-engine=xelatex', 
                                '--variable', f'CJKmainfont={CJKFONT}',
                                '--variable', 'CJKoptions=AutoFakeBold',
                        ])
