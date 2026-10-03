#!/usr/bin/env python3
"""Compõe a aquarela existente com rótulos vetoriais e exporta o miolo em cinza."""
from pathlib import Path
from figure_style import write_svg
from render_figure import export_print
import base64
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'
SOURCE = ART / 'arte-cap1-01-v3.png'
SVG = ART / 'arte-cap1-01-diagrama.svg'
PRINT = ART / 'arte-cap1-01-diagrama-print.png'

def text_lines(x, y, lines, size=36, anchor='middle'):
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else 46}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}">{spans}</text>'

def card(key, top, lines):
    height = 140
    baseline = top + (height - (len(lines)-1)*46)/2 + 12
    return f'<g id="{key}"><rect x="145" y="{top}" width="400" height="{height}" rx="16" fill="white" stroke="#888" stroke-width="1.5"/>{text_lines(345, baseline, lines)}</g>'

encoded = base64.b64encode(SOURCE.read_bytes()).decode('ascii')
parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1500" height="1400" viewBox="0 0 1500 1400" role="img" aria-labelledby="title desc">
<title id="title">Do fenômeno ambiental à ação em saúde</title>
<desc id="desc">Cinco cenas hipotéticas em aquarela ilustram perigo, exposição, efeitos, resposta e proteção. As setas ligam perigo e proteção à exposição, exposição a efeitos e efeitos à resposta. Duas setas pontilhadas indicam a ação sobre exposição e proteção. As cenas se passam em bairro urbano com prédios residenciais, casas, comércio, calçadas e arborização.</desc>
<metadata>Composição editorial para Dados e Indicadores de Clima e Ambiente para a Saúde. Aquarela: ferramenta integrada image_gen; prompt em arte-cap1-01-v3.prompt.txt. Referência visual: assets/references/aquarela-grafite-nanquim.png, fornecida pelo autor. Montagem: scripts/build_cap1_art.py. Licença: a mesma dos textos autorais da obra.</metadata>
<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L10 4 L0 8 Z" fill="#555"/></marker></defs>
<rect width="1500" height="1400" fill="white"/>
<image x="560" y="65" width="930" height="1162.14" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{encoded}"/>
<g fill="none" stroke="#555" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)">
<path id="perigo-exposicao" d="M345 220 V375"/>
<path id="exposicao-efeitos" d="M345 515 V645"/>
<path id="efeitos-resposta" d="M345 785 V910"/>
<path id="protecao-exposicao" d="M145 1260 H30 V425 H145"/>
<path id="resposta-exposicao" d="M145 975 H100 V475 H145" stroke-dasharray="5 10"/>
<path id="resposta-protecao" d="M345 1050 V1190" stroke-dasharray="5 10"/>
</g>
<g font-family="Libertinus Serif, Georgia, serif" fill="#353535">''']
parts += [
    card('perigo', 80, ['Perigo ou condição', 'ambiental']),
    card('exposicao', 375, ['Quem e o que', 'está exposto?']),
    card('efeitos', 645, ['Efeitos sobre pessoas,', 'territórios e serviços']),
    card('resposta', 910, ['Vigilância, prevenção,', 'cuidado e resposta']),
    card('protecao', 1190, ['Vulnerabilidades e', 'capacidades de', 'proteção']),
    '<text x="84" y="955" transform="rotate(-90 84 955)" font-size="33" stroke="white" stroke-width="8" paint-order="stroke fill">Reduz risco e gera aprendizado</text>',
    '<rect x="165" y="1102" width="365" height="47" fill="white"/>',
    text_lines(345, 1134, ['Fortalece proteção'], size=34),
    text_lines(1040, 1330, ['Cenas hipotéticas', 'para leitura dos componentes'], size=30),
    '</g></svg>'
]
write_svg(SVG, '\n'.join(parts))
export_print(SVG, PRINT)
print(SVG.relative_to(ROOT))
print(PRINT.relative_to(ROOT))
