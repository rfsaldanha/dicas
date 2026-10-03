"""Exporta SVGs autocontidos com as mesmas fontes e imagens usadas na web.

Requer Playwright/Chromium e ImageMagick. A decodificação das imagens e o
carregamento das fontes são verificados antes de produzir o PNG de impressão.
"""
from pathlib import Path
import math
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright


def export_print(svg, output, width=2700):
    svg, output = Path(svg), Path(output)
    root = ET.parse(svg).getroot()
    _, _, sw, sh = map(float, root.attrib['viewBox'].split())
    height = math.ceil(width * sh / sw)
    with tempfile.TemporaryDirectory(prefix='dicas-figure-') as folder:
        rgba = Path(folder) / 'composicao.png'
        gray = Path(folder) / 'impressao.png'
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel=os.environ.get('DICAS_BROWSER_CHANNEL'))
            try:
                page = browser.new_page(viewport={'width': width, 'height': height},
                                        device_scale_factor=1)
                page.set_content('<!doctype html><html><head><style>'
                                 'html,body{margin:0;padding:0;overflow:hidden}'
                                 'svg{display:block}'
                                 '</style></head><body>' + svg.read_text() + '</body></html>',
                                 wait_until='load')
                page.evaluate('''async ([width, height]) => {
                    const svg = document.querySelector('svg');
                    svg.setAttribute('width', width);
                    svg.setAttribute('height', height);
                    const faces = [...document.fonts];
                    await Promise.all(faces.map(face => face.load()));
                    await document.fonts.ready;
                    if (!faces.length || faces.some(face => face.status !== 'loaded'))
                        throw new Error('Fontes incorporadas não foram carregadas.');
                    const images = [...document.querySelectorAll('image')];
                    if (!images.length) throw new Error('SVG sem aquarela incorporada.');
                    await Promise.all(images.map(async element => {
                        const image = new Image();
                        image.src = element.getAttribute('href') ||
                            element.getAttributeNS('http://www.w3.org/1999/xlink', 'href');
                        await image.decode();
                    }));
                }''', [width, height])
                page.screenshot(path=str(rgba), animations='disabled')
            finally:
                browser.close()
        # A largura máxima de uso no miolo é 120 mm. A densidade do raster
        # exportado não substitui a conferência da resolução efetiva da aquarela.
        subprocess.run(['magick', str(rgba), '-background', 'white',
                        '-alpha', 'remove', '-alpha', 'off', '-colorspace', 'Gray',
                        '-depth', '8', '-units', 'PixelsPerInch',
                        '-density', str(width * 25.4 / 120),
                        '-define', 'png:color-type=0', str(gray)], check=True)
        output.write_bytes(gray.read_bytes())
