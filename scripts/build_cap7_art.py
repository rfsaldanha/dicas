#!/usr/bin/env python3
"""Compõe as 13 figuras conceituais do capítulo 7, sem dados simulados.

Uso: DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap7_art.py [00 ... 12]
Cenas produzidas com image_gen; rótulos e relações permanecem editáveis.
"""
import base64
import hashlib
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image
from figure_style import write_svg
from render_figure import export_print

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'assets/figures'
INK, GREEN, BLUE, TERRA = '#303B36', '#536B50', '#597482', '#AE6B50'
SAND, PALE = '#F3F0E8', '#EEF2F4'
RASTER_VERSIONS = {'00': 'v2'}
SPECS = [
('00', 'conceitos', 'fig-temperatura-conceitos',
 'Condições térmicas, exposição e efeitos na saúde',
 'Duas cenas hipotéticas mostram um trabalhador da construção civil cansado em um canteiro sob calor e uma pessoa em situação de rua encolhida sob uma manta no frio. Ambos têm expressões sérias. O esquema distingue temperatura do ar e da superfície, índices calculados, exposição, resposta fisiológica e efeito em saúde. Moradia, trabalho e proteção modificam as relações. As setas não demonstram causalidade.',
 True, 'Conceitos discutidos no capítulo; referências de termorregulação, exposição e efeitos.'),
('01', 'observacao', 'fig-temperatura-observacao',
 'Do sensor de temperatura do ar à síntese diária',
 'Estação ilustrativa em terreno aberto. O fluxo liga observação com abrigo e horário, controle de qualidade e síntese diária de média, máxima e mínima. A máxima de leituras horárias pode diferir do extremo instrumental.',
 True, 'OMM, guias de instrumentos e práticas climatológicas.'),
('02', 'ar-superficie', 'fig-temperatura-ar-superficie',
 'Temperatura do ar e temperatura da superfície medem componentes distintos',
 'Paisagem hipotética com satélite, superfícies, estação em área aberta e pessoa à sombra. Rótulos distinguem temperatura da superfície, temperatura do ar e microambiente. A perspectiva não representa escala de satélite, resolução ou dados medidos.',
 True, 'Voogt e Oke (2003); NASA, Land Surface Temperature.'),
('03', 'referencias', 'fig-referencias-termicas',
 'Três referências para interpretar calor e frio',
 'Três faixas comparam valor absoluto, posição na climatologia e associação epidemiológica. Temperatura, percentil e temperatura de mínima mortalidade são referências diferentes. Não são propostos valores de alerta.',
 False, 'OMM; Zhang et al. (2005); Gasparrini et al. (2015).'),
('04', 'episodios', 'fig-episodios-termicos',
 'Dias classificados e sequências persistentes',
 'Calendário esquemático sem temperaturas observadas. Círculos indicam critério atendido, traços indicam não atendido e interrogação indica lacuna. Uma sequência de três dias atende à persistência TX90; outra de seis atende à persistência WSDI ou CSDI se a variável e o limiar próprios forem cumpridos. Lacunas não unem episódios.',
 False, 'ETCCDI/Climdex e protocolos das fichas CLI-CAL-01, CLI-CAL-02 e CLI-FRI-01.'),
('05', 'indices', 'fig-indices-biometeorologicos',
 'Trocas térmicas e domínios dos índices biometeorológicos',
 'Pessoa em ambiente externo entre superfície exposta ao sol e árvore. O quadro associa temperatura e umidade ao HI e Humidex; acrescenta vento para AT e radiação para UTCI; distingue as medidas instrumentais do WBGT/IBUTG. Atividade e vestimenta condicionam a interpretação.',
 True, 'Steadman; Masterton; Bröde et al.; ISO 7243 e NHO 06.'),
('06', 'ilhas', 'fig-ilhas-calor-contexto',
 'Estrutura urbana, balanço de energia e referência de comparação',
 'Dois ambientes urbanos hipotéticos com materiais e cobertura vegetal diferentes. O esquema relaciona geometria e materiais, sombra e evapotranspiração à interpretação do contraste térmico. Comparar exige a mesma variável, período e referência. As cenas não quantificam temperaturas ou benefícios.',
 True, 'Oke (1982); Stewart e Oke (2012).'),
('07', 'trabalho', 'fig-trabalho-termico',
 'Calor e frio no trabalho: ambiente, atividade e proteção',
 'Duas cenas hipotéticas mostram trabalho externo com área de pausa e trabalho em câmara refrigerada. Rótulos destacam carga ambiental, esforço, roupa, tempo de permanência e recuperação. A imagem não estabelece limites ocupacionais.',
 True, 'NIOSH; OMS/OMM; Fundacentro, NHO 06.'),
('08', 'defasagens', 'fig-temperatura-defasagens',
 'Da exposição ao registro: diferentes tempos',
 'Etapas distinguem exposição térmica, resposta biológica, procura por cuidado, atendimento e registro. As conexões separam defasagem biológica, tempo até o cuidado e atraso informacional. As distâncias gráficas não correspondem a durações.',
 False, 'Gasparrini et al. (2010); capítulos 4 e 14.'),
('09', 'selecao', 'fig-selecao-termica',
 'Escolher a medida a partir da pergunta',
 'Matriz de decisão relaciona extremos a séries de temperatura, persistência a sequências, carga térmica a variáveis simultâneas e alcance a território e população. Toda escolha passa por verificação de fonte, escala, qualidade e finalidade.',
 False, 'Fichas do capítulo 16 e critérios de seleção do capítulo 5.'),
('10', 'protocolo', 'fig-protocolo-termico',
 'Entradas, referências, cálculo e documentação',
 'Quatro etapas: qualificar entradas; fixar calendário e referência; calcular na célula e agregar; documentar resultado e cobertura. Exceções são explícitas: pessoas-dia soma exposição e extensão regional acompanha componentes espaciais.',
 False, 'Protocolos das 23 fichas térmicas do livro.'),
('11', 'gestao', 'fig-gestao-termica',
 'Preparação, resposta e aprendizagem para calor e frio',
 'Três cenas hipotéticas mostram planejamento, visita de cuidado e infraestrutura do serviço. Um ciclo vetorial articula preparar, monitorar, agir e avaliar, com retorno ao planejamento. As cenas não representam cobertura ou eficácia medidas.',
 True, 'OMM/OMS (2015); OMS (2023); Ministério da Saúde, Nota Técnica Conjunta 270/2026.'),
('12', 'navegacao', 'fig-navegacao-termica',
 'Percurso entre contexto, ficha, fonte e aplicação',
 'Roteiro liga capítulo de contexto, ficha de indicador e fonte com versão e método. O retorno apoia interpretação e aplicação. Indicadores urbanos, de vulnerabilidade, efeitos e resposta complementam o percurso.',
 False, 'Arquitetura editorial do livro.'),
]


