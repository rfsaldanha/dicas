#!/usr/bin/env python3
"""Compõe 20 pranchas do capítulo 8: esquemas conceituais, sem dados observados.

Uso: DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap8_art.py [00 ... 19]
Aquarelas originais produzidas por image_gen; textos e conexões em SVG editável.
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
# Número de produção, nome, âncora estável, legenda, texto alternativo, raster, fonte.
SPECS = [
('00','conceitos','fig-cadeia-hidrometeorologica','Da precipitação às exposições e aos efeitos na saúde',
 'Três paisagens hipotéticas contrastam chuva regular, excesso e déficit. O esquema distingue precipitação, estiagem e seca, processos hidrológicos e movimentos de massa, exposição, efeitos sanitários e desastre. Água, vetores, alimento, ar e serviços mediam relações modificadas por vulnerabilidade e capacidade.',True,'IPCC (2022); UNDRR; OMS; Lowe et al. (2021).'),
('01','observacao','fig-precipitacao-observacao','Observar a chuva, definir o intervalo e interpretar a medida',
 'Pluviômetro e técnico em terreno aberto, com cidade distante. Três etapas relacionam lâmina em milímetros, intervalo de acumulação e suporte espacial. A estação observa um ponto; a média territorial exige método próprio.',True,'OMM, guias de instrumentos e práticas climatológicas.'),
('02','intensidade','fig-chuvas-intensas','Intensidade, máximo diário e volume em dias muito úmidos',
 'Três linhas diferenciam intensidade por intervalo, Rx1day como máximo diário e R95p como soma acima do percentil 95. O período-base pertence à definição de R95p. Não há série numérica nem limiar sanitário proposto.',False,'Climdex; fichas CLI-PRC-01 e CLI-PRC-03.'),
('03','persistencia','fig-chuvas-persistentes','Acumulação em janela e sequência de dias úmidos',
 'Sequência didática de símbolos distingue dia úmido, dia seco e dado ausente. Uma janela Rx5day inclui cinco dias válidos, mesmo contendo dia seco; CWD acompanha dias úmidos consecutivos. O desenho não contém medições e a lacuna não é classificada como seca.',False,'Climdex; fichas CLI-PRC-02 e CLI-PRC-05.'),
('04','ausencia','fig-ausencia-chuva','Dia seco, déficit climático e escassez de água',
 'Três perguntas separam CDD, SPI-3 e disponibilidade de água. CDD classifica sequências, SPI-3 compara acumulados com a referência e escassez requer informação de oferta, demanda e acesso. Não se trata de uma sequência obrigatória.',False,'OMM (2012, 2016); fichas CLI-PRC-04 e CLI-SEC-01.'),
('05','seca','fig-propagacao-seca','Propagação do déficit e diferentes tempos de recuperação',
 'Paisagem hipotética com cultivo estressado, reservatório baixo e bairro. O esquema distingue precipitação, solo e vegetação, rios e reservatórios e acesso a água e alimentos. Demanda, calor, armazenamento e resposta modificam a propagação; o retorno da chuva não recupera tudo ao mesmo tempo.',True,'OMM (2016); IPCC (2022); Ministério da Saúde (2026).'),
('06','processos','fig-processos-hidrologicos','Distinção conceitual entre cheia, inundação, alagamento e enxurrada',
 'Quatro cortes vetoriais sem escala mostram água elevada dentro do canal, transbordamento sobre margens, água acumulada em depressão urbana e escoamento concentrado sobre declive. Profundidade, velocidade e duração são dimensões complementares.',False,'Cemaden, definições de ameaças naturais; OMS (2014).'),
('07','encostas','fig-encostas-chuva','Chuva, suscetibilidade da encosta e consequências',
 'Encosta urbana hipotética com cicatriz de deslizamento e material sobre acesso viário. Chuva antecedente e recente interage com material, relevo e drenagem; pessoas, redes e acessos podem ser atingidos. A imagem não classifica o risco de um local real.',True,'Cemaden; OMS, Landslides.'),
('08','vias','fig-vias-hidrossanitarias','Vias entre condições hidrometeorológicas e saúde',
 'Esquema relaciona chuva, déficit e resposta territorial a seis vias: energia da água e detritos; água e saneamento; habitats de vetores; alimentos e ar; perdas e deslocamentos; serviços e acesso. Efeitos dependem da exposição, vulnerabilidade, capacidade e tempo.',False,'IPCC (2022); OMS; capítulos 13 a 15.'),
('09','recuperacao','fig-recuperacao-exposicoes','Exposições durante o evento, o retorno e a recuperação',
 'Duas cenas hipotéticas mostram rua inundada sem pessoas na água e preparação de limpeza após a água baixar. Adultos usam roupas compridas, botas e luvas. O esquema distingue perigos do evento, exposições no retorno e necessidade de acompanhamento; a cena não é um protocolo de limpeza.',True,'OMS (2014); OMS (2022), pesquisa em gestão de riscos de emergências e desastres.'),
('10','agua','fig-agua-contato','Da água no ambiente ao contato e ao consumo',
 'Três vinhetas hipotéticas mostram córrego turvo, infraestrutura de abastecimento e uso doméstico. O esquema distingue transporte de contaminantes, tratamento e distribuição, armazenamento e uso. Um ramo separa ingestão de contato com água ou lama; leptospirose é uma zoonose bacteriana, sem vetor mosquito.',True,'Levy et al. (2016); Ministério da Saúde, Leptospirose.'),
('11','vetores','fig-chuva-vetores','Chuva e seca podem modificar habitats por caminhos distintos',
 'Quintais hipotéticos contrastam recipiente enchido pela chuva e tambor aberto usado para armazenamento durante período seco. Agente observa o segundo recipiente. O esquema relaciona água nos recipientes, manejo, temperatura e vetor à possibilidade de transmissão, condicionada ao agente e à população suscetível.',True,'Lowe et al. (2021); IPCC (2022).'),
('12','alimento-ar','fig-seca-alimento-ar','Seca, acesso a alimentos e exposição à poeira e fumaça',
 'Vinhetas hipotéticas de produção e acesso a alimentos e de ambiente seco com fumaça distante. Duas vias distinguem produção, renda e acesso de emissões, transporte e concentração. SPI e CDD não medem diretamente nutrição nem material particulado.',True,'OMS, Drought; IPCC (2022); OMS (2021), qualidade do ar.'),
('13','deslocamento','fig-deslocamento-cuidado','Perdas, deslocamento e continuidade do apoio psicossocial',
 'Pessoa com bagagem em acolhimento temporário e conversa reservada com profissional em outra vinheta. O esquema relaciona perdas, mudança da rotina, redes de apoio e acompanhamento. As pessoas têm expressões sérias; a imagem não atribui diagnósticos.',True,'Waite et al. (2017); OMS; Freitas et al. (2014).'),
('14','servicos','fig-continuidade-hidrica','Dependências que sustentam o atendimento',
 'Unidade de saúde hipotética com reservação de água, acesso viário e ambiente de atendimento. O esquema separa infraestrutura, chegada de pessoas e insumos e cuidado continuado. Unidade fora da inundação também pode perder capacidade.',True,'OMS (2023), sistemas de saúde resilientes ao clima.'),
('15','relogios','fig-relogios-hidrometeorologicos','Relógios do fenômeno, da exposição e do registro sanitário',
 'Quatro faixas distinguem precipitação ou déficit, resposta hidrológica, contato e deslocamento, e sintomas, atendimento e notificação. Setas não têm escala de tempo; defasagem física, biológica e atraso informacional são distintos.',False,'Gasparrini et al. (2010); Levy et al. (2016); capítulos 4 e 14.'),
('16','fontes','fig-fontes-hidrometeorologicas','Cinco camadas de informação para perguntas diferentes',
 'Matriz relaciona precipitação a observações ou estimativas, processo físico a nível ou mancha, exposição a presença e território, impacto a cadastro de consequências e saúde a registros sanitários. Cada camada mantém fonte, tempo e definição.',False,'OMM; UNDRR; arquitetura das fichas do livro.'),
('17','protocolo','fig-protocolo-precipitacao','Calendário, qualidade e ordem das operações',
 'Fluxo parte da precipitação diária qualificada e se divide. Índices anuais são calculados por célula antes da média municipal; SPI-3 começa pela precipitação média municipal, seguida de somas e ajuste. Ambos exigem documentação de versão, referência e cobertura.',False,'Protocolos das sete fichas do capítulo 17; ECMWF.'),
('18','gestao','fig-gestao-hidrometeorologica','Preparar, acompanhar, agir e aprender',
 'Equipe em reunião e visita a uma comunidade, em cenas hipotéticas. Ciclo vetorial articula preparação, acompanhamento, ação e avaliação; gatilhos exigem responsabilidade e contexto. A cena não representa eficácia medida.',True,'OMS (2023); Ministério da Saúde (2026); capítulo 6.'),
('19','navegacao','fig-navegacao-hidrologica','Da pergunta à ficha e à leitura conjunta',
 'Roteiro liga contexto do fenômeno, fichas operacionais, fontes e protocolo, e indicadores complementares de ambiente e saúde. Links no texto permitem retorno ao contexto e acesso ao indicador específico.',False,'Arquitetura editorial do livro.'),
]

def text(x,y,lines,size=46,step=55,weight=400,anchor='middle',fill=INK):
    if isinstance(lines,str): lines=[lines]
    spans=''.join(f'<tspan x="{x}" dy="{0 if i==0 else step}">{escape(s)}</tspan>' for i,s in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">{spans}</text>'

def panel(x,y,w,h,title,lines=(),fill=SAND):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="#A4ADA7" stroke-width="2"/>'+text(x+w/2,y+65,title,size=50,weight=700)+text(x+w/2,y+128,lines)

def arrow(d):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#arrow)"/>'

def picture():
    return '<use href="#aquarela" x="30" y="0" width="1740" height="580"/>'

def row(y,items):
    w=(1720-60*(len(items)-1))/len(items)
    return [panel(40+i*(w+60),y,w,220,title,lines) for i,(title,lines) in enumerate(items)]

def scene(items,note,second=None):
    p=[picture()]+row(620,items)
    if second:
        p+=row(910,second)
        p += [arrow('M900 840 V900')]
        y=1210
    else: y=935
    p += [text(900,y,note,size=44)]
    return y+100,p

def comparison(rows,note):
    p=[]
    for i,(title,lines,meaning) in enumerate(rows):
        y=30+270*i
        p += [panel(40,y,880,215,title,lines),arrow(f'M920 {y+110} H1010'),text(1390,y+85,meaning,step=58)]
    y=270*len(rows)+60
    p += [text(900,y,note,size=44)]
    return y+95,p

def layout(n):
    if n=='00':
        p=[picture()]+row(610,[('Precipitação',['Água que chega','à superfície']),('Estiagem e seca',['Redução ou déficit','com referência explícita']),('Processos físicos',['Água e terreno','respondem ao contexto'])])
        p += [text(900,910,['Cheia: nível sobe • Inundação: transbordamento','Alagamento: acúmulo • Enxurrada: escoamento rápido','Movimento de massa: solo ou rocha se desloca'],size=45,step=58)]
        p += [arrow('M900 1050 V1100')]+row(1110,[('Exposição',['Quem, onde, como','e por quanto tempo']),('Vias intermediárias',['Água, vetores, alimento,','ar e serviços']),('Consequências',['Saúde, cuidado','e perturbação social'])])
        p += [text(900,1410,['Vulnerabilidade e capacidade modificam as relações.','Desastre envolve perturbação grave; chuva não equivale a dano.'],size=44)]
        return 1540,p
    if n=='01':return scene([('Medir',['Lâmina em mm','Instrumento e manutenção']),('Definir o intervalo',['Início e fim da acumulação','Calendário e fuso']),('Representar o lugar',['Ponto, grade e município','Suportes diferentes'])],['O total precisa de duração; a intensidade depende do intervalo.'])
    if n=='02':return comparison([('Intensidade',['Lâmina por intervalo','Por exemplo: mm/h'],['Concentração temporal','depende da resolução']),('Rx1day',['Maior acumulado diário','Unidade: mm'],['Um máximo diário pode','ocultar um pico subdiário']),('R95p',['Soma dos dias acima de P95','Base de dias úmidos'],['Volume em mm; difere','da porcentagem R95pTOT'])],'Nenhuma dessas medidas define, sozinha, impacto sanitário.')
    if n=='03':
        p=[text(900,70,'Sequência conceitual, sem volumes de chuva observados',size=49,weight=700)]
        seq=[1,1,0,1,1,1,None,1,0]
        for i,v in enumerate(seq):
            x=165+i*168
            p.append(f'<rect x="{x}" y="150" width="132" height="130" rx="8" fill="white" stroke="#809087" stroke-width="2"/>')
            if v==1:p.append(f'<circle cx="{x+66}" cy="214" r="29" fill="{BLUE}"/>')
            else:p.append(text(x+66,232,'?' if v is None else '—',size=66))
        p += [f'<path d="M165 295 V330 H969 V295 M669 410 V445 H1137 V410" fill="none" stroke="{INK}" stroke-width="3"/>',text(560,380,'Janela de cinco dias',size=43),text(900,510,'Três dias úmidos consecutivos',size=43)]
        p += row(550,[('Rx5day',['Soma em cinco dias válidos','e seleção do maior total']),('CWD',['Maior sequência com','precipitação ≥ 1 mm/dia'])])
        p += [text(900,855,'● Dia úmido     — Dia seco     ? Dado ausente',size=45),text(900,930,'A lacuna interrompe a sequência observada; não é dia seco.',size=44)]
        return 1000,p
    if n=='04':return comparison([('CDD',['Precipitação < 1 mm/dia','Maior sequência'],['Quantos dias seguidos','atendem à regra?']),('SPI-3',['Acumulado de três meses','Distribuição de referência'],['Quão deficitário ou úmido','é o trimestre?']),('Escassez de água',['Oferta, demanda e acesso','Infraestrutura e gestão'],['Há água disponível','para os usos necessários?'])],'Ausência de chuva, seca e escassez não são equivalentes.')
    if n=='05':return scene([('Déficit de chuva',['Referência e duração','da anomalia']),('Solo e vegetação',['Armazenamento','e demanda das plantas']),('Rios e reservatórios',['Vazão, nível','e volume disponível'])],['Calor, demanda, armazenamento e resposta modificam a propagação.','Retorno da chuva e recuperação dos impactos têm tempos distintos.'],[('Acesso e meios de vida',['Abastecimento, alimento e renda']),('Saúde e serviços',['Exposição e continuidade do cuidado'])])
    if n=='06':
        p=[]
        names=[('Cheia','Nível elevado dentro do canal'),('Inundação','Água ultrapassa as margens'),('Alagamento','Acúmulo por drenagem insuficiente'),('Enxurrada','Escoamento concentrado e rápido')]
        for i,(name,caption) in enumerate(names):
            x=40+(i%2)*900;y=30+(i//2)*490
            p += [f'<rect x="{x}" y="{y}" width="820" height="450" rx="10" fill="white" stroke="#A4ADA7" stroke-width="2"/>',text(x+410,y+65,name,size=52,weight=700),text(x+410,y+400,caption,size=42)]
            if i<2:
                p += [f'<path d="M{x+50} {y+190} H{x+220} L{x+325} {y+310} H{x+495} L{x+600} {y+190} H{x+770} V{y+340} H{x+50} Z" fill="{SAND}" stroke="{INK}" stroke-width="3"/>']
                if i==0:p.append(f'<path d="M{x+240} {y+213} H{x+580} L{x+495} {y+309} H{x+325} Z" fill="#B7CED9" stroke="{BLUE}" stroke-width="3"/>')
                else:p.append(f'<path d="M{x+50} {y+156} H{x+770} V{y+189} H{x+600} L{x+495} {y+309} H{x+325} L{x+220} {y+189} H{x+50} Z" fill="#B7CED9" stroke="{BLUE}" stroke-width="3"/>')
            elif i==2:
                p += [f'<path d="M{x+50} {y+190} L{x+180} {y+270} H{x+650} L{x+770} {y+190} V{y+335} H{x+50} Z" fill="{SAND}" stroke="{INK}" stroke-width="3"/>',f'<path d="M{x+117} {y+231} H{x+709} L{x+650} {y+270} H{x+180} Z" fill="#B7CED9" stroke="{BLUE}" stroke-width="3"/>',f'<rect x="{x+550}" y="{y+270}" width="80" height="24" fill="{INK}"/>']
            else:
                p += [f'<path d="M{x+60} {y+145} L{x+740} {y+305} V{y+340} H{x+60} Z" fill="{SAND}" stroke="{INK}" stroke-width="3"/>',f'<path d="M{x+100} {y+144} Q{x+260} {y+147} {x+410} {y+218} T{x+720} {y+287}" fill="none" stroke="#B7CED9" stroke-width="24"/>',arrow(f'M{x+240} {y+160} L{x+410} {y+200}'),arrow(f'M{x+470} {y+212} L{x+640} {y+251}')]
        p += [text(900,1060,'Esquemas sem escala; os processos podem coexistir.',size=44),text(900,1125,'Profundidade, velocidade e duração completam a interpretação.',size=44)]
        return 1190,p
    if n=='07':return scene([('Chuva',['Acumulado antecedente','e intensidade recente']),('Suscetibilidade',['Material, relevo,','cobertura e drenagem']),('Consequências',['Pessoas, moradias,','redes e acessos'])],['A cena é hipotética e não substitui avaliação técnica da encosta.'])
    if n=='08':
        p=[panel(40,20,1720,195,'Condições hidrometeorológicas',['Chuva • déficit • resposta da bacia e do território']),arrow('M900 215 V265')]
        p+=row(280,[('Energia e detritos',['Trauma, afogamento','e soterramento']),('Água e saneamento',['Contato, consumo','e higiene']),('Habitat de vetores',['Recipientes, ambiente','e transmissão'])])
        p+=row(550,[('Alimento e ar',['Acesso a alimentos,','poeira e fumaça']),('Perdas e deslocamento',['Moradia, renda','e saúde mental']),('Serviços e acesso',['Capacidade e','continuidade do cuidado'])])
        p += [arrow('M900 770 V835'),panel(40,850,1720,220,'Exposição e efeitos',['População, lugar, duração, vulnerabilidade e capacidade de resposta']),text(900,1150,'As vias se relacionam; as setas não demonstram causalidade local.',size=44)]
        return 1220,p
    if n=='09':return scene([('Evento',['Água, detritos','e estruturas instáveis']),('Retorno',['Contato, limpeza','e deslocamentos']),('Recuperação',['Acompanhamento','e acesso ao cuidado'])],['A exposição pode continuar depois de a água baixar.'])
    if n=='10':return scene([('Ambiente',['Transporte e diluição','de contaminantes']),('Abastecimento',['Tratamento','e distribuição']),('Uso doméstico',['Armazenamento,','consumo e higiene'])],['Leptospirose: zoonose bacteriana associada a contato; sem mosquito vetor.'],[('Ingestão',['Água e alimentos contaminados']),('Contato',['Água ou lama contaminadas'])])
    if n=='11':return scene([('Com chuva',['Recipientes podem','acumular água']),('Durante seca',['Falhas no abastecimento','podem ampliar armazenamento'])],['Temperatura, manejo, agente e população suscetível condicionam transmissão.','Chuvas fortes também podem remover formas imaturas de certos habitats.'],[('Habitat e vetor',['Água disponível e condições locais']),('Contato e transmissão',['Exposição, circulação do agente e tempo'])])
    if n=='12':return scene([('Produção e acesso',['Cultivos, renda, preços','e proteção social']),('Qualidade do ar',['Poeira, fogo, transporte','e concentração'])],['SPI e CDD não medem nutrição nem material particulado.'],[('Alimentação',['Disponibilidade e acesso','precisam de medida própria']),('Exposição respiratória',['Concentração e presença','humana precisam de dados'])])
    if n=='13':return scene([('Perdas',['Moradia, bens,','renda e vínculos']),('Deslocamento',['Abrigo e mudanças','na rotina e no acesso']),('Acompanhamento',['Redes de apoio','e cuidado continuado'])],['Sofrimento não equivale automaticamente a diagnóstico.'])
    if n=='14':return scene([('Infraestrutura',['Água, energia,','comunicação e insumos']),('Acesso',['Pacientes, trabalhadores','e transporte']),('Cuidado',['Atendimento, vigilância','e seguimento'])],['Uma unidade fora da área inundada também pode perder capacidade.'])
    if n=='15':return comparison([('Meteorológico',['Chuva ou déficit','Início, duração e intensidade'],['Quando a condição','ambiental ocorreu?']),('Hidrológico',['Solo, rios e inundação','Resposta da bacia'],['Quando e onde','a água se modificou?']),('Exposição',['Contato e presença','Deslocamento e interrupções'],['Quem foi exposto,','como e por quanto tempo?']),('Sanitário',['Sintomas e cuidado','Atendimento e notificação'],['Quando houve adoecimento','e quando foi registrado?'])],'Faixas sem escala: defasagem biológica e atraso de registro são distintos.')
    if n=='16':return comparison([('Precipitação',['Estação, radar, satélite','ou reanálise'],['Quantidade, distribuição','e resolução']),('Processo físico',['Nível, vazão, umidade','ou mancha inundada'],['Resposta do sistema','no lugar e no tempo']),('Exposição',['População, presença','e serviços no território'],['Quem ou o que pode','entrar em contato']),('Impacto registrado',['Ocorrência, dano','e interrupção'],['Consequência documentada','segundo o cadastro']),('Saúde',['Caso, atendimento','ou óbito'],['Desfecho e cobertura','da fonte sanitária'])],'Conservar fonte, versão, calendário e definição de cada camada.')
    if n=='17':
        p=[panel(40,20,1720,210,'Precipitação diária qualificada',['Produto e versão • acumulação UTC • unidade • lacunas']),arrow('M900 230 V285'),arrow('M900 285 H450 V340'),arrow('M900 285 H1350 V340')]
        p += [panel(40,355,820,230,'Seis índices anuais',['Calcular por célula','Máximos, somas ou sequências']),panel(940,355,820,230,'SPI-3',['Primeiro a precipitação','média municipal por área']),arrow('M450 585 V655'),arrow('M1350 585 V655'),panel(40,670,820,245,'Depois agregar',['Média dos índices por área','Malha municipal IBGE 2022']),panel(940,670,820,245,'Depois transformar',['Meses completos e trimestres','Ajuste por mês de término']),arrow('M450 915 V975 H900 V1025'),arrow('M1350 915 V975 H900')]
        p += [panel(40,1040,1720,215,'Publicar com documentação',['Período-base, calendário, suporte, cobertura, parâmetros e sinalizações']),text(900,1335,'A ordem das operações faz parte da definição do indicador.',size=44)]
        return 1400,p
    if n=='18':
        p=[picture()]
        for x,y,title,lines in [(40,630,'Preparar',['Riscos, recursos e responsabilidades']),(940,630,'Acompanhar',['Previsão, observação e contexto']),(940,945,'Agir',['Comunicação, proteção e cuidado']),(40,945,'Avaliar',['Acesso, decisões e consequências'])]:p.append(panel(x,y,820,230,title,lines))
        p += [arrow('M860 745 H930'),arrow('M1350 860 V935'),arrow('M940 1060 H870'),arrow('M450 945 V870'),text(900,1260,'Gatilho operacional exige contexto, responsável e ação acordada.',size=44)]
        return 1330,p
    if n=='19':
        p=[]
        for i,(title,lines) in enumerate([('Contexto do fenômeno',['Conceito, pergunta, mecanismo e limites']),('Ficha operacional',['Sete indicadores com definição, cálculo e disponibilidade']),('Fonte e protocolo',['Produto, versão, calendário, cobertura e processamento']),('Leitura conjunta',['Temperatura • água • ar • território • exposição • saúde • resposta'])]):
            y=25+i*270;p.append(panel(40,y,1720,210,title,lines))
            if i<3:p.append(arrow(f'M900 {y+210} V{y+260}'))
        p += [text(900,1160,'Consulte as fichas complementares e o retorno ao contexto no texto.',size=44)]
        return 1230,p
    raise ValueError(n)

def build(spec):
    number,slug,identifier,title,alt,watercolor,source=spec
    height,parts=layout(number)
    base=f'arte-cap8-{number}-{slug}'
    meta=dict(number=number,slug=slug,id=identifier,title=title,alt=alt,svg=base+'.svg',
              print=base+'-print.png',watercolor=watercolor,source=source,conceptual=True,
              composition='scripts/build_cap8_art.py',max_print_width_mm=120,
              license='Composição autoral sob GPL-3.0, conforme LICENSE; fontes externas mantêm suas condições de uso.')
    definition=''
    if watercolor:
        original=ART/f'arte-cap8-{number}-v1.png'
        sw,sh=Image.open(original).size
        meta.update(raster=original.name,prompt=original.with_suffix('.prompt.txt').name,
                    tool='image_gen',tool_version='Não informada pela ferramenta',
                    reference='assets/references/aquarela-grafite-nanquim.png',
                    reference_delivery='Referência original exibida antes da primeira geração; demais chamadas usam a aquarela anterior da série como referência imediata de continuidade, com o mesmo parágrafo de direção de arte.',
                    original_dimensions_px=[sw,sh],sha256_original=hashlib.sha256(original.read_bytes()).hexdigest(),
                    min_effective_raster_ppi=round(sw/(120/25.4),1))
        if number=='14':
            meta['reference_delivery']='Folha de contato das composições 00 a 11, 15 a 17 e 19 exibida como referência imediata; mesmo parágrafo de direção de arte da série.'
        encoded=base64.b64encode(original.read_bytes()).decode('ascii')
        definition=f'<image id="aquarela" width="1740" height="580" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{encoded}"/>'
    document=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{height}" viewBox="0 0 1800 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(alt)}</desc>
<metadata>{escape(json.dumps(meta,ensure_ascii=False))}</metadata>
<defs>{definition}<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="{INK}"/></marker></defs>
<rect width="1800" height="{height}" fill="white"/>
<g font-family="Libertinus Serif, Georgia, serif" fill="{INK}">{''.join(parts)}</g></svg>'''
    write_svg(ART/meta['svg'],document)
    export_print(ART/meta['svg'],ART/meta['print'],require_raster=watercolor)
    print(base,flush=True)
    return meta

if __name__=='__main__':
    selected=set(sys.argv[1:]) or {s[0] for s in SPECS}
    unknown=selected-{s[0] for s in SPECS}
    if unknown:raise SystemExit('Números desconhecidos: '+', '.join(sorted(unknown)))
    manifest=ART/'arte-cap8-manifest.json'
    records={r['number']:r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    for spec in SPECS:
        if spec[0] in selected:records[spec[0]]=build(spec)
    manifest.write_text(json.dumps([records[k] for k in sorted(records)],ensure_ascii=False,indent=2)+'\n')
