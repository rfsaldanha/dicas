#!/usr/bin/env python3
"""Compõe as sete aquarelas do capítulo 2 com textos e relações editáveis."""
from pathlib import Path
from xml.sax.saxutils import escape
import base64
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'


def label(x, y, lines, size=46, step=54, weight='normal'):
    if isinstance(lines, str):
        lines = [lines]
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" font-weight="{weight}">{spans}</text>'


def picture(name, crop, x, y, w, h):
    cx, cy, cw, ch = crop
    scale = min(w / cw, h / ch)
    left, top = x + (w - cw * scale) / 2, y + (h - ch * scale) / 2
    return (f'<defs><clipPath id="clip-{name}" clipPathUnits="userSpaceOnUse"><rect x="{left}" y="{top}" width="{cw*scale}" height="{ch*scale}"/></clipPath></defs>'
            f'<g id="{name}" clip-path="url(#clip-{name})"><use xlink:href="#aquarela" transform="translate({left} {top}) scale({scale}) translate({-cx} {-cy})"/></g>')


def line(d, dashed=False, arrow=True):
    dash = ' stroke-dasharray="9 11"' if dashed else ''
    marker = ' marker-end="url(#arrow)"' if arrow else ''
    return f'<path d="{d}" fill="none" stroke="#555" stroke-width="3.5" stroke-linejoin="round"{dash}{marker}/>'