def text(x, y, lines, size=46, step=55, weight=400, anchor='middle', fill=INK):
    if isinstance(lines, str):
        lines = [lines]
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(t)}</tspan>'
                    for i, t in enumerate(lines))
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}">{spans}</text>')


def panel(x, y, w, h, title, lines=(), fill=SAND):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
            f'fill="{fill}" stroke="#A4ADA7" stroke-width="2"/>'
            + text(x+w/2, y+65, title, size=51, weight=700)
            + text(x+w/2, y+128, lines))


def arrow(d, dashed=False):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3" '
            + ('stroke-dasharray="10 8" ' if dashed else '')
            + 'marker-end="url(#arrow)"/>')


def raster_path(number):
    version = RASTER_VERSIONS.get(number, 'v1')
    return ART / f'arte-cap7-{number}-{version}.png'


def picture(number, x, y, w, h, crop=None):
    sw, sh = Image.open(raster_path(number)).size
    cx, cy, cw, ch = crop or (0, 0, sw, sh)
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{cx} {cy} {cw} {ch}" '
            f'overflow="hidden"><use href="#aquarela"/></svg>')


def layout(n):
    p = []
    if n == '00':
        sw, sh = Image.open(raster_path(n)).size
        p += [picture(n, 30, 0, 1740, 590, (0, 0, sw, sh*.74)),
              text(450, 610, 'Calor'), text(1350, 610, 'Frio'),
              panel(40, 660, 750, 210, 'Condições térmicas',
                    ['Ar e superfície: alvos distintos', 'Umidade, radiação e vento']),
              panel(1040, 660, 720, 210, 'Índices térmicos',
                    ['Combinações calculadas', 'Hipóteses e domínio próprios'], PALE),
              arrow('M790 760 H1030'), text(915, 715, 'Cálculo', size=42),
              arrow('M310 870 V950')]
        for x,title,lines in [(40,'Exposição',['Lugar, presença,','duração e atividade']),
                              (630,'Resposta fisiológica',['Trocas de calor','e sobrecarga']),
                              (1220,'Efeito em saúde',['Desfecho observado','ou estimado'])]:
            p.append(panel(x, 960, 540, 210, title, lines))
        p += [arrow('M580 1060 H620'), arrow('M1170 1060 H1210'),
              text(900, 1250, 'Moradia, trabalho, condições de saúde e proteção modificam as relações.'),
              text(900, 1320, 'Esquema conceitual: as setas não demonstram causalidade.', size=43)]
        return 1370, p
    if n == '01':
        p += [picture(n, 30, 0, 1740, 760)]
        for x,title,lines in [(40,'Observar',['Sensor, abrigo e entorno','Horário e frequência']),
                              (630,'Qualificar',['Unidade e completude','Metadados e rupturas']),
                              (1220,'Resumir',['Média, máxima e mínima','Dia e método definidos'])]:
            p.append(panel(x, 780, 540, 225, title, lines))
        p += [arrow('M580 890 H620'),arrow('M1170 890 H1210'),
              text(900,1080,['Máxima das leituras horárias ≠ extremo instrumental.',
                              'A observação representa seu entorno, não todo o município.'],size=44)]
        return 1190,p
    if n == '02':
        p += [picture(n, 30, 240, 1740, 790),
              text(420, 75,['Superfícies vistas','pelo sensor'], size=44),
              arrow('M340 165 L260 740'),
              text(870, 75,['Ar no entorno','da estação'], size=44),
              arrow('M870 165 L845 650'),
              text(1440, 75,['Microambiente','e presença'],size=44),
              arrow('M1450 165 L1510 825')]
        for x,title,lines in [(40,'Superfície',['Material, emissividade','e horário de passagem']),
                              (630,'Ar',['Abrigo, altura','e janela da observação']),
                              (1220,'Exposição',['Sombra, atividade','e tempo de permanência'])]:
            p.append(panel(x, 1070, 540, 220, title, lines))
        p += [text(900,1360,'Cena hipotética, fora de escala; sem temperaturas observadas.',size=44)]
        return 1420,p
    if n == '03':
        rows=[('Valor absoluto',['Qual é a temperatura?','Variável e unidade definidas'],
               ['A mesma temperatura pode','ter significados locais distintos.']),
              ('Referência climática',['Quão incomum é a condição?','Percentil ou anomalia'],
               ['Depende do período-base','e da janela de comparação.']),
              ('Referência de saúde',['Qual a associação com o desfecho?','População, modelo e defasagens'],
               ['Não define uma temperatura','ideal para todas as pessoas.'])]
        for i,(title,lines,caution) in enumerate(rows):
            y=40+i*300
            p += [panel(40,y,990,230,title,lines),
                  arrow(f'M1030 {y+110} H1120'),
                  text(1450,y+90,caution,step=60)]
        p += [text(900, 985,'Calor e frio exigem referência explícita; não há limiar sanitário universal.',size=44)]
        return 1040,p
    if n == '04':
        p += [text(900,55,'Calendário conceitual: cada posição representa um dia',size=47,weight=700)]
        patterns=[('Critério diário',[1,0,1,1,1,0,None,1,1,1,1,1,1]),
                  ('O que se reconhece',None)]
        for i,v in enumerate(patterns[0][1]):
            x=75+i*128
            p.append(f'<rect x="{x}" y="135" width="105" height="125" rx="7" fill="white" stroke="#809087" stroke-width="2"/>')
            if v==1:
                p.append(f'<circle cx="{x+52.5}" cy="198" r="26" fill="{GREEN}"/>')
            else:
                p.append(text(x+52.5,214,'?' if v is None else '—',size=59))
        for x,w,caption in [(75,105,'Isolado'),(331,361,'Três dias'),(971,745,'Seis dias')]:
            p += [f'<path d="M{x} 280 V310 H{x+w} V280" fill="none" stroke="{INK}" stroke-width="3"/>',
                  text(x+w/2,375,caption,size=44)]
        p += [panel(40,430,840,240,'TX90',['TX > P90 por ≥ 3 dias','Janela do percentil: 15 dias']),
              panel(920,430,840,240,'WSDI / CSDI',['TX > P90 / TN < P10 por ≥ 6 dias','Janela do percentil: 5 dias']),
              text(900,755,'Cada definição exige sua própria variável e seu próprio limiar.',size=45),
              text(900,820,'A sequência desenhada ilustra apenas a regra de persistência.',size=45),
              text(900,910,'● Critério atendido     — Não atendido     ? Dado ausente',size=44),
              text(900,980,'Lacunas não recebem zero nem unem automaticamente sequências.',size=44)]
        return 1040,p
    if n == '05':
        p += [picture(n,30,0,1740,590),
              text(900,630,'Ambiente, atividade e vestimenta condicionam as trocas.',size=46)]
        rows=[('Temperatura + umidade','HI / Humidex','Calor úmido; fórmulas distintas'),
              ('Temperatura + umidade + vento','AT','Formulação externa à sombra'),
              ('Ar + umidade + vento + radiação','UTCI','Modelo termofisiológico'),
              ('Bulbo úmido natural + globo (+ ar)','WBGT / IBUTG','Triagem e avaliação ocupacional')]
        for i,(inputs,index,use) in enumerate(rows):
            y=690+i*155
            p += [f'<rect x="40" y="{y}" width="1720" height="132" rx="8" fill="{SAND if i%2==0 else PALE}"/>',
                  text(65,y+58,inputs,size=43,anchor='start'),
                  text(65,y+111,use,size=42,anchor='start'),
                  arrow(f'M1130 {y+66} H1250'),text(1490,y+85,index,size=50,weight=700)]
        p += [text(900,1370,'Ar no WBGT: componente adicional quando há carga solar direta.',size=43),
              text(900,1435,'Índice equivalente não é temperatura corporal nem diagnóstico.',size=43)]
        return 1490,p
    if n == '06':
        p += [picture(n,30,0,1740,810),
              text(450,835,'Estrutura e materiais'),text(1350,835,'Cobertura e sombra'),
              panel(40,900,840,235,'Balanço de energia',
                    ['Absorção e armazenamento','Evaporação e liberação de calor']),
              panel(920,900,840,235,'Comparação explícita',
                    ['Ar ou superfície; dia ou noite','Referência e método compatíveis']),
              text(900,1210,'A paisagem sugere mecanismos; o contraste térmico exige medição.',size=45)]
        return 1270,p
    if n == '07':
        p += [picture(n,30,0,1740,810),
              panel(40,830,840,230,'Trabalho no calor',
                    ['Radiação, esforço e roupa','Pausas, água e aclimatização']),
              panel(920,830,840,230,'Trabalho no frio',
                    ['Frio, umidade e permanência','Roupa, abrigo e recuperação']),
              text(900,1130,'Avaliar o posto e a atividade com método apropriado.',size=47),
              text(900,1195,'Uma temperatura externa não resume a exposição ocupacional.',size=44)]
        return 1250,p
    if n == '08':
        entries=[('Exposição',['Condição e permanência'],'Defasagem biológica'),
                 ('Resposta biológica',['Efeito pode se distribuir no tempo'],'Tempo até o cuidado'),
                 ('Procura e atendimento',['Acesso e oferta também interferem'],'Atraso informacional'),
                 ('Registro e consolidação',['Data do evento ≠ data da publicação'],None)]
        for i,(title,lines,lag) in enumerate(entries):
            y=30+i*260
            p.append(panel(40,y,990,190,title,lines))
            if lag:
                p += [arrow(f'M535 {y+190} V{y+250}'),
                      text(1380,y+200,lag,size=46)]
        p += [text(900,1120,'Janelas devem ser justificadas; distâncias não representam durações.',size=44),
              text(900,1190,'Sazonalidade, tendência e qualidade do dado integram a análise.',size=44)]
        return 1250,p
    if n == '09':
        entries=[('Extremos',['TX90p, TXx e TN90p'],['Série de temperatura','e referência apropriada']),
                 ('Persistência',['WSDI, CSDI e ondas'],['Sequências completas','e regra de continuidade']),
                 ('Carga térmica',['HI, AT, Humidex, UTCI, IBUTG'],['Entradas simultâneas','e contexto de uso']),
                 ('Alcance',['Extensão e pessoas-dia'],['Território, duração','e população compatíveis'])]
        for i,(title,indices,needs) in enumerate(entries):
            y=30+i*245
            p += [panel(40,y,870,200,title,indices),
                  arrow(f'M910 {y+100} H1040'),
                  text(1400,y+80,needs,size=46,step=60)]
        p += [text(900,1090,'Verificar fonte, escala, qualidade e finalidade em todas as escolhas.',size=44)]
        return 1150,p
    if n == '10':
        entries=[('1. Entradas e qualidade',['Produto, versão e variáveis','Unidades, simultaneidade e lacunas']),
                 ('2. Referências temporais',['Dia UTC, base e percentil','Janela e regra do episódio']),
                 ('3. Cálculo e agregação',['Indicador primeiro na célula','Depois, síntese territorial definida']),
                 ('4. Disponibilidade e registro',['Cobertura, método e evidência','Dado aberto ≠ série já produzida'])]
        for i,(title,lines) in enumerate(entries):
            y=30+i*270
            p.append(panel(40,y,1120,225,title,lines))
            if i<3:p.append(arrow(f'M600 {y+225} V{y+260}'))
        p += [text(1480,620,['Exceções','documentadas:'],size=47,weight=700),
              text(1480,780,['Pessoas-dia:','somar exposição'],size=44),
              text(1480,935,['Extensão:','componente regional'],size=44)]
        return 1110,p
    if n == '11':
        p += [picture(n,30,0,1740,710)]
        for x,title in [(310,'Planejamento'),(900,'Cuidado'),(1490,'Serviços')]:
            p.append(text(x,745,title,size=47))
        entries=[(40,820,'Preparar',['Território e responsabilidades']),
                 (940,820,'Monitorar',['Previsão, observação e serviços']),
                 (940,1130,'Agir',['Proteção e continuidade']),
                 (40,1130,'Avaliar',['Acesso, resposta e resultados'])]
        for x,y,t,l in entries:p.append(panel(x,y,820,205,t,l))
        p += [arrow('M860 920 H930'),arrow('M1350 1025 V1120'),
              arrow('M940 1230 H870'),arrow('M450 1130 V1035'),
              text(900,1410,'O ciclo abrange calor e frio; registrar decisões permite aprender.',size=44)]
        return 1470,p
    if n == '12':
        p += [panel(40,30,1720,195,'Contexto: capítulo 7',
                    ['Conceito, finalidade, interpretação e limites']),
              arrow('M900 225 V285'),
              panel(40,300,1720,195,'Ficha: capítulo 16',
                    ['Código, definição, fórmula, fonte e protocolo']),
              arrow('M900 495 V555'),
              panel(40,570,1720,195,'Fonte e processamento',
                    ['Produto, versão, extração, qualidade e resultado']),
              arrow('M900 765 V825'),
              panel(40,840,1720,195,'Aplicação e leitura conjunta',
                    ['Ambiente urbano • vulnerabilidade • efeitos • resposta']),
              text(900,1100,'Capítulos de fichas complementares: 20, 22, 23 e 24.',size=46),
              text(900,1170,'A ficha oferece retorno ao contexto; os links estão no texto e no quadro.',size=43)]
        return 1230,p
    raise ValueError(n)


