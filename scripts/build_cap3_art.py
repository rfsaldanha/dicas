#!/usr/bin/env python3
"""Compõe as oito artes do capítulo 3; mantém rótulos e relações editáveis.

Uso: python3 scripts/build_cap3_art.py [01 ... 08]
Originais e prompts: assets/figures/arte-cap3-*. O manifesto preserva a ordem.
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
MANIFEST = json.loads((ART / 'arte-cap3-manifest.json').read_text())


def text(x, y, lines, size=48, step=58, weight='normal', anchor='middle'):
    if isinstance(lines, str):
        lines = [lines]
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}">{spans}</text>'


def line(d, arrow=True, dashed=False):
    marker = ' marker-end="url(#arrow)"' if arrow else ''
    dash = ' stroke-dasharray="12 10"' if dashed else ''
    return f'<path d="{d}" fill="none" stroke="#4c5553" stroke-width="3.5" stroke-linejoin="round"{marker}{dash}/>'


def box(x, y, w, h, fill='white', dashed=False):
    dash = ' stroke-dasharray="14 10"' if dashed else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="#66706b" stroke-width="2.5"{dash}/>'


def picture(name, crop, x, y, w, h, sw, sh):
    # Frações do original: não altera a cena; apenas recorta as vinhetas.
    cx, cy, cw, ch = crop
    cx, cw, cy, ch = cx * sw, cw * sw, cy * sh, ch * sh
    scale = min(w / cw, h / ch)
    left, top = x + (w - cw * scale) / 2, y + (h - ch * scale) / 2
    return (f'<defs><clipPath id="clip-{name}" clipPathUnits="userSpaceOnUse"><rect x="{left}" y="{top}" width="{cw*scale}" height="{ch*scale}"/></clipPath></defs>'
            f'<g clip-path="url(#clip-{name})"><use xlink:href="#aquarela" transform="translate({left} {top}) scale({scale}) translate({-cx} {-cy})"/></g>')


def calendar_sequence(x, y):
    """Exemplo simbólico: lacuna não confirma nem prolonga uma sequência."""
    parts = [text(x+265, y+35, 'Dias consecutivos', 42)]
    states = ['fora', 'atende', 'atende', 'atende', 'ausente', 'atende', 'fora']
    for i, state in enumerate(states):
        left = x+i*76
        parts += [box(left, y+58, 68, 85, fill='#f3f0e8' if state == 'atende' else 'white',
                      dashed=state == 'ausente'),
                  text(left+34, y+90, str(i+1), 33)]
        if state == 'ausente':
            parts.append(text(left+34, y+132, '?', 34))
        else:
            fill = '#303b36' if state == 'atende' else 'white'
            parts.append(f'<circle cx="{left+34}" cy="{y+120}" r="10" fill="{fill}" stroke="#303b36" stroke-width="3"/>')
    # Apenas dias observados contíguos são agrupados; a lacuna fica fora.
    parts += [line(f'M{x+76} {y+151} v12 h220 v-12', arrow=False),
              f'<circle cx="{x+18}" cy="{y+198}" r="10" fill="#303b36"/>',
              text(x+42, y+211, 'Atende', 38, anchor='start'),
              f'<circle cx="{x+272}" cy="{y+198}" r="10" fill="white" stroke="#303b36" stroke-width="3"/>',
              text(x+296, y+211, 'Não atende', 38, anchor='start'),
              text(x+265, y+260, '?  Sem dado', 38)]
    return parts


def layout(number, sw, sh):
    p = []
    def pic(name, crop, x, y, w, h):
        return picture(name, crop, x, y, w, h, sw, sh)
    if number == '01':
        height = 1880
        p += [pic('observacao', (0, 0, 1, 1), 30, 125, 770, 1390)]
        rows = [
            ('Fenômeno', 'Processo de interesse'),
            ('Conceito', 'Dimensão a representar'),
            ('Variável', 'Característica a observar'),
            ('Dado', 'Registro situado no espaço e tempo'),
            ('Medida derivada', 'Regra aplicada aos registros'),
            ('Indicador', 'Medida vinculada a finalidade'),
            ('Informação para decisão', 'Interpretação em contexto'),
        ]
        for i, (heading, detail) in enumerate(rows):
            y = 50 + i * 220
            p += [box(845, y, 805, 170), text(1247, y+64, heading, 52), text(1247, y+126, detail, 40)]
            if i < 6:
                p.append(line(f'M1247 {y+170} V{y+212}'))
        p += [line('M1650 1455 H1750 V20 H1247 V43', dashed=True),
              '<g transform="translate(1710 740) rotate(-90)">'+text(0,0,'Rever a pergunta e o método',40)+'</g>',
              text(415,1505,['Observar não dispensa','escolher e interpretar.'],48),
              box(60,1640,1680,145,fill='#f1f4f1'),
              text(900,1695,'Documentar escolhas, fontes, transformações e limites',48),
              text(900,1755,'A documentação acompanha todo o percurso.',43),
              text(900,1840,'Esquema conceitual; o fluxo não quantifica perda de informação.',38)]
    elif number == '02':
        height = 1970
        rows = [
            (['Observações horárias'], ['Grandeza, suporte, horários', 'e registros válidos']),
            (['Máximo entre observações', 'válidas do dia'], ['Limites do dia e cobertura mínima;', 'picos podem não ser captados.']),
            (['Aplicação do critério térmico'], ['Referência, período-base', 'e operador de comparação']),
            (['Identificação de sequências'], ['Continuidade dos dias que atendem', 'ao critério; dado ausente não', 'confirma interrupção.']),
            (['Delimitação de episódios'], ['Duração mínima e regras', 'de início, término e separação']),
            (['Medidas de frequência', 'e duração'], ['Número de episódios, total de dias', 'participantes e duração máxima']),
        ]
        # Limites medidos nas vinhetas de v2, cuja separação não coincide
        # exatamente com terços da altura. Nenhum recorte inclui outra cena.
        crops = [(0, 0, .49, .331), (.505, 0, .49, .333),
                 (0, .337, .49, .297), None,
                 (0, .642, .49, .338), (.505, .642, .49, .338)]
        for i,(heading, detail) in enumerate(rows):
            y = 20 + i*280
            if i == 3:
                p += calendar_sequence(40, y)
            else:
                p.append(pic(f'etapa-{i}', crops[i], 35, y+20, 540, 240))
            block_height = len(heading)*54 + 18 + len(detail)*50
            baseline = y+(280-block_height)/2+40
            p += [text(660,y+157,str(i+1),58),
                  text(770,baseline,heading,51,step=54,anchor='start'),
                  text(770,baseline+len(heading)*54+18,detail,44,step=50,anchor='start')]
            if i<5:
                p.append(line(f'M660 {y+188} V{y+373}'))
        p += [box(60,1730,1680,95,fill='#f1f4f1'),
              text(900,1792,'Dia quente isolado não define automaticamente uma onda de calor.',43),
              text(900,1878,['Calendário ilustrativo, sem dados observados.',
                             'A sequência destacada não estabelece a duração mínima de um episódio.'],39,step=48)]
    elif number == '03':
        height = 1620
        p += [text(450,65,'Vegetação contabilizada',52),text(1350,65,'Acesso ao parque',52),
              pic('bairro',(0,0,1,1),20,105,1760,1174),
              text(450,1340,['A área verde privada entra no', 'indicador de cobertura vegetal.'],46,step=54),
              box(920,1300,810,105,fill='#f3f0e8'),
              text(1325,1366,'Acesso exclusivo aos moradores',44),
              text(900,1490,'Vegetação no bairro não garante acesso de todos à sombra do parque.',44),
              text(900,1575,'Bairro hipotético; sem estimativas de cobertura ou exposição individual.',38)]
    elif number == '04':
        height = 2030
        labels = [('Água','Abastecimento e continuidade'),('Energia','Funcionamento dos equipamentos'),
                  ('Acesso','Chegada de pessoas e insumos'),('Pessoal','Disponibilidade e organização')]
        for i,(heading, detail) in enumerate(labels):
            col,row = i%2,i//2; x=col*900; y=row*700
            p += [text(x+450,y+65,heading,55),pic(f'componente-{i}',(col/2,row/2,.5,.5),x+80,y+100,740,480),text(x+450,y+635,detail,42)]
        # Uma conexão de síntese; o retorno explicita que os componentes permanecem disponíveis.
        p += [box(80,0,1640,1380,fill='none'),line('M900 1380 V1500'),
              box(300,1520,1200,155),text(900,1580,'Síntese: combinação segundo regras explícitas',49),
              text(900,1640,'O que pode compensar o quê?',46),
              line('M300 1597 H35 V35 H75',dashed=True),
              text(900,1780,['Consultar os componentes permite reconhecer','condições críticas que a média pode ocultar.'],48),
              text(900,1930,'Retorno aos componentes: preservar o significado de cada dimensão.',42),
              text(900,2000,'Serviço hipotético; sem pontuações, resultados ou ranking.',38)]
    elif number == '05':
        height = 1780
        p += [box(80,20,610,130),text(385,75,'FQI da RIPSA',54),text(385,125,'Referência estrutural',42),
              line('M710 85 H1060'),text(890,62,'Inspiração',39),
              box(1080,20,640,130),text(1400,75,'Fichas deste livro',54),text(1400,125,'Adaptação e ampliação',42),
              pic('equipe',(0,0,1,1),30,230,730,1050)]
        groups=[('Identificação','Código e títulos'),('Significado','Conceito, interpretação, usos e limites'),
                ('Cálculo','Fontes, fórmula e procedimentos'),('Recortes','Categorias e granularidade'),
                ('Gestão e comunicação',['Atualização, responsabilidade,','notas e análise descritiva'])]
        p += [line('M1400 150 V190 H800 V1310',arrow=False)]
        for i,(heading,detail) in enumerate(groups):
            y=230+i*225
            p += [line(f'M800 {y+85} H865'),box(880,y,850,185),text(1305,y+62,heading,52),text(1305,y+120,detail,41,step=47)]
        p += [box(60,1430,1680,215,fill='#f1f4f1'),text(900,1485,'Extensões de clima, ambiente e saúde',50),
              text(900,1550,['Resoluções, referências, limiares, processamento e incerteza','Comparabilidade, defasagens e aplicação na gestão'],43,step=56),
              text(900,1700,'Blocos didáticos da obra; códigos próprios, sem equivalência ao catálogo da RIPSA.',38),
              text(900,1750,'FQI: Ficha de Qualificação do Indicador.',38)]
    elif number == '06':
        height = 1620
        p += [box(70,20,1660,960),text(900,90,'Estabelecimentos elegíveis — denominador',53),
              text(900,150,'Mesmo território, data e critérios de inclusão',43),
              box(325,235,1150,670,fill='#f5f6f3'),
              text(900,305,'Com plano de contingência — numerador',49),
              pic('plano',(0,0,1,1),410,345,980,515),
              text(900,1060,'Proporção (%)',53),
              text(820,1150,'Estabelecimentos elegíveis com plano',47),line('M270 1178 H1370',arrow=False),
              text(820,1240,'Total de estabelecimentos elegíveis',47),text(1480,1195,'× 100',52),
              text(900,1365,['Situação desconhecida precisa de tratamento explícito.','Denominador igual a zero: proporção indefinida.'],45),
              text(900,1550,['Desenho conceitual: áreas e ícones não representam quantidades.'],39)]
    elif number == '07':
        height = 1640
        p += [text(300,65,['Unidade de','observação'],50),text(900,65,['Unidade de','análise'],50),text(1500,65,'População-alvo',50),
              pic('unidades',(0,0,1,1),15,165,1770,1180),
              text(300,1390,['Estação no bairro:', 'produz registros pontuais.'],44,step=52),
              text(900,1390,['O mesmo bairro:', 'recebe a medida territorial.'],44,step=52),
              text(1500,1390,['Moradores do bairro:', 'população-alvo.'],44,step=52),
              text(900,1530,'Atribuir a medida exige método e avaliação de representatividade.',44),
              text(900,1590,'O valor territorial não mede automaticamente a exposição de cada pessoa.',38)]
    elif number == '08':
        height = 2080
        labels=[('Perigo','Calor intenso no bairro'),('Exposição','Pessoas sob sol, sem cobertura'),
                ('Vulnerabilidade','Moradia com proteção térmica limitada'),('Baixa capacidade de resposta','Serviço com recursos limitados')]
        # Bordas de cada vinheta verificadas no original v3.
        crops=[(0,0,.493,.337),(.505,0,.49,.338),
               (0,.343,.493,.322),(.505,.343,.49,.322)]
        for i,(heading,detail) in enumerate(labels):
            col,row=i%2,i//2;x=col*900;y=row*500
            p += [text(x+450,y+62,heading,46),pic(f'dimensao-{i}',crops[i],x+70,y+95,760,340),text(x+450,y+474,detail,40)]
        # Setas independentes: as quatro dimensões entram na leitura do risco.
        p += [line('M100 490 H35 V1160 H390'),line('M1700 490 H1765 V1160 H1410'),
              line('M450 990 V1040 H740 V1080'),line('M1350 990 V1040 H1060 V1080'),
              box(410,1100,980,135,fill='#f1f4f1'),text(900,1185,'Risco à saúde',60),line('M900 1240 V1300'),
              text(900,1370,'Possíveis efeitos sobre a saúde',53),
              pic('efeitos',(.505,.669,.49,.328),450,1410,900,405),
              text(900,1890,'Atendimento por mal-estar associado ao calor: uma possibilidade.',41),
              text(900,1960,'As setas organizam conceitos; não são uma equação de risco.',43),
              text(900,2025,'Cenas hipotéticas. Exposição não implica adoecimento inevitável.',39)]
    else:
        raise ValueError(number)
    return 1800, height, p


def compose(a):
    data=(ART/a['source']).read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Original não é PNG: '+a['source'])
    sw,sh=struct.unpack('>II',data[16:24]);width,height,parts=layout(a['number'],sw,sh)
    encoded=base64.b64encode(data).decode('ascii')
    metadata=(f"Elaboração para esta obra. Ferramenta integrada image_gen; versão não informada. "
              f"Prompt: {a['prompt']}. Referência: aquarela-grafite-nanquim.png, fornecida junto do original à ferramenta de edição. "
              f"Intervenções editoriais: {a.get('review', 'disposição de vinhetas, rótulos e setas em SVG')}. "
              f"Exportação em escala de cinza com Chromium e ImageMagick. "
              f"Reprodução da montagem: python3 scripts/build_cap3_art.py {a['number']}. Arquivos autorais: GPL-3.0; fontes mantêm suas licenças.")
    svg=ART/a['svg'];out=ART/a['print']
    write_svg(svg, f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(a['title'])}</title><desc id="desc">{escape(a['alt'])}</desc>
<metadata>{escape(metadata)}</metadata>
<defs><image id="aquarela" width="{sw}" height="{sh}" xlink:href="data:image/png;base64,{encoded}"/>
<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="#4c5553"/></marker></defs>
<rect width="{width}" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="#303b36">'''+ '\n'.join(parts)+'</g></svg>\n')
    export_print(svg, out)
    print(svg.relative_to(ROOT),flush=True)


if __name__=='__main__':
    selected=sys.argv[1:] or [a['number'] for a in MANIFEST]
    for number in selected:
        compose(next(a for a in MANIFEST if a['number']==number))