def box(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="white" stroke="#888" stroke-width="2"/>'


def layout(number, sw, sh):
    if number == '01':
        slug, title, width, height = 'referencias', 'Duas finalidades para escolher a referência climática', 1800, 1810
        desc = ('Duas equipes ilustram a comparação com uma base histórica fixa e o planejamento com uma normal recente. '
                'Ambas exigem documentar período e método e avaliar exposição, vulnerabilidade e capacidade de resposta. '
                'Referência estatística não é limite de segurança. Cenas conceituais, sem dados observados.')
        parts = [
            label(900, 65, 'Séries climáticas documentadas', 52),
            line('M900 95 V120 H450 V150'), line('M900 120 H1350 V150'),
            label(450, 205, 'Comparar com o passado', 48),
            label(1350, 205, 'Caracterizar um período recente', 48),
            picture('duas-equipes', (0, 80, sw, 820), 20, 245, 1760, 940),
            label(450, 1215, 'Base histórica mantida fixa', 46, weight='bold'),
            label(1350, 1215, 'Normal climatológica recente', 46, weight='bold'),
            label(450, 1285, ['Como as condições mudaram', 'em relação à mesma referência?'], 43),
            label(1350, 1285, ['Que condições descrevem o período', 'usado no planejamento?'], 43),
            line('M450 1370 V1420 H900', arrow=False), line('M1350 1370 V1420 H900 V1480'),
            box(120, 1500, 1560, 140),
            label(900, 1555, 'Documentar período e método', 48),
            label(900, 1610, 'Avaliar exposição, vulnerabilidade e capacidade de resposta', 43),
            label(900, 1715, 'Referência estatística não é limite de segurança', 46),
            label(900, 1780, 'Finalidades complementares. Esquema conceitual, sem dados observados.', 38),
        ]
    elif number == '02':
        slug, title, width, height = 'cascatas', 'Eventos combinados e efeitos em cascata', 1800, 2070
        desc = ('À esquerda, calor e fumaça atingem um bairro hipotético ao mesmo tempo. À direita, uma inundação se ramifica em interrupção de acesso e falha de energia, comprometendo chegada de equipes e insumos, equipamentos e comunicação. Os caminhos convergem na redução da capacidade operacional de uma unidade com prédio intacto.')
        parts = [
            label(450, 65, 'Eventos combinados', 54), label(1350, 65, 'Efeitos em cascata', 54),
            picture('dois-paineis', (0, 0, sw, sh), 20, 110, 1760, 1174),
            label(450, 1370, ['Calor e fumaça', 'podem coincidir'], 50),
            label(450, 1535, ['Combinações também podem', 'ocorrer em sequência.'], 44),
            label(450, 1740, ['Não se presume uma soma', 'dos efeitos isolados.'], 42),
            label(1350, 1360, 'Inundação', 48),
            line('M1350 1390 V1420 H1110 V1450'), line('M1350 1420 H1600 V1450'),
            label(1110, 1500, ['Acesso', 'interrompido'], 44),
            label(1600, 1500, ['Falha de', 'energia'], 44),
            line('M1110 1585 V1615'), line('M1600 1585 V1600'),
            label(1110, 1670, ['Equipes e insumos', 'não chegam'], 40),
            label(1600, 1640, ['Equipamentos', 'e comunicação', 'afetados'], 40, step=48),
            line('M1110 1750 V1790 H1350', arrow=False), line('M1600 1750 V1790 H1350 V1830'),
            label(1350, 1885, ['Capacidade operacional', 'reduzida'], 44),
            label(900, 2010, 'Prédio intacto não garante serviço funcionando. Caminhos hipotéticos.', 40),
        ]
    elif number == '07':
        slug, title, width, height = 'grades', 'Dados em grade: organização e limites de interpretação', 1800, 1840
        desc = ('Três cenas distinguem uma estação meteorológica, uma malha sobre um território hipotético e ambientes diversos dentro de uma célula. A malha não pressupõe instrumento em cada célula nem valor idêntico em cada residência. Camadas ilustram momentos distintos, sem temperaturas ou escala quantitativa.')
        parts = [
            label(300, 60, ['Observação', 'em um ponto'], 47),
            label(900, 60, ['Valores organizados', 'em uma malha'], 47),
            label(1500, 60, ['Ambientes dentro', 'de uma célula'], 47),
            picture('territorio', (0, 0, sw, 700), 20, 150, 1760, 805),
            '<rect x="660" y="220" width="480" height="600" fill="white" fill-opacity="0.12" stroke="#333" stroke-width="3"/>',
        ]
        for x in range(780, 1140, 120):
            parts.append(line(f'M{x} 220 V820', arrow=False))
        for y in range(340, 820, 120):
            parts.append(line(f'M660 {y} H1140', arrow=False))
        parts += [
            '<rect x="900" y="460" width="120" height="120" fill="none" stroke="#222" stroke-width="7"/>',
            line('M1020 460 L1240 350', dashed=True, arrow=False),
            label(900, 1025, 'O método de produção varia conforme o produto.', 44),
            box(130, 1075, 1540, 185),
            label(900, 1140, ['O valor pode representar um ponto, uma média', 'ou outra operação: conferir os metadados.'], 46),
            label(900, 1340, 'Momentos distintos de uma mesma variável', 48),
            picture('camadas-temporais', (0, 715, sw, 230), 30, 1380, 1740, 265),
            label(900, 1700, 'Célula não é medição em cada residência. Mais zoom não cria observações.', 41),
            label(900, 1790, 'Território hipotético; cores ilustrativas, sem valores de temperatura.', 39),
        ]
    else:
        raise SystemExit('Arte ainda não configurada: ' + number)
    return slug, title, width, height, desc, parts


def compose(number):
    source = ART / f'arte-cap2-{number}-v1.png'
    data = source.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    sw, sh = struct.unpack('>II', data[16:24])
    slug, title, width, height, desc, parts = layout(number, sw, sh)
    encoded = base64.b64encode(data).decode('ascii')
    svg = ART / f'arte-cap2-{number}-{slug}.svg'
    out = ART / f'arte-cap2-{number}-{slug}-print.png'
    document = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<metadata>Elaboração para esta obra. Ilustração: ferramenta integrada image_gen. Prompt: arte-cap2-{number}-v1.prompt.txt. Referência visual: aquarela-grafite-nanquim.png, fornecida pelo autor e apresentada na conversa. Montagem: scripts/build_cap2_art.py {number}. Licença: a mesma dos textos autorais da obra.</metadata>
<defs><image id="aquarela" width="{sw}" height="{sh}" xlink:href="data:image/png;base64,{encoded}"/><marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="#555"/></marker></defs>
<rect width="{width}" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="#353535">'''
    svg.write_text(document + '\n'.join(parts) + '</g></svg>\n')
    with tempfile.TemporaryDirectory(prefix='dicas-cap2-art-') as folder:
        rgba = Path(folder) / 'composicao.png'
        subprocess.run(['inkscape', str(svg), '--export-type=png', '--export-width=2700', '--export-filename=' + str(rgba)], check=True)
        subprocess.run(['convert', str(rgba), '-background', 'white', '-alpha', 'remove', '-alpha', 'off', '-colorspace', 'Gray', '-depth', '8', '-define', 'png:color-type=0', str(out)], check=True)
    print(svg.relative_to(ROOT))
    print(out.relative_to(ROOT))


if __name__ == '__main__':
    compose(sys.argv[1])
