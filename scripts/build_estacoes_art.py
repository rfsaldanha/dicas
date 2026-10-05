#!/usr/bin/env python3
"""Compõe as sete figuras do apêndice B. Dados vêm dos recortes oficiais locais."""
from pathlib import Path
from xml.sax.saxutils import escape
import base64
import csv
import hashlib
import json
import sys
from PIL import Image
from figure_style import write_svg
from render_figure import export_print

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'
DATA = ROOT / 'data-raw/estacoes'
INK = '#303b36'
BLUE = '#597482'
GREEN = '#536b50'
META = []


def text(x, y, lines, size=46, anchor='middle', step=56, weight='normal'):
    if isinstance(lines, str):
        lines = [lines]
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}">' +
            ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(line)}</tspan>' for i, line in enumerate(lines)) + '</text>')


def image(name, x, y, w, h, crop=None):
    encoded = base64.b64encode((ART / name).read_bytes()).decode()
    sw, sh = Image.open(ART / name).size
    view = crop or (0, 0, sw, sh)
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{" ".join(map(str, view))}">'
            f'<image width="{sw}" height="{sh}" href="data:image/png;base64,{encoded}"/></svg>')


def box(x, y, w, h, fill='#f3f0e8'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#aab1ac" stroke-width="2"/>'


def arrow(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{INK}" stroke-width="4" marker-end="url(#arrow)"/>'


def build(slug, height, parts, title, alt, sources=(), prompts=()):
    svg = ART / f'estacoes-{slug}.svg'
    metadata = {'title': title, 'alt': alt, 'svg': svg.name, 'print': f'estacoes-{slug}-print.png',
                'type': 'aquarela e composição vetorial' if sources else 'vetorial',
                'sources': list(sources), 'prompts': list(prompts),
                'tool': 'image_gen integrada; versão não informada' if sources else 'Python/SVG',
                'style_reference': 'assets/references/aquarela-grafite-nanquim.png' if sources else None,
                'reference_transport': 'Prévia JPEG da referência fornecida na conversa; artes seguintes usaram a prancha anterior para continuidade.' if sources else None,
                'license': 'GPL-3.0 para arquivos autorais; fontes de dados mantêm seus termos.',
                'review': 'Revisão técnica e visual pelo assistente; esquemas sem escala, sem dados inventados.',
                'reproduce': 'python3 scripts/build_estacoes_art.py'}
    for name in sources:
        im = Image.open(ART / name)
        metadata.setdefault('originals', []).append({'file': name, 'size': list(im.size), 'sha256': hashlib.sha256((ART / name).read_bytes()).hexdigest()})
    content = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{height}" viewBox="0 0 1800 {height}" role="img" aria-labelledby="title desc">'
               f'<title id="title">{escape(title)}</title><desc id="desc">{escape(alt)}</desc>'
               f'<metadata>{escape(json.dumps(metadata, ensure_ascii=False))}</metadata>'
               '<defs><marker id="arrow" markerWidth="18" markerHeight="16" refX="16" refY="8" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L18 8 L0 16 Z" fill="#303b36"/></marker></defs>'
               f'<rect width="1800" height="{height}" fill="white"/><g fill="{INK}" font-family="Libertinus Serif, Georgia, serif">' +
               ''.join(parts) + '</g></svg>')
    write_svg(svg, content)
    export_print(svg, ART / metadata['print'], require_raster=bool(sources))
    META.append(metadata)
    print(svg.name, flush=True)


def plates():
    parts = []
    labels = [('Abrigo e psicrômetro', 'Temperatura e umidade'), ('Pluviômetro e proveta', 'Precipitação acumulada'),
              ('Heliógrafo', 'Duração do brilho solar'), ('Registrador em papel', 'Traçado ao longo do tempo')]
    for i, (title, detail) in enumerate(labels):
        x, y = 35 + (i % 2) * 900, (i // 2) * 725
        parts += [image('estacoes-convencional-v1.png', x, y, 830, 552, ((i % 2)*768, (i // 2)*512, 768, 512)),
                  text(x+415, y+613, title, 49), text(x+415, y+671, detail, 44)]
    build('convencional', 1450, parts, 'Instrumentos de observação convencional',
          'Abrigo com psicrômetro, pluviômetro, heliógrafo e registrador de papel em quatro painéis.',
          ['estacoes-convencional-v1.png'], ['estacoes-convencional.prompt.txt'])
    parts = [image('estacoes-automatica-v1.png', 0, 0, 1800, 1200)]
    marks = [(1210, 115), (780, 650), (430, 785), (1370, 815), (920, 985), (1090, 850)]
    labels = ['Vento: velocidade e direção', 'Temperatura e umidade protegidas', 'Pluviômetro', 'Piranômetro', 'Registrador e armazenamento', 'Painel solar e alimentação']
    for i, ((x, y), label) in enumerate(zip(marks, labels), 1):
        parts += [f'<circle cx="{x}" cy="{y}" r="30" fill="white" stroke="{INK}" stroke-width="3"/>', text(x, y+16, str(i), 43),
                  text(70+(i-1)%2*900, 1260+(i-1)//2*77, f'{i}. {label}', 45, anchor='start')]
    build('automatica', 1490, parts, 'Componentes de uma estação meteorológica automática',
          'Mastro com sensores de vento, proteção de temperatura e umidade, pluviômetro, piranômetro, registrador e painel solar.',
          ['estacoes-automatica-v1.png'], ['estacoes-automatica.prompt.txt'])
    parts = [image('estacoes-ar-v2.png', 0, 0, 1800, 1030, (0, 0, 1536, 880))]
    for x, title, detail in [(295, 'Analisadores automáticos', 'Entrada de ar e instrumentos'), (890, 'Análise em laboratório', 'Pesagem controlada do filtro'), (1500, 'Sensor compacto', 'Resposta a avaliar em campo')]:
        parts += [text(x, 1090, title, 47), text(x, 1150, detail, 40)]
    steps = [['Coleta com', 'vazão conhecida'], ['Acondicionamento', 'e transporte'], ['Análise e', 'controles'], ['Concentração', 'e validação']]
    for i, lines in enumerate(steps):
        x=30+i*448
        parts += [box(x, 1240, 394, 165), text(x+197, 1305, lines, 45)]
        if i < 3: parts.append(arrow(x+397, 1320, x+442, 1320))
    parts.append(text(900, 1485, 'Na gravimetria: massa coletada ÷ volume de ar amostrado.', 43))
    build('ar', 1530, parts, 'Instrumentação de qualidade do ar e etapas da amostragem',
          'Abrigo de analisadores, balança em laboratório e sensor compacto. Fluxo da coleta até a concentração.',
          ['estacoes-ar-v2.png'], ['estacoes-ar.prompt.txt', 'estacoes-ar-v2.prompt.txt'])


def location():
    parts=[]
    for i in range(3):
        y=35+i*425
        parts.append(box(20, y, 1760, 390, '#ffffff'))
        # Diagramas qualitativos; dimensões gráficas não codificam medidas reais.
        if i == 0:
            parts += [f'<path d="M70 {y+300} H650" stroke="{GREEN}" stroke-width="5"/>',
                      f'<rect x="270" y="{y+155}" width="150" height="100" fill="#f3f0e8" stroke="{INK}" stroke-width="4"/>',
                      f'<path d="M265 {y+154} H425 M295 {y+255} V{y+300} M395 {y+255} V{y+300} M490 {y+300} V{y+72} M445 {y+72} H535" fill="none" stroke="{INK}" stroke-width="5"/>']
            for a in range(5):parts.append(f'<path d="M280 {y+170+a*16} H410" stroke="#737e77" stroke-width="2"/>')
            title='Meteorologia em terreno aberto';desc=['Exposição dos sensores, altura e obstáculos', 'fazem parte da observação.'];question='Que condições o ponto representa?'
        else:
            road=y+298
            parts += [f'<rect x="55" y="{road}" width="600" height="54" fill="#d6d9d7"/>', f'<path d="M65 {road+27} H640" stroke="white" stroke-width="4" stroke-dasharray="22 18"/>']
            for x,h in [(85,110),(210,160),(520,135)]:
                parts.append(f'<rect x="{x}" y="{y+220-h}" width="85" height="{h}" fill="#eceeea" stroke="#727d76" stroke-width="3"/>')
            sy=road-80 if i == 1 else y+95
            parts += [f'<rect x="355" y="{sy}" width="100" height="70" fill="#e7eef1" stroke="{INK}" stroke-width="4"/>',f'<path d="M405 {sy} V{sy-55} M390 {sy-55} H420" stroke="{INK}" stroke-width="4"/>']
            if i == 2:
                for x in [285,475]: parts += [f'<path d="M{x} {y+225} V{y+155}" stroke="{GREEN}" stroke-width="5"/>',f'<circle cx="{x}" cy="{y+145}" r="32" fill="#dbe4d6" stroke="{GREEN}" stroke-width="3"/>']
                title='Qualidade do ar: fundo urbano';desc=['Busca representar o ambiente urbano', 'com menor influência imediata da via.'];question='Qual entorno é representado?'
            else:
                title='Qualidade do ar: influência do tráfego';desc=['A posição em relação à via e ao vento', 'ajuda a interpretar as concentrações.'];question='Qual fonte e população interessam?'
        parts += [text(735,y+85,title,49,anchor='start'),text(735,y+170,desc,44,anchor='start',step=61),text(735,y+315,question,44,anchor='start')]
    parts.append(text(900,1370,'Contextos hipotéticos, sem escala ou raio universal de cobertura.',43))
    build('localizacao',1420,parts,'Objetivo de monitoramento e representatividade da estação','Três contextos: meteorologia aberta, tráfego e fundo urbano. Cada um responde a uma pergunta.')


def networks():
    parts=[]
    for x,title in [(65,'Meteorologia'),(945,'Qualidade do ar')]:
        parts.append(text(x+395,65,title,55))
    rows=[
        (115,170,['Estação da rede INMET','Instrumentos e registro'],['Estação ambiental','Coleta e analisadores']),
        (355,215,['Operação e controle de qualidade','INMET e arranjos de cooperação','Dados e histórico da estação'],['Órgão ambiental / operador','Método, calibração e validação','Dados e histórico da estação']),
        (650,220,['Acesso nacional','Catálogo, mapa e históricos','BDMEP'],['Acesso pela rede de origem','QUALAR e relatórios, por exemplo','MonitorAr: estações integradas']),
    ]
    for y,h,left,right in rows:
        for x,lines in [(65,left),(945,right)]: parts += [box(x,y,790,h),text(x+395,y+65,lines,44,step=59)]
    for x in [460,1340]:
        parts += [arrow(x,287,x,335),arrow(x,574,x,630)]
    parts += [arrow(460,875,460,907),arrow(460,974,460,1000),text(460,950,'Conforme participação e fluxo definido',36)]
    parts += [box(65,1020,790,340,'#eef2ed'),text(460,1085,['Cooperação OMM','WIGOS: integração observacional','OSCAR/Surface: metadados','WIS 2.0: intercâmbio'],44,step=65)]
    parts += [box(945,1020,790,340,'#eef2ed'),text(1340,1085,['Cooperação em composição atmosférica','GAW: programa da OMM','Adesão e contribuição específicas','Sem vínculo automático de toda rede'],41,step=65)]
    parts.append(text(900,1450,['Código, metadados e qualidade acompanham o dado.', 'Integração exige arranjos institucionais e técnicos.'],44,step=60))
    build('redes',1550,parts,'Responsabilidades e caminhos de publicação das observações','Fluxos de meteorologia e ar ambiente, com funções nacionais e internacionais distintas.')


def graphs():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.ticker import FuncFormatter
    for p in (ROOT/'assets/fonts').glob('LibertinusSerif-*.otf'):
        font_manager.fontManager.addfont(str(p))
    plt.rcParams.update({'font.family':'Libertinus Serif','font.size':12,'svg.fonttype':'none','axes.labelcolor':INK,'text.color':INK,'xtick.color':INK,'ytick.color':INK,'axes.edgecolor':INK})
    rows=list(csv.DictReader((DATA/'inmet-a701-2024-01-01.csv').open()))
    fig, axes=plt.subplots(2,1,figsize=(6.2,4.8),sharex=True,layout='constrained')
    for ax,key,label,color,lim in [(axes[0],'temperatura_c','Temperatura (°C)',GREEN,(17,27)),(axes[1],'umidade_pct','Umidade relativa (%)',BLUE,(50,85))]:
        ax.plot(range(24),[float(r[key]) for r in rows],color=color,marker='o',markersize=3.7,linewidth=1.5)
        ax.set_ylabel(label);ax.set_ylim(*lim);ax.set_xlim(0,23);ax.grid(axis='y',color='#d5d9d6',linewidth=.6)
        ax.spines[['top','right']].set_visible(False);ax.yaxis.set_major_formatter(FuncFormatter(lambda n,pos:f'{n:g}'.replace('.',',')))
    axes[-1].set_xticks([0,6,12,18,23],['00:00','06:00','12:00','18:00','23:00'])
    axes[-1].set_xlabel('Hora UTC — 1º de janeiro de 2024')
    save_plot(fig,'inmet-dados','Temperatura e umidade horárias observadas em São Paulo–Mirante','inmet-a701-2024-01-01.csv')
    air=list(csv.DictReader((DATA/'cetesb-mp25-2021.csv').open()))
    fig,ax=plt.subplots(figsize=(6.2,4.4));fig.subplots_adjust(left=.39,right=.95,bottom=.2,top=.95)
    for i,r in enumerate(air):
        if r['representatividade_anual']=='S':
            v=int(r['media_publicada_ug_m3']);ax.plot(v,i,'o',color=GREEN,markersize=6);ax.text(v+.7,i,str(v),va='center',fontsize=12)
        else:
            ax.text(12,i,'Sem representatividade\nanual',ha='center',va='center',fontsize=11,color='#666e68')
    ax.set_yticks(range(len(air)),[r['estacao'].replace('São José do Rio Preto','São José do\nRio Preto') for r in air]);ax.invert_yaxis();ax.set_ylim(5.65,-.65)
    ax.set_xlim(0,25);ax.set_xticks(range(0,26,5));ax.set_xlabel('MP₂,₅ (µg/m³) — 2021')
    ax.grid(axis='x',color='#d5d9d6',linewidth=.6);ax.set_axisbelow(True);ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0,pad=12)
    save_plot(fig,'cetesb-dados','Médias de MP₂,₅ com representatividade anual no recorte da CETESB','cetesb-mp25-2021.csv')


def save_plot(fig,slug,title,data):
    import matplotlib.pyplot as plt
    path=ART/f'estacoes-{slug}.svg';fig.savefig(path,format='svg',metadata={'Title':title,'Description':f'Dados reais: data-raw/estacoes/{data}. Sem imputação.'});plt.close(fig)
    write_svg(path,path.read_text());export_print(path,ART/f'estacoes-{slug}-print.png',require_raster=False)
    META.append({'title':title,'svg':path.name,'print':f'estacoes-{slug}-print.png','type':'gráfico de dados reais','data':f'data-raw/estacoes/{data}','data_sha256':hashlib.sha256((DATA/data).read_bytes()).hexdigest(),'reproduce':'python3 scripts/build_estacoes_data.py && python3 scripts/build_estacoes_art.py','license':'Desenho autoral GPL-3.0; dados mantêm condições das instituições produtoras.'})
    print(path.name,flush=True)


if __name__ == '__main__':
    plates();location();networks();graphs()
    (ART/'estacoes-manifest.json').write_text(json.dumps(META,ensure_ascii=False,indent=2)+'\n')
