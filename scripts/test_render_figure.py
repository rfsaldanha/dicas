"""Verifica exportação vetorial e preservação da saída quando um raster falha."""
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from playwright.sync_api import Error
from figure_style import write_svg
from render_figure import export_print


class FigureExportTest(unittest.TestCase):
    def test_vector_requires_explicit_opt_in(self):
        with tempfile.TemporaryDirectory() as folder:
            svg, output = Path(folder) / 'vector.svg', Path(folder) / 'print.png'
            write_svg(svg, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60">'
                      '<rect width="100" height="60" fill="white"/>'
                      '<circle cx="50" cy="30" r="20" fill="black"/></svg>')
            with self.assertRaisesRegex(Error, 'SVG sem aquarela incorporada'):
                export_print(svg, output, width=300)
            self.assertFalse(output.exists())
            export_print(svg, output, width=300, require_raster=False)
            with Image.open(output) as im:
                self.assertEqual(im.mode, 'L')
                self.assertEqual(im.size, (300, 180))
                self.assertEqual(im.getpixel((150, 90)), 0)
                self.assertEqual(im.getpixel((0, 0)), 255)

    def test_corrupt_raster_never_replaces_previous_output(self):
        with tempfile.TemporaryDirectory() as folder:
            svg, output = Path(folder) / 'broken.svg', Path(folder) / 'print.png'
            write_svg(svg, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60">'
                      '<image width="100" height="60" href="data:image/png;base64,AA=="/></svg>')
            for require_raster in [True, False]:
                with self.subTest(require_raster=require_raster):
                    output.write_bytes(b'previous-output')
                    with self.assertRaisesRegex(Error, 'source image cannot be decoded'):
                        export_print(svg, output, width=300, require_raster=require_raster)
                    self.assertEqual(output.read_bytes(), b'previous-output')


if __name__ == '__main__':
    unittest.main()
