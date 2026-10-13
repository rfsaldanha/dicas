#!/usr/bin/env python3
"""Compõe oito figuras: cinco aquarelas preservadas e três diagramas editáveis.

DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap16_art.py [01 ... 08]
Rótulos e relações conceituais são vetoriais; não há dados empíricos nas cenas.
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
WIDTH, PRINT_WIDTH = 1800, 117
INK, GREEN, BLUE = '#303B36', '#536B50', '#597482'
SAND, PALE, TERRA = '#F3F0E8', '#EEF2F4', '#985739'
SPECS = [
 dict(number='01', slug='praticas', id='fig-comunicacao-praticas', watercolor=True,
 title='Práticas de aviso: sinais e significados compartilhados',
 alt='Duas vinhetas conceituais mostram um sino e uma conversa atual com rádio e celular. Os rótulos distinguem o aviso histórico documentado dos canais contemporâneos e destacam reconhecimento e interpretação compartilhados. Não há sequência de substituição tecnológica nem reconstrução de um episódio histórico.',
 citations='[@iphan2016sinos, p. 120, 145; @who2017riskcommunication]',
 purpose='Relacionar a antiguidade das práticas de aviso à necessidade de interpretação compartilhada, sem propor evolução tecnológica linear.',
 montage='Duas vinhetas sem conexão cronológica; rótulos inferiores e uma faixa comum de interpretação. Nenhum mapa, data ou episódio reconstruído.',
 link='Os canais podem funcionar juntos, como na @fig-comunicacao-praticas.'),
 dict(number='02', slug='condicoes', id='fig-comunicacao-condicoes', watercolor=True,
 title='Receber o aviso e conseguir agir são condições diferentes',
 alt='Três cenas de um bairro hipotético mostram cuidado de pessoa idosa, mobilidade em cadeira de rodas e organização do trabalho. Rótulos associam cada necessidade à continuidade do cuidado, ao transporte acessível e à organização do trabalho. Barreiras demandam providências públicas, sem julgamento da conduta dos moradores.',
 citations='[@beck2010risco; @araujoCardoso2007comunicacao; @valencio2014tecnicismo]',
 purpose='Tornar visíveis condições materiais de proteção e sua relação com responsabilidades institucionais.',
 montage='Três cenas na mesma escala, com rótulos de cuidado, mobilidade e trabalho. Faixa inferior associa barreiras a providências públicas e compromissos institucionais.',
 link='Essas situações pedem providências diferentes, como mostra a @fig-comunicacao-condicoes.'),
 dict(number='03', slug='escuta', id='fig-comunicacao-escuta', watercolor=False,
 title='Escuta que modifica a decisão',
 alt='Ciclo de quatro núcleos: relato dos moradores e comunicadores locais; verificação com agentes comunitários e equipes técnicas; decisão com responsável, recursos e prazo; resposta com acompanhamento do apoio. Uma seta retorna da resposta à escuta. A impossibilidade de atender requer justificativa e discussão de alternativas.',
 citations='[@who2017riskcommunication; @araujoCardoso2007comunicacao; @loose2025entrevista]',
 purpose='Explicar como a participação modifica decisões e exige resposta e acompanhamento.',
 montage='Quatro caixas em duas linhas. Percurso horário com setas e retorno tracejado à escuta. Faixa final sobre justificativa e alternativas. Rótulos identificam participantes e responsabilidades.',
 link='O retorno à escuta, na @fig-comunicacao-escuta, permite verificar se a solução funcionou.'),
 dict(number='04', slug='evidencias', id='fig-comunicacao-evidencias', watercolor=False,
 title='Observação, previsão e projeção apoiam decisões diferentes',
 alt='Três campos paralelos distinguem observação do que foi medido ou registrado, previsão para área e período e projeção condicionada a cenários. Todos precisam explicitar fonte, território, validade e limites e apoiar a decisão pertinente à sua escala. Novas evidências levam à revisão e à explicação das atualizações; os campos não são etapas sucessivas.',
 citations='[@rsu2026integridade, p. 4, 6–7]',
 purpose='Distinguir tipos de evidência e suas escalas de decisão sem inventar probabilidades.',
 montage='Três campos paralelos, sem setas entre si, com convergência a uma faixa de contexto e a decisões pertinentes. Revisão retorna à avaliação, sem converter observação em previsão ou projeção.',
 link='Na @fig-comunicacao-evidencias, cada tipo de informação apoia decisões conforme sua finalidade; a chegada de novos dados pode exigir revisão.'),
 dict(number='05', slug='enchentes', id='fig-comunicacao-enchentes', watercolor=True,
 title='Enchentes: orientação acompanhada de transporte e acolhimento',
 alt='Situação hipotética de preparação para saída: equipe orienta moradores em rua seca junto a transporte acessível, enquanto outra vinheta mostra acolhimento com acompanhante e bolsa de cuidados. Os rótulos exigem rota verificada, transporte confirmado e acolhimento acessível, com continuidade do cuidado. Não representa Canoas ou uma operação real.',
 citations='[@who2017riskcommunication; @valencio2014tecnicismo]',
 purpose='Associar orientação de saída às condições verificadas de deslocamento, acolhimento e cuidado.',
 montage='Duas vinhetas e três rótulos: rota verificada, transporte confirmado, acolhimento acessível. Faixa sobre acompanhantes e continuidade do cuidado. Identificar situação hipotética.',
 link='Na preparação para saída da @fig-comunicacao-enchentes, o transporte acessível e o acolhimento precisam funcionar em conjunto.'),
 dict(number='06', slug='calor', id='fig-comunicacao-calor', watercolor=True,
 title='Calor: proteção também depende das condições de trabalho',
 alt='Duas vinhetas hipotéticas mostram trabalhadores em pausa com sombra e água, junto ao responsável pelas atividades, e apoio de serviço público a pessoa idosa com dificuldade de mobilidade. Rótulos ligam pausas e reorganização do trabalho aos empregadores e o acesso à proteção às equipes públicas. Não há limites de temperatura ou horários inventados.',
 citations='[@who2026heat]',
 purpose='Relacionar proteção do calor à organização do trabalho e à oferta pública de apoio.',
 montage='Duas vinhetas com rótulos separados para medidas dos empregadores e serviços públicos. Faixa final sobre responsabilidades e recursos pactuados, sem limiares climáticos.',
 link='As duas cenas da @fig-comunicacao-calor mostram responsabilidades complementares: organizar o trabalho e fazer o apoio público chegar às pessoas.'),
 dict(number='07', slug='fumaca', id='fig-comunicacao-fumaca', watercolor=True,
 title='Fumaça e calor exigem proteção coordenada',
 alt='Uma paisagem hipotética com fumaça externa aparece separada de um espaço coletivo de acolhimento acessível. Três rótulos exigem verificar condições de ar e temperatura, organizar acesso e assegurar assistência. A adequação do ambiente depende de verificação; a cor da fumaça não mede concentração e fechar janelas não é apresentado como solução universal.',
 citations='[@who2023wildfires; @who2026heat]',
 purpose='Mostrar que reduzir exposição à fumaça exige considerar calor, acesso e assistência conjuntamente.',
 montage='Duas cenas independentes e três rótulos inferiores. Sem fluxo de ar desenhado, gradiente quantitativo ou promessa de eficácia de equipamento. Faixa ressalta a verificação do ambiente.',
 link='A @fig-comunicacao-fumaca reúne essas verificações.'),
 dict(number='08', slug='falhas', id='fig-comunicacao-falhas', watercolor=False,
 title='Uma falha no apoio exige correção e acompanhamento',
 alt='Fluxo hipotético começa com transporte anunciado que não chega: registrar a falha, acionar responsável e verificar alternativa. Com alternativa confirmada, atualizar a orientação e realizar o apoio. Sem alternativa, comunicar a limitação, manter a demanda pendente e retornar à coordenação. Somente atendimento verificado permite concluir o registro, dar uma resposta e corrigir procedimentos; pedidos sem confirmação permanecem abertos.',
 citations='[@who2017riskcommunication; @rsu2026integridade, p. 7]',
 purpose='Explicitar resposta a falhas sem promessa de alternativa inexistente e sem encerrar pedidos por simples encaminhamento.',
 montage='Fluxo vertical com bifurcação entre alternativa confirmada e não confirmada. A segunda volta à coordenação. Após o apoio, verificação condiciona conclusão; ausência de confirmação mantém pedido aberto. Faixa final sobre correção de procedimentos.',
 link='A @fig-comunicacao-falhas mostra por que o acompanhamento continua depois da correção do aviso.')
]


def text(x, y, lines, size=50, weight=400, anchor='middle', fill=INK, step=62):
    if isinstance(lines, str): lines = [lines]
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else step}">{escape(t)}</tspan>' for i, t in enumerate(lines))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">{spans}</text>'


def panel(x, y, w, h, title, lines=(), fill=SAND):
    titles = [title] if isinstance(title, str) else title
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#7D8880" stroke-width="2"/>'
            + text(x+w/2, y+65, titles, weight=700)
            + text(x+w/2, y+65+62*len(titles)+16, lines, size=48, step=59))


def arrow(path, dashed=False):
    dash = ' stroke-dasharray="12 9"' if dashed else ''
    return f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="3"{dash} marker-end="url(#arrow)"/>'


def original_path(n):
    version = 'v2' if n == '07' else 'v1'
    return ART/f'arte-cap16-{n}-{version}.png'


def raster(n):
    w,h = Image.open(original_path(n)).size
    return f'<svg x="20" y="0" width="1760" height="1174" viewBox="0 0 {w} {h}"><use href="#aquarela"/></svg>'


def layout(n):
    if n in {'01', '02', '05', '06', '07'}:
        parts=[raster(n)]
        if n == '01':
            labels=[('Aviso histórico', ['Toque de rebate documentado', 'em Minas Gerais']),
                    ('Canais contemporâneos', ['Rádio, celular e conversa', 'podem coexistir'])]
            footer='Reconhecer o sinal e compartilhar seu significado.'
        elif n == '02':
            labels=[('Cuidado', ['Continuidade do cuidado', 'e acompanhamento']),
                    ('Mobilidade', ['Transporte e', 'acolhimento acessíveis']),
                    ('Trabalho', ['Organizar o trabalho', 'e viabilizar a saída'])]
            footer='Poder público e empregadores precisam garantir condições de proteção.'
        elif n == '05':
            labels=[('Rota verificada', ['Ação e destino', 'compreensíveis']),
                    ('Transporte confirmado', ['Acesso e apoio', 'ao deslocamento']),
                    ('Acolhimento acessível', ['Acompanhantes e', 'continuidade do cuidado'])]
            footer='Situação hipotética: confirmar as condições antes de anunciar.'
        elif n == '06':
            labels=[('Medidas dos empregadores', ['Pausas, água e sombra;', 'reorganização das atividades']),
                    ('Apoio dos serviços públicos', ['Água, locais adequados', 'e apoio ao deslocamento'])]
            footer='Identificar responsáveis, recursos e condições de acesso.'
        else:
            labels=[('Verificar o ambiente', ['Condições de ar', 'e temperatura']),
                    ('Organizar acesso', ['Apoio ao deslocamento', 'conforme a necessidade']),
                    ('Assegurar assistência', ['Acolhimento e', 'continuidade do cuidado'])]
            footer='A equipe responsável precisa verificar a adequação do ambiente.'
        gap=30; w=(1720-gap*(len(labels)-1))/len(labels)
        for i,(title,lines) in enumerate(labels):
            parts.append(panel(40+i*(w+gap),1175,w,245,title,lines,PALE if i%2 else SAND))
        parts.append(text(900,1495,footer,size=46))
        return 1540,parts
    if n == '03':
        return 1140,[
            panel(100,40,730,270,'Relato dos moradores', ['Moradores e', 'comunicadores locais']),
            panel(970,40,730,270,'Verificação conjunta', ['Agentes comunitários e', 'equipes técnicas e públicas'],PALE),
            arrow('M830 175 H970'), arrow('M1335 310 V510'),
            panel(970,510,730,270,'Decisão com responsável', ['O que fazer e com quais recursos;', 'quem faz e quando responde']),
            panel(100,510,730,270,'Resposta e acompanhamento', ['Explicar a decisão e', 'conferir se o apoio chegou'],PALE),
            arrow('M970 645 H830'), arrow('M465 510 V310',True),
            text(510,417,'Reabrir a escuta',size=46,anchor='start'),
            panel(100,890,1600,210,'Se a demanda não puder ser atendida',
                  ['Justificar, discutir alternativas e acompanhar a necessidade.'])]
    if n == '04':
        p=[]
        for x,title,lines in [(40,'Observação',['O que foi medido', 'ou registrado']),
                             (635,'Previsão',['Estimativa para uma', 'área e um período']),
                             (1230,'Projeção',['O que pode mudar', 'em cada cenário'])]:
            p.append(panel(x,35,530,280,title,lines,PALE))
            p.append(arrow(f'M{x+265} 315 V415'))
        p += [panel(40,415,1720,215,'Apresentar a informação completa',
                    ['Fonte · território · validade · limites']),
              arrow('M900 630 V740'),
              panel(190,740,1420,215,'Usar a informação para decidir',
                    ['Ação imediata ou planejamento, conforme a escala.'],PALE),
              arrow('M900 955 V1065'),
              panel(190,1065,1420,215,'Rever a orientação e explicar a mudança',
                    ['Novos dados, correções e mudanças na situação.']),
              arrow('M1610 1170 H1740 V690 H1500 V740',True),
              text(900,1370,'Os três campos são paralelos; não constituem etapas sucessivas.',size=46)]
        return 1425,p
    if n == '08':
        return 1720,[
            panel(310,25,1180,175,'Transporte anunciado não chega', ['Situação hipotética'],PALE),
            arrow('M900 200 V275'),
            panel(310,275,1180,175,'Registrar a falha e acionar responsável', ['Coordenação verifica alternativas.']),
            arrow('M900 450 V500 H480 V560'), arrow('M900 500 H1320 V560'),
            panel(100,560,760,280,'Alternativa confirmada',
                  ['Atualizar a orientação;', 'organizar e realizar o apoio.'],PALE),
            panel(950,560,750,280,'Alternativa não confirmada',
                  ['Comunicar a limitação;', 'manter a demanda pendente.']),
            arrow('M1700 690 H1760 V360 H1490',True),
            arrow('M480 840 V930'),
            panel(100,930,760,225,'Verificar o atendimento', ['Conferir com equipe e usuário.'],PALE),
            arrow('M860 1040 H950'),
            panel(950,930,750,225,'Sem confirmação', ['Pedido permanece aberto.']),
            arrow('M1700 1040 H1760 V360 H1490',True),
            arrow('M480 1155 V1290'), text(530,1236,'Atendimento confirmado',size=46,anchor='start'),
            panel(100,1290,1600,230,'Concluir o registro e dar uma resposta',
                  ['Registrar o apoio e ouvir as pessoas;', 'definir quem corrige as falhas e em que prazo.']),
            text(900,1620,['Setas tracejadas: retornar à coordenação.',
                           'Uma atualização da mensagem não encerra o atendimento.'],size=46,step=58)]
    raise ValueError(n)


def build(spec):
    n=spec['number']; height,parts=layout(n)
    basename=f'arte-cap16-{n}-{spec["slug"]}'
    meta={**spec, 'svg':basename+'.svg', 'print':basename+'-print.png',
          'width':WIDTH, 'height':height, 'print_width_mm':PRINT_WIDTH,
          'conceptual':True, 'license':'A mesma dos textos autorais da obra',
          'composition':'Composição própria; rótulos, conexões e tipografia editáveis',
          'font':'Source Sans 3; fontes incorporadas',
          'source':'Elaboração conceitual a partir de '+spec['citations']}
    definition=''
    if spec['watercolor']:
        original=original_path(n)
        w,h=Image.open(original).size
        # A aquarela ocupa no máximo 1760/1800 da largura de impressão.
        ppi=w/((PRINT_WIDTH*1760/WIDTH)/25.4)
        if ppi<300: raise ValueError(f'{n}: resolução efetiva abaixo de 300 ppi ({ppi:.1f})')
        meta.update(raster=original.name,prompt=original.with_suffix('.prompt.txt').name,
                    tool='image_gen',tool_version='Não informada pela ferramenta',
                    reference='assets/references/aquarela-grafite-nanquim.png',
                    reference_delivery='Prévia JPEG de 600 × 400 px exibida na conversa; num_last_images_to_include=1.',
                    original_dimensions_px=[w,h],sha256_original=hashlib.sha256(original.read_bytes()).hexdigest(),
                    min_effective_raster_ppi=round(ppi,1),
                    interventions='Direção de arte, revisão visual, rótulos vetoriais e conversão para impressão em cinza; raster original preservado.')
        if n == '07':
            meta.update(previous_versions=[{'raster':'arte-cap16-07-v1.png', 'prompt':'arte-cap16-07-v1.prompt.txt'}],
                        edit_reference='arte-cap16-07-v1.png',
                        reference_delivery='Geração original com prévia JPEG de 600 × 400 px da referência de estilo; edição da imagem original visível na conversa; num_last_images_to_include=1 em ambas.')
        encoded=base64.b64encode(original.read_bytes()).decode('ascii')
        definition=f'<image id="aquarela" width="{w}" height="{h}" href="data:image/png;base64,{encoded}"/>'
    fonts=[]
    for variant,weight in [('Regular',400),('Bold',700)]:
        encoded=base64.b64encode((ROOT/f'assets/fonts/SourceSans3-{variant}.woff2').read_bytes()).decode('ascii')
        fonts.append('@font-face{font-family:"Source Sans 3";font-weight:'+str(weight)+';src:url("data:font/woff2;base64,'+encoded+'") format("woff2");}')
    document=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="{height}" viewBox="0 0 1800 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(spec['title'])}</title><desc id="desc">{escape(spec['alt'])}</desc>
<metadata>{escape(json.dumps(meta,ensure_ascii=False))}</metadata>
<style id="cap16-fonts">{''.join(fonts)}</style>
<defs>{definition}<marker id="arrow" markerWidth="16" markerHeight="14" refX="14" refY="7" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L16 7 L0 14 Z" fill="{INK}"/></marker></defs>
<rect width="1800" height="{height}" fill="white"/>
<g font-family="'Source Sans 3', sans-serif" fill="{INK}">{''.join(parts)}</g></svg>'''
    write_svg(ART/meta['svg'],document)
    export_print(ART/meta['svg'],ART/meta['print'],width=1800,require_raster=spec['watercolor'])
    print(basename,flush=True)
    return meta


if __name__=='__main__':
    selected=set(sys.argv[1:]) or {s['number'] for s in SPECS}
    unknown=selected-{s['number'] for s in SPECS}
    if unknown: raise SystemExit('Códigos desconhecidos: '+', '.join(sorted(unknown)))
    manifest=ART/'arte-cap16-manifest.json'
    records={r['number']:r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    for spec in SPECS:
        if spec['number'] in selected: records[spec['number']]=build(spec)
    manifest.write_text(json.dumps([records[k] for k in sorted(records)],ensure_ascii=False,indent=2)+'\n')
