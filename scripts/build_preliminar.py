#!/usr/bin/env python3
"""Compila a edição parcial em fontes isolados e publica apenas após validar."""

from pathlib import Path
import shutil
import subprocess
import tempfile

from check_preliminar import check_site


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = (
    "_extensions", "assets", "backmatter", "chapters", "data-raw",
    "frontmatter", "includes", "indicators", "scripts", "sources", "styles",
)


def main():
    destination = ROOT / "_output/preliminar"
    # Não copiar _output é essencial: existem provas e sites completos
    # versionados que não devem entrar na publicação parcial.
    with tempfile.TemporaryDirectory(prefix="dicas-preliminar-") as temporary:
        stage = Path(temporary)
        for name in SOURCE_DIRS:
            shutil.copytree(
                ROOT / name, stage / name,
                ignore=shutil.ignore_patterns("__pycache__", "*_files", ".DS_Store"),
            )
        for source in [*ROOT.glob("_quarto*.yml"), ROOT / "index.qmd",
                       ROOT / "references.bib", ROOT / "LICENSE"]:
            shutil.copy2(source, stage / source.name)
        subprocess.run(["quarto", "render", "--profile", "preliminar"],
                       cwd=stage, check=True)
        output = stage / "_output/preliminar"
        (output / ".nojekyll").touch()
        check_site(stage, output)
        # Uma falha de renderização/validação preserva a última prévia válida.
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(output, destination)
    print(f"Edição preliminar validada: {destination}")


if __name__ == "__main__":
    main()
