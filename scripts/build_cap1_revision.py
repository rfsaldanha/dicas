#!/usr/bin/env python3
"""Compõe as seis figuras da revisão do capítulo 1; mantém textos editáveis."""
import base64
import json
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image
from figure_style import write_svg
from render_figure import export_print

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'
INK, GREEN, BLUE, TERRA = '#303B36', '#536B50', '#597482', '#AE6B50'
RECORDS = []


def label(x, y, lines, size=46, step=54, anchor='middle', weight=400, fill=INK):
    if isinstance(lines, str):
        lines = [lines]
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(line)}</tspan>'
                    for i, line in enumerate(lines))
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}">{spans}</text>')


def raster(number, x, y, width, height, crop=None):
    source = ART / f'arte-cap1-{number}-v1.png'
    sw, sh = Image.open(source).size
    if crop is None:
        crop = (0, 0, sw, sh)
    cx, cy, cw, ch = crop
    return (f'<svg x="{x}" y="{y}" width="{width}" height="{height}" '
            f'viewBox="{cx} {cy} {cw} {ch}" overflow="hidden">'
            f'<use href="#aquarela-{number}"/></svg>')


def save(number, slug, identifier, title, alt, height, parts, *, watercolor=False,
         print_width='100%', source=None):
    basename = f'arte-cap1-{number}-{slug}'
    metadata = {
        'id': identifier, 'number': number, 'svg': basename + '.svg',
        'print': basename + '-print.png', 'title': title, 'alt': alt,
        'print_width': print_width, 'watercolor': watercolor,
        'composition': 'scripts/build_cap1_revision.py',
        'license': 'GPL-3.0 para a composição autoral; referências mantêm suas condições de uso.',
    }
    image_definition = ''
    if watercolor:
        metadata.update(raster=f'arte-cap1-{number}-v1.png',
                        prompt=f'arte-cap1-{number}-v1.prompt.txt',
                        tool='image_gen; versão não informada',
                        reference='assets/references/aquarela-grafite-nanquim.png')
        original = ART / metadata['raster']
        sw, sh = Image.open(original).size
        encoded = base64.b64encode(original.read_bytes()).decode('ascii')
        image_definition = (f'<image id="aquarela-{number}" width="{sw}" height="{sh}" '
                            f'href="data:image/png;base64,{encoded}"/>')
        print_mm = 120 * float(print_width.rstrip('%')) / 100
        raster_mm = print_mm * 800 / 1800 if number == '12' else print_mm
        raster_pixels = sw / 2 if number == '12' else sw
        metadata.update(source_pixels=[sw, sh], max_print_width_mm=print_mm,
                        min_effective_raster_ppi=round(raster_pixels / (raster_mm / 25.4), 1))
    if source:
        metadata['source'] = source
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{height}" viewBox="0 0 1800 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(alt)}</desc>
<metadata>{escape(json.dumps(metadata, ensure_ascii=False))}</metadata>
<defs>{image_definition}<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="{INK}"/></marker></defs>
<rect width="1800" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="{INK}">
{''.join(parts)}
</g></svg>'''
    write_svg(ART / metadata['svg'], svg)
    export_print(ART / metadata['svg'], ART / metadata['print'], require_raster=watercolor)
    RECORDS.append(metadata)
    print(basename, flush=True)


def compose():
    parts = [raster('07', 0, 120, 1800, 768)]
    for x, heading, lines in [
        (300, 'Tempo meteorológico', ['O que ocorre agora?', 'Horas e dias']),
        (900, 'Clima', ['Como varia e se repete?', 'Séries de muitos anos']),
        (1500, 'Ambiente', ['Em que condições se vive?', 'Natureza e infraestrutura']),
    ]:
        parts += [label(x, 65, heading, size=52, weight=700), label(x, 960, lines, size=43)]
    parts += [label(900, 1140, ['O mesmo território, três perguntas.',
                              'O clima exige séries históricas; as cenas são apenas ilustrativas.'], size=42)]
    save('07', 'tempo-clima-ambiente', 'fig-tempo-clima-ambiente',
         'Tempo, clima e ambiente: três leituras do mesmo território',
         'Três painéis em aquarela mostram um bairro hipotético. À esquerda, chuva em um momento; '
         'no centro, vistas repetidas da mesma rua sob chuva, sol e vento; à direita, rio, vegetação, '
         'moradias, prédios e serviços. Os rótulos distinguem condições do momento, padrões em séries '
         'históricas e condições naturais e construídas. As três vistas centrais não constituem uma série climática.',
         1260, parts, watercolor=True)

    parts = [
        '<rect x="250" y="180" width="740" height="320" fill="#F3F0E8"/>',
        '<rect x="990" y="180" width="740" height="320" fill="#EEF2EE"/>',
        '<rect x="250" y="500" width="740" height="320" fill="#F3F5F6"/>',
        '<rect x="990" y="500" width="740" height="320" fill="#F6EFEB"/>',
        f'<path d="M250 500 H1760 M990 820 V140" fill="none" stroke="{INK}" stroke-width="4"/>',
        label(620, 75, ['Imediatos ou', 'de curto prazo'], size=49, weight=700),
        label(1360, 75, ['Prolongados ou', 'cumulativos'], size=49, weight=700),
        label(225, 330, 'Direto', anchor='end', size=49, weight=700),
        label(225, 660, 'Indireto', anchor='end', size=49, weight=700),
        '<text x="28" y="500" transform="rotate(-90 28 500)" text-anchor="middle" font-size="40">Mecanismo predominante</text>',
        label(620, 305, ['Trauma pela', 'ação da água']),
        label(1360, 305, ['Sequela persistente', 'do trauma']),
        label(620, 630, ['Interrupção do cuidado', 'por falta de energia']),
        label(1360, 630, ['Agravamento associado à', 'interrupção de tratamentos']),
        label(990, 905, 'Temporalidade predominante', size=48, weight=700),
        label(900, 1005, ['Domínios analíticos, sem escala quantitativa ou sequência obrigatória.',
                          'Um efeito prolongado pode começar durante o evento.'], size=42),
    ]
    save('08', 'quadrantes', 'fig-quadrantes-impacto',
         'Mecanismo e temporalidade: dois eixos para analisar os impactos',
         'Gráfico de quatro quadrantes sem escala numérica. Na horizontal, efeitos imediatos ou de curto prazo '
         'à esquerda e prolongados ou cumulativos à direita; na vertical, mecanismo direto acima e indireto abaixo. '
         'Os exemplos são trauma pela água, sequela do trauma, interrupção do cuidado por falta de energia '
         'e agravamento associado à interrupção de tratamentos. Não há sequência obrigatória entre quadrantes.',
         1130, parts)

    # Curvas de Bézier editoriais: não representam estimativas, dados ou funções ajustadas.
    parts = [
        label(900, 62, 'Impactos e necessidades de resposta podem se sobrepor', size=49, weight=700),
        f'<path d="M150 130 V700 H1740" fill="none" stroke="{INK}" stroke-width="4" marker-end="url(#arrow)"/>',
        f'<path d="M150 700 V130" fill="none" stroke="{INK}" stroke-width="4" marker-end="url(#arrow)"/>',
        '<text x="65" y="400" transform="rotate(-90 65 400)" text-anchor="middle" font-size="48">Impactos</text>',
        f'<path d="M160 680 C185 440 205 210 330 230 C430 245 500 540 730 640 C940 680 1250 675 1720 682" fill="none" stroke="{TERRA}" stroke-width="8"/>',
        f'<path d="M160 680 C320 675 360 605 560 430 S840 315 1030 490 S1400 630 1720 666" fill="none" stroke="{BLUE}" stroke-width="8" stroke-dasharray="24 14"/>',
        f'<path d="M160 682 C310 673 550 610 740 540 S1100 325 1340 280 S1550 285 1720 305" fill="none" stroke="{GREEN}" stroke-width="8" stroke-dasharray="4 16" stroke-linecap="round"/>',
        label(360, 192, 'A', size=52, weight=700, fill=TERRA),
        label(800, 287, 'B', size=52, weight=700, fill=BLUE),
        label(1400, 238, 'C', size=52, weight=700, fill=GREEN),
        label(425, 773, 'Horas–dias', size=48, weight=700),
        label(940, 773, 'Semanas–meses', size=48, weight=700),
        label(1460, 773, 'Meses–anos', size=48, weight=700),
        label(950, 848, 'Escala temporal', size=48),
    ]
    for x, color, key, lines, dash in [
        (325, TERRA, 'A', ['Resgate e socorro', 'Traumas agudos e óbitos'], ''),
        (900, BLUE, 'B', ['Cuidado e vigilância de', 'doenças transmissíveis', 'e não transmissíveis', 'Retomada dos serviços'], '24 14'),
        (1475, GREEN, 'C', ['Cuidado e vigilância de', 'condições crônicas e', 'efeitos psicossociais', 'Reabilitação e reconstrução'], '4 16'),
    ]:
        parts += [f'<path d="M{x-100} 925 H{x+15}" stroke="{color}" stroke-width="8" stroke-dasharray="{dash}" stroke-linecap="round"/>',
                  label(x+55, 940, key, size=49, weight=700, fill=color), label(x, 1010, lines, size=42, step=50)]
    parts += [label(900, 1280, ['Curvas acrescentadas nesta adaptação: não são dados observados.',
                               'Alturas, durações e espaçamentos não têm escala quantitativa.'], size=42)]
    save('09', 'curvas-impacto', 'fig-curvas-impacto-desastres',
         'Impactos e respostas em diferentes tempos após um desastre',
         'Esquema com eixo vertical Impactos e horizontal Escala temporal, sem valores numéricos. '
         'Três curvas editoriais se sobrepõem: A, contínua, destaca resgate, trauma e óbitos; B, tracejada, '
         'cuidado e vigilância de doenças transmissíveis e não transmissíveis e retomada dos serviços; '
         'C, pontilhada, condições crônicas, efeitos psicossociais, reabilitação e reconstrução. '
         'Os horizontes são horas a dias, semanas a meses e meses a anos. As curvas foram acrescentadas '
         'ao esquema temporal de Freitas et al. (2014), não são dados observados e não definem limites universais.',
         1410, parts, source={'citation': 'freitas2014desastres', 'figure': 1,
             'doi': '10.1590/1413-81232014199.00732014',
             'antecedent': 'Redmond (2005), DOI 10.1136/bmj.330.7502.1259, citado por Freitas et al.',
             'adaptation': 'Composição autoral baseada no conceito; curvas didáticas acrescentadas. '
                           'A figura publicada contém blocos temporais, sem curvas. Não reproduz a imagem original.'})

    parts = []
    for cx, cy, color, dash in [(650, 450, TERRA, ''), (1150, 450, BLUE, '20 12'), (900, 820, GREEN, '4 12')]:
        parts += [f'<circle cx="{cx}" cy="{cy}" r="370" fill="{color}" fill-opacity="0.13" stroke="{color}" stroke-width="5" stroke-dasharray="{dash}"/>']
    parts += [
        label(585, 310, 'Perigo', size=57, weight=700),
        label(585, 373, ['Evento ou condição', 'capaz de causar dano'], size=42, step=50),
        label(1215, 310, 'Exposição', size=57, weight=700),
        label(1215, 373, ['Presença de pessoas,', 'bens e serviços'], size=42, step=50),
        label(900, 928, 'Vulnerabilidade', size=57, weight=700),
        label(900, 1000, ['Suscetibilidade e', 'limitações de proteção'], size=42, step=50),
        '<rect x="805" y="560" width="190" height="78" rx="16" fill="white" fill-opacity="0.9"/>',
        label(900, 617, 'Risco', size=62, weight=700),
        label(900, 1290, ['Interação conceitual entre os componentes do risco.',
                          'Áreas e interseções não representam probabilidades.'], size=42),
    ]
    save('10', 'venn-risco', 'fig-venn-risco', 'Perigo, exposição e vulnerabilidade interagem na produção do risco',
         'Três círculos parcialmente sobrepostos representam perigo, exposição e vulnerabilidade. '
         'Risco ocupa a interseção dos três. Rótulos, posições e diferentes tracejados permitem distinguir '
         'os componentes sem depender de cor. Áreas e interseções não representam probabilidades ou quantidades.',
         1420, parts, source={'citations': ['ipcc2022glossario', 'undrr2017terminology']})

    parts = [raster('11', 0, 110, 1800, 900)]
    for x, heading, lines in [
        (300, 'Chuva e inundação', ['Quanto chove?', 'Qual a profundidade', 'e a extensão da água?']),
        (900, 'Calor persistente', ['Qual a intensidade?', 'Por quanto tempo?', 'Há alívio à noite?']),
        (1500, 'Poluição do ar', ['Qual a concentração?', 'Onde e por quanto tempo', 'ela se mantém?']),
    ]:
        parts += [label(x, 65, heading, size=50, weight=700), label(x, 1075, lines, size=43, step=52)]
    parts += [label(900, 1300, ['Em todos os casos: onde ocorre e com que frequência ou probabilidade?',
                               'Caracterizar o perigo não informa, sozinho, quem sofrerá dano.'], size=42)]
    save('11', 'perigos', 'fig-caracterizacao-perigo', 'Caracterizar o perigo: intensidade, duração e território',
         'Três aquarelas hipotéticas mostram chuva e inundação de um bairro, calor sobre uma rua '
         'e poluição do ar em área urbana. Perguntas distinguem chuva, profundidade e extensão da água; '
         'intensidade e duração do calor e alívio noturno; concentração e permanência de poluentes. '
         'Localização, frequência e probabilidade completam a caracterização. Não se representam medidas observadas.',
         1410, parts, watercolor=True)

    sw, sh = Image.open(ART / 'arte-cap1-12-v1.png').size
    parts = []
    panels = [
        (80, 115, 0, 0, 'Moradia', ['Materiais, ventilação', 'e condições do entorno']),
        (920, 115, sw/2, 0, 'Trabalho', ['Tempo de exposição,', 'pausas e proteção']),
        (80, 1125, 0, sh/2, 'Acesso ao cuidado', ['Mobilidade, acolhimento', 'e continuidade da atenção']),
        (920, 1125, sw/2, sh/2, 'Presença nos dados', ['Escuta e busca ativa', 'revelam necessidades']),
    ]
    for x, y, cx, cy, heading, lines in panels:
        parts += [label(x+400, y-40, heading, size=53, weight=700),
                  raster('12', x, y, 800, 800, (cx, cy, sw/2, sh/2)),
                  label(x+400, y+860, lines, size=46, step=54)]
    parts += [label(900, 2160, ['As possibilidades de proteção dependem de condições concretas de vida.',
                               'Cenas hipotéticas; nenhuma categoria social define sozinha o risco.'], size=42)]
    save('12', 'desigualdades', 'fig-desigualdades-risco', 'Quatro caminhos das desigualdades na produção do risco',
         'Quatro aquarelas mostram uma moradora abrindo a janela, trabalhadores urbanos com diferentes '
         'momentos de esforço e pausa, uma pessoa em cadeira de rodas chegando ao serviço de saúde '
         'e uma agente comunitária ouvindo uma moradora. Os rótulos relacionam moradia, trabalho, acesso '
         'ao cuidado e presença nos dados às possibilidades de proteção. São situações hipotéticas, sem escores de vulnerabilidade.',
         2300, parts, watercolor=True, print_width='90%')
    (ART / 'arte-cap1-revisao-manifest.json').write_text(
        json.dumps(RECORDS, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    compose()
