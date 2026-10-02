#!/usr/bin/env python3
"""Compõe as sete artes do capítulo 4 com texto e relações editáveis.

Uso: python3 scripts/build_cap4_art.py [01 ... 07]
As aquarelas são originais gerados sequencialmente; não contêm dados observados.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import base64
import hashlib
import json
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'
MANIFEST = json.loads((ART / 'arte-cap4-manifest.json').read_text())
INK = '#303b36'


def text(x, y, lines, size=48, step=57, anchor='middle'):
    if isinstance(lines, str):
        lines = [lines]
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}">{spans}</text>'


def line(d, arrow=False, dashed=False, width=3.5, stroke='#4c5553'):
    marker = ' marker-end="url(#arrow)"' if arrow else ''
    dash = ' stroke-dasharray="14 10"' if dashed else ''
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"{marker}{dash}/>'


def box(x, y, w, h, fill='white'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="#66706b" stroke-width="2.5"/>'


def picture(name, crop, x, y, w, h, sw, sh):
    cx, cy, cw, ch = crop
    cx, cw, cy, ch = cx * sw, cw * sw, cy * sh, ch * sh
    scale = min(w / cw, h / ch)
    pw, ph = cw * scale, ch * scale
    left, top = x + (w - pw) / 2, y + (h - ph) / 2
    svg = (f'<defs><clipPath id="clip-{name}"><rect x="{left}" y="{top}" width="{pw}" height="{ph}"/></clipPath></defs>'
           f'<g clip-path="url(#clip-{name})"><use href="#aquarela" xlink:href="#aquarela" transform="translate({left} {top}) scale({scale}) translate({-cx} {-cy})"/></g>')
    return svg, (left, top, pw, ph)


def layout(number, sw, sh):
    p = []
    placements = []

    def pic(name, crop, x, y, w, h):
        svg, area = picture(name, crop, x, y, w, h, sw, sh)
        placements.append({'name': name, 'crop': crop, 'area': area})
        p.append(svg)
        return area

    if number == '01':
        height = 1830
        rows = [('Localização', ['Onde o registro', 'está referenciado?'], 'Estação e residência'),
                ('Suporte em área', ['A que porção do espaço', 'o valor se refere?'], 'Células de uma grade'),
                ('Unidade de análise', ['Para que território', 'a síntese será calculada?'], 'Limite municipal')]
        for i, (heading, detail, example) in enumerate(rows):
            y = 30 + i * 550
            x, top, w, h = pic('suporte-'+str(i), (0, .18, 1, .76), 30, y, 1020, 465)
            if i == 0:
                for px, py in [(.255, .48), (.79, .66)]:
                    p.append(f'<circle cx="{x+px*w}" cy="{top+py*h}" r="16" fill="white" stroke="{INK}" stroke-width="6"/>')
            elif i == 1:
                for j in range(5):
                    xx = x + (.1 + .2*j)*w
                    p.append(line(f'M{xx} {top+.08*h} V{top+.92*h}', width=4))
                for j in range(4):
                    yy = top + (.08 + .28*j)*h
                    p.append(line(f'M{x+.1*w} {yy} H{x+.9*w}', width=4))
                p.append(f'<rect x="{x+.3*w}" y="{top+.36*h}" width="{.2*w}" height="{.28*h}" fill="#fff" fill-opacity=".2" stroke="{INK}" stroke-width="8"/>')
            else:
                coords = [(.1,.3),(.32,.1),(.61,.19),(.88,.12),(.93,.66),(.7,.9),(.43,.8),(.16,.9)]
                pts = ' '.join(f'{x+u*w},{top+v*h}' for u,v in coords)
                p.append(f'<polygon points="{pts}" fill="white" fill-opacity=".08" stroke="{INK}" stroke-width="6" stroke-dasharray="20 10"/>')
            p += [text(1400,y+120,heading,55), text(1400,y+210,detail,45), text(1400,y+365,example,43)]
            if i < 2:
                p.append(line(f'M65 {y+510} H1735', width=1.5, stroke='#c6ccc5'))
        p += [text(900,1730,'Compartilhar uma localização não torna os suportes equivalentes.',45),
              text(900,1790,'Paisagem hipotética; camadas esquemáticas, sem escala cartográfica.',38)]
    elif number == '02':
        height = 1850
        rows = [('Unidades de referência', ['Um mesmo território', 'dividido em quatro partes.']),
                ('Efeito de escala', ['Agregação de pares:', 'duas unidades maiores.']),
                ('Efeito de zoneamento', ['Quatro unidades novamente,', 'com outros limites.'])]
        for i, (heading, detail) in enumerate(rows):
            y = 25 + i*550
            x, top, w, h = pic('territorio-'+str(i), (0,0,1,1), 25,y,1070,480)
            x0,x1,y0,y1 = x+.1*w,x+.9*w,top+.1*h,top+.9*h
            p.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="{INK}" stroke-width="5"/>')
            if i in (0,1):
                p.append(line(f'M{(x0+x1)/2} {y0} V{y1}',width=5))
                if i == 0:
                    p.append(line(f'M{x0} {(y0+y1)/2} H{x1}',width=5))
            else:
                for j in range(1,4):
                    yy = y0+(y1-y0)*j/4
                    p.append(line(f'M{x0} {yy} H{x1}',width=5))
            p += [text(1400,y+150,heading,51),text(1400,y+255,detail,45)]
        p += [box(65,1660,1670,95,fill='#f1f4f1'),text(900,1723,'Mudar a divisão pode mudar a síntese e as associações entre áreas.',43),
              text(900,1810,'Mesma cena repetida; casas e pigmentos não representam contagens ou medidas.',37)]
    elif number == '03':
        height = 2190
        rows = [('Condição ambiental','Quando ocorreu o fenômeno?'),
                ('Exposição','Quando e onde houve contato?'),
                ('Possível efeito','Quando surgiram alterações na saúde?'),
                ('Atendimento','Quando o cuidado foi recebido?'),
                ('Registro','Quando o evento entrou no sistema?'),
                ('Publicação','Quando a informação ficou disponível?')]
        for i,(heading,detail) in enumerate(rows):
            y=20+i*310
            pic('tempo-'+str(i),((i%3)/3,(i//3)/2,1/3,1/2),45,y,580,275)
            p += [text(1230,y+105,heading,54),text(1230,y+185,detail,42)]
            if i<5:
                p.append(line(f'M700 {y+150} V{y+385}',arrow=True,dashed=i in (0,1),width=3))
        p += [box(65,1900,1670,195,fill='#f1f4f1'),text(900,1962,'Tempos diferentes exigem campos de data diferentes.',47),
              text(900,2025,['Conexões tracejadas: caminhos possíveis, sem causalidade demonstrada.'],39),
              text(900,2150,'Cenas conceituais; espaçamento e setas não quantificam durações.',38)]
    elif number == '04':
        height = 1420
        pic('previsao',(0,0,1,.84),50,150,1700,840)
        p += [text(440,80,'Inicialização da rodada',55),text(1360,80,'Tempo de validade',55),
              line('M330 1050 H1460',arrow=True,width=4),
              line('M400 1020 V1080',width=4),line('M1400 1020 V1080',width=4),
              text(900,1012,'Horizonte: +24 h',52),
              text(410,1150,['28/07/2026','00 UTC'],49),text(1400,1150,['29/07/2026','00 UTC'],49),
              text(900,1315,'Validade da previsão não é data de acesso nem confirmação do observado.',42),
              text(900,1380,'Datas do exemplo CAMS; paisagem ilustrativa, sem representar o tempo ocorrido.',37)]
    elif number == '05':
        height=2110
        pic('qualidade',(0,0,1,1),480,0,840,540)
        p += [box(360,555,1080,120,fill='#f1f4f1'),text(900,635,'Adequado para qual uso?',61),
              line('M900 675 V725 M450 725 H1350 M450 725 V1730 M1350 725 V1730',width=3)]
        rows=[('Exatidão e validade',['O valor representa','o fenômeno de interesse?']),
              ('Completude',['Os registros esperados','estão presentes e válidos?']),
              ('Representatividade',['Locais, períodos e grupos','cobrem o universo de interesse?']),
              ('Oportunidade',['A informação chega','a tempo da decisão?']),
              ('Consistência',['Códigos, unidades e relações','internas são coerentes?']),
              ('Homogeneidade',['Mudou o fenômeno','ou o processo de observação?']),
              ('Comparabilidade',['Definições e recortes','permitem comparação?']),
              ('Rastreabilidade',['Origem e transformações','podem ser reconstruídas?'])]
        for i,(heading,detail) in enumerate(rows):
            col,row=i%2,i//2;x=60+col*900;y=775+row*280
            p += [box(x,y,780,230),text(x+390,y+70,heading,50),text(x+390,y+137,detail,43,step=52)]
        p += [text(900,2010,'Dimensões complementares: não formam nota única nem ranking.',44),
              text(900,2080,'Síntese editorial; o requisito depende da pergunta e das consequências do uso.',37)]
    elif number == '06':
        height=2070
        rows=[('Zero verdadeiro',['Observação válida igual a zero.','Preservar o valor e a unidade.']),
              ('Registro ausente',['Não há valor utilizável.','Investigar a ausência; não preencher com zero.']),
              ('Abaixo da detecção',['Limitação do método de medição.','Não equivale a ausência da substância.']),
              ('Não aplicável',['Campo fora do domínio daquela observação.','Distinguir de uma falha de preenchimento.']),
              ('Dado suprimido',['Valor não divulgado para proteção.','Não reconstruir por diferença entre totais.'])]
        for i,(heading,detail) in enumerate(rows):
            y=20+i*370
            pic('estado-'+str(i),((i%3)/3,(i//3)/2,1/3,1/2),40,y,535,325)
            p += [text(1170,y+95,heading,53),text(1170,y+175,detail,42,step=57)]
            if i<4:
                p.append(line(f'M610 {y+335} H1740',stroke='#c6ccc5',width=1.5))
        p += [box(60,1880,1680,95,fill='#f1f4f1'),text(900,1942,'O dicionário da fonte deve distinguir os estados e seus códigos.',44),
              text(900,2030,'Instrumentos e documentos são símbolos; não representam medições reais.',38)]
    elif number == '07':
        height=2190
        pic('equipe',(0,0,1,1),415,0,970,550)
        rows=[('Pergunta e população','Definir o que se deseja saber e para quem.'),
              ('Fontes e versões','Identificar produtos, extrações e responsabilidades.'),
              ('Espaço, tempo e população','Compatibilizar suporte, janelas e denominadores.'),
              ('Qualidade, incerteza e proteção','Examinar adequação, sensibilidade e divulgação.')]
        for i,(heading,detail) in enumerate(rows):
            y=580+i*205
            p += [box(280,y,1240,165),text(900,y+62,heading,51),text(900,y+120,detail,41)]
            if i<3:
                p.append(line(f'M900 {y+165} V{y+200}',arrow=True))
        p += [line('M280 1275 H90 V660 H265',arrow=True,dashed=True),
              '<g transform="translate(140 985) rotate(-90)">'+text(0,0,'Rever se inadequado',39)+'</g>',
              line('M900 1360 V1460 M320 1460 H1480 M320 1460 V1520 M900 1460 V1520 M1480 1460 V1520',width=3),
              text(900,1430,'A pergunta define a análise e seus requisitos.',41)]
        cards=[('Associação',['Variação conjunta','entre as variáveis.'],['Descrever padrões;','examinar dependências','e limites do desenho.']),
               ('Efeito causal',['Contraste sob exposições','ou intervenções distintas.'],['Definir o contraste;','justificar desenho,','ajustes e hipóteses.']),
               ('Atribuição',['Contribuição relativa','a um contrafactual.'],['Explicitar a referência;','sustentar a interpretação','causal e a incerteza.'])]
        for i,(heading,question,requirements) in enumerate(cards):
            x=50+i*580
            p += [box(x,1540,540,450),text(x+270,1615,heading,52),text(x+270,1690,question,39,step=52),
                  text(x+270,1840,requirements,38,step=51)]
        p += [text(900,2060,'Não há passagem automática de associação para causalidade ou atribuição.',42),
              text(900,2140,'Fluxo conceitual; as três saídas não são etapas sucessivas.',38)]
    else:
        raise ValueError(number)
    return 1800,height,p,placements


def compose(a):
    data=(ART/a['source']).read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Original não é PNG: '+a['source'])
    if hashlib.sha256(data).hexdigest() != a['sha256_original']:
        raise ValueError('Original difere do manifesto: '+a['source'])
    sw,sh=struct.unpack('>II',data[16:24])
    width,height,parts,placements=layout(a['number'],sw,sh)
    # 120 mm é a largura máxima de uso editorial destas composições.
    for item in placements:
        native_width = item['crop'][2]*sw
        used_mm = item['area'][2]/width*120
        dpi=native_width/(used_mm/25.4)
        if dpi < 300:
            raise ValueError(f"Resolução efetiva insuficiente: {a['number']} {item['name']} {dpi:.1f} dpi")
    metadata=json.dumps({
        'tool':'image_gen','tool_version':a['tool_version'],'prompt':a['prompt'],
        'reference':a['reference'],'reference_delivery':a['reference_delivery'],
        'sha256_original':hashlib.sha256(data).hexdigest(),
        'interventions':'Inspeção visual; disposição e recorte de vinhetas; limites, conexões e rótulos em SVG; exportação em cinza.',
        'license':a['license'],'reproduce':'python3 scripts/build_cap4_art.py '+a['number'],
        'maximum_print_width_mm':120,'placements':placements},ensure_ascii=False)
    encoded=base64.b64encode(data).decode('ascii')
    svg=ART/a['svg'];out=ART/a['print']
    svg.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(a['title'])}</title><desc id="desc">{escape(a['alt'])}</desc>
<metadata>{escape(metadata)}</metadata>
<defs><image id="aquarela" width="{sw}" height="{sh}" xlink:href="data:image/png;base64,{encoded}"/>
<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="#4c5553"/></marker></defs>
<rect width="{width}" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="{INK}">'''+ '\n'.join(parts)+'</g></svg>\n')
    with tempfile.TemporaryDirectory(prefix='dicas-cap4-art-') as folder:
        rgba=Path(folder)/'composicao.png'
        subprocess.run(['inkscape',str(svg),'--export-type=png','--export-width=2400','--export-filename='+str(rgba)],check=True,stdout=subprocess.DEVNULL)
        subprocess.run(['convert',str(rgba),'-background','white','-alpha','remove','-alpha','off','-colorspace','Gray','-depth','8','-units','PixelsPerInch','-density','508','-define','png:color-type=0',str(out)],check=True)
    print(svg.relative_to(ROOT),flush=True)


if __name__=='__main__':
    selected=sys.argv[1:] or [a['number'] for a in MANIFEST]
    for number in selected:
        compose(next(a for a in MANIFEST if a['number']==number))