def build(spec):
    number,slug,identifier,title,alt,watercolor,source=spec
    height,parts=layout(number)
    basename=f'arte-cap7-{number}-{slug}'
    meta=dict(number=number,slug=slug,id=identifier,title=title,alt=alt,
              svg=basename+'.svg',print=basename+'-print.png',watercolor=watercolor,
              composition='scripts/build_cap7_art.py',source=source,
              license='Composição autoral sob GPL-3.0, conforme LICENSE; fontes externas mantêm suas condições de uso.',
              conceptual=True,print_width='100%',max_print_width_mm=120,
              review='Relações conceituais, legibilidade, anatomia e instrumentos conferidos; sem dados observados.')
    definition=''
    if watercolor:
        original=raster_path(number)
        sw,sh=Image.open(original).size
        meta.update(raster=original.name,prompt=original.with_suffix('.prompt.txt').name,
                    tool='image_gen',tool_version='Não informada pela ferramenta',
                    reference='assets/references/aquarela-grafite-nanquim.png',
                    reference_delivery='Prévia JPEG de 800 × 533 px da referência, exibida na conversa.',
                    original_dimensions_px=[sw,sh],sha256_original=hashlib.sha256(original.read_bytes()).hexdigest(),
                    min_effective_raster_ppi=round(sw/(120/25.4),1))
        if number=='00':
            meta.update(
                previous_raster='arte-cap7-00-v1.png',
                previous_prompt='arte-cap7-00-v1.prompt.txt',
                reference_delivery='Prévias JPEG exibidas na conversa: alvo v1 em 1000 × 500 px e referência visual em 975 × 650 px.',
                revision='v2: trabalhador da construção civil no calor e pessoa em situação de rua no frio; expressões sérias, sem cenas felizes.',
                review='Cenas, anatomia, dignidade da representação e contraste em cinza conferidos; esquema vetorial preservado; sem dados observados.')
        if number=='07':
            meta['reference_delivery']='Aquarela CAP7-06 como referência imediata de continuidade, derivada da referência visual da série.'
        encoded=base64.b64encode(original.read_bytes()).decode('ascii')
        definition=f'<image id="aquarela" width="{sw}" height="{sh}" href="data:image/png;base64,{encoded}"/>'
    document=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{height}" viewBox="0 0 1800 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(alt)}</desc>
<metadata>{escape(json.dumps(meta,ensure_ascii=False))}</metadata>
<defs>{definition}<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="{INK}"/></marker></defs>
<rect width="1800" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="{INK}">{''.join(parts)}</g></svg>'''
    write_svg(ART/meta['svg'],document)
    export_print(ART/meta['svg'],ART/meta['print'],require_raster=watercolor)
    print(basename,flush=True)
    return meta


if __name__=='__main__':
    selected=set(sys.argv[1:]) or {s[0] for s in SPECS}
    manifest=ART/'arte-cap7-manifest.json'
    records={r['number']:r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    for spec in SPECS:
        if spec[0] in selected:records[spec[0]]=build(spec)
    manifest.write_text(json.dumps([records[k] for k in sorted(records)],ensure_ascii=False,indent=2)+'\n')
