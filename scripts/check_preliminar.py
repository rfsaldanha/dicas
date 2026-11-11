#!/usr/bin/env python3
"""Verifica o artefato publicado, incluindo links sob o prefixo /dicas/."""

from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET


BASE = "https://rfsaldanha.github.io/dicas/"
EDITION = "Versão preliminar — Partes I e II"


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("id", "name"):
            if attrs.get(key):
                self.ids.add(attrs[key])
        for key in ("href", "src", "poster", "data-src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            match = re.search(r"url=(.*)", attrs.get("content", ""), re.I)
            if match:
                self.links.append(match[1].strip(" '\""))


def inspect(root, profile):
    result = subprocess.run(
        ["quarto", "inspect", "--profile", profile], cwd=root,
        text=True, capture_output=True, check=True,
    )
    return json.loads(result.stdout)


def check_site(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    info = inspect(root, "preliminar")
    book = info["config"]["book"]
    inputs = [x["file"] for x in book["render"] if "file" in x]
    chapter_paths = [p for p in inputs if p.startswith("chapters/")]
    expected_chapters = sorted(
        p.relative_to(root).as_posix()
        for part in ("part-1", "part-2")
        for p in (root / "chapters" / part).glob("*.qmd")
    )
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    require(chapter_paths == expected_chapters and len(chapter_paths) == 12,
            "O perfil deve conter exatamente os capítulos 1–12, na ordem.")
    expected_inputs = [
        "index.qmd", "frontmatter/agradecimentos.qmd", "frontmatter/prefacio.qmd",
        "frontmatter/siglas.qmd", *expected_chapters, "backmatter/glossario.qmd",
        "backmatter/referencias.qmd", "backmatter/apendice-metodologico.qmd",
        "backmatter/apendice-estacoes.qmd",
    ]
    require(inputs == expected_inputs, "Páginas editoriais ou ordem diferentes da edição aprovada.")
    require(book["site-url"] == BASE, "Endereço público incorreto.")
    pages = {str(Path(p).with_suffix(".html")) for p in inputs}
    aliases = {}
    for source in inputs:
        metadata = info["fileInformation"][source]["metadata"]
        for alias in metadata.get("aliases", []):
            aliases[alias.lstrip("/")] = str(Path(source).with_suffix(".html"))
    expected_html = pages | aliases.keys()
    actual_html = {p.relative_to(output).as_posix() for p in output.rglob("*.html")}
    require(actual_html == expected_html,
            f"Páginas ausentes: {sorted(expected_html - actual_html)}; "
            f"páginas indevidas: {sorted(actual_html - expected_html)}")
    documents = {}
    for relative in sorted(actual_html):
        text = (output / relative).read_text(encoding="utf-8")
        documents[relative] = Document(text)
        if relative in pages:
            require(EDITION in text, f"Identificação preliminar ausente: {relative}")
            require("quarto-sidebar" in text, f"Navegação ausente: {relative}")
            require(not re.search(r"(?:Parte III|Parte IV)\s*</span>", text),
                    f"Parte excluída na navegação: {relative}")
            require(not re.search(r"\?@?(?:fig|tbl|sec|eq|qua)-", text),
                    f"Referência cruzada não resolvida: {relative}")
        if relative in aliases:
            require(Path(aliases[relative]).name in text and "window.location.hash" in text,
                    f"Redirecionamento inválido: {relative}")
    for number, source in enumerate(chapter_paths, 1):
        target = output / Path(source).with_suffix(".html")
        if target.exists():
            require(f'<span class="chapter-number">{number}</span>' in target.read_text(),
                    f"Numeração incorreta: {source}")

    checked = set()

    def check_link(source, href):
        resolved = urlsplit(urljoin(BASE + source, href))
        if resolved.scheme not in ("http", "https") or resolved.netloc != urlsplit(BASE).netloc:
            return
        require(resolved.path.startswith("/dicas/"), f"Link escapa de /dicas/: {source}: {href}")
        if not resolved.path.startswith("/dicas/"):
            return
        relative = unquote(resolved.path[len("/dicas/"):])
        if not relative or relative.endswith("/"):
            relative += "index.html"
        key = (relative, resolved.fragment)
        if key in checked:
            return
        checked.add(key)
        target = output / relative
        require(not relative.endswith(".qmd"), f"Link para fonte Quarto local: {source}: {href}")
        require(target.is_file(), f"Destino inexistente: {source}: {href}")
        if resolved.fragment and relative in documents:
            # O redirecionamento do Quarto preserva o fragmento na página atual.
            document = documents.get(aliases.get(relative, relative))
            require(document is not None and unquote(resolved.fragment) in document.ids,
                    f"Âncora inexistente: {source}: {href}")

    for relative, document in documents.items():
        for href in document.links:
            check_link(relative, href)
    for css in output.rglob("*.css"):
        for href in re.findall(r"url\(\s*['\"]?([^'\"\s)]+)", css.read_text()):
            check_link(css.relative_to(output).as_posix(), href)
    search = json.loads((output / "search.json").read_text())
    search_pages = set()
    for entry in search:
        href = entry["href"]
        check_link("index.html", href)
        path = urlsplit(urljoin(BASE, href)).path.removeprefix("/dicas/")
        search_pages.add(path)
    require(search_pages == pages, f"Páginas incorretas na busca: {search_pages ^ pages}")
    sitemap = output / "sitemap.xml"
    require(sitemap.exists(), "Sitemap ausente.")
    if sitemap.exists():
        for element in ET.parse(sitemap).iter():
            if element.tag.endswith("}loc"):
                check_link("index.html", element.text)
    require((output / ".nojekyll").is_file(), "Arquivo .nojekyll ausente.")
    for path in output.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(output)
        require(not path.is_symlink(), f"Link simbólico no artefato: {relative}")
        require(relative.parts[0] not in ("_output", "docs", "indicators", "sources", "scripts"),
                f"Material fora da edição: {relative}")
        require(path.suffix not in (".qmd", ".typ", ".R", ".lua", ".yml", ".yaml"),
                f"Arquivo-fonte no artefato: {relative}")
        if path.suffix == ".pdf":
            require(relative.as_posix().startswith("data-raw/estacoes/") and
                    path.name.endswith("-original.pdf"), f"PDF editorial no artefato: {relative}")
        with path.open("rb") as stream:
            require(not stream.read(80).startswith(b"version https://git-lfs.github.com/spec/v1"),
                    f"Ponteiro LFS sem conteúdo: {relative}")
    if errors:
        raise RuntimeError("Falha na edição preliminar:\n- " + "\n- ".join(errors))
    print(f"Validado: {len(pages)} páginas, {len(aliases)} redirecionamentos, "
          f"{len(chapter_paths)} capítulos e {len(checked)} destinos internos.")


if __name__ == "__main__":
    check_site(Path(__file__).resolve().parents[1],
               sys.argv[1] if len(sys.argv) > 1 else "_output/preliminar")
