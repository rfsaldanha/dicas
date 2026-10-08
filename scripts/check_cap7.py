#!/usr/bin/env python3
"""Verifica a integração editorial do capítulo 7 e seus artefatos gráficos."""
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTER = ROOT/'chapters/part-2/07-temperatura-condicoes-termicas.qmd'


def check(rendered=False):
    text=CHAPTER.read_text()
    manifest=json.loads((ROOT/'assets/figures/arte-cap7-manifest.json').read_text())
    sections=re.split(r'(?m)^## ',text)
    assert len(sections)==13, 'Esperadas introdução e 12 seções.'
    assert not re.search(r'(?m)^## Síntese',text), 'Síntese ainda presente.'
    assert len(manifest)==13 and len({r['id'] for r in manifest})==13
    bib=set(re.findall(r'(?m)^@\w+\{([^,]+)',(ROOT/'references.bib').read_text()))
    cited=set(re.findall(r'@([A-Za-z][\w-]+)',text))
    assert not (cited-bib-{r['id'] for r in manifest}), 'Referência não resolvida.'
    figure_list=(ROOT/'backmatter/lista-figuras.qmd').read_text()
    for section,r in zip(sections,manifest):
        assert len(re.findall(r'\{#fig-',section))==1, 'Cada seção deve ter uma figura.'
        assert '{#'+r['id'] in section and '@'+r['id'] in section
        assert '@'+r['id'] in figure_list
        assert re.search(r'\]\(\.\./\.\./chapters/.+?\.qmd',section), 'Seção sem remissão a capítulo.'
        for key in ('svg','print'):
            assert (ROOT/'assets/figures'/r[key]).is_file(),r[key]
        svg=ET.parse(ROOT/'assets/figures'/r['svg']).getroot()
        ns={'s':'http://www.w3.org/2000/svg'}
        assert svg.find('s:title',ns) is not None and svg.find('s:desc',ns) is not None
        data=(ROOT/'assets/figures'/r['print']).read_bytes()
        assert data[:8]==b'\x89PNG\r\n\x1a\n' and data[24:26]==bytes([8,0]), 'PNG deve ser cinza de 8 bits.'
        if r['watercolor']:
            src=ROOT/'assets/figures'/r['raster']
            assert hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256_original']
            assert r['min_effective_raster_ppi']>=300
            assert (ROOT/'assets/figures'/r['prompt']).is_file()
    anchors=re.findall(r'<span id="(sec-[^"]+)"></span>',text)
    cardchapter=ROOT/'chapters/part-4/16-fichas-temperatura-condicoes-termicas.qmd'
    expected=re.findall(r'indicators/includes/([a-z0-9-]+)\.qmd',cardchapter.read_text())
    assert len(anchors)==23 and set(anchors)=={'sec-'+c for c in expected}
    directory=text.split('## Localização das fichas operacionais')[1]
    rows='\n'.join(l for l in directory.splitlines() if l.startswith('|'))
    for code in expected:
        assert '#sec-'+code+')' in rows,code
    for target in re.findall(r'\]\(([^)]+\.qmd(?:#[^)]+)?)\)',text):
        file,_,anchor=target.partition('#')
        dest=(CHAPTER.parent/file).resolve()
        assert dest.is_file(),target
        if anchor:
            body=dest.read_text()
            for include in re.findall(r'include ([^ ]+\.qmd)',body):
                body+='\n'+(dest.parent/include).resolve().read_text()
            assert '{#'+anchor in body or 'id="'+anchor+'"' in body,target
    if rendered:
        html=(ROOT/'_output/web/chapters/part-2/07-temperatura-condicoes-termicas.html').read_text()
        for r in manifest:
            assert 'id="'+r['id']+'"' in html
        for a in anchors:
            assert 'id="'+a+'"' in html
        for target in re.findall(r'\]\(([^)]+\.qmd#[^)]+)\)',text):
            file,anchor=target.split('#')
            relative=(CHAPTER.parent/file).resolve().relative_to(ROOT)
            dest=(ROOT/'_output/web'/relative).with_suffix('.html')
            assert 'id="'+anchor+'"' in dest.read_text(),str(dest)+'#'+anchor
    print('Capítulo 7: 13 figuras, 12 seções, 23 âncoras; citações, links e artefatos válidos.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--rendered',action='store_true')
    check(parser.parse_args().rendered)
