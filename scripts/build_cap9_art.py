#!/usr/bin/env python3
"""Monta as 11 figuras do capítulo 9; cenas conceituais, sem dados simulados.

DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap9_art.py [00 ... 10]
Aquarelas produzidas por image_gen; texto e relações permanecem vetoriais.
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
VERSIONS = {'04': 'v2'}
# Código, nome, identificador editorial, legenda, descrição, aquarela, fonte.
SPECS = [
('00', 'conceitos', 'fig-cadeia-ar-saude', 'Da emissão ao efeito sobre a saúde',
 'Bairro hipotético com fogo distante, fumaça, moradias e visita de saúde. O esquema distingue emissão, concentração ambiente, exposição, dose e efeito, com transporte e transformação entre fonte e concentração. Meteorologia, microambientes e suscetibilidade modificam as relações; as setas não atribuem causalidade a casos individuais.',
 True, 'OMS (2021); EPA (2019), avaliação de exposição; fundamentos discutidos no capítulo.'),
('01', 'fontes', 'fig-ar-fontes', 'Fontes, emissões e formação de poluentes',
 'Paisagem hipotética reúne tráfego, indústria, solo exposto e fogo em vegetação. Rótulos distinguem fontes móveis, fixas e difusas. Poluentes primários são emitidos; secundários se formam na atmosfera. A dimensão ou cor da fumaça não representa participação nas emissões.',
 True, 'OMS (2021); EPA, Enhanced Air Sensor Guidebook (2022).'),
('02', 'particulas', 'fig-ar-particulas', 'Tamanho, composição e interpretação do material particulado',
 'Esquema vetorial mostra PM2,5 dentro da fração PM10, cujos cortes aerodinâmicos são 2,5 e 10 micrômetros. Composição, forma e densidade aparecem como propriedades adicionais. A deposição depende de partículas e respiração; os cortes não são fronteiras anatômicas. O desenho não está em escala.',
 False, 'EPA, Integrated Science Assessment for Particulate Matter (2019); OMS (2021).'),
('03', 'gases', 'fig-ar-gases', 'Gases emitidos e poluentes formados na atmosfera',
 'Dois percursos distinguem emissões diretas de CO, SO₂ e óxidos de nitrogênio e formação fotoquímica de ozônio a partir de precursores. Transformações também contribuem para partículas secundárias. Concentração, unidade e tempo de média permanecem específicos de cada poluente.',
 False, 'OMS (2021); EPA, Ground-level Ozone Basics; MMA (2025).'),
('04', 'observacao', 'fig-ar-observacao', 'Observação pontual, coluna atmosférica e campo modelado',
 'Estação de referência e sensor compacto estão em terreno aberto, com técnica e cidade ao fundo. Um satélite fora de escala representa observação da coluna. Quatro campos diferenciam estação, sensor avaliado por co-localização, satélite e modelo. AOD é adimensional e não equivale a PM2,5 superficial.',
 True, 'EPA, Enhanced Air Sensor Guidebook (2022) e guia de co-localização; Hu et al. (2025).'),
('05', 'fogo', 'fig-ar-fogo', 'Ocorrência de fogo, foco detectado e área queimada',
 'Três painéis mostram fogo em vegetação, grade esquemática de detecção sobre a mesma cena e cicatriz após o fogo. Os dois primeiros reutilizam exatamente o mesmo recorte; a terceira vinheta representa outro momento. Células destacadas não são detecções reais e a grade não tem resolução geográfica. Focos não são contagem de incêndios nem área queimada.',
 True, 'INPE, perguntas frequentes do Programa Queimadas; protocolo da ficha de área queimada.'),
('06', 'transporte', 'fig-fumaca-exposicao', 'Do foco de fogo à dose: medidas que não devem ser confundidas',
 'Pluma liga fogo em vegetação a uma cidade distante em paisagem hipotética. O esquema distingue fogo e emissões, transporte e transformação, observação orbital, concentração medida ou modelada, exposição em microambientes e dose. Pluma elevada não determina sozinha concentração no solo; PM2,5 total não é a parcela de fogo.',
 True, 'INPE; Reid et al. (2016); Hu et al. (2025); EPA (2019), avaliação de exposição.'),
('07', 'exposicao', 'fig-ar-exposicao', 'Microambientes, duração da exposição e efeitos na saúde',
 'Três cenas conceituais apresentam trabalho na rua, mãe e criança em casa e pessoa idosa em consulta. Os quadros distinguem concentrações de curto prazo e médias prolongadas, com atividade, proteção, suscetibilidade e acesso ao cuidado. Não há séries, frequências ou riscos simulados.',
 True, 'EPA (2019); Reid et al. (2016); Ye et al. (2021).'),
('08', 'selecao', 'fig-ar-selecao', 'Escolher a medida conforme a pergunta',
 'Cinco linhas associam exposição prolongada a PM2,5 anual ponderado; concentrações diárias elevadas a P99; comunicação a IQAr; parcela de fumaça a PM2,5 de fogo; extensão territorial a área queimada. As medidas mantêm diferentes suportes e não formam uma escala única de risco.',
 False, 'Protocolos das cinco fichas do capítulo 18.'),
('09', 'protocolo', 'fig-ar-protocolo', 'Da entrada documentada ao resultado com cobertura',
 'Fluxo liga escolha de produto e versão, controle de qualidade, cálculo e publicação. Três ramificações distinguem séries de estação, grades com população e cicatrizes territoriais. Cada uma mantém regras próprias; cobertura, unidade e incerteza acompanham o resultado.',
 False, 'Protocolos das cinco fichas do capítulo 18 e princípios do capítulo 4.'),
('10', 'gestao', 'fig-ar-gestao', 'Monitoramento, decisão, comunicação e avaliação',
 'Três cenas de aquarela mostram equipe intersetorial, orientação no trabalho e unidade de saúde em funcionamento. O ciclo vetorial liga monitorar, decidir, comunicar e avaliar, retornando ao planejamento. Responsabilidades e recursos sustentam as ações; as cenas não medem eficácia.',
 True, 'MMA (2025); Ministério da Saúde, Nota Técnica Conjunta 217/2024; capítulos 6 e 15.'),
]


def text(x, y, lines, size=51, step=61, weight=400, anchor='middle', fill=INK):
    if isinstance(lines, str): lines = [lines]
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(s)}</tspan>' for i,s in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">{spans}</text>'


def box(x,y,w,h,title,lines=(),fill=SAND):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="#A4ADA7" stroke-width="2"/>'
            +text(x+w/2,y+65 if lines else y+h/2+20,title,size=56,weight=700)+(text(x+w/2,y+133,lines) if lines else ''))


def arrow(d,dashed=False):
    dash=' stroke-dasharray="10 8"' if dashed else ''
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3"{dash} marker-end="url(#arrow)"/>'


def raster(n): return ART/f'arte-cap9-{n}-{VERSIONS.get(n,"v1")}.png'


def picture(n,x=40,y=0,w=1720,h=1000,crop=None):
    sw,sh=Image.open(raster(n)).size
    cx,cy,cw,ch=crop or (0,0,sw,sh)
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{cx} {cy} {cw} {ch}" overflow="hidden"><use href="#aquarela"/></svg>'


def row3(y,entries,h=235):
    return [box(40+i*590,y,540,h,title,lines) for i,(title,lines) in enumerate(entries)]


def layout(n):
    p=[]
    if n=='00':
        p=[picture(n,h=910)]
        p+=row3(920,[('Emissão',['Massa liberada','por uma fonte']),('Transporte',['Transformação','e dispersão']),('Concentração',['Quantidade por','volume de ar'])])
        p+=[arrow('M580 1040 H620'),arrow('M1170 1040 H1210'),arrow('M1490 1155 V1210 H310 V1260')]
        p+=row3(1270,[('Exposição',['Contato ao longo','do tempo']),('Dose',['Inalada, depositada','ou absorvida']),('Efeito',['Alteração observada','ou estimada'])])
        p+=[arrow('M580 1390 H620'),arrow('M1170 1390 H1210'),text(900,1590,['Meteorologia • microambientes • atividade • suscetibilidade'],size=48),text(900,1660,'Relações conceituais; sem atribuição de casos individuais.',size=48)]
        return 1730,p
    if n=='01':
        p=[picture(n,h=960)]
        p+=row3(940,[('Móveis',['Tráfego e máquinas']),('Fixas',['Instalações e processos']),('Difusas',['Solo e queima em área'])],200)
        p+=[box(40,1210,810,250,'Poluentes primários',['Liberados diretamente','por uma fonte']),arrow('M850 1330 H940'),box(960,1210,800,250,'Poluentes secundários',['Formados a partir','de precursores'],PALE),text(900,1550,'Meteorologia e química modificam a concentração ambiente.',size=49)]
        return 1620,p
    if n=='02':
        p=[f'<rect x="70" y="50" width="960" height="640" rx="55" fill="{SAND}" stroke="{GREEN}" stroke-width="4"/>',
           text(550,145,'Fração PM10',size=62,weight=700),text(550,220,'Corte aerodinâmico: 10 µm'),
           f'<rect x="180" y="295" width="740" height="315" rx="40" fill="{PALE}" stroke="{BLUE}" stroke-width="4"/>',
           text(550,395,'Fração PM2,5',size=62,weight=700),text(550,475,'Corte: 2,5 µm'),text(550,550,'Integra a fração PM10'),
           box(1100,55,630,300,'Composição',['Carbono, sais,','compostos orgânicos','e minerais']),
           box(1100,385,630,270,'Outras propriedades',['Forma e densidade','também importam']),
           box(70,780,1660,230,'Deposição no organismo',['Depende das partículas, da respiração e da pessoa.','Os cortes não definem fronteiras anatômicas.']),
           text(900,1100,'As massas de PM10 e PM2,5 não são parcelas independentes.',size=49),text(900,1175,'Esquema conceitual, sem escala geométrica ou dados observados.',size=47)]
        return 1240,p
    if n=='03':
        p=[box(40,40,1720,220,'Fontes e processos de combustão',['Veículos, indústria, energia e fogo']),
           arrow('M430 260 V360'),arrow('M1320 260 V360'),
           box(40,370,810,305,'Emissão direta',['CO • SO₂ • óxidos','de nitrogênio','Composição depende da fonte']),
           box(950,370,810,305,'Precursores',['Óxidos de nitrogênio','e compostos orgânicos voláteis','+ radiação solar'],PALE),
           arrow('M1690 675 V780'),text(1355,733,'Reações fotoquímicas',size=48),
           box(950,790,810,210,'Ozônio troposférico',['Formação secundária']),
           box(40,790,810,210,'Outras transformações',['Partículas secundárias'],PALE),arrow('M440 675 V780'),
           box(40,1100,1720,230,'Interpretar cada poluente',['Concentração + unidade + tempo de média','PM2,5 não substitui a medição dos gases.']),
           text(900,1420,'Esquema de processos, sem equações químicas ou taxas de reação.',size=47)]
        return 1490,p
    if n=='04':
        p=[picture(n,h=1000)]
        for i,(title,lines) in enumerate([('Estação',['Concentração em um ponto','Método e entorno']),('Sensor suplementar',['Comparar com referência','Co-localização e deriva']),('Satélite',['Coluna atmosférica','Passagem e nuvens']),('Modelo',['Campo estimado em grade','Emissões, química e tempo'])]):
            x=40+(i%2)*900; y=1040+(i//2)*300
            p.append(box(x,y,820,240,title,lines,SAND if i<2 else PALE))
        p+=[text(900,1655,'AOD ≠ PM2,5 na superfície; resolução não garante acurácia local.',size=47),text(900,1720,'Cena hipotética; satélite fora de escala.',size=47)]
        return 1790,p
    if n=='05':
        sw,sh=Image.open(raster(n)).size
        # O mesmo recorte é usado em ocorrência e detecção: geografia idêntica.
        for i,crop in enumerate([(0,0,sw/3,sh),(0,0,sw/3,sh),(2*sw/3,0,sw/3,sh)]):
            p.append(picture(n,x=35+i*590,y=120,w=550,h=780,crop=crop))
        for i,t in enumerate(['Ocorrência','Detecção','Cicatriz']):p.append(text(310+i*590,70,t,size=58,weight=700))
        for x in range(665,1146,80):p.append(f'<path d="M{x} 195 V835" stroke="{BLUE}" stroke-width="2" fill="none"/>')
        for y in range(195,836,80):p.append(f'<path d="M665 {y} H1145" stroke="{BLUE}" stroke-width="2" fill="none"/>')
        for x,y in [(905,275),(985,275),(985,355)]:p.append(f'<rect x="{x}" y="{y}" width="80" height="80" fill="{TERRA}" fill-opacity="0.3" stroke="{TERRA}" stroke-width="4"/>')
        p+=row3(960,[('Fogo em vegetação',['Um evento pode','durar várias passagens']),('Foco ativo',['Registro do sensor','e do algoritmo']),('Área queimada',['Superfície mapeada','após o fogo'])],240)
        p+=[text(900,1290,'Focos ≠ incêndios distintos ≠ área queimada.',size=53,weight=700),text(900,1360,'Grade e células ilustrativas; sem resolução ou detecções reais.',size=47)]
        return 1430,p
    if n=='06':
        p=[picture(n,h=950)]
        p+=row3(970,[('Fogo e emissão',['Detecção não mede','massa emitida']),('Pluma',['Transporte','e transformação']),('Observação orbital',['Fogo ou aerossóis','na coluna'])],240)
        p+=[arrow('M580 1090 H620'),arrow('M1170 1090 H1210')]
        p+=[arrow('M900 1210 V1310'),box(40,1320,810,235,'Concentração',['Estação: medida em um ponto','Modelo: estimada em grade']),box(950,1320,810,235,'Exposição e dose',['Microambientes e permanência','Ventilação, deposição e absorção']),arrow('M850 1440 H940'),
            text(900,1640,'Pluma elevada não determina sozinha a concentração no solo.',size=48),text(900,1710,'PM2,5 total ≠ parcela atribuível ao fogo.',size=51,weight=700)]
        # A ligação da pluma à concentração entra pela caixa, sem passar pela observação orbital.
        p[6]=arrow('M900 1210 V1270 H440 V1310')
        return 1780,p
    if n=='07':
        p=[picture(n,h=960)]
        p+=row3(930,[('Trabalho',['Atividade e duração']),('Moradia',['Infiltração e proteção']),('Cuidado',['Suscetibilidade e acesso'])],200)
        p+=[box(40,1210,820,250,'Curto prazo',['Horas, dias e episódios','Efeitos podem ter defasagem']),box(940,1210,820,250,'Exposição prolongada',['Meses ou anos','Conforme o desenho do estudo'],PALE),text(900,1550,'Uma resposta aguda pode ocorrer sobre uma doença crônica.',size=49),text(900,1620,'Concentração externa não é dose individual.',size=51,weight=700)]
        return 1690,p
    if n=='08':
        rows=[('Exposição prolongada','PM2,5 anual ponderado','Recorte urbano e população'),('Concentrações diárias elevadas','P99 das médias de 24 h','Estação e distribuição anual'),('Comunicação de curto prazo','IQAr','Maior subíndice disponível'),('Parcela atribuível ao fogo','PM2,5 de fogo ponderado','Modelo de fonte e população'),('Extensão territorial do fogo','Área municipal queimada','União de cicatrizes no ano')]
        p=[text(470,70,'Pergunta',size=58,weight=700),text(1370,70,'Medida e suporte',size=58,weight=700)]
        for i,(q,m,s) in enumerate(rows):
            y=130+i*245
            p += [box(40,y,820,200,q,(),SAND),arrow(f'M860 {y+95} H930'),box(950,y,810,200,m,[s],PALE)]
        p+=[text(900,1430,'Fonte, período, unidade e cobertura acompanham todas as medidas.',size=48)]
        return 1500,p
    if n=='09':
        p=[box(40,40,1720,210,'Fixar as entradas',['Produto • versão • variável • calendário • suporte']),arrow('M900 250 V320'),box(40,330,1720,210,'Qualificar os dados',['Validação • unidades • duplicações • lacunas • completude'])]
        for x in [310,900,1490]:p.append(arrow(f'M{x} 540 V670'))
        p+=row3(680,[('Estações',['Médias por poluente','P99 e subíndices']),('Grades e população',['Conservar população','Recorte e ponderação']),('Cicatrizes',['União anual de áreas','Proporção territorial'])],250)
        for x in [310,900,1490]:p.append(arrow(f'M{x} 930 V1050'))
        p+=[box(40,1060,1720,240,'Publicar com rastreabilidade',['Resultado + unidade + cobertura + incerteza','Guardar denominadores, regras e motivos das ausências.']),text(900,1390,'Cada ficha mantém suas regras; calculável não significa já validado.',size=48)]
        return 1460,p
    if n=='10':
        p=[picture(n,h=960)]
        p+=[box(90,1030,740,220,'Monitorar',['Dado, previsão e cobertura']),box(970,1030,740,220,'Decidir',['Responsáveis e recursos']),box(970,1380,740,220,'Comunicar e agir',['Medidas viáveis e acessíveis']),box(90,1380,740,220,'Avaliar',['Alcance e continuidade']),arrow('M830 1140 H960'),arrow('M1340 1250 V1370'),arrow('M970 1490 H840'),arrow('M460 1380 V1260'),text(900,1690,'A avaliação orienta o próximo planejamento.',size=52)]
        return 1760,p
    raise ValueError(n)


def build(spec):
    number,slug,identifier,title,alt,watercolor,source=spec
    height,parts=layout(number)
    basename=f'arte-cap9-{number}-{slug}'
    meta=dict(number=number,slug=slug,id=identifier,title=title,alt=alt,svg=basename+'.svg',
              print=basename+'-print.png',watercolor=watercolor,source=source,
              composition='scripts/build_cap9_art.py',conceptual=True,max_print_width_mm=120,export_width_px=1600 if watercolor else 1800,
              license='Composição autoral sob GPL-3.0, conforme LICENSE; fontes externas mantêm suas condições de uso.')
    definition=''
    if watercolor:
        original=raster(number); sw,sh=Image.open(original).size
        meta.update(raster=original.name,prompt=original.with_suffix('.prompt.txt').name,
                    tool='image_gen',tool_version='Não informada pela ferramenta',
                    reference='assets/references/aquarela-grafite-nanquim.png',
                    reference_delivery=('Prévia JPEG de 700 px da referência exibida na conversa.' if number=='00' else 'Aquarela CAP9-00 como referência imediata, derivada da referência visual da série.'),
                    original_dimensions_px=[sw,sh],sha256_original=hashlib.sha256(original.read_bytes()).hexdigest(),
                    min_effective_raster_ppi=round(sw/(120/25.4),1))
        if number=='04':
            meta.update(previous_raster='arte-cap9-04-v1.png',previous_prompt='arte-cap9-04-v1.prompt.txt',
                        reference_delivery='Prévia JPEG de 900 px da versão v1 exibida para edição.',
                        revision='Remoção de copa e arbustos junto à cabine; sensor compacto ventilado.')
        if number=='05':meta['assembly']='Primeiro recorte repetido nos painéis de ocorrência e detecção; terceiro painel usa a vinheta de cicatriz.'
        encoded=base64.b64encode(original.read_bytes()).decode('ascii')
        definition=f'<image id="aquarela" width="{sw}" height="{sh}" href="data:image/png;base64,{encoded}"/>'
    fonts=''
    for suffix,weight in [('Regular',400),('Bold',700)]:
        data=base64.b64encode((ROOT/f'assets/fonts/SourceSans3-{suffix}.woff2').read_bytes()).decode('ascii')
        fonts+=f'@font-face{{font-family:"Source Sans 3";font-weight:{weight};src:url("data:font/woff2;base64,{data}") format("woff2");}}'
    document=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{height}" viewBox="0 0 1800 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(alt)}</desc>
<metadata>{escape(json.dumps(meta,ensure_ascii=False))}</metadata>
<style>{fonts}</style><defs>{definition}<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="{INK}"/></marker></defs>
<rect width="1800" height="{height}" fill="white"/>
<g font-family="'Source Sans 3', sans-serif" fill="{INK}">{''.join(parts)}</g></svg>'''
    write_svg(ART/meta['svg'],document)
    export_print(ART/meta['svg'],ART/meta['print'],width=1600 if watercolor else 1800,require_raster=watercolor)
    print(basename,flush=True)
    return meta


if __name__=='__main__':
    selected=set(sys.argv[1:]) or {s[0] for s in SPECS}
    manifest=ART/'arte-cap9-manifest.json'
    records={r['number']:r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    for spec in SPECS:
        if spec[0] in selected:records[spec[0]]=build(spec)
    manifest.write_text(json.dumps([records[k] for k in sorted(records)],ensure_ascii=False,indent=2)+'\n')
