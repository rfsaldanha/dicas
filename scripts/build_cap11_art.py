#!/usr/bin/env python3
"""Compõe nove figuras conceituais: seis aquarelas e três esquemas vetoriais.

DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap11_art.py [00 ... 08]
Os originais são produzidos com image_gen; rótulos e relações são editáveis.
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
SPECS = [['00', 'conceitos', 'fig-terra-saude', 'Cobertura, uso e ocupação: caminhos entre território e saúde', 'A mesma paisagem hipotética distingue cobertura física, função de uso e distribuição da ocupação. Processos ambientais e sociais se ligam à exposição e à proteção antes dos efeitos na saúde.', True, 'IBGE (2013); IPCC (2022); OMS Europa (2016).'], ['01', 'transformacoes', 'fig-terra-transformacoes', 'Transformações da paisagem e vias de exposição', 'Duas vistas conceituais mostram mudanças de vegetação, cultivo e construção. O esquema distingue transformação, processo e contato humano, sem áreas medidas ou resultados observados.', True, 'IBGE (2013); IPCC (2022); INPE e MapBiomas.'], ['02', 'acesso', 'fig-verde-acesso', 'Vegetação, acesso e uso no mesmo bairro', 'Bairro hipotético com jardim privado à esquerda e parque público com entrada à direita. Vegetação, acesso e uso são dimensões distintas. Os critérios de 300 m lineares e 400 m caminháveis pertencem a fichas diferentes; o desenho não está em escala.', True, 'OMS Europa (2016); ODS 11.7.1; fichas do capítulo 20.'], ['03', 'calor', 'fig-terra-calor', 'Superfície, ar e ambiente interno na leitura do calor urbano', 'Cena conceitual com área aberta, bairro e corte de moradia. Superfície observada, ar medido e ambiente interno são alvos diferentes. A referência não urbana exige controle; a paisagem não define um par de estações.', True, 'Oke (1982); Voogt e Oke (2003); Jin (2012).'], ['04', 'fragmentacao', 'fig-terra-fragmentacao', 'Configuração da paisagem e interfaces de contato', 'Manchas de mata em matriz de pastagem e cultivo, com corredor e moradias. Configuração, circulação de agentes e contato humano são etapas diferentes; não há risco sanitário universal associado à vegetação.', True, 'Fahrig (2003); Gibb et al. (2020); IPCC (2022).'], ['05', 'equidade', 'fig-terra-equidade', 'Condições de acesso e distribuição dos benefícios do verde', 'Duas cenas com vegetação: degraus e passeio danificado dificultam entrada à esquerda; acesso nivelado e sombra favorecem circulação e convivência à direita. São condições ilustrativas, sem resultados antes e depois.', True, 'OMS Europa (2016); Markevych et al. (2017); Anguelovski et al. (2022).'], ['06', 'fontes', 'fig-terra-fontes', 'Da pergunta territorial à fonte e à medida', 'Quatro percursos relacionam imagens, mapas classificados, cadastros e população às medidas possíveis. Versão, data, escala e validação delimitam a interpretação; imagem não comprova acesso público.', False, 'IBGE (2013); MapBiomas (2023); capítulos 4, 5 e 20.'], ['07', 'protocolo', 'fig-terra-protocolo', 'Quatro protocolos e suas operações distintas', 'NDVI combina tempo, entorno e ponderação populacional; espaço público separa área e percurso; verde público usa distância linear; SUHII conserva o produto e separa dia e noite. Validade e universo antecedem a publicação.', False, 'Protocolos das fichas AMB-VEG-01 e AMB-URB-01 a 03.'], ['08', 'gestao', 'fig-camadas-urbanas', 'Camadas territoriais, decisão e avaliação distributiva', 'Vegetação, espaço e acesso, contraste térmico e população alimentam o diagnóstico. Priorizar, executar, manter e avaliar formam um ciclo com retorno ao diagnóstico e critérios explícitos.', False, 'Capítulos 6, 11 e 13 a 15; CDC (2024).']]

def text(x,y,lines,size=46,step=56,weight=400,anchor='middle',fill=INK):
    if isinstance(lines,str): lines=[lines]
    spans=''.join(f'<tspan x="{x}" dy="{0 if i==0 else step}">{escape(t)}</tspan>' for i,t in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">{spans}</text>'


def panel(x,y,w,h,title,lines=(),fill=SAND):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="#A4ADA7" stroke-width="2"/>'
            +text(x+w/2,y+63,title,size=50,weight=700)+text(x+w/2,y+128,lines))


def arrow(d,dashed=False):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3" '+('stroke-dasharray="10 8" ' if dashed else '')+'marker-end="url(#arrow)"/>'



def picture(n):
    sw,sh=Image.open(ART/f'arte-cap11-{n}-v1.png').size
    return f'<svg x="30" y="0" width="1740" height="{1740*sh/sw}" viewBox="0 0 {sw} {sh}"><use href="#aquarela"/></svg>'

def three(y,items,h=220):
    return [panel(x,y,540,h,title,lines) for x,(title,lines) in zip((40,630,1220),items)]

def layout(n):
    y={'00':930,'01':880,'02':1000,'03':800,'04':970,'05':970}.get(n,0)
    p=[picture(n)] if n<='05' else []
    if n=='00':
        p+=three(y,[('Cobertura',['O que recobre','a superfície']),('Uso',['Que atividades','e funções ocorrem']),('Ocupação',['Como população','e estruturas se distribuem'])])
        p += [arrow(f'M310 {y+220} V{y+245} H900 V{y+265}'),arrow(f'M900 {y+220} V{y+240}'),arrow(f'M1490 {y+220} V{y+245} H925'),panel(40,y+280,1720,190,'Processos ambientais e sociais',['Calor, água, ar, habitats, trabalho, mobilidade e convívio']),arrow(f'M900 {y+470} V{y+515}'),text(900,y+575,'Exposição e proteção → efeitos na saúde',size=50),text(900,y+650,'Desigualdades, regulação e infraestrutura atravessam os caminhos.',size=44)]
        return y+710,p
    if n=='01':
        p+=three(y,[('Transformação',['Cobertura, uso','e configuração']),('Processo',['Energia, água,','emissões e habitats']),('Contato',['Onde, quando','e quem se expõe'])])
        p += [arrow(f'M580 {y+110} H615'),arrow(f'M1170 {y+110} H1205'),text(900,y+310,'Mapear a mudança é uma etapa da investigação.',size=48),text(900,y+385,'População, atividade e proteção completam a leitura.',size=46)]
        return y+445,p
    if n=='02':
        p+=three(y,[('Vegetação',['Pública ou privada','na imagem']),('Acesso',['Entrada, percurso','e barreiras']),('Uso',['Permanência','e atividades'])])
        p += [panel(40,y+265,830,205,'300 m lineares',['Ao limite do verde público','contínuo com pelo menos 1 ha']),panel(930,y+265,830,205,'400 m caminháveis',['À entrada do espaço','aberto público']),text(900,y+550,'Critérios de fichas distintas; desenho sem escala métrica.',size=45)]
        return y+610,p
    if n=='03':
        p+=three(y,[('Ar',['Abrigo, altura','e horário definidos']),('Superfície',['Telhados, pavimentos','e copas vistos pelo sensor']),('Ambiente interno',['Materiais, ventilação','e condições de uso'])])
        p += [panel(40,y+265,1720,185,'SUHII: contraste com uma referência',['Conservar produto e referência; separar dia e noite.']),text(900,y+530,'Contraste pequeno não demonstra ausência de calor.',size=46)]
        return y+590,p
    if n=='04':
        p+=three(y,[('Mancha e borda',['Habitat considerado','e sua interface']),('Matriz',['Mosaico que envolve','as manchas']),('Conectividade',['Ligação espacial','e deslocamento possível'])])
        p += [panel(40,y+265,1720,185,'A investigação precisa de mais etapas',['Paisagem → agente e hospedeiros → contato humano']),text(900,y+530,'O risco depende da doença, da escala e do contexto.',size=46)]
        return y+590,p
    if n=='05':
        p += [panel(40,y,830,200,'Barreiras ao usufruto',['Percurso, entrada','e manutenção']),panel(930,y,830,200,'Condições favoráveis',['Acessibilidade, sombra','e convivência']),arrow(f'M455 {y+200} V{y+250} H900 V{y+290}'),arrow(f'M1345 {y+200} V{y+250} H920'),panel(40,y+310,1720,180,'Avaliar quem recebe os benefícios',['Distribuição, permanência dos moradores e participação']),text(900,y+570,'Vegetação presente não garante acesso, uso ou equidade.',size=45)]
        return y+630,p
    if n=='06':
        rows=[('Verdor',['Reflectância','e qualidade'],['NDVI','no entorno']),('Mudança',['Mapas classificados','compatíveis'],['Permanências','e transições']),('Oferta e acesso',['Cadastro público','e rede datados'],['Área e população','atendida']),('Distribuição',['População e malhas','compatíveis'],['Denominadores','e grupos'])]
        for i,(q,s,m) in enumerate(rows):
            y=30+i*270
            p+=three(y,[(q,['Pergunta']),('Fonte',s),('Medida',m)])
            p += [arrow(f'M580 {y+110} H615'),arrow(f'M1170 {y+110} H1205')]
        p += [text(900,1190,'Versão, data, escala e validação delimitam a interpretação.',size=46),text(900,1260,'A imagem não comprova acesso público.',size=46)]
        return 1320,p
    if n=='07':
        rows=[('AMB-VEG-01',['Mediana anual → entorno','→ ponderação populacional'],['NDVI','adimensional']),('AMB-URB-01',['União de áreas públicas;','rede e entradas para acesso'],['% de área;','% de população']),('AMB-URB-02',['Verde público ≥1 ha;','zonas de 300 m lineares'],['% de população','próxima']),('AMB-URB-03',['YCEO v4, 2003–2018;','média municipal por área'],['SUHII em °C','dia / noite'])]
        for i,(code,method,result) in enumerate(rows):
            y=30+i*260
            p += [panel(40,y,420,210,code,['Ficha']),panel(530,y,720,210,'Operações',method),panel(1320,y,440,210,'Saída',result),arrow(f'M460 {y+100} H515'),arrow(f'M1250 {y+100} H1305')]
        p += [text(900,1130,'Conservar universo, validade, cobertura e versão.',size=48),text(900,1205,'Ausente, zero e não aplicável são situações distintas.',size=46)]
        return 1270,p
    if n=='08':
        p=[panel(40,30,830,190,'Vegetação',['Verdor e cobertura']),panel(930,30,830,190,'Espaços e acesso',['Oferta, percurso e proximidade']),panel(40,270,830,190,'Contraste térmico',['Superfície; dia e noite']),panel(930,270,830,190,'População e proteção',['Moradia, mobilidade e grupos']),arrow('M455 220 V245 H900 V550'),arrow('M1345 220 V245 H920'),arrow('M455 460 V510 H900 V550'),arrow('M1345 460 V510 H920'),panel(190,570,1420,180,'Diagnóstico orientado pela pergunta',['Preservar componentes e explicitar critérios']),arrow('M900 750 V805'),panel(190,825,1420,180,'Priorizar e executar',['Responsabilidade, recursos e participação']),arrow('M900 1005 V1060'),panel(190,1080,1420,180,'Manter e avaliar',['Acesso, uso, saúde e distribuição dos benefícios']),arrow('M1610 1170 H1720 V660 H1625',True),text(900,1340,'Resultados e dificuldades alimentam a revisão das ações.',size=46)]
        return 1400,p
    raise ValueError(n)


def build(spec):
    number,slug,identifier,title,alt,watercolor,source=spec
    height,parts=layout(number)
    basename=f'arte-cap11-{number}-{slug}'
    meta=dict(number=number,slug=slug,id=identifier,title=title,alt=alt,svg=basename+'.svg',print=basename+'-print.png',watercolor=watercolor,
              composition='scripts/build_cap11_art.py',source=source,conceptual=True,
              license='Composição autoral sob GPL-3.0, conforme LICENSE; fontes externas mantêm suas condições de uso.',
              max_print_width_mm=120,print_export_width_px=1800)
    definition=''
    if watercolor:
        original=ART/f'arte-cap11-{number}-v1.png'
        sw,sh=Image.open(original).size
        meta.update(raster=original.name,prompt=original.with_suffix('.prompt.txt').name,tool='image_gen',tool_version='Não informada pela ferramenta',
                    reference='assets/references/aquarela-grafite-nanquim.png',reference_delivery='Prévia JPEG de 800 × 533 px exibida antes de cada geração; num_last_images_to_include=1. Leitura direta indisponível por falha de isolamento.',
                    original_dimensions_px=[sw,sh],sha256_original=hashlib.sha256(original.read_bytes()).hexdigest(),
                    min_effective_raster_ppi=round(sw/(120/25.4),1))
        encoded=base64.b64encode(original.read_bytes()).decode('ascii')
        definition=f'<image id="aquarela" width="{sw}" height="{sh}" href="data:image/png;base64,{encoded}"/>'
    document=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{height}" viewBox="0 0 1800 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(alt)}</desc>
<metadata>{escape(json.dumps(meta,ensure_ascii=False))}</metadata>
<defs>{definition}<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="{INK}"/></marker></defs>
<rect width="1800" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="{INK}">{''.join(parts)}</g></svg>'''
    write_svg(ART/meta['svg'],document)
    export_print(ART/meta['svg'],ART/meta['print'],width=1800,require_raster=watercolor)
    print(basename,flush=True)
    return meta


if __name__=='__main__':
    selected=set(sys.argv[1:]) or {s[0] for s in SPECS}
    unknown=selected-{s[0] for s in SPECS}
    if unknown:raise SystemExit('Códigos desconhecidos: '+', '.join(sorted(unknown)))
    manifest=ART/'arte-cap11-manifest.json'
    records={r['number']:r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    for spec in SPECS:
        if spec[0] in selected:records[spec[0]]=build(spec)
    manifest.write_text(json.dumps([records[k] for k in sorted(records)],ensure_ascii=False,indent=2)+'\n')
