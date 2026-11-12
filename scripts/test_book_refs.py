#!/usr/bin/env python3
"""Regressões de destinos, títulos, numeração e referências da edição parcial."""
import html
import json
import re
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from book_refs import ROOT
from check_book_refs import check


def nodes(value, kind):
    if isinstance(value, dict):
        if value.get('t') == kind:
            yield value
        for child in value.values():
            yield from nodes(child, kind)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child, kind)


class BookReferences(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='dicas-refs-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'scripts').mkdir()
        (self.root/'chapters').mkdir()
        for name in ('chapter_metadata.lua', 'chapter_titles.lua', 'preliminar-links.lua'):
            shutil.copy2(ROOT/'scripts'/name, self.root/'scripts'/name)
        (self.root/'index.qmd').write_text('# Abertura {.unnumbered}\n')
        (self.root/'chapters/a.qmd').write_text('# Primeiro {#sec-a}\n\nConsulte @sec-b: []{.chapter-title-ref target="sec-b"}.\n')
        (self.root/'chapters/b.qmd').write_text('# Segundo {#sec-b}\n')
        (self.root/'_quarto.yml').write_text('project:\n  type: book\nlang: pt-BR\nfilters:\n  - scripts/chapter_titles.lua\nformat: html\n')
        self.config(('a','b'))
        (self.root/'_quarto-preliminar.yml').write_text('book:\n  chapters:\n    - chapters/a.qmd\n')

    def config(self, order):
        (self.root/'_quarto-web.yml').write_text(
            'book:\n  title: Prova de referências\n  chapters:\n    - index.qmd\n'+
            ''.join(f'    - chapters/{name}.qmd\n' for name in order))

    def pandoc(self, text, filter_name):
        process = subprocess.run(['quarto','pandoc','-f','markdown','-t','json',
                                  '--lua-filter=scripts/'+filter_name],
                                 input=text, text=True, capture_output=True, cwd=self.root, check=True)
        return json.loads(process.stdout)

    def test_retitle_and_renumber_in_rendered_book(self):
        for order, title, number in [(('a','b'),'Segundo',2), (('b','a'),'Título atualizado',1)]:
            self.config(order)
            (self.root/'chapters/b.qmd').write_text(f'# {title} {{#sec-b}}\n')
            process = subprocess.run(['quarto','render','--profile','web'], cwd=self.root,
                                     capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stdout+process.stderr)
            page = (self.root/'_book/chapters/a.html').read_text()
            self.assertIn(title, page)
            self.assertIn('b.html', page)
            self.assertRegex(html.unescape(page), rf'Capítulo\s+{number}\b')
            self.assertNotIn('chapter-title-ref', page)
            self.assertNotIn('quarto-xref-unresolved', page)

    def test_omitted_reference_tracks_full_order_and_preserves_bibliography(self):
        for order, number in [(('a','b'),2),(('b','a'),1)]:
            self.config(order)
            document = self.pandoc('Consulte @sec-b [@fonte; @outra].', 'preliminar-links.lua')
            strings = [node['c'] for node in nodes(document, 'Str')]
            self.assertIn(f'capítulo {number}', strings)
            citations = [c['citationId'] for node in nodes(document, 'Cite') for c in node['c'][0]]
            self.assertEqual(citations, ['fonte','outra'])

    def test_unknown_target_and_manual_number_are_rejected(self):
        path = self.root/'chapters/a.qmd'
        for content, message in [('@sec-ausente', 'destinos inexistentes'),
                                 ('capítulo 2', 'número de capítulo manual'),
                                 ('@sec-b (@sec-b)', 'remissão repetida'),
                                 ('@sec-a e 2', 'número manual em remissão agrupada')]:
            path.write_text('# Primeiro {#sec-a}\n\n'+content)
            with self.assertRaisesRegex(AssertionError, message):
                check(self.root)

    def test_title_without_target_fails(self):
        with self.assertRaises(subprocess.CalledProcessError):
            self.pandoc('[]{.chapter-title-ref target="sec-ausente"}', 'chapter_titles.lua')


if __name__ == '__main__':
    unittest.main(verbosity=2)
