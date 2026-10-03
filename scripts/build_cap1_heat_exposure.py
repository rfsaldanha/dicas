#!/usr/bin/env python3
"""Compõe as quatro vinhetas de exposição ao calor com rótulos editáveis."""
from pathlib import Path
from figure_style import write_svg
from render_figure import export_print
import base64
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'
SOURCE = ART / 'arte-cap1-03-v2.png'
SVG = ART / 'arte-cap1-03-exposicao.svg'
PRINT = ART / 'arte-cap1-03-exposicao-print.png'


def label(x, y, lines, size=46, step=50):
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(line)}</tspan>'
                    for i, line in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}">{spans}</text>'


encoded = base64.b64encode(SOURCE.read_bytes()).decode('ascii')
parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1800" height="1390" viewBox="0 0 1800 1390" role="img" aria-labelledby="title desc">
<title id="title">Uma pessoa, diferentes condições térmicas</title>
<desc id="desc">Quatro vinhetas em bairro urbano misto, com edifícios, casas, calçadas e praça, acompanham a mesma mulher: saída de casa pela manhã, caminhada sob sol intenso, trabalho físico e pausa à sombra com água, e repouso em casa à noite com calor retido. A estação meteorológica mede em um ponto, enquanto a exposição depende dos ambientes, períodos, duração, atividade e proteção ao longo do percurso. A sequência é didática, sem duração medida.</desc>
<metadata>Elaboração para esta obra. Ilustração: ferramenta integrada image_gen. Prompt: arte-cap1-03-v2.prompt.txt. Referência visual: aquarela-grafite-nanquim.png, fornecida pelo autor. Montagem: scripts/build_cap1_heat_exposure.py. Licença: a mesma dos textos autorais da obra.</metadata>
<defs><marker id="arrow" markerWidth="11" markerHeight="9" refX="10" refY="4.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L11 4.5 L0 9 Z" fill="#555"/></marker></defs>
<rect width="1800" height="1390" fill="white"/>
<image x="20" y="160" width="1760" height="880" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{encoded}"/>
<path d="M220 115 H130 V350" fill="none" stroke="#555" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="#353535">''']
parts += [
    label(240, 50, ['Medição em', 'um ponto']),
    label(240, 1070, ['Manhã'], size=48),
    label(675, 1070, ['Deslocamento'], size=48),
    label(1110, 1070, ['Trabalho e pausas'], size=48),
    label(1545, 1070, ['Noite'], size=48),
    label(240, 1125, ['Residência e entorno'], size=40),
    label(675, 1125, ['Rua sob sol intenso'], size=40),
    label(1110, 1125, ['Esforço e proteção'], size=40),
    label(1545, 1125, ['Calor retido'], size=40),
    label(900, 1230, ['A exposição depende de local, horário, duração,',
                      'atividade e condições ambientais'], size=46, step=54),
    label(900, 1350, ['Sequência didática; as larguras não representam durações medidas.'], size=36),
    '</g></svg>'
]
write_svg(SVG, '\n'.join(parts))
export_print(SVG, PRINT)
print(SVG.relative_to(ROOT))
print(PRINT.relative_to(ROOT))
