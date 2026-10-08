#!/usr/bin/env python3
"""Compõe dez ilustrações do capítulo 12: cinco aquarelas e cinco esquemas.

DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap12_art.py [00 ... 09]
Originais image_gen preservados; textos e conexões permanecem editáveis.
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
SPECS = [
('00', 'conceitos', 'fig-risco-desastre', 'Evento, risco, desastre e saúde: conceitos complementares',
 'Paisagem hipotética mostra chuva, moradias próximas ao rio e uma unidade de saúde em área mais alta. Oito campos distinguem extremo, severo, perigo, exposição, vulnerabilidade, capacidade, risco e desastre. Efeitos diretos e indiretos na saúde dependem da interação no território; não há uma sequência inevitável de risco para desastre.', True,
 'UNDRR (2017); IPCC (2021, 2022); OMS (2019).'),
('01', 'perigos', 'fig-desastre-perigos', 'Perigos distintos e vias de dano em tempestades',
 'Quatro vinhetas hipotéticas mostram tempestade com raio, vento, granizo e tornado. Os rótulos relacionam perigos a lesões, danos à moradia e falhas de infraestrutura. Não representam frequência, escala comparável ou intensidade observada.', True,
 'UNDRR/ISC, Hazard Information Profiles (2025).'),
('02', 'componentes', 'fig-desastre-componentes', 'Condições do território modificam o risco',
 'Um mesmo perigo é considerado em duas configurações hipotéticas. Uma tem ocupação exposta, moradias frágeis e acesso único; a outra combina menor exposição, estruturas protegidas e alternativas de cuidado. A comparação distingue exposição, vulnerabilidade e capacidade, sem pesos, escores ou garantia de ausência de impactos.', False,
 'UNDRR (2017); OMS (2021); Lacerda e Freitas (2024).'),
('03', 'danos', 'fig-desastre-danos', 'Pessoas, moradias e meios de vida: unidades diferentes',
 'Três cenas conceituais mostram atendimento de uma pessoa, moradia com telhado danificado e comércio afetado por inundação. O esquema distingue componentes de afetação e destaca que uma pessoa pode aparecer em mais de um componente. Mortes e desaparecimentos são acompanhados separadamente; as vinhetas não representam contagens.', True,
 'Nações Unidas (2024), metadados ODS 1.5.1; fichas DES-HUM-01 e DES-HUM-02.'),
('04', 'servicos', 'fig-desastre-servicos', 'A continuidade depende do prédio, das redes e do cuidado',
 'Unidade de saúde hipotética permanece fisicamente intacta, enquanto um poste danificado e uma via alagada afetam seu entorno. Água, energia, acesso, equipes e insumos são dependências do funcionamento. Dano físico, interrupção e alternativa assistencial são registros distintos; equipamentos desenhados não comprovam funcionamento.', True,
 'Nações Unidas (2024), metadados ODS 11.5.3; OMS (2023, 2024).'),
('05', 'recuperacao', 'fig-desastre-recuperacao', 'Acompanhamento da saúde durante o deslocamento e a recuperação',
 'Três vinhetas conceituais mostram acolhimento de uma família, consulta de acompanhamento e cuidado no território em recuperação. Uma faixa temporal qualitativa destaca necessidades sobrepostas, continuidade do tratamento e apoio psicossocial. Não há duração fixa nem promessa de recuperação linear.', True,
 'Freitas et al. (2014); Ministério da Saúde (2024); OMS (2025).'),
('06', 'vigilancia', 'fig-desastre-vigilancia', 'Da informação verificada à ação e ao acompanhamento',
 'Fluxo liga alerta, verificação local, decisão, ação e acompanhamento. Retorno tracejado orienta revisar a informação e a decisão. Um identificador de episódio conecta registros preservando fonte, horário, versão, unidade e incerteza.', False,
 'OMS (2019, 2022, 2023); capítulo 6.'),
('07', 'fontes', 'fig-desastre-fontes', 'Pergunta, fonte e unidade de observação',
 'Matriz associa condições esperadas a alertas, danos a S2iD e Atlas, eventos de saúde aos sistemas sanitários, continuidade a registros locais e população ao IBGE. A integração exige compatibilidade temporal, territorial e conceitual; vinculação não é automática.', False,
 'Atlas Digital de Desastres; DATASUS; IBGE; Cemaden; capítulo 5.'),
('08', 'protocolo', 'fig-desastre-protocolo', 'Quatro fichas e dois caminhos de obtenção dos dados',
 'Duas colunas separam dados abertos do Atlas, usados nas fichas DES-HUM-01 e DES-SAU-01, de dados locais necessários às fichas DES-HUM-02 e DES-SAU-02. O fluxo destaca versão, completude, unidade e publicação. Ausência de registro, incompletude e zero informado permanecem distintos.', False,
 'Protocolos das quatro fichas do capítulo 21.'),
('09', 'gestao', 'fig-linha-tempo-desastre', 'Registros e decisões ao longo de um desastre',
 'Cinco etapas relacionam preparação, alerta, impacto e resposta, recuperação e avaliação. Cada etapa distingue os registros necessários e as decisões correspondentes. O retorno ao planejamento indica correções e aprendizagem; as fases podem se sobrepor.', False,
 'OMS (2019, 2024); capítulos 6 e 15.'),
]


def text(x, y, lines, size=48, step=57, weight=400, anchor='middle', fill=INK):
    if isinstance(lines, str): lines = [lines]
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(t)}</tspan>' for i,t in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">{spans}</text>'


def panel(x, y, w, h, title, lines=(), fill=SAND, title_size=53, body_size=48):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="#A4ADA7" stroke-width="2"/>'
            + text(x+w/2, y+65, title, size=title_size, weight=700)
            + text(x+w/2, y+127, lines, size=body_size))


def arrow(d, dashed=False, head=True):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3" '+('stroke-dasharray="12 9" ' if dashed else '')+('marker-end="url(#arrow)"' if head else '')+'/>'


def picture(n, y=0, h=750):
    sw,sh=Image.open(ART/f'arte-cap12-{n}-v1.png').size
    return f'<svg x="30" y="{y}" width="1740" height="{h}" viewBox="0 0 {sw} {sh}"><use href="#aquarela"/></svg>'


def layout(n):
    if n == '00':
        p=[picture(n,0,680)]
        pairs=[('Extremo',['Raridade na distribuição'], 'Severo',['Intensidade ou potencial de dano']),
               ('Perigo',['Potencial de causar dano'], 'Exposição',['Pessoas e bens onde pode atuar']),
               ('Vulnerabilidade',['Condições de suscetibilidade'], 'Capacidade',['Recursos e condições para agir']),
               ('Risco',['Possibilidade de perdas'], 'Desastre',['Perturbação grave concretizada'])]
        for i,(a,b,c,d) in enumerate(pairs):
            y=690+190*i
            p += [panel(40,y,830,165,a,b,PALE if i%2==0 else SAND),panel(930,y,830,165,c,d,PALE if i%2==0 else SAND)]
        p += [text(900,1510,'Saúde: efeitos diretos e indiretos, imediatos e tardios.',size=49),
              text(900,1575,'Perigo, exposição, vulnerabilidade e capacidade interagem no risco.',size=45),
              text(900,1640,'Prevenção e preparação reduzem riscos.',size=45),
              text(900,1705,'Resposta e recuperação podem modificar capacidades.',size=45)]
        return 1770,p
    if n == '01':
        p=[picture(n,0,780)]
        for x,title,lines in [(40,'Chuva e raios',['Inundação, lesões','e falhas em redes']), (480,'Vento',['Objetos projetados','e danos estruturais']), (920,'Granizo',['Lesões e danos','às coberturas']), (1360,'Tornado',['Faixa localizada','de ventos intensos'])]:
            p.append(panel(x,795,400,255,title,lines,title_size=51,body_size=46))
        p += [text(900,1135,'Separar o perigo observado do dano atribuído.',size=51),
              text(900,1200,'Fenômenos ilustrados sem escalas ou frequências comparáveis.',size=46)]
        return 1270,p
    if n == '02':
        p=[panel(200,30,1400,180,'Mesmo perigo considerado',['Exemplo conceitual: chuva intensa'],PALE),
           arrow('M900 210 V265 H470 V300'),arrow('M900 265 H1330 V300'),
           text(470,365,'Configuração A',size=58,weight=700),text(1330,365,'Configuração B',size=58,weight=700)]
        rows=[('Exposição',['Moradias em área inundável'],['Menor ocupação da área inundável']),
              ('Vulnerabilidade',['Construções frágeis','e barreiras de mobilidade'],['Proteção construtiva','e acessibilidade']),
              ('Capacidade',['Acesso único e serviços','sem alternativa local'],['Rotas alternativas e recursos','de continuidade verificados'])]
        for i,(title,a,b) in enumerate(rows):
            y=415+270*i
            p += [panel(60,y,800,235,title,a),panel(940,y,800,235,title,b,PALE)]
        p += [text(900,1295,'Diferentes condições podem produzir diferentes impactos.',size=49),
              text(900,1360,'Sem pesos ou escores; maior capacidade não garante ausência de dano.',size=45)]
        return 1430,p
    if n == '03':
        p=[picture(n,0,720)]
        for x,title,lines in [(40,'Saúde',['Feridos ou enfermos','atribuídos ao evento']), (630,'Moradia',['Residentes em imóveis','danificados ou destruídos']), (1220,'Meios de vida',['Pessoas com atividades','interrompidas ou destruídas'])]:
            p.append(panel(x,750,540,245,title,lines,body_size=45))
        p += [panel(100,1040,1600,180,'Afetação direta: componentes B-2 a B-5',['Uma pessoa pode participar de mais de um componente.'],PALE,title_size=51),
              text(900,1300,'Mortes e desaparecimentos são acompanhados separadamente.',size=47),
              text(900,1365,'Pessoas, famílias, moradias e atendimentos não são a mesma unidade.',size=44)]
        return 1430,p
    if n == '04':
        p=[picture(n,0,790)]
        p += [panel(40,810,830,210,'Redes e acesso',['Água, energia, comunicação','e transporte']),
              panel(930,810,830,210,'Condições de cuidado',['Equipes, equipamentos','e insumos disponíveis'])]
        p += [arrow('M455 1020 V1070 H900 V1110'),arrow('M1345 1020 V1070 H900',head=False),
              panel(140,1125,1520,205,'Funcionamento verificado',['Dano físico, interrupção e alternativa assistencial','precisam de registros próprios.'],PALE),
              text(900,1410,'Prédio intacto e equipamentos presentes não comprovam continuidade.',size=45)]
        return 1480,p
    if n == '05':
        p=[picture(n,0,700)]
        for x,title,lines in [(40,'Acolhimento',['Destino, necessidades','e acesso ao cuidado']), (630,'Acompanhamento',['Tratamento, reabilitação','e apoio psicossocial']), (1220,'Recuperação',['Moradia, serviços','e vínculos no território'])]:
            p.append(panel(x,725,540,245,title,lines,body_size=47))
        p += [arrow('M80 1035 H1720'),text(900,1115,'Tempo de acompanhamento, sem duração fixa',size=51),
              text(900,1190,'Necessidades se sobrepõem; reabrir serviços não encerra o cuidado.',size=45)]
        return 1260,p
    if n == '06':
        stages=[('Alerta',['Previsão, território, validade e incerteza']),('Verificação',['Ocorrência, pessoas, danos e necessidades']),('Decisão e ação',['Responsável, prioridade, recursos e execução']),('Acompanhamento',['Cobertura, efeitos, interrupções e correções'])]
        p=[]
        for i,(title,lines) in enumerate(stages):
            y=30+i*245
            p.append(panel(200,y,1400,180,title,lines,PALE if i%2==0 else SAND))
            if i<3:p.append(arrow(f'M900 {y+180} V{y+230}'))
        p += [arrow('M1600 850 H1710 V365 H1615',True),
              panel(100,1040,1600,225,'Registros ligados ao mesmo episódio',['Preservar fonte, horário, versão, unidade e incerteza.','O retorno tracejado orienta revisão da informação.'],PALE)]
        return 1330,p
    if n == '07':
        p=[text(210,70,'Pergunta',size=54,weight=700),text(810,70,'Fonte',size=54,weight=700),text(1435,70,'Unidade',size=54,weight=700)]
        rows=[(['O que pode','acontecer?'],['Serviços meteorológicos','e Cemaden'],['Previsão e alerta','com validade']),
              (['Qual dano','foi registrado?'],['S2iD / Atlas'],['Registro municipal','por evento']),
              (['Qual evento','de saúde?'],['SIM / SIH/SUS'],['Óbito / internação','no universo coberto']),
              (['O serviço','funcionou?'],['Registros locais','e identificação CNES'],['Estabelecimento,','serviço e intervalo']),
              (['Qual população','de referência?'],['IBGE'],['População e','território compatíveis'])]
        for i,(a,b,c) in enumerate(rows):
            y=110+195*i
            p.append(f'<rect x="30" y="{y}" width="1740" height="170" rx="8" fill="{SAND if i%2==0 else PALE}"/>')
            p += [text(225,y+67,a,size=49),text(815,y+67,b,size=49),text(1435,y+67,c,size=49),
                  f'<path d="M470 {y+20} V{y+150} M1160 {y+20} V{y+150}" stroke="#A4ADA7" stroke-width="2"/>']
        p += [text(900,1170,'Integrar exige tempo, território e critérios de vinculação.',size=49),
              text(900,1235,'Sistemas têm finalidades distintas; proximidade não comprova atribuição.',size=44)]
        return 1300,p
    if n == '08':
        p=[panel(40,30,830,185,'Dados abertos',['Atlas: edição fixada']),panel(930,30,830,185,'Dados locais',['Registros vinculados ao episódio'],PALE),
           panel(40,265,830,230,'DES-HUM-01',['Mortes e desaparecimentos','Contagem e taxa por 100 mil']),
           panel(40,535,830,230,'DES-SAU-01',['Registros de instalações públicas','danificadas ou destruídas']),
           panel(930,265,830,230,'DES-HUM-02',['Componentes de afetação B-2 a B-5','Soma composta e taxa por 100 mil'],PALE,body_size=46),
           panel(930,535,830,230,'DES-SAU-02',['Interrupções documentadas','Unir intervalos da mesma chave'],PALE),
           arrow('M455 765 V815 H900 V860'),arrow('M1345 765 V815 H900',head=False),
           panel(100,875,1600,240,'Publicar com contexto',['Versão, território, período, unidade e completude','Denominador compatível quando houver taxa'],SAND),
           text(900,1200,'Sem registro, incompleto e zero informado são condições distintas.',size=46)]
        return 1270,p
    if n == '09':
        p=[text(645,65,'Registros',size=54,weight=700),text(1375,65,'Decisões',size=54,weight=700)]
        rows=[('Preparação',['Exposição, recursos','e dependências'],['Reduzir riscos','e preparar alternativas']),
              ('Alerta',['Perigo previsto,','validade e território'],['Verificar e mobilizar','conforme o plano']),
              ('Impacto e resposta',['Danos, necessidades','e serviços interrompidos'],['Priorizar cuidado','e manter continuidade']),
              ('Recuperação',['Capacidade restaurada','e necessidades persistentes'],['Reabrir com segurança','e reduzir vulnerabilidades']),
              ('Avaliação',['Tempos, cobertura,','falhas e desigualdades'],['Corrigir e acompanhar','a execução das mudanças'])]
        for i,(title,a,b) in enumerate(rows):
            y=110+225*i
            p += [f'<rect x="75" y="{y}" width="1650" height="190" rx="8" fill="{SAND if i%2==0 else PALE}"/>',
                  text(270,y+84,['Impacto e','resposta'] if title=='Impacto e resposta' else title,size=45,weight=700),
                  text(725,y+78,a,size=47),text(1380,y+78,b,size=47),arrow(f'M1030 {y+98} H1085')]
        p += [arrow('M75 1120 H25 V190 H60',True),text(900,1330,'Fases podem se sobrepor; a avaliação retorna ao planejamento.',size=47)]
        return 1400,p
    raise ValueError(n)


def build(spec):
    number,slug,fid,title,alt,watercolor,source=spec
    height,parts=layout(number)
    basename=f'arte-cap12-{number}-{slug}'
    meta=dict(number=number,id=fid,title=title,alt=alt,watercolor=watercolor,source=source,
              svg=basename+'.svg',print=basename+'-print.png',width=1800,height=height,
              conceptual=True,license='A mesma dos textos autorais da obra',
              composition='Composição própria; rótulos, conexões e tipografia editáveis',
              print_width_mm=120)
    definition=''
    if watercolor:
        original=ART/f'arte-cap12-{number}-v1.png'
        sw,sh=Image.open(original).size
        meta.update(raster=original.name,prompt=original.with_suffix('.prompt.txt').name,
                    tool='image_gen',tool_version='Não informada pela ferramenta',
                    reference='assets/references/aquarela-grafite-nanquim.png',
                    reference_delivery='Prévia JPEG de 600 × 400 px exibida na conversa; num_last_images_to_include=1.',
                    original_dimensions_px=[sw,sh],sha256_original=hashlib.sha256(original.read_bytes()).hexdigest(),
                    min_effective_raster_ppi=round(sw/(120/25.4),1))
        assert meta['min_effective_raster_ppi']>=300
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
    manifest=ART/'arte-cap12-manifest.json'
    records={r['number']:r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    for spec in SPECS:
        if spec[0] in selected:records[spec[0]]=build(spec)
    manifest.write_text(json.dumps([records[k] for k in sorted(records)],ensure_ascii=False,indent=2)+'\n')
