#!/usr/bin/env python3
"""Confere remissões nativas e ausência de numeração editorial manual."""
from pathlib import Path
import re
from book_refs import ROOT, chapters, section_ids, visible


def check(root=ROOT):
    ids = section_ids(root)
    inventory = chapters(root)
    chapter_paths = {(root/item['path']).resolve(): identifier for identifier, item in inventory.items()}
    files = [*root.glob('chapters/**/*.qmd'), *root.glob('frontmatter/*.qmd'),
             *root.glob('backmatter/*.qmd'), *root.glob('includes/*.qmd'),
             *root.glob('indicators/includes/*.qmd'), *root.glob('indicators/generated-*.qmd')]
    count = 0
    for path in files:
        text = visible(path.read_text())
        refs = set(re.findall(r'@(sec-[\w-]+)', text))
        assert not refs-ids, f'{path}: destinos inexistentes: {refs-ids}'
        assert not re.search(r'fig-alt="[^"]*@sec-',text), f'{path}: referência em atributo de texto alternativo'
        assert not re.search(r'(?i)\bcapítulos?\s+\d+', text), f'{path}: número de capítulo manual'
        assert not re.search(r'(?i)\bcapítulo\s+@sec-', text), f'{path}: prefixo repetido'
        assert not re.search(r'(@sec-[\w-]+) \(\1\)', text), f'{path}: remissão repetida'
        assert not re.search(r'@sec-[\w-]+(?: e |, | a )\d', text), f'{path}: número manual em remissão agrupada'
        for identifier in re.findall(r'\.chapter-title-ref target="([^"]+)"',text):
            assert identifier in inventory, f'{path}: título sem capítulo: {identifier}'
        for target in re.findall(r'\]\(([^)]+\.qmd(?:#[^)]+)?)\)',text):
            file, _, anchor = target.partition('#')
            identifier = chapter_paths.get((path.parent/file).resolve())
            assert not identifier or (anchor and anchor != identifier), f'{path}: remissão a capítulo sem @sec: {target}'
        count += len(refs)
    print(f'Remissões: {len(inventory)} capítulos; {count} destinos citados em {len(files)} fontes; identificadores válidos.')


if __name__ == '__main__':
    check()
