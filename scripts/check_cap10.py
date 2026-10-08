#!/usr/bin/env python3
"""Confere integração editorial, destinos e artefatos do capítulo 10."""
import argparse
import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
CHAPTER=ROOT/'chapters/part-2/10-agua-saneamento-qualidade-ambiental.qmd'


def check(rendered=False):
    body=CHAPTER.read_text()
    records=json.loads((ROOT/'assets/figures/arte-cap10-manifest.json').read_text())
    assert len(records)==14 and len({r['id'] for r in records})==14
    assert sum(r['watercolor'] for r in records)==7
    assert len(re.findall(r'(?m)^## ',body))==9
    assert len(re.findall(r'(?m)^### ',body))==4
    assert not re.search(r'(?m)^## Síntese',body)
    assert 'FIG10:' not in body and '[[C:' not in body
    assert '#fig-cadeia-agua-saneamento' in body
    assert '/chapters/part-2/08-agua-saneamento-qualidade-ambiental.html' in body
    parts=re.split(r'(?m)^#{2,3} ',body)
    for part,r in zip(parts,records):
        assert len(re.findall(r'\{#fig-',part))==1, 'Figura ausente ou duplicada: '+r['number']
        assert '{#'+r['id'] in part and '@'+r['id'] in part
        assert re.search(r'\]\(../../chapters/part-4/.+?\.qmd',part),'Trecho sem ficha relacionada: '+r['number']
    bib=re.findall(r'(?m)^@\w+\{([^,]+)',(ROOT/'references.bib').read_text())
    assert len(bib)==len(set(bib)),'Chaves bibliográficas repetidas'
    refs=set(re.findall(r'@([A-Za-z][\w-]+)',body))
    assert not (refs-set(bib)-{r['id'] for r in records}), 'Citação não resolvida'
    listing=(ROOT/'backmatter/lista-figuras.qmd').read_text()
    ns={'s':'http://www.w3.org/2000/svg'}
    for r in records:
        assert '@'+r['id'] in listing
        svg=ET.parse(ROOT/'assets/figures'/r['svg']).getroot()
        assert svg.find('s:title',ns) is not None and svg.find('s:desc',ns) is not None
        assert svg.find("s:style[@id='dicas-fonts']",ns) is not None
        png=(ROOT/'assets/figures'/r['print']).read_bytes()
        assert png[:8]==b'\x89PNG\r\n\x1a\n' and png[24:26]==bytes([8,0]),'PNG precisa ser cinza de 8 bits'
        assert struct.unpack('>I',png[16:20])[0]>=1418
        if r['watercolor']:
            original=ROOT/'assets/figures'/r['raster']
            assert hashlib.sha256(original.read_bytes()).hexdigest()==r['sha256_original']
            assert r['min_effective_raster_ppi']>=300
            assert (ROOT/'assets/figures'/r['prompt']).is_file()
    cards=ROOT/'chapters/part-4/19-fichas-agua-saneamento-qualidade-ambiental.qmd'
    expected=re.findall(r'indicators/includes/([a-z0-9-]+)\.qmd',cards.read_text())
    anchors=re.findall(r'<span id="(sec-[^"]+)"></span>',body)
    assert len(anchors)==9 and set(anchors)=={'sec-'+c for c in expected}
    directory=body.split('## Localização das fichas operacionais')[1]
    rows='\n'.join(l for l in directory.splitlines() if l.startswith('|'))
    for code in expected:assert '#sec-'+code+')' in rows,code
    targets=re.findall(r'\]\(([^)]+\.qmd(?:#[^)]+)?)\)',body)
    for target in targets:
        file,_,anchor=target.partition('#')
        dest=(CHAPTER.parent/file).resolve()
        assert dest.is_file(),target
        if anchor:
            content=dest.read_text()
            for include in re.findall(r'include ([^ ]+\.qmd)',content):content+='\n'+(dest.parent/include).resolve().read_text()
            assert '{#'+anchor in content or 'id="'+anchor+'"' in content,target
        if rendered:
            html=(ROOT/'_output/web'/dest.relative_to(ROOT)).with_suffix('.html')
            assert html.is_file(),str(html)
            if anchor:assert 'id="'+anchor+'"' in html.read_text(),str(html)+'#'+anchor
    if rendered:
        html=(ROOT/'_output/web'/CHAPTER.relative_to(ROOT)).with_suffix('.html').read_text()
        for r in records:assert 'id="'+r['id']+'"' in html
        for anchor in anchors:assert 'id="'+anchor+'"' in html
        alias=(ROOT/'_output/web/chapters/part-2/08-agua-saneamento-qualidade-ambiental.html').read_text()
        assert '10-agua-saneamento-qualidade-ambiental.html' in alias and 'window.location.hash' in alias
        assert '## Síntese' not in html
        assert 'href="../../chapters/part-4/19-fichas-agua-saneamento-qualidade-ambiental.html#sec-san-agu-01"' in html
    print(f'Capítulo 10: 14 figuras (7 aquarelas), 9 seções, 4 subseções, 9 âncoras, {len(refs-set(r["id"] for r in records))} referências; integração válida.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--rendered',action='store_true')
    check(parser.parse_args().rendered)
