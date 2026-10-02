#!/usr/bin/env python3
"""Monta as aquarelas conceituais finais do capítulo 1, sem alterar os originais."""
from pathlib import Path
import base64
import subprocess
import tempfile
import sys
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'


def label(x, y, lines, size=48, step=54):
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(line)}</tspan>'
                    for i, line in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}">{spans}</text>'


def vignette(name, crop, x, y, w, h):
    cx, cy, cw, ch = crop
    scale = min(w / cw, h / ch)
    left, top = x + (w - cw * scale) / 2, y + (h - ch * scale) / 2
    return (f'<defs><clipPath id="clip-{name}" clipPathUnits="userSpaceOnUse">'
            f'<rect x="{left}" y="{top}" width="{cw * scale}" height="{ch * scale}"/>'
            f'</clipPath></defs><g id="{name}" clip-path="url(#clip-{name})">'
            f'<use xlink:href="#aquarela" transform="translate({left} {top}) scale({scale}) translate({-cx} {-cy})"/>'
            f'</g>')


def compose(number):
    source = ART / f'arte-cap1-{number}-v1.png'
    from PIL import Image
    with Image.open(source) as im:
        sw, sh = im.size
    if number == '04':
        slug, title, width, height = 'dose', 'Da medida ambiental à dose absorvida', 1800, 1810
        desc = ('Quatro perguntas distintas sobre água: o que foi medido, quem pode acessar a água, '
                'se houve consumo e quanto do contaminante atravessou as barreiras do organismo. '
                'As vinhetas não são ligadas por setas: uma etapa não comprova a seguinte.')
        parts = [
            label(450, 60, ['Medida ambiental'], size=52),
            label(1350, 60, ['Exposição potencial'], size=52),
            vignette('coleta', (0, 0, 760, 501), 20, 100, 840, 540),
            vignette('rede', (768, 0, 768, 504), 940, 100, 840, 540),
            label(450, 705, ['O que foi medido', 'na água?']),
            label(1350, 705, ['Quem pode acessar', 'essa água?']),
            label(450, 855, ['Contato individual'], size=52),
            label(1350, 855, ['Dose absorvida'], size=52),
            vignette('contato', (0, 506, 755, 518), 20, 890, 840, 540),
            vignette('organismo', (780, 505, 540, 519), 940, 890, 840, 540),
            label(450, 1495, ['Houve consumo?', 'Quanto e quando?']),
            label(1350, 1495, ['Quanto do contaminante', 'atravessou as barreiras', 'do organismo?']),
            label(900, 1728, ['Uma etapa não comprova a seguinte']),
            label(900, 1780, ['A absorção requer informação própria.'], size=40),
        ]
    elif number == '05':
        slug, title, width, height = 'territorios', 'O mesmo perigo pode produzir riscos diferentes', 1800, 1900
        desc = ('Dois territórios hipotéticos enfrentam o mesmo episódio de calor. No primeiro, '
                'sombra, ventilação, água regular, apoio e serviços preparados favorecem a proteção. '
                'No segundo, pouca sombra, trabalho externo intenso, moradias quentes, água distante '
                'e serviços frágeis aumentam as barreiras, embora exista apoio entre vizinhos. '
                'Condições favoráveis e desfavoráveis podem coexistir.')
        parts = [
            label(900, 65, ['Mesmo episódio de calor'], size=56),
            label(450, 160, ['Território A'], size=52),
            label(1350, 160, ['Território B'], size=52),
            vignette('territorios', (0, 0, sw, sh), 10, 200, 1780, 1187),
            label(450, 1440, ['Mais sombra e ventilação', 'Água regular',
                              'Serviços preparados e apoio'], size=44, step=50),
            label(1350, 1440, ['Pouca sombra; moradias quentes', 'Trabalho externo intenso',
                               'Água distante e serviços frágeis'], size=44, step=50),
            label(450, 1630, ['Maior capacidade', 'de proteção'], size=52),
            label(1350, 1630, ['Maior exposição e menor', 'capacidade de proteção'], size=52),
            label(900, 1800, ['Territórios hipotéticos. Condições favoráveis e',
                              'desfavoráveis podem coexistir.'], size=42, step=50),
        ]
    elif number == '06':
        slug, title, width, height = 'justica', 'Quatro perguntas da justiça ambiental e climática', 1800, 1760
        desc = ('Quatro cenas com o mesmo destaque: moradores observam diferenças de sombra, água e '
                'acesso ao cuidado; uma reunião inclui moradores, trabalhadores, técnica e pessoa '
                'com deficiência; conhecimento local é compartilhado numa caminhada; pessoas de '
                'diferentes gerações discutem proteção diante de fontes de emissão da produção e '
                'do transporte. Não há inventário de emissões ou atribuição de quantidades.')
        parts = [
            label(450, 60, ['Distribuição'], size=52),
            label(1350, 60, ['Participação'], size=52),
            vignette('distribuicao', (0, 0, 758, 480), 20, 100, 840, 540),
            vignette('participacao', (767, 0, 769, 480), 940, 100, 840, 540),
            label(450, 705, ['Quem recebe danos', 'e proteção?']),
            label(1350, 705, ['Quem participa', 'das decisões?']),
            label(450, 870, ['Reconhecimento'], size=52),
            label(1350, 870, ['Responsabilidades'], size=52),
            vignette('reconhecimento', (0, 510, 758, 499), 20, 900, 840, 540),
            vignette('responsabilidades', (767, 510, 769, 499), 940, 900, 840, 540),
            label(450, 1505, ['Quais conhecimentos', 'são reconhecidos?']),
            label(1350, 1505, ['Quem contribui para o problema', 'e quem arca com os custos?'], size=46),
            label(900, 1710, ['Exemplos conceituais; sem quantificação de emissões ou custos.'], size=40),
        ]
    else:
        raise SystemExit('Arte ainda não configurada: '+number)
    source = ART / f'arte-cap1-{number}-v1.png'
    encoded = base64.b64encode(source.read_bytes()).decode('ascii')
    svg = ART / f'arte-cap1-{number}-{slug}.svg'
    out = ART / f'arte-cap1-{number}-{slug}-print.png'
    document = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<metadata>Elaboração para esta obra. Ilustração: ferramenta integrada image_gen. Prompt: arte-cap1-{number}-v1.prompt.txt. Referência: aquarela-grafite-nanquim.png, fornecida pelo autor. Montagem: scripts/build_cap1_remaining_art.py {number}. Licença: a mesma dos textos autorais da obra.</metadata>
<defs><image id="aquarela" width="{sw}" height="{sh}" xlink:href="data:image/png;base64,{encoded}"/></defs>
<rect width="{width}" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="#353535">'''
    svg.write_text(document + '\n'.join(parts) + '</g></svg>')
    with tempfile.TemporaryDirectory(prefix='dicas-cap1-art-') as folder:
        rgba = Path(folder) / 'composicao.png'
        subprocess.run(['inkscape', str(svg), '--export-type=png', '--export-width=2700',
                        '--export-filename='+str(rgba)], check=True)
        subprocess.run(['convert', str(rgba), '-background', 'white', '-alpha', 'remove',
                        '-alpha', 'off', '-colorspace', 'Gray', '-depth', '8',
                        '-define', 'png:color-type=0', str(out)], check=True)
    print(svg.relative_to(ROOT))
    print(out.relative_to(ROOT))


if __name__ == '__main__':
    compose(sys.argv[1])
