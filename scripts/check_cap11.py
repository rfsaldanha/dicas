#!/usr/bin/env python3
"""Confere figuras, citações, remissões e compatibilidade do capítulo 11."""
import argparse
import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
CHAPTER = ROOT / "chapters/part-2/11-uso-cobertura-terra-ambiente-urbano.qmd"

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.links, self.images = [], [], []
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag == "img":
            self.images.append(a)

def expanded(path):
    body = path.read_text()
    return re.sub(r"\{\{< include ([^ ]+\.qmd) >\}\}",
                  lambda m: expanded((path.parent / m[1]).resolve()), body)

def check(rendered=False):
    body = CHAPTER.read_text()
    records = json.loads((ROOT/"assets/figures/arte-cap11-manifest.json").read_text())
    assert len(records) == 9 and len({r["id"] for r in records}) == 9
    assert sum(r["watercolor"] for r in records) == 6
    assert len(re.findall(r"(?m)^## ", body)) == 8
    assert not re.search(r"(?m)^### |^## Síntese|%%FIG|%%LEGACY", body)
    ids = {r["id"] for r in records}
    assert {"fig-terra-saude", "fig-camadas-urbanas"} <= ids
    parts = re.split(r"(?m)^## ", body)
    assert len(parts) == len(records)
    for part, r in zip(parts, records):
        assert len(re.findall(r"\{#fig-", part)) == 1, r["number"]
        assert "{#"+r["id"] in part and "@"+r["id"] in part
        assert re.search(r"\]\(../../chapters/part-4/.+?\.qmd", part), r["number"]
        assert re.search(r"\[@[a-zA-Z]", part), "Seção sem referência: "+r["number"]
    bib = re.findall(r"(?m)^@\w+\{([^,]+)", (ROOT/"references.bib").read_text())
    assert len(bib) == len(set(bib))
    refs = set(re.findall(r"@([A-Za-z][\w-]+)", body))
    citations = {ref for ref in refs if not ref.startswith(("fig-", "qua-", "sec-"))}
    assert not citations-set(bib), citations-set(bib)
    listing = (ROOT/"backmatter/lista-figuras.qmd").read_text()
    ns = {"s": "http://www.w3.org/2000/svg"}
    for r in records:
        assert listing.count("@"+r["id"]+" ") == 1, r["id"]
        svg = ET.parse(ROOT/"assets/figures"/r["svg"]).getroot()
        assert svg.find("s:title", ns) is not None and svg.find("s:desc", ns) is not None
        assert svg.find("s:style[@id='dicas-fonts']", ns) is not None
        png = (ROOT/"assets/figures"/r["print"]).read_bytes()
        assert png[:8] == b"\x89PNG\r\n\x1a\n" and png[24:26] == bytes([8, 0])
        assert struct.unpack(">I", png[16:20])[0] >= 1418
        if r["watercolor"]:
            original = ROOT/"assets/figures"/r["raster"]
            assert hashlib.sha256(original.read_bytes()).hexdigest() == r["sha256_original"]
            assert r["min_effective_raster_ppi"] >= 300
            assert (ROOT/"assets/figures"/r["prompt"]).is_file()
    cards = ROOT/"chapters/part-4/20-fichas-uso-cobertura-terra-ambiente-urbano.qmd"
    expected = {"sec-"+c for c in re.findall(r"indicators/includes/([a-z0-9-]+)\.qmd", cards.read_text())}
    anchors = re.findall(r'<span id="(sec-[^"]+)"></span>', body)
    assert len(anchors) == 4 and set(anchors) == expected
    targets = re.findall(r"\]\(([^)]+\.qmd(?:#[^)]+)?)\)", body)
    for target in targets:
        file, _, anchor = target.partition("#")
        dest = (CHAPTER.parent/file).resolve()
        assert dest.is_file(), target
        if anchor:
            content = expanded(dest)
            assert "{#"+anchor in content or 'id="'+anchor+'"' in content, target
    if rendered:
        web = ROOT/"_output/web"
        html = (web/CHAPTER.relative_to(ROOT)).with_suffix(".html")
        page = Page(html)
        content_ids = [i for i in page.ids if i not in {"quarto-text-highlighting-styles", "quarto-bootstrap"}]
        assert len(content_ids) == len(set(content_ids)), "IDs duplicados"
        assert ids|expected|{"qua-indicadores-urbano"} <= set(page.ids)
        assert "quarto-unresolved-ref" not in html.read_text()
        cache = {}
        for href in page.links:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            dest = (web/parsed.path.lstrip("/") if parsed.path.startswith("/") else html.parent/parsed.path).resolve() if parsed.path else html
            if dest.is_dir():
                dest = dest/"index.html"
            assert dest.is_file(), href
            if dest.suffix == ".html" and parsed.fragment:
                if dest not in cache:
                    cache[dest] = set(Page(dest).ids)
                assert unquote(parsed.fragment) in cache[dest], href
        for r in records:
            assert any(r["svg"] in a.get("src", "") and a.get("alt") for a in page.images), r["svg"]
        for code in expected:
            href = "../../chapters/part-4/"+cards.with_suffix(".html").name+"#"+code
            assert href in page.links, href
        card_html = (web/cards.relative_to(ROOT)).with_suffix(".html")
        assert any("11-uso-cobertura-terra-ambiente-urbano.html" in h for h in Page(card_html).links)
        alias = (web/"chapters/part-2/09-uso-cobertura-terra-ambiente-urbano.html").read_text()
        assert "11-uso-cobertura-terra-ambiente-urbano.html" in alias and "window.location.hash" in alias
    print(f"Capítulo 11: oito seções, nove figuras (seis aquarelas), quatro âncoras e {len(citations)} referências válidas.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rendered", action="store_true")
    check(parser.parse_args().rendered)
