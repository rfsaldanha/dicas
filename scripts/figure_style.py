"""Fontes autocontidas nos SVGs: imagens HTML não carregam fontes externas.

Não altera cenas, coordenadas, texto, relações ou espessuras conceituais.
Os compositores importam write_svg; a execução direta atualiza a série existente.
"""
import base64
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent


def style_svg(document):
    document = re.sub(r'<style id="dicas-fonts">.*?</style>\s*', '', document, flags=re.S)
    faces = []
    for name, weight in [('Regular', 400), ('Bold', 700)]:
        source = ROOT / 'assets/fonts' / f'LibertinusSerif-{name}.woff2'
        encoded = base64.b64encode(source.read_bytes()).decode('ascii')
        faces.append(
            '@font-face{font-family:"Libertinus Serif";'
            f'font-style:normal;font-weight:{weight};'
            f'src:url("data:font/woff2;base64,{encoded}") format("woff2");}}'
        )
    style = '<style id="dicas-fonts">' + ''.join(faces) + '</style>\n'
    return re.sub(r'(<svg\b[^>]*>)\s*', lambda m: m[1] + '\n' + style, document, count=1)


def write_svg(path, document):
    styled = style_svg(document)
    if not path.exists() or path.read_text() != styled:
        path.write_text(styled)


if __name__ == '__main__':
    paths = sorted((ROOT / 'assets/figures').glob('arte-cap*.svg'))
    for path in paths:
        write_svg(path, path.read_text())
    print(f'Fontes incorporadas em {len(paths)} diagramas editáveis.')
