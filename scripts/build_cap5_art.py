#!/usr/bin/env python3
"""Compõe três artes do capítulo 5 a partir dos originais gerados sequencialmente.

Uso: python3 scripts/build_cap5_art.py [01 02 03]
Preserva as cenas originais; textos e conexões permanecem editáveis no SVG.
"""
from pathlib import Path
from figure_style import write_svg
from render_figure import export_print
from xml.sax.saxutils import escape
import base64
import json
import struct
import sys

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'
MANIFEST = json.loads((ART / 'arte-cap5-manifest.json').read_text())


def text(x, y, lines, size=48, step=57):
    if isinstance(lines, str):
        lines = [lines]
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(s)}</tspan>' for i, s in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}">{spans}</text>'


def box(x, y, w, h, fill='white'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="#66706b" stroke-width="2.5"/>'


def arrow(d):
    return f'<path d="{d}" fill="none" stroke="#4c5553" stroke-width="3.5" stroke-linejoin="round" marker-end="url(#arrow)"/>'


def picture(x, y, w, h, sw, sh):
    scale = min(w / sw, h / sh)
    x += (w-sw*scale)/2
    y += (h-sh*scale)/2
    return f'<use xlink:href="#aquarela" transform="translate({x} {y}) scale({scale})"/>'


def layout(number, sw, sh):
    p = []
    if number == '01':
        height = 1720
        p.append(picture(20, 40, 760, 1490, sw, sh))
        rows = [
            ('Instituição responsável', 'Quem produz, mantém e distribui?'),
            ('Programa ou sistema', 'Para qual finalidade se registra?'),
            ('Produto e versão', 'Qual conjunto foi utilizado?'),
            ('Variável', 'Qual definição, código e unidade?'),
            ('Via de acesso', 'Por qual arquivo, serviço ou painel?'),
            ('Extração datada', 'Quais filtros, arquivos e parâmetros?'),
        ]
        for i, (title, detail) in enumerate(rows):
            y = 50 + i*245
            p += [box(815, y, 920, 185), text(1275, y+72, title, 52), text(1275, y+137, detail, 43)]
            if i < 5:
                p.append(arrow(f'M1275 {y+185} V{y+230}'))
        p += [text(900, 1580, 'As setas indicam detalhamento da documentação.', 45),
              text(900, 1645, 'Os níveis podem envolver diferentes organizações.', 43)]
    elif number == '02':
        height = 1860
        p += [box(60, 30, 1680, 160, '#f1f4f1'),
              text(900, 91, 'Pergunta e requisitos de uso', 55),
              text(900, 151, 'Variável, território, período e atraso aceitável', 44),
              arrow('M1230 190 V255'),
              box(760, 275, 940, 185), text(1230, 340, 'Examinar fontes candidatas', 51),
              text(1230, 407, 'Conceito, cobertura, acesso e metadados', 42),
              arrow('M760 368 H615'),
              box(60, 300, 540, 280, '#f8f4ef'),text(330, 365, 'Não atende', 49),
              text(330, 435, ['Buscar outra fonte','ou rever a pergunta','com justificativa'], 43, 55),
              arrow('M330 300 V235 H390 V202'),
              '<path d="M1230 460 V481" fill="none" stroke="#4c5553" stroke-width="3.5"/>',
              text(1225, 534, 'Atende aos requisitos', 43), arrow('M1230 552 V592'),
              picture(35, 630, 710, 1040, sw, sh),
              box(790, 610, 910, 175),text(1245, 678, 'Fontes elegíveis', 53),
              text(1245, 742, 'Comparar alternativas adequadas', 43),
              arrow('M1245 785 V858'),
              box(790, 875, 910, 210),text(1245, 940, 'Avaliar vantagens e limites', 51),
              text(1245, 1003, ['Atraso, resolução, estabilidade','e manutenção'], 44, 55),
              arrow('M1245 1085 V1153'),
              box(790, 1170, 910, 200),text(1245, 1237, 'Escolher e justificar', 53),
              text(1245, 1298, ['Registrar também alternativas','descartadas e suas razões'], 43, 53),
              arrow('M1245 1370 V1442'),
              box(790, 1460, 910, 205, '#f1f4f1'),text(1245, 1523, 'Documentar na ficha', 52),
              text(1245, 1585, ['Produto, edição, função da fonte','e condições de uso'], 43, 53),
              text(900, 1775, 'Vantagens não compensam requisitos indispensáveis ausentes.', 43)]
    elif number == '03':
        height = 1950
        p.append(picture(25, 85, 760, 1520, sw, sh))
        rows = [
            ('Fonte e versão', 'Identificar o produto de entrada'),
            ('Extração datada', 'Registrar consulta, filtros e arquivos'),
            ('Originais preservados', 'Guardar cópias permitidas e manifesto'),
            ('Tratamento e qualidade', 'Documentar conversões e exclusões'),
            ('Cálculo especificado', 'Guardar código, regras e parâmetros'),
            ('Validação', 'Examinar método, dados e interpretação'),
            ('Publicação e uso', 'Vincular resultado, versão e finalidade'),
            ('Revisão', 'Registrar mudanças e avaliar recálculo'),
        ]
        for i, (title, detail) in enumerate(rows):
            y = 35 + i*208
            p += [box(815, y, 880, 158), text(1255, y+63, title, 50), text(1255, y+120, detail, 40)]
            if i < 7:
                p.append(arrow(f'M1255 {y+158} V{y+195}'))
        p += [arrow('M1695 1565 H1760 V114 H1710'),
              box(50, 1700, 1660, 155, '#f1f4f1'),
              text(880, 1760, 'Documentação em todas as etapas', 51),
              text(880, 1820, 'Entradas, operações, decisões e responsáveis', 44),
              text(900, 1910, 'Revisões podem exigir nova extração e recálculo.', 42)]
    else:
        raise ValueError(number)
    return 1800, height, p


def compose(a):
    data = (ART / a['source']).read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Original não é PNG: ' + a['source'])
    sw, sh = struct.unpack('>II', data[16:24])
    width, height, parts = layout(a['number'], sw, sh)
    encoded = base64.b64encode(data).decode('ascii')
    metadata = (f"Elaboração para esta obra. Ferramenta integrada image_gen; versão não informada. "
                f"Prompt: {a['prompt']}. Referência de estilo: aquarela-grafite-nanquim.png, fornecida junto do original à ferramenta de edição. "
                f"Geração sequencial: {a['generation_order']} de 3. Composição editorial: rótulos e setas editáveis; "
                f"exportação em escala de cinza com Chromium e ImageMagick. Revisão técnica e visual pelo assistente; revisão do autor pendente. "
                f"Reprodução: python3 scripts/build_cap5_art.py {a['number']}. Arquivos autorais: GPL-3.0.")
    svg = ART / a['svg']
    write_svg(svg, f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(a['title'])}</title><desc id="desc">{escape(a['alt'])}</desc>
<metadata>{escape(metadata)}</metadata>
<defs><image id="aquarela" width="{sw}" height="{sh}" xlink:href="data:image/png;base64,{encoded}"/>
<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="#4c5553"/></marker></defs>
<rect width="{width}" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="#303b36">''' + '\n'.join(parts) + '</g></svg>\n')
    export_print(svg, ART/a['print'])
    print(svg.relative_to(ROOT), flush=True)


if __name__ == '__main__':
    for number in sys.argv[1:] or [a['number'] for a in MANIFEST]:
        compose(next(a for a in MANIFEST if a['number'] == number))
