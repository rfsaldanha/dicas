#!/usr/bin/env python3
"""Compõe as aquarelas do capítulo 6 com rótulos e conexões editáveis.

Uso: DICAS_BROWSER_CHANNEL=chrome python3 scripts/build_cap6_art.py [01 02 03]
Os originais e os prompts são preservados; a versão de impressão usa tons de cinza.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import base64
import json
import struct
import sys
from figure_style import write_svg
from render_figure import export_print

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'
MANIFEST = json.loads((ART / 'arte-cap6-manifest.json').read_text())


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
        height = 1640
        p.append(picture(20, 140, 760, 1240, sw, sh))
        rows = [
            ('Definir a pergunta', ['População, território e período']),
            ('Reunir evidências', ['Indicadores, fontes e escuta']),
            ('Interpretar a situação', ['Necessidades e desigualdades']),
            ('Pactuar prioridades', ['Critérios e possibilidades de ação']),
            ('Organizar a resposta', ['Ações, recursos e responsáveis']),
            ('Acompanhar e avaliar', ['Entregas, resultados e revisão']),
        ]
        for i, (title, detail) in enumerate(rows):
            y = 40 + i*230
            p += [box(815, y, 895, 170), text(1262, y+67, title, 53), text(1262, y+130, detail, 44)]
            if i < 5:
                p.append(arrow(f'M1262 {y+170} V{y+215}'))
        p += [arrow('M1710 1275 H1760 V125 H1722'),
              box(50, 1420, 1690, 150, '#f1f4f1'),
              text(895, 1480, 'Participação e documentação em todo o processo', 51),
              text(895, 1540, 'Indicadores qualificados, contexto territorial e conhecimento local', 43),
              text(900, 1618, 'As setas representam etapas do trabalho e sua revisão.', 43)]
    elif number == '02':
        height = 1580
        p.append(picture(20, 60, 770, 1300, sw, sh))
        rows = [
            ('Antes do período de maior risco', 'Preparar', ['Atualizar a situação territorial', 'e corrigir lacunas de proteção']),
            ('Durante o episódio', 'Responder', ['Ativar medidas e acompanhar', 'necessidades e capacidade']),
            ('Depois do episódio', 'Revisar', ['Avaliar entregas e resultados', 'e atualizar a análise e o plano']),
        ]
        for i, (period, title, detail) in enumerate(rows):
            y = 95 + i*425
            p += [box(815, y, 895, 320), text(1262, y+63, period, 45),
                  text(1262, y+138, title, 57), text(1262, y+216, detail, 46, 60)]
            if i < 2:
                p.append(arrow(f'M1262 {y+320} V{y+409}'))
        p += [arrow('M1710 1105 H1760 V255 H1722'),
              box(50, 1370, 1690, 135, '#f1f4f1'),
              text(895, 1428, 'Vigilância, escuta e atualização ao longo de todo o ciclo', 49),
              text(895, 1480, 'Perigos, condições de saúde, acesso e resposta dos serviços', 43),
              text(900, 1558, 'As fases podem se sobrepor; o calendário é definido localmente.', 43)]
    elif number == '03':
        height = 1620
        p += [box(50, 25, 1690, 145, '#f1f4f1'),
              text(895, 83, 'Síntese da análise de situação de saúde', 53),
              text(895, 141, 'Necessidades, desigualdades e respostas existentes', 45),
              picture(20, 225, 760, 1160, sw, sh),
              arrow('M1262 170 V220'),
              box(815, 235, 895, 370), text(1262, 301, 'Examinar critérios públicos', 52),
              text(1262, 375, ['Magnitude e tendência', 'Desigualdade e proteção possível', 'Viabilidade, recursos e atribuições', 'Incertezas e lacunas de informação'], 44, 62),
              arrow('M1262 605 V665'),
              box(815, 680, 895, 175), text(1262, 746, 'Pactuar prioridades', 54),
              text(1262, 809, 'Moradores, trabalhadores e gestores', 44),
              arrow('M1262 855 V917'),
              box(815, 932, 895, 190), text(1262, 997, 'Definir a execução', 54),
              text(1262, 1060, ['Ações, orçamento, responsáveis e prazos'], 43),
              arrow('M1262 1122 V1182'),
              box(815, 1197, 895, 190), text(1262, 1261, 'Acompanhar e rever', 54),
              text(1262, 1325, 'Entregas, acesso e resultados', 44),
              arrow('M1710 1292 H1770 V98 H1745'),
              box(50, 1440, 1690, 130, '#f8f4ef'),
              text(895, 1496, 'Registrar as razões da escolha e os limites da decisão', 49),
              text(895, 1548, 'Manter visíveis as demandas que continuam sem resposta', 43)]
    else:
        raise ValueError(number)
    return 1800, height, p


def compose(a):
    data = (ART/a['source']).read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Original não é PNG: '+a['source'])
    sw, sh = struct.unpack('>II', data[16:24])
    width, height, parts = layout(a['number'], sw, sh)
    encoded = base64.b64encode(data).decode('ascii')
    metadata = (f"Elaboração para esta obra. Ferramenta integrada image_gen; versão não informada. "
                f"Prompt: {a['prompt']}. Referência visual inspecionada pelo assistente: {a['reference']}; "
                f"estilo descrito no prompt, sem anexação do arquivo por falha do sandbox. "
                f"Composição editorial com rótulos e setas editáveis. Cenas conceituais sem dados observados. "
                f"Reprodução: python3 scripts/build_cap6_art.py {a['number']}. Arquivos autorais: GPL-3.0.")
    svg = ART/a['svg']
    write_svg(svg, f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(a['title'])}</title><desc id="desc">{escape(a['alt'])}</desc>
<metadata>{escape(metadata)}</metadata>
<defs><image id="aquarela" width="{sw}" height="{sh}" xlink:href="data:image/png;base64,{encoded}"/>
<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="#4c5553"/></marker></defs>
<rect width="{width}" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="#303b36">'''+'\n'.join(parts)+'</g></svg>\n')
    export_print(svg, ART/a['print'])
    print(svg.relative_to(ROOT), flush=True)


if __name__ == '__main__':
    for number in sys.argv[1:] or [a['number'] for a in MANIFEST]:
        compose(next(a for a in MANIFEST if a['number'] == number))
