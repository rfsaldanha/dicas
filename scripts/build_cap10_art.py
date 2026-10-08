#!/usr/bin/env python3
"""Compõe 14 figuras conceituais: sete aquarelas e sete esquemas vetoriais.

DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap10_art.py [00 ... 13]
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
SPECS = [
('00','conceitos','fig-cadeia-agua-saneamento','Água, saneamento e saúde: conceitos e relações',
 'Paisagem hipotética relaciona abastecimento, instalação sanitária e cuidado. O esquema distingue água segura, esgotamento, higiene, qualidade ambiental, exposição, efeitos e resposta. Segurança hídrica reúne condições que precisam persistir no tempo.',True,'OMS (2018, 2020, 2022); Lei nº 11.445/2007.'),
('01','abastecimento','fig-agua-abastecimento','Do manancial ao consumo: barreiras e responsabilidades',
 'Paisagem hipotética mostra captação, tratamento, reservação e cidade. O esquema acompanha a cadeia até o uso, distinguindo controle pelo responsável e vigilância pela autoridade de saúde. A paisagem não prescreve uma tecnologia de tratamento.',True,'OMS (2023), Water safety plan manual; Ministério da Saúde (2024).'),
('02','acesso','fig-agua-acesso','Acesso, disponibilidade e qualidade são requisitos distintos',
 'Duas cenas conceituais mostram uso de água no quintal e transporte de recipiente. Três requisitos de serviço seguro aparecem separados: fonte no local, disponibilidade e qualidade. A aparência da água não comprova potabilidade.',True,'JMP, Drinking water; Howard et al. (2020).'),
('03','microbiologia','fig-agua-microbiologia','Da amostra microbiológica ao alcance da interpretação',
 'O percurso liga ponto e momento, coleta e análise, resultado e avaliação. Ausência de E. coli em 100 mL se refere à amostra; detecção indica necessidade de ação. Cobertura do plano e representatividade limitam conclusões populacionais.',False,'Ministério da Saúde (2024); Oliveira Júnior et al. (2019).'),
('04','desinfeccao','fig-agua-desinfeccao','Turbidez e residual: observações complementares',
 'Três cenas hipotéticas mostram tratamento, análise e ponto de consumo. O esquema distingue partículas, barreira de desinfecção e etapa de coleta. A figura não descreve um procedimento de coleta nem certifica a segurança pela aparência.',True,'OMS (2022), Guidelines for drinking-water quality; Portarias GM/MS nº 888 e nº 2.472/2021.'),
('05','quimica','fig-agua-quimica','Substância, concentração e tempo na avaliação da exposição',
 'Etapas separam fonte, ocorrência no meio, contato humano e efeito investigado. Duas notas distinguem concentração de duração e limite de quantificação de ausência. As setas indicam percurso de investigação, sem atribuição causal automática.',False,'OMS (2022); Ministério da Saúde (2024).'),
('06','esgotamento','fig-esgotamento-cadeia','Cadeias de esgotamento em rede e de soluções locais',
 'Duas cenas conceituais representam rede urbana e solução local com remoção de lodo. Percursos distinguem coleta, transporte, tratamento e destinação, incluindo tratamento e disposição no local. A segurança depende de verificar toda a cadeia.',True,'OMS (2022), Sanitation safety planning; JMP, Sanitation.'),
('07','higiene','fig-higiene-ambiente','Higiene, drenagem e resíduos: escalas complementares',
 'Três vinhetas mostram lavagem das mãos, manutenção de drenagem e armazenamento de resíduos de serviço de saúde. Rótulos distinguem meios e práticas, escoamento e contato, coleta e destino. Cores dos recipientes não representam uma norma de segregação.',True,'JMP, Hygiene; OMS/UNICEF (2022), WASH FIT; Lei nº 11.445/2007.'),
('08','vias','fig-agua-vias-saude','Vias de exposição e investigação dos efeitos na saúde',
 'Três linhas distinguem transmissão fecal-oral, contato com água ou solo contaminados e exposição química. As linhas se ligam à investigação de efeitos; suscetibilidade, proteção e acesso ao cuidado modificam as relações.',False,'OMS (2018, 2022); Ministério da Saúde, Leptospirose; Hernán e Robins (2020).'),
('09','seguranca','fig-seguranca-hidrica-dimensoes','Dimensões complementares de segurança hídrica para a saúde',
 'Seis campos descrevem acesso, quantidade, qualidade, confiabilidade, ecossistemas e continuidade dos serviços essenciais. Campos sem pesos, escores ou magnitudes; o conjunto orienta perguntas e não constitui um índice.',False,'ANA (2019); OMS (2023, 2024).'),
('10','fontes','fig-agua-fontes','Da pergunta à fonte e à unidade de observação',
 'Quatro linhas relacionam população e domicílios ao IBGE e levantamentos locais, amostras ao Sisagua, operação ao SINISA e comparação internacional ao JMP. Integrar exige compatibilizar ano, universo e denominador.',False,'Oliveira Júnior et al. (2019); JMP; SINISA 2025; capítulo 5.'),
('11','protocolo','fig-agua-protocolo','Selecionar, classificar e publicar sem trocar denominadores',
 'O fluxo separa elegibilidade, validade, classificação e publicação. Três bases são distintas: população, resultados de amostras e volumes de esgoto. Ausente, indeterminado e zero conservam significados próprios.',False,'Protocolos das nove fichas do capítulo 19.'),
('12','gestao','fig-agua-gestao','Da identificação do problema à verificação da resposta',
 'Três cenas hipotéticas mostram planejamento, observação e comunicação. O ciclo conecta verificar, avaliar risco, agir e acompanhar, com retorno ao planejamento. A quantidade de ações não demonstra por si só proteção alcançada.',True,'OMS (2023), Water safety plan manual; Ministério da Saúde (2024).'),
('13','navegacao','fig-agua-navegacao','Percurso entre contexto, fichas e aplicação',
 'O percurso começa no capítulo 10, passa pelas nove fichas do capítulo 19 e chega à fonte e à decisão. Três famílias distinguem serviços populacionais, amostras de água e indicadores administrativos. Capítulos complementares apoiam estudos integrados.',False,'Arquitetura editorial do livro e fichas do capítulo 19.'),
]


def text(x,y,lines,size=46,step=56,weight=400,anchor='middle',fill=INK):
    if isinstance(lines,str): lines=[lines]
    spans=''.join(f'<tspan x="{x}" dy="{0 if i==0 else step}">{escape(t)}</tspan>' for i,t in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">{spans}</text>'


def panel(x,y,w,h,title,lines=(),fill=SAND):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="#A4ADA7" stroke-width="2"/>'
            +text(x+w/2,y+63,title,size=50,weight=700)+text(x+w/2,y+128,lines))


def arrow(d,dashed=False):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3" '+('stroke-dasharray="10 8" ' if dashed else '')+'marker-end="url(#arrow)"/>'


def picture(n,y=0,h=730):
    sw,sh=Image.open(ART/f'arte-cap10-{n}-v1.png').size
    return f'<svg x="30" y="{y}" width="1740" height="{h}" viewBox="0 0 {sw} {sh}"><use href="#aquarela"/></svg>'


def three(y,items,h=220):
    out=[]
    for x,(title,lines) in zip((40,630,1220),items):out.append(panel(x,y,540,h,title,lines))
    return out


def layout(n):
    p=[]
    if n=='00':
        p=[picture(n,0,640)]
        p+=three(650,[('Água segura',['Acesso, quantidade','e potabilidade']),('Esgotamento',['Manejo seguro','das excretas']),('Higiene',['Meios disponíveis','e práticas de cuidado'])])
        p+=[panel(40,910,800,190,'Qualidade ambiental',['Condições dos meios e seus usos']),panel(960,910,800,190,'Exposição e efeitos',['Contato, duração e investigação']),arrow('M840 1000 H950'),
            text(900,1165,'Resposta: prevenir, vigiar, corrigir e acompanhar.',size=46),text(900,1230,'Segurança hídrica: manter essas condições ao longo do tempo.',size=45)]
        return 1290,p
    if n=='01':
        p=[picture(n)]
        p+=three(745,[('Manancial',['Proteção e captação']),('Tratamento',['Barreiras adequadas']),('Distribuição',['Reservação e rede'])],190)
        p += [arrow('M580 835 H620'),arrow('M1170 835 H1210'),arrow('M1490 935 V990 H1290 V1030'),
              panel(920,1045,840,200,'Uso e armazenamento',['Domicílios e instituições']),panel(40,1045,800,200,'Controle e vigilância',['Responsabilidades distintas']),
              text(900,1320,'Inspeção, operação e análises se complementam.',size=46)]
        return 1380,p
    if n=='02':
        p=[picture(n)]
        p+=three(740,[('No local',['Fonte melhorada','no domicílio ou terreno']),('Quando necessária',['Disponibilidade','para os usos']),('Com qualidade',['Sem contaminação fecal','e química prioritária'])])
        p+=[text(900,1030,'Serviço seguro reúne os requisitos; rede isoladamente não basta.',size=45),text(900,1100,'Quantidade, custo, tempo e acessibilidade também afetam o uso.',size=44)]
        return 1160,p
    if n=='03':
        rows=[('Ponto e momento',['Onde, quando e por que coletar']),('Coleta e análise',['Volume, método, conservação e identificação']),('Resultado classificável',['Ausência ou presença de E. coli em 100 mL'])]
        for i,(title,lines) in enumerate(rows):
            y=30+i*255;p.append(panel(160,y,1480,185,title,lines))
            if i<2:p.append(arrow(f'M900 {y+185} V{y+240}'))
        p+=[panel(40,820,830,240,'Ausência na amostra',['Não exclui outros agentes','ou locais não observados']),panel(930,820,830,240,'Detecção na amostra',['Investigar e proteger','conforme risco e protocolo']),
            text(900,1140,'O plano de amostragem delimita o alcance da interpretação.',size=46)]
        return 1210,p
    if n=='04':
        p=[picture(n,0,660)]
        p+=three(680,[('Turbidez',['Partículas e desempenho','das barreiras físicas']),('Residual',['Agente, concentração','e permanência']),('Ponto de coleta',['Tratamento, distribuição','ou consumo'])],245)
        p+=[text(900,1000,'Comparar exige identificar tecnologia, etapa, unidade e método.',size=45),text(900,1070,'Água transparente e residual conforme não provam segurança integral.',size=44)]
        return 1140,p
    if n=='05':
        rows=[('Fonte',['Geologia, atividades e materiais']),('Ocorrência no meio',['Substância, concentração e método']),('Contato humano',['Via, consumo e duração']),('Efeito investigado',['Suscetibilidade e outras exposições'])]
        for i,(title,lines) in enumerate(rows):
            y=30+i*240;p.append(panel(160,y,1480,180,title,lines))
            if i<3:p.append(arrow(f'M900 {y+180} V{y+225}'))
        p+=[text(900,1045,'Abaixo do limite de quantificação não significa concentração zero.',size=44),text(900,1110,'O percurso orienta a investigação; não demonstra causalidade.',size=45)]
        return 1180,p
    if n=='06':
        p=[picture(n,0,760)]
        p+=[panel(40,790,830,285,'Sistema em rede',['Coleta → transporte','Tratamento → destinação','Verificar cada etapa']),panel(930,790,830,285,'Solução local',['Contenção e tratamento no local','Lodo removido: transporte','e tratamento fora do local']),
            text(900,1150,'A existência da instalação não comprova o manejo seguro.',size=46),text(900,1220,'População atendida e volume tratado têm denominadores distintos.',size=44)]
        return 1280,p
    if n=='07':
        p=[picture(n,0,700)]
        p+=three(720,[('Higiene',['Meios disponíveis','não medem práticas']),('Drenagem',['Manutenção da rede','Contato e exposição']),('Resíduos',['Da coleta ao destino','Verificar cada etapa'])],245)
        p+=[text(900,1040,'Domicílio, rua e serviço de saúde exigem avaliações próprias.',size=46),text(900,1110,'Cenas conceituais; cores dos recipientes não codificam normas.',size=43)]
        return 1170,p
    if n=='08':
        rows=[('Via fecal-oral',['Excretas → água, mãos,','alimentos e objetos → ingestão'],['Barreiras de saneamento,','água segura e higiene']),('Contato ambiental',['Água ou solo contaminados','e contato humano'],['Agente, reservatório','e porta de entrada']),('Exposição química',['Substância no meio','e contato ao longo do tempo'],['Concentração, duração','e outras vias de exposição'])]
        for i,(title,lines,caution) in enumerate(rows):
            y=30+i*305;p+=[panel(40,y,950,245,title,lines),arrow(f'M990 {y+120} H1090'),text(1430,y+105,caution)]
        p+=[panel(40,975,1720,195,'Investigação dos efeitos',['População, desfecho, período e desenho compatíveis']),text(900,1240,'Suscetibilidade, proteção e acesso ao cuidado modificam as relações.',size=43)]
        return 1300,p
    if n=='09':
        items=[('Acesso',['Quem utiliza o serviço?','Distância e acessibilidade']),('Quantidade',['Há água para os usos?','Demanda e restrições']),('Qualidade',['Quais barreiras funcionam?','Parâmetros e vigilância']),('Confiabilidade',['O serviço se mantém?','Operação e manutenção']),('Ecossistemas',['Como os meios são protegidos?','Mananciais e destinação']),('Serviços essenciais',['O cuidado pode continuar?','Alternativas e recuperação'])]
        for i,(title,lines) in enumerate(items):p.append(panel(40+(i%2)*890,30+(i//2)*290,830,240,title,lines,fill=SAND if i%2==0 else PALE))
        p+=[text(900,965,'Dimensões complementares: sem pesos, pontuação ou índice novo.',size=45),text(900,1035,'Interpretar o conjunto preservando cada universo de observação.',size=44)]
        return 1100,p
    if n=='10':
        rows=[('População e domicílios','IBGE e levantamentos locais','Uso do serviço e desigualdades'),('Amostra e abastecimento','Sisagua','Parâmetro, ponto e momento'),('Prestador e município','SINISA','Atendimento e operação'),('Estimativas harmonizadas','JMP','Definição e comparação internacional')]
        for i,(unit,src,use) in enumerate(rows):
            y=30+i*235;p += [panel(40,y,900,180,unit,[use]),arrow(f'M940 {y+90} H1035'),text(1400,y+105,src,size=48,weight=700)]
        p += [text(900,1040,'Mesmo município não significa mesmo universo ou denominador.',size=45),text(900,1110,'Registrar fonte, ano, versão, cobertura e finalidade.',size=46)]
        return 1170,p
    if n=='11':
        rows=[('Selecionar',['Fonte, módulo, universo e período']),('Validar',['Duplicatas, unidade, método e campos obrigatórios']),('Classificar',['Regra da ficha; indeterminados documentados']),('Publicar',['Valor, numerador, denominador, cobertura e versão'])]
        for i,(title,lines) in enumerate(rows):
            y=30+i*230;p.append(panel(160,y,1480,175,title,lines))
            if i<3:p.append(arrow(f'M900 {y+175} V{y+215}'))
        p+=three(970,[('População',['Serviços utilizados']),('Resultados',['Amostras classificáveis']),('Volumes',['Esgoto coletado'])],190)
        p+=[text(900,1235,'Ausente, indeterminado e zero conservam significados distintos.',size=45)]
        return 1300,p
    if n=='12':
        p=[picture(n,0,670)]
        for x,y,title,lines in [(40,700,'Verificar',['Registro e contexto']), (980,700,'Avaliar',['Risco e população']), (980,1000,'Agir',['Correção e comunicação']), (40,1000,'Acompanhar',['Resposta e aprendizagem'])]:p.append(panel(x,y,780,200,title,lines))
        p += [arrow('M820 800 H965'),arrow('M1370 900 V980'),arrow('M980 1100 H840'),arrow('M430 1000 V920'),text(900,1280,'Planejar responsabilidades e documentar o seguimento.',size=46)]
        return 1340,p
    if n=='13':
        p=[panel(40,30,1720,185,'Capítulo 10: contexto',['Conceitos, interpretação e limites']),arrow('M900 215 V275'),panel(40,290,1720,185,'Capítulo 19: nove fichas',['Definição, método, disponibilidade e fontes'])]
        p+=three(525,[('Serviços',['SAN-AGU-01','SAN-ESG-01 / SAN-HIG-01']),('Amostras',['SAN-AGU-02 e 03','SAN-AGU-04']),('Administração',['SAN-AGU-05','SAN-ESG-02 e 03'])],235)
        p+=[arrow('M900 760 V820'),panel(40,835,1720,185,'Fonte → resultado → decisão',['Preservar versão, universo e denominador']),text(900,1090,'Fichas complementares: capítulos 17, 20, 21, 22, 23 e 24.',size=46),text(900,1155,'Links para cada destino acompanham o texto e o diretório.',size=44)]
        return 1220,p
    raise ValueError(n)


def build(spec):
    number,slug,identifier,title,alt,watercolor,source=spec
    height,parts=layout(number)
    basename=f'arte-cap10-{number}-{slug}'
    meta=dict(number=number,slug=slug,id=identifier,title=title,alt=alt,svg=basename+'.svg',print=basename+'-print.png',watercolor=watercolor,
              composition='scripts/build_cap10_art.py',source=source,conceptual=True,
              license='Composição autoral sob GPL-3.0, conforme LICENSE; fontes externas mantêm suas condições de uso.',
              max_print_width_mm=120,print_export_width_px=1800,review='Cenas conceituais; relações, rótulos e legibilidade verificados em provas de web e impressão.')
    definition=''
    if watercolor:
        original=ART/f'arte-cap10-{number}-v1.png'
        sw,sh=Image.open(original).size
        meta.update(raster=original.name,prompt=original.with_suffix('.prompt.txt').name,tool='image_gen',tool_version='Não informada pela ferramenta',
                    reference='assets/references/aquarela-grafite-nanquim.png',reference_delivery='Prévia JPEG de 800 × 533 px exibida na conversa; num_last_images_to_include=1.',
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
    manifest=ART/'arte-cap10-manifest.json'
    records={r['number']:r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    for spec in SPECS:
        if spec[0] in selected:records[spec[0]]=build(spec)
    manifest.write_text(json.dumps([records[k] for k in sorted(records)],ensure_ascii=False,indent=2)+'\n')
