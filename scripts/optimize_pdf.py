#!/usr/bin/env python3
"""Recomprime imagens em cinza sem alterar pixels, resolução ou paginação.

Executado antes do pré-voo somente quando o PDF ultrapassa 140 MB.
Dependências opcionais para esse caso: requirements-print.txt.
"""
import hashlib
import io
import os
from pathlib import Path
import struct
import sys
import tempfile


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def png_payload(image):
    buffer = io.BytesIO()
    image.save(buffer, format='PNG', compress_level=9)
    png = buffer.getvalue()
    chunks = []
    position = 8
    while position < len(png):
        length = struct.unpack('>I', png[position:position + 4])[0]
        if png[position + 4:position + 8] == b'IDAT':
            chunks.append(png[position + 8:position + 8 + length])
        position += length + 12
    return b''.join(chunks)


def optimize(path):
    if path.stat().st_size <= 140_000_000:
        print('PDF abaixo de 140 MB; recompressão dispensada.')
        return
    try:
        import pymupdf
        from PIL import Image
    except ImportError as error:
        raise SystemExit('PDF acima de 140 MB. Instale requirements-print.txt e '
                         'indique esse Python em DICAS_PYTHON.') from error

    original_hash = digest(path)
    size_before = path.stat().st_size
    document = pymupdf.open(path)
    text_before = [page.get_text() for page in document]
    toc_before = document.get_toc()
    links_before = [len(page.get_links()) for page in document]
    # garbage=1 preserva os índices; conferir cada fluxo após reabrir o PDF.
    decoded_hashes = {}
    changed = 0
    for xref in range(1, document.xref_length()):
        if document.xref_get_key(xref, 'Subtype')[1] != '/Image':
            continue
        if document.xref_get_key(xref, 'BitsPerComponent')[1] != '8':
            continue
        pixels = pymupdf.Pixmap(document, xref)
        if pixels.n != 1:
            continue
        raw = document.xref_stream(xref)
        if len(raw) != pixels.width * pixels.height:
            continue
        image = Image.frombytes('L', (pixels.width, pixels.height), raw)
        compressed = png_payload(image)
        if len(compressed) >= len(document.xref_stream_raw(xref)):
            continue
        decoded_hashes[xref] = hashlib.sha256(raw).hexdigest()
        document.update_stream(xref, compressed, compress=False)
        document.xref_set_key(xref, 'Filter', '/FlateDecode')
        document.xref_set_key(xref, 'DecodeParms',
                             f'<< /Predictor 15 /Colors 1 /BitsPerComponent 8 '
                             f'/Columns {pixels.width} >>')
        assert document.xref_stream(xref) == raw, 'Pixels alterados na recompressão.'
        changed += 1

    handle, name = tempfile.mkstemp(prefix='.dicas-pdf-', suffix='.pdf', dir=path.parent)
    os.close(handle)
    temporary = Path(name)
    try:
        document.save(temporary, garbage=1, deflate=True, use_objstms=1)
        document.close()
        with pymupdf.open(temporary) as result:
            assert [page.get_text() for page in result] == text_before, 'Texto ou páginas alterados.'
            assert result.get_toc() == toc_before, 'Sumário alterado.'
            assert [len(page.get_links()) for page in result] == links_before, 'Links alterados.'
            for xref, expected in decoded_hashes.items():
                assert hashlib.sha256(result.xref_stream(xref)).hexdigest() == expected, 'Pixels alterados no PDF salvo.'
        if digest(path) != original_hash:
            raise RuntimeError('Outra compilação alterou o PDF; saída concorrente preservada.')
        if temporary.stat().st_size < size_before:
            temporary.replace(path)
        print(f'PDF sem perda: {changed} imagens; {size_before} → {path.stat().st_size} bytes; '
              'pixels, texto, páginas, sumário e quantidade de links conferidos.')
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == '__main__':
    optimize(Path(sys.argv[1] if len(sys.argv) > 1 else
                  '_output/print/dados-indicadores-clima-ambiente-saude.pdf'))
