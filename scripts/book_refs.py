"""Destinos editoriais compartilhados pelos verificadores de capítulos."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def visible(text):
    return re.sub(r'<!--.*?-->|```.*?```', '', text, flags=re.S)


def chapters(root=ROOT):
    paths = re.findall(r'^\s*- (chapters/\S+\.qmd)\s*$',
                       (root/'_quarto-web.yml').read_text(), re.M)
    result = {}
    for number, path in enumerate(paths, 1):
        match = re.search(r'^# (.*?) \{#(sec-[\w-]+)', (root/path).read_text(), re.M)
        assert match, path
        result[match[2]] = dict(number=number, title=match[1], path=path)
    return result


def section_ids(root=ROOT):
    files = [*root.glob('chapters/**/*.qmd'), *root.glob('indicators/includes/*.qmd'),
             *root.glob('frontmatter/*.qmd'), *root.glob('backmatter/*.qmd')]
    return {identifier for path in files for identifier in
            re.findall(r'(?m)^#+ .*?\{#(sec-[\w-]+)', visible(path.read_text()))}


def chapter_remission(text, part=None):
    if re.search(r'\]\([^)]*chapters/'+(f'part-{part}/' if part else '')+r'[^)]+\.qmd', text):
        return True
    referenced = set(re.findall(r'@(sec-[\w-]+)', text))
    return any(identifier in referenced and (part is None or f'part-{part}/' in item['path'])
               for identifier, item in chapters().items())
