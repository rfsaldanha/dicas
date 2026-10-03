# Fontes da identidade editorial

| Família | Versão | Origem oficial | Licença |
|---|---|---|---|
| Libertinus Serif | 7.051 | [Libertinus v7.051](https://github.com/alerque/libertinus/releases/tag/v7.051) | `LICENSE-Libertinus.txt` |
| Source Sans 3 | 3.052R | [Source Sans 3.052R](https://github.com/adobe-fonts/source-sans/releases/tag/3.052R) | `LICENSE-SourceSans3.txt` |

Os arquivos OTF foram extraídos das distribuições oficiais. As cópias WOFF2 foram convertidas com FontTools 4.66.1 e Brotli 1.2.0, sem redução de caracteres nem alteração do desenho ou dos nomes das fontes. `manifest.json` registra os hashes SHA-256 de cada arquivo. As licenças próprias das fontes acompanham a distribuição.

O perfil de impressão usa `font-paths: [assets/fonts]`, dispensando instalação no sistema. Os estilos web usam `@font-face` e caminhos locais, preservando a tipografia sem consultas a provedores externos de fontes. Os compositores de figuras usam `scripts/figure_style.py` para incorporar as fontes nos SVGs.

Para repetir a conversão em um ambiente que tenha FontTools e Brotli instalados:

```python
from pathlib import Path
from fontTools.ttLib import TTFont

for path in Path("assets/fonts").glob("*.otf"):
    font = TTFont(path)
    font.flavor = "woff2"
    font.save(path.with_suffix(".woff2"))
```

Depois de substituir uma fonte, atualizar o manifesto e executar `python3 scripts/figure_style.py` antes de renderizar a web.
