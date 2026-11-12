#!/usr/bin/env python3
"""Verifica referências, navegação e acessibilidade das figuras do capítulo 12."""
import argparse
import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from book_refs import chapter_remission, section_ids

ROOT=Path(__file__).resolve().parent.parent
CHAPTER=ROOT/'chapters/part-2/12-eventos-severos-desastres.qmd'


def check(rendered=False):
    body=CHAPTER.read_text()
    records=json.loads((ROOT/'assets/figures/arte-cap12-manifest.json').read_text())
    assert len(records)==10 and len({r['id'] for r in records})==10
    assert sum(r['watercolor'] for r in records)==5
    parts=re.split(r'(?m)^## ',body)
    assert len(parts)==10,'Esperadas introdução e nove seções'
    assert not re.search(r'(?m)^## Síntese',body)
    assert 'FIG12:' not in body
    assert '#sec-desastres}' in body
    assert '/chapters/part-2/10-eventos-severos-desastres.html' in body
    assert {records[0]['id'],records[-1]['id']}=={'fig-risco-desastre','fig-linha-tempo-desastre'}
    for part,r in zip(parts,records):
        assert len(re.findall(r'\{#fig-',part))==1,'Figura ausente ou duplicada: '+r['number']
        assert '{#'+r['id'] in part and '@'+r['id'] in part
        assert chapter_remission(part, part=4),'Seção sem ficha relacionada: '+r['number']
        assert re.search(r'\[@[A-Za-z]|\[@|; @',part),'Seção sem referência bibliográfica: '+r['number']
    bib=re.findall(r'(?m)^@\w+\{([^,]+)',(ROOT/'references.bib').read_text())
    assert len(bib)==len(set(bib)),'Chaves bibliográficas repetidas'
    refs=set(re.findall(r'@([A-Za-z][\w-]+)',body))
    crossrefs={r['id'] for r in records}|{'qua-indicadores-desastre'}|section_ids()
    assert not (refs-set(bib)-crossrefs),'Citação não resolvida: '+str(refs-set(bib)-crossrefs)
    listing=(ROOT/'backmatter/lista-figuras.qmd').read_text()
    ns={'s':'http://www.w3.org/2000/svg'}
    for r in records:
        assert '@'+r['id'] in listing
        svg=ET.parse(ROOT/'assets/figures'/r['svg']).getroot()
        assert svg.find('s:title',ns) is not None and svg.find('s:desc',ns) is not None
        assert svg.find("s:style[@id='dicas-fonts']",ns) is not None
        png=(ROOT/'assets/figures'/r['print']).read_bytes()
        assert png[:8]==b'\x89PNG\r\n\x1a\n' and png[24:26]==bytes([8,0]),'PNG deve ser cinza de 8 bits'
        assert struct.unpack('>I',png[16:20])[0]>=1418
        if r['watercolor']:
            original=ROOT/'assets/figures'/r['raster']
            assert hashlib.sha256(original.read_bytes()).hexdigest()==r['sha256_original']
            assert r['min_effective_raster_ppi']>=300
            assert (ROOT/'assets/figures'/r['prompt']).is_file()
    cards=ROOT/'chapters/part-4/22-fichas-eventos-severos-desastres.qmd'
    expected=re.findall(r'indicators/includes/([a-z0-9-]+)\.qmd',cards.read_text())
    anchors=re.findall(r'<span id="(sec-[^"]+)"></span>',body)
    assert len(anchors)==4 and set(anchors)=={'sec-'+c for c in expected}
    targets=set(re.findall(r'\]\(([^)]+\.qmd(?:#[^)]+)?)\)',body))
    for target in targets:
        file,_,anchor=target.partition('#')
        dest=(CHAPTER.parent/file).resolve()
        assert dest.is_file(),target
        if anchor:
            content=dest.read_text()
            for include in re.findall(r'include ([^ ]+\.qmd)',content):
                content+='\n'+(dest.parent/include).resolve().read_text()
            assert '{#'+anchor in content or 'id="'+anchor+'"' in content,target
        if rendered:
            html=(ROOT/'_output/web'/dest.relative_to(ROOT)).with_suffix('.html')
            assert html.is_file(),str(html)
            if anchor:assert 'id="'+anchor+'"' in html.read_text(),str(html)+'#'+anchor
    if rendered:
        html=(ROOT/'_output/web'/CHAPTER.relative_to(ROOT)).with_suffix('.html').read_text()
        for r in records:assert 'id="'+r['id']+'"' in html
        for anchor in anchors:assert 'id="'+anchor+'"' in html
        assert not re.search(r'<h2[^>]*>[^<]*Síntese',html)
        assert 'href="../../chapters/part-4/22-fichas-eventos-severos-desastres.html#sec-des-hum-01"' in html
        assert not re.search(r'href="(?!https?://)[^"]+\.qmd(?:#|\")',html),'Link QMD não convertido'
    print(f'Capítulo 12: 10 figuras (5 aquarelas), 9 seções, 4 âncoras, {len(refs-set(crossrefs))} referências e {len(targets)} destinos; integração válida.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--rendered',action='store_true')
    check(parser.parse_args().rendered)
