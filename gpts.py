import concurrent.futures
import env
from GeneralAgent import Agent
import utils as u

def translate_md(input_file, target_lang='Chinese (Simplified)', output_file='output.translated.md', verbose=False):
    if target_lang == '':
        return
    pass

def _translate_md(input_file, target_lang='Chinese (Simplified)', output_file='output.translated.md', verbose=False):
    md, ok = u.read_file(input_file)
    if not ok:
        return False
    parts = split_markdown(md)
    content = _tx(parts, target_lang, verbose)
    return u.write_file(output_file, content)

def prompt(lang):
    return f'You are a translator. You need translate user content into {lang} fluently maintaining the original markdown and LaTeX format.'

def split_markdown(md):
    # split with headline
    lines = md.split('\n')
    paragraphs = []
    for idx, line in enumerate(lines):
        if line.startswith('#'):
            paragraphs.append('\n'.join(lines[:idx]))
            lines = lines[idx:]
    if len(lines) > 0:
        paragraphs.append('\n'.join(lines))
    return paragraphs


def _translate(index: int, lang: str, md: str) -> tuple[int, str]:
    agent = Agent(role=prompt(lang), api_key=env.OpenAI_Key, base_url=env.OpenAI_BaseUrl, model=env.Model)
    content = agent.run([md], display=False)
    return index, content

def _tx(parts, lang, verbose):
    contents = [''] * len(parts)
    with concurrent.futures.ThreadPoolExecutor(max_workers=env.MaxThread) as executor:
        futures = [executor.submit(_translate, index, lang, part) for index, part in enumerate(parts)]
        for future in concurrent.futures.as_completed(futures):
            index, content = future.result()
            contents[index] = content
    return '\n\n'.join(contents)