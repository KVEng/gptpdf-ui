from md2pdf import md2pdf
import os
from os import path

wd = os.getcwd()
wdir = path.join(wd, 'test')

md2pdf('test.md', 'output.pdf', wdir)