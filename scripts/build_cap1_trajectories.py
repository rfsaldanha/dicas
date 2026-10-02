#!/usr/bin/env python3
"""Compõe as trajetórias com vinhetas da aquarela e conexões editáveis."""
from pathlib import Path
import base64
import subprocess
import tempfile
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'
SOURCE = ART / 'arte-cap1-02-v1.png'
SVG = ART / 'arte-cap1-02-trajetorias.svg'
PRINT = ART / 'arte-cap1-02-trajetorias-print.png'


def label(x, y, lines, size=40, anchor='middle'):
    spans=''.join(f'<tspan x="{x}" dy="{0 if i==0 else 46}">{escape(t)}</tspan>' for i,t in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}">{spans}</text>'


def vignette(name, crop, x, y, w, h):
    # Recortes vetoriais reorganizam as cenas; o PNG gerado é preservado.
    cx, cy, cw, ch = crop
    scale = min(w / cw, h / ch)
    left, top = x + (w - cw * scale) / 2, y + (h - ch * scale) / 2
    return (f'<defs><clipPath id="clip-{name}" clipPathUnits="userSpaceOnUse">'
            f'<rect x="{left}" y="{top}" width="{cw * scale}" height="{ch * scale}"/>'
            f'</clipPath></defs><g id="{name}" clip-path="url(#clip-{name})">'
            f'<use xlink:href="#aquarela" transform="translate({left} {top}) scale({scale}) translate({-cx} {-cy})"/>'
            f'</g>')

encoded=base64.b64encode(SOURCE.read_bytes()).decode('ascii')
parts=[f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1600" height="1800" viewBox="0 0 1600 1800" role="img" aria-labelledby="title desc">
<title id="title">Trajetórias possíveis após uma inundação</title>
<desc id="desc">A inundação se ramifica em lesão, falha de energia e acesso e perda de moradia. A lesão pode exigir reabilitação. Falhas de serviços podem interromper o cuidado e, junto da perda de moradia, dificultar o acompanhamento. A retomada do tratamento e a recuperação da moradia são possibilidades de apoio. Uma seta pontilhada mostra um novo evento alcançando a família antes da recuperação. São caminhos possíveis, sem escala temporal fixa.</desc>
<metadata>Elaboração para esta obra. Ilustração: image_gen. Prompt: arte-cap1-02-v1.prompt.txt. Referência visual: aquarela-grafite-nanquim.png. Montagem: scripts/build_cap1_trajectories.py. Licença: a mesma dos textos autorais da obra.</metadata>
<defs>
<image id="aquarela" width="1536" height="1024" xlink:href="data:image/png;base64,{encoded}"/>
<marker id="arrow" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L12 5 L0 10 Z" fill="#555"/></marker>
</defs>
<rect width="1600" height="1800" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="#353535">''']
parts += [
    label(190,90,['Evento']),
    label(710,70,['Efeitos e','mediações']),
    label(1350,70,['Acompanhamento','e apoio']),
    label(200,255,['Caminhos possíveis;','podem coexistir'],size=36),
    vignette('inundacao',(0,225,543,438),10,580,340,300),
    vignette('lesao',(552,0,477,332),500,165,420,255),
    vignette('reabilitacao',(1040,0,496,340),1130,165,450,255),
    vignette('falha-servicos',(544,344,482,310),500,630,420,265),
    vignette('retomada',(1040,347,496,306),1130,630,450,265),
    vignette('perda-moradia',(538,667,489,291),500,1280,420,245),
    vignette('recuperacao-moradia',(1036,667,500,291),1130,1280,450,245),
    vignette('novo-evento',(0,665,543,292),10,1330,340,210),
    label(180,945,['Inundação']),
    label(710,480,['Lesão']),
    label(1350,480,['Reabilitação']),
    label(710,950,['Falha de energia/acesso'],size=38),
    label(710,1040,['Interrupção','do cuidado'],size=38),
    label(1350,950,['Retomada do tratamento'],size=34),
    label(710,1590,['Perda de moradia']),
    label(1350,1590,['Apoio à recuperação','da moradia'],size=38),
    label(190,1570,['Novo evento','antes da','recuperação'],size=36),
    '<rect x="1110" y="1110" width="475" height="126" rx="16" fill="white" stroke="#888" stroke-width="1.5"/>',
    label(1347,1160,['Dificuldades de','acompanhamento'],size=38),
    label(800,1722,['Início, persistência e repetição — sem escala de dias'],size=38),
    label(800,1770,['Processos graduais também podem iniciar trajetórias'],size=38),
    '</g>',
    '<g fill="none" stroke="#555" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)">',
    '<path id="inundacao-lesao" d="M350 720 H425 V285 H495"/>',
    '<path id="inundacao-servicos" d="M350 760 H495"/>',
    '<path id="inundacao-moradia" d="M350 800 H425 V1330 H495"/>',
    '<path id="lesao-reabilitacao" d="M925 285 H1120"/>',
    '<path id="servicos-interrupcao" d="M710 970 V1010"/>',
    '<path id="interrupcao-acompanhamento" d="M925 1040 H1015 V1144 H1105"/>',
    '<path id="moradia-acompanhamento" d="M925 1580 H1015 V1205 H1105"/>',
    '<path id="moradia-recuperacao" d="M1015 1580 H1120"/>',
    '<path id="apoio-tratamento" d="M1347 1105 V985"/>',
    '<path id="recorrencia" d="M350 1460 H495" stroke-dasharray="8 12"/>',
    '</g></svg>'
]
SVG.write_text('\n'.join(parts))
with tempfile.TemporaryDirectory(prefix='dicas-trajetorias-') as d:
    png=Path(d)/'composicao.png'
    subprocess.run(['inkscape',str(SVG),'--export-type=png','--export-width=2600','--export-filename='+str(png)],check=True)
    subprocess.run(['convert',str(png),'-background','white','-alpha','remove','-alpha','off','-colorspace','Gray','-depth','8','-define','png:color-type=0',str(PRINT)],check=True)
print(SVG.relative_to(ROOT))
print(PRINT.relative_to(ROOT))
