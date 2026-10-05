"""Pranchas conceituais do capítulo 4; geometria ilustrativa, sem dados simulados."""


def layout(number, sw, sh, text, line, box, picture):
    parts, placements = [], []

    def pic(name, x, y, w, h):
        svg, area = picture(name, (0, 0, 1, 1), x, y, w, h, sw, sh)
        placements.append({'name': name, 'crop': (0, 0, 1, 1), 'area': area})
        parts.append(svg)
        return area

    def territory(area, name, grid=False, residents=False, clip=False):
        x, y, w, h = area
        pts = [(0.19, .17), (.62, .12), (.86, .35), (.77, .9), (.3, .86), (.15, .54)]
        polygon = ' '.join(f'{x+a*w},{y+b*h}' for a, b in pts)
        parts.append(f'<defs><clipPath id="zone-{name}"><polygon points="{polygon}"/></clipPath></defs>')
        if clip:
            path = f'M{x} {y} h{w} v{h} h{-w} Z M' + polygon.replace(' ', ' L') + ' Z'
            parts.append(f'<path d="{path}" fill="white" fill-rule="evenodd" opacity=".75"/>')
            parts.append(f'<g clip-path="url(#zone-{name})">')
        if grid:
            for j in range(1, 5):
                parts.append(line(f'M{x+j*w/5} {y+.05*h} V{y+.95*h}', width=4))
            for j in range(1, 4):
                parts.append(line(f'M{x+.05*w} {y+j*h/4} H{x+.95*w}', width=4))
        if residents:
            # Símbolos de localização, sem equivalência com pessoas ou totais.
            for a, b in [(.36,.26),(.4,.31),(.44,.4),(.49,.44),(.54,.5),(.48,.6),
                         (.57,.68),(.65,.74),(.7,.77),(.75,.7),(.83,.66),(.87,.75)]:
                parts.append(f'<circle cx="{x+a*w}" cy="{y+b*h}" r="12" fill="#AE6B50" stroke="white" stroke-width="4"/>')
        if clip:
            parts.append('</g>')
        parts.append(f'<polygon points="{polygon}" fill="none" stroke="#303b36" stroke-width="6" stroke-dasharray="20 9"/>')

    def formula(x, y, size=61):
        sub = lambda s: f'<tspan baseline-shift="sub" font-size="65%">{s}</tspan>'
        parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}">'
                     f'x̄{sub("pop,m")} = ∑{sub("g")}(x{sub("g")} · p{sub("gm")}) / ∑{sub("g")}p{sub("gm")}</text>')

    if number == '08':
        height = 2280
        rows = [
            ('Campo ambiental', ['Cada célula g representa', 'um valor ambiental xg.'], True, False, False),
            ('População residente', ['Localizar os moradores', 'em relação à mesma grade.'], False, True, False),
            ('Recorte territorial', ['pgm: população na parte de g', 'que pertence ao território m.'], True, True, True),
        ]
        for i, (title, detail, grid, residents, clip) in enumerate(rows):
            y = 20 + i*540
            a = pic('ponderacao-'+str(i), 20, y, 920, 480)
            territory(a, 'ponderacao-'+str(i), grid, residents, clip)
            parts += [text(1370, y+130, title, 56), text(1370, y+240, detail, 47, step=66)]
            if i < 2:
                parts.append(line(f'M55 {y+510} H1745', width=1.5, stroke='#c6ccc5'))
        parts += [box(80, 1660, 1640, 330, '#f1f4f1'), text(900, 1735, 'Síntese: cada valor recebe o peso da população correspondente', 46)]
        formula(900, 1850)
        parts += [text(900, 1940, 'Somar valor × população; dividir pela população incluída.', 46),
                  text(900, 2070, 'A ponderação muda a síntese; não muda o valor ambiental da célula.', 44),
                  text(900, 2140, 'Exigir população positiva e examinar a cobertura dos valores válidos.', 43),
                  text(900, 2220, 'Paisagem e pontos conceituais; não representam medições nem contagens.', 40)]
    elif number == '09':
        height = 2080
        a = pic('sobreposicao', 35, 100, 900, 490)
        territory(a, 'sobreposicao', grid=True, clip=True)
        parts += [text(1370, 170, 'Sobreposição espacial', 54),
                  text(1370, 285, ['Cruzar grade e território.', 'Identificar partes internas', 'e células cortadas pelo limite.'], 45, step=65),
                  text(900, 660, 'A interseção delimita a contribuição; a estatística depende da pergunta.', 43),
                  line('M55 720 H1745', width=1.5, stroke='#c6ccc5')]
        # Duas malhas cobrem exatamente o mesmo domínio, sem totais inventados.
        for i, name in enumerate(['Origem', 'Destino']):
            x = 60 + i*470
            a = pic('malha-'+str(i), x, 800, 410, 300)
            ax, ay, aw, ah = a
            parts.append(f'<rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" fill="white" fill-opacity=".3" stroke="#303b36" stroke-width="5"/>')
            if i == 0:
                parts.append(line(f'M{ax+aw/2} {ay} V{ay+ah}', width=5))
            else:
                for j in (1, 2):
                    parts.append(line(f'M{ax} {ay+ah*j/3} H{ax+aw}', width=5))
            parts.append(text(x+205, 1165, name, 45))
        parts += [line('M475 945 H520', arrow=True, width=4),
                  text(1370, 830, 'Interpolação areal', 54),
                  text(1370, 935, ['Transferir totais entre malhas.', 'Ponderar por área pressupõe', 'uniformidade na origem.'], 45, step=65),
                  text(900, 1260, 'Conservar o total no domínio comum; dados auxiliares mudam as hipóteses.', 43),
                  line('M55 1320 H1745', width=1.5, stroke='#c6ccc5')]
        a = pic('peso', 35, 1380, 900, 490)
        territory(a, 'peso', grid=True, residents=True, clip=True)
        parts += [text(1370, 1470, ['Ponderação populacional', 'da exposição'], 51, step=62),
                  text(1370, 1640, ['Combinar ambiente e população', 'já compatibilizados.', 'Mudar os pesos da síntese.'], 45, step=65),
                  text(900, 1935, 'Ponderar não redistribui a temperatura ou a concentração.', 44),
                  text(900, 2035, 'Malhas, paisagem e símbolos ilustrativos; sem valores observacionais.', 40)]
    elif number == '10':
        height = 2240
        rows = [
            ('Média', ['Nível médio', 'Pode ocultar picos', 'e variação interna.']),
            ('Soma', ['Quantidade acumulada', 'Pode ocultar a distribuição', 'no período.']),
            ('Máximo', ['Maior valor', 'Não informa frequência', 'nem persistência.']),
            ('Contagem', ['Frequência', 'Perde a ordem', 'dos dias selecionados.']),
            ('Sequência', ['Persistência', 'Não resume a intensidade', 'durante o episódio.']),
        ]
        for i, (title, detail) in enumerate(rows):
            y = 20 + i*410
            parts += [text(200, y+100, title, 58), text(1390, y+100, detail, 46, step=65)]
            if i < 3:
                expressions = [('x₁, x₂, …, xₙ', 'x̄ = (x₁ + x₂ + … + xₙ) / n'),
                               ('p₁ + p₂ + … + pₙ', 'Precipitação de intervalos → total'),
                               ('{x₁, x₂, …, xₙ}', 'Selecionar max{x₁, x₂, …, xₙ}')]
                parts += [box(420, y+25, 690, 105, '#f1f4f1'), text(765, y+95, expressions[i][0], 53),
                          line(f'M765 {y+135} V{y+185}', arrow=True),
                          text(765, y+255, expressions[i][1], 42)]
                if i == 0:
                    parts.append(text(765, y+330, 'Pesos iguais; observações comparáveis.', 38))
                if i == 1:
                    parts.append(text(765, y+330, 'p em mm; intervalos sem sobreposição.', 38))
            else:
                # Mesmo padrão esquemático nos dois painéis, sem contagem publicada.
                active = [True, False, True, True, True, False]
                for j, selected in enumerate(active):
                    x = 425 + j*110
                    parts.append(box(x, y+35, 92, 100, '#d5ded4' if selected else 'white'))
                    parts.append(text(x+46, y+105, '✓' if selected else '–', 54))
                if i == 4:
                    parts.append(line(f'M645 {y+160} V{y+180} H955 V{y+160}', width=5))
                parts.append(text(765, y+255, 'Somar dias que atendem ao critério.' if i == 3 else 'Buscar o maior bloco consecutivo.', 41))
                parts.append(text(765, y+330, '✓ atende ao critério; – não atende.', 38))
            if i < 4:
                parts.append(line(f'M55 {y+375} H1745', width=1.5, stroke='#c6ccc5'))
        parts += [text(900, 2120, 'Definir variável, unidade, intervalo, critério e regra para dados ausentes.', 43),
                  text(900, 2200, 'Símbolos e calendário esquemático: não constituem uma série observada.', 40)]
    elif number == '11':
        height = 1820
        parts += [text(900, 80, 'Partindo do dia do desfecho', 60),
                  text(900, 155, 'Examinar exposições do mesmo dia e dos dias anteriores.', 47),
                  line('M145 300 H1660', arrow=True, width=4)]
        for x, label in [(280, 't − k'), (850, 't − 1'), (1430, 't')]:
            parts += [line(f'M{x} 282 V318', width=4), text(x, 365, label, 54),
                      box(x-210, 420, 420, 105, '#f1f4f1'), text(x, 490, 'Exposição', 47)]
        parts += [text(565, 365, '…', 48), line('M280 545 V575 H1430 V545', dashed=True),
                  text(750, 650, 'Janela de exposições candidatas', 43),
                  box(1210, 610, 440, 115), text(1430, 685, 'Desfecho em t', 48),
                  line('M1430 530 V595', dashed=True),
                  text(900, 805, 'Defasagem zero: mesmo intervalo. Defasagem positiva: exposição anterior.', 42),
                  line('M55 875 H1745', width=1.5, stroke='#c6ccc5'),
                  text(900, 975, 'Partindo do dia da exposição', 60),
                  text(900, 1050, 'Acompanhar possíveis desfechos no mesmo dia e depois.', 47),
                  line('M145 1190 H1660', arrow=True, width=4)]
        for x, label in [(280, 't'), (850, 't + 1'), (1430, 't + k')]:
            parts += [line(f'M{x} 1172 V1208', width=4), text(x, 1255, label, 54)]
        parts += [text(1140, 1255, '…', 48), box(65, 1310, 430, 110, '#f1f4f1'), text(280, 1382, 'Exposição em t', 47),
                  line('M280 1460 V1490 H1430 V1460', dashed=True),
                  text(950, 1380, 'Janela de possíveis desfechos', 46),
                  text(900, 1580, 'k delimita a janela de dias: não há duração universal.', 45),
                  text(900, 1670, 'A linha temporal organiza a análise; não demonstra efeito causal.', 43),
                  text(900, 1760, 'Atrasos biológicos, assistenciais e de registro exigem campos e hipóteses próprios.', 39)]
    else:
        raise ValueError(number)
    # Mesma notação da equação do capítulo, com índices realmente subscritos.
    parts = [p.replace('ambiental xg.', 'ambiental x<tspan baseline-shift="sub" font-size="65%">g</tspan>.')
             .replace('pgm: população', 'p<tspan baseline-shift="sub" font-size="65%">gm</tspan>: população')
             for p in parts]
    return 1800, height, parts, placements
