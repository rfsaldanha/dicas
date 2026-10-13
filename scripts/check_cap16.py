#!/usr/bin/env python3
"""Confere integração, proveniência e acessibilidade das oito figuras do capítulo 16."""
import argparse
import base64
import hashlib
import html
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTER = ROOT / 'chapters/part-3/16-comunicacao-risco-saude-clima.qmd'
ART = ROOT / 'assets/figures'
NS = {'s': 'http://www.w3.org/2000/svg'}


def png_size(data):
    assert data[:8] == b'\x89PNG\r\n\x1a\n', 'Arquivo PNG inválido'
    return struct.unpack('>II', data[16:24])


def check(rendered=False):
    source = CHAPTER.read_text()
    visible = re.sub(r'<!--.*?-->', '', source, flags=re.S)
    records = json.loads((ART / 'arte-cap16-manifest.json').read_text())
    assert [r['number'] for r in records] == [f'{n:02}' for n in range(1, 9)]
    assert sum(r['watercolor'] for r in records) == 5
    ids = [r['id'] for r in records]
    assert len(set(ids)) == 8
    assert re.findall(r'\{#(fig-[\w-]+)', visible) == ids, 'Ordem ou identificação das oito figuras incorreta'
    assert len(re.findall(r'\{#qua-', visible)) == 3, 'Os três quadros devem permanecer no capítulo'
    assert '#sec-comunicacao-risco}' in visible
    assert len(re.findall(r'<!-- ARTE CAP16-', source)) == 8
    bib = set(re.findall(r'(?m)^@\w+\{([^,]+)', (ROOT / 'references.bib').read_text()))
    refs = set(re.findall(r'@([A-Za-z][\w-]+)', visible))
    missing = {r for r in refs if not r.startswith(('fig-', 'sec-', 'qua-', 'tbl-'))} - bib
    assert not missing, f'Citações sem referência bibliográfica: {missing}'
    listing = (ROOT / 'backmatter/lista-figuras.qmd').read_text()
    for record in records:
        name = record['number']
        marker = re.search(r'<!-- ARTE CAP16-' + name + r'\n(.*?)-->', source, re.S)
        assert marker, f'Marcador de produção ausente: {name}'
        for field in ('Finalidade:', 'Composição e montagem:', 'Rótulos:', 'Legenda:', 'Fontes:', 'Texto alternativo:'):
            assert field in marker[1], f'{name}: campo ausente {field}'
        assert '@' + record['id'] in visible and '@' + record['id'] in listing
        assert 'fig-alt="' + record['alt'] + '"' in visible
        assert f'print-src="{record["print"]}"' in visible
        assert f'print-width="{record["print_width_mm"]}mm"' in visible
        assert record['citations'] in visible
        svg = ET.parse(ART / record['svg']).getroot()
        assert svg.find('s:title', NS).text == record['title']
        assert svg.find('s:desc', NS).text == record['alt']
        assert json.loads(svg.find('s:metadata', NS).text) == record
        assert svg.find("s:style[@id='cap16-fonts']", NS) is not None
        labels = [' '.join(node.itertext()) for node in svg.findall('.//s:text', NS)]
        assert labels and all(label in marker[1] for label in labels), f'{name}: rótulos não documentados'
        assert svg.find('s:g', NS).get('font-family') == "'Source Sans 3', sans-serif"
        png = (ART / record['print']).read_bytes()
        width, height = png_size(png)
        assert png[24:26] == bytes([8, 0]), f'{name}: impressão deve ser cinza de 8 bits'
        assert (width, height) == (record['width'], record['height'])
        assert width * 25.4 / record['print_width_mm'] >= 300
        images = svg.findall('.//s:image', NS)
        if record['watercolor']:
            assert len(images) == 1
            original = (ART / record['raster']).read_bytes()
            assert hashlib.sha256(original).hexdigest() == record['sha256_original']
            assert list(png_size(original)) == record['original_dimensions_px']
            assert base64.b64decode(images[0].get('href').split(',', 1)[1]) == original
            viewport = svg.find('.//s:g/s:svg', NS)
            original_width = png_size(original)[0]
            effective_width_mm = record['print_width_mm'] * float(viewport.get('width')) / record['width']
            ppi = original_width * 25.4 / effective_width_mm
            assert ppi >= 300 and round(ppi, 1) == record['min_effective_raster_ppi']
            assert (ART / record['prompt']).read_text().strip() in marker[1]
            assert record['tool'] == 'image_gen'
            assert (ROOT / record['reference']).is_file()
            for previous in record.get('previous_versions', []):
                assert (ART / previous['raster']).is_file()
                assert (ART / previous['prompt']).read_text().strip() in marker[1]
        else:
            assert not images, f'{name}: diagrama deve permanecer vetorial'
    if rendered:
        path = (ROOT / '_output/web' / CHAPTER.relative_to(ROOT)).with_suffix('.html')
        page = re.sub(r'<!--.*?-->', '', path.read_text(), flags=re.S)
        assert 'ARTE CAP16-' not in page, 'Comentário de produção exposto ao leitor'
        assert not re.search(r'@(fig|sec|qua|tbl)-[\w-]+', page), 'Remissão não resolvida'
        for i, record in enumerate(records, 1):
            figure_id = record['id']
            assert page.count(f'id="{figure_id}"') == 1
            captions = re.findall(r'<figcaption\b[^>]*>(.*?)</figcaption>', page, re.S)
            expected = f'Figura 16.{i}:'
            assert any(expected in ' '.join(html.unescape(re.sub('<[^>]+>', '', c)).split()) for c in captions), expected
            images = re.findall(r'<img\b[^>]*>', page)
            image_tag = next((t for t in images if record['svg'] in t), '')
            assert image_tag and f'alt="{record["alt"]}"' in html.unescape(image_tag)
            published = ROOT / '_output/web/assets/figures' / record['svg']
            assert published.read_bytes() == (ART / record['svg']).read_bytes()
        assert 'glightbox' in page, 'Ampliação das figuras não habilitada'
    print('Capítulo 16: oito figuras (cinco aquarelas e três diagramas), três quadros, fontes, textos alternativos e resolução válidos.' + (' HTML: numeração 16.1–16.8 conferida.' if rendered else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rendered', action='store_true')
    check(parser.parse_args().rendered)
