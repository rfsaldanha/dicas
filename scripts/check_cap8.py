#!/usr/bin/env python3
"""Valida remissões, cobertura editorial e artefatos do capítulo 8."""
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from book_refs import chapter_remission, section_ids
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parent.parent
CHAPTER=ROOT/'chapters/part-2/08-precipitacao-secas-eventos-hidrologicos.qmd'

class Page(HTMLParser):
    def __init__(self,path):
        super().__init__()
        self.ids=[];self.links=[];self.images=[]
        self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='img':self.images.append(a)

def expanded(path):
    text=path.read_text()
    return re.sub(r'\{\{< include ([^ ]+\.qmd) >\}\}',
                  lambda m:expanded((path.parent/m[1]).resolve()),text)

def check(rendered=False):
    text=CHAPTER.read_text()
    records=json.loads((ROOT/'assets/figures/arte-cap8-manifest.json').read_text())
    parts=re.split(r'(?m)^#{2,3} ',text)
    assert len(re.findall(r'(?m)^## ',text))==9,'Esperadas nove seções.'
    assert len(re.findall(r'(?m)^### ',text))==10,'Esperadas dez subseções.'
    assert len(parts)==len(records)==20,'Esperadas 20 figuras, uma por trecho.'
    assert not re.search(r'(?m)^## Síntese',text)
    assert '<!-- CAP8:' not in text,'Marcador de produção ainda presente.'
    ids={r['id'] for r in records}
    assert len(ids)==20 and {'fig-cadeia-hidrometeorologica','fig-processos-hidrologicos'}<=ids
    bib=re.findall(r'(?m)^@\w+\{([^,]+)',(ROOT/'references.bib').read_text())
    assert len(bib)==len(set(bib)),'Chave BibTeX duplicada.'
    cited=set(re.findall(r'@([A-Za-z][\w-]+)',text))
    assert not cited-set(bib)-ids-section_ids(),cited-set(bib)-ids-section_ids()
    figure_list=(ROOT/'backmatter/lista-figuras.qmd').read_text()
    for part,r in zip(parts,records):
        assert len(re.findall(r'\{#fig-',part))==1,'Trecho sem figura própria ou com duplicação.'
        assert '{#'+r['id'] in part and '@'+r['id'] in part,r['id']
        assert '@'+r['id'] in figure_list,r['id']
        assert chapter_remission(part),'Trecho sem remissão a capítulo.'
        for key in ('svg','print'):assert (ROOT/'assets/figures'/r[key]).is_file(),r[key]
        svg=ET.parse(ROOT/'assets/figures'/r['svg']).getroot()
        ns={'s':'http://www.w3.org/2000/svg'}
        assert svg.find('s:title',ns) is not None and svg.find('s:desc',ns) is not None
        png=(ROOT/'assets/figures'/r['print']).read_bytes()
        assert png[:8]==b'\x89PNG\r\n\x1a\n' and png[24:26]==bytes([8,0]),r['print']
        if r['watercolor']:
            raster=ROOT/'assets/figures'/r['raster']
            assert hashlib.sha256(raster.read_bytes()).hexdigest()==r['sha256_original']
            assert r['min_effective_raster_ppi']>=300
            assert (ROOT/'assets/figures'/r['prompt']).is_file()
    expected={'sec-cli-prc-'+str(n).zfill(2) for n in range(1,7)}|{'sec-cli-sec-01'}
    anchors=re.findall(r'<span id="(sec-[^"]+)"></span>',text)
    assert len(anchors)==7 and set(anchors)==expected
    for target in re.findall(r'\]\(([^)]+\.qmd(?:#[^)]+)?)\)',text):
        file,_,anchor=target.partition('#')
        dest=(CHAPTER.parent/file).resolve()
        assert dest.is_file(),target
        if anchor:
            body=expanded(dest)
            assert '{#'+anchor in body or 'id="'+anchor+'"' in body,target
    for code in expected:
        assert '#'+code+')' in text.split('## Localização das fichas operacionais')[1]
    if rendered:
        web=ROOT/'_output/web'
        rendered_chapter=(web/CHAPTER.relative_to(ROOT)).with_suffix('.html')
        assert 'quarto-unresolved-ref' not in rendered_chapter.read_text(), 'Remissão não resolvida no HTML.'
        page=Page(rendered_chapter)
        # O Quarto repete IDs de estilos nas alternativas claro/escuro.
        content_ids=[i for i in page.ids if i not in {'quarto-text-highlighting-styles','quarto-bootstrap'}]
        assert len(content_ids)==len(set(content_ids)),'ID de conteúdo duplicado no HTML.'
        assert ids|expected<=set(page.ids)
        cache={}
        for href in page.links:
            parsed=urlsplit(href)
            if parsed.scheme or parsed.netloc or not parsed.path.endswith('.html'):continue
            dest=(web/parsed.path.lstrip('/')).resolve() if parsed.path.startswith('/') else (rendered_chapter.parent/parsed.path).resolve()
            assert dest.is_file(),href
            if parsed.fragment:
                if dest not in cache:cache[dest]=set(Page(dest).ids)
                assert unquote(parsed.fragment) in cache[dest],href
        assert not any('.qmd' in h for h in page.links if not urlsplit(h).scheme)
        assert all(i.get('alt') for i in page.images if 'arte-cap8-' in i.get('src',''))
        card=Page(web/'chapters/part-4/18-fichas-precipitacao-secas-eventos-hidrologicos.html')
        assert expected<=set(card.ids)
        assert any(urlsplit(h).path.endswith('/08-precipitacao-secas-eventos-hidrologicos.html')
                   and urlsplit(h).fragment in ('', 'sec-precipitacao') for h in card.links)
        assert 'sec-precipitacao' in page.ids
        alias=(web/'chapters/part-2/06-precipitacao-secas-eventos-hidrologicos.html').read_text()
        assert '08-precipitacao-secas-eventos-hidrologicos.html' in alias
    print('Capítulo 8: 9 seções, 10 subseções, 20 figuras e 7 âncoras; citações e links válidos.'
          + (' HTML e retornos conferidos.' if rendered else ''))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--rendered',action='store_true')
    check(parser.parse_args().rendered)
