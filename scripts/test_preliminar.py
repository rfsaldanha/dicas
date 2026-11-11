#!/usr/bin/env python3
"""Regressões de referências mistas e rejeição de artefatos incompletos."""

from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import check_preliminar


ROOT = Path(__file__).resolve().parents[1]


def nodes(value, kind):
    if isinstance(value, dict):
        if value.get("t") == kind:
            yield value
        for child in value.values():
            yield from nodes(child, kind)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child, kind)


class References(unittest.TestCase):
    def filtered(self, markdown):
        result = subprocess.run(
            ["quarto", "pandoc", "-f", "markdown", "-t", "json",
             "--lua-filter=scripts/preliminar-links.lua"],
            cwd=ROOT, input=markdown, text=True, capture_output=True, check=True,
        )
        return json.loads(result.stdout)

    def test_bibliography_survives_mixed_reference(self):
        document = self.filtered(
            "No @sec-efeitos-saude [@hernan2020causal; @gasparrini2010dlnm]."
        )
        citations = [c["citationId"] for node in nodes(document, "Cite") for c in node["c"][0]]
        self.assertEqual(citations, ["hernan2020causal", "gasparrini2010dlnm"])
        self.assertIn("capítulo 14", [node["c"] for node in nodes(document, "Str")])

    def test_only_omitted_local_links_are_removed(self):
        links = {
            "ficha": "../../chapters/part-4/17-fichas-temperatura-condicoes-termicas.qmd#sec-cli-tem-01",
            "catálogo": "../../backmatter/indice-fontes.qmd#inmet",
            "capítulo": "../../chapters/part-1/01-clima-ambiente-saude.qmd",
            "alias": "/chapters/part-4/14-indicador-decisao.html#sec-indicador-decisao",
            "fonte": "https://github.com/rfsaldanha/dicas/blob/main/chapters/part-4/17-fichas-temperatura-condicoes-termicas.qmd",
        }
        document = self.filtered(" ".join(f"[**{label}**]({url})" for label, url in links.items()))
        self.assertEqual([node["c"][2][0] for node in nodes(document, "Link")],
                         [links[key] for key in ("capítulo", "alias", "fonte")])
        self.assertEqual(len(list(nodes(document, "Strong"))), 5)


class Artifact(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = ROOT / "_output/preliminar"
        if not (source / "index.html").exists():
            raise RuntimeError("Execute make preliminar antes dos testes do artefato.")
        cls.temporary = tempfile.TemporaryDirectory(prefix="dicas-preliminar-test-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.site = Path(cls.temporary.name) / "site"
        shutil.copytree(source, cls.site)
        cls.info = check_preliminar.inspect(ROOT, "preliminar")

    def check(self):
        with patch.object(check_preliminar, "inspect", return_value=self.info):
            check_preliminar.check_site(ROOT, self.site)

    def test_rejects_omitted_page_even_without_navigation_link(self):
        path = self.site / "chapters/part-3/13-exposicao-vulnerabilidade.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.write_text("<p>Conteúdo que não deve ser publicado.</p>")
            with self.assertRaisesRegex(RuntimeError, "páginas indevidas"):
                self.check()
        finally:
            path.unlink()

    def test_rejects_broken_anchor(self):
        path = self.site / "index.html"
        original = path.read_text()
        try:
            path.write_text(original + '<a href="frontmatter/prefacio.html#ancora-inexistente">Teste</a>')
            with self.assertRaisesRegex(RuntimeError, "Âncora inexistente"):
                self.check()
        finally:
            path.write_text(original)

    def test_rejects_full_book_pdf(self):
        path = self.site / "livro-completo.pdf"
        try:
            path.write_bytes(b"%PDF-1.7\n")
            with self.assertRaisesRegex(RuntimeError, "PDF editorial"):
                self.check()
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
