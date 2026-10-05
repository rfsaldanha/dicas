#!/usr/bin/env python3
"""Extrai e confere os dois exemplos do apêndice B, sem acesso à rede."""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data-raw/estacoes'
COLUMNS = {
    'temperatura_c': 'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
    'umidade_pct': 'UMIDADE RELATIVA DO AR, HORARIA (%)',
    'precipitacao_mm': 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
    'radiacao_kj_m2': 'RADIACAO GLOBAL (Kj/m²)',
    'maxima_hora_anterior_c': 'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)',
    'minima_hora_anterior_c': 'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)',
}
STATIONS = ['Ibirapuera', 'Pico do Jaraguá', 'Pinheiros', 'Santana', 'Osasco', 'São José do Rio Preto']


def make_csv(rows):
    s = io.StringIO(newline='')
    w = csv.DictWriter(s, fieldnames=list(rows[0]), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    return s.getvalue()


def extract():
    raw = (DATA / 'inmet-a701-2024-original.csv').read_bytes()
    meta = json.loads((DATA / 'inmet-proveniencia.json').read_text())
    assert hashlib.sha256(raw).hexdigest() == meta['raw_sha256'], 'Original INMET alterado'
    lines = raw.decode('latin1').splitlines()
    obs = []
    for row in csv.DictReader(lines[8:], delimiter=';'):
        if row['Data'] != '2024/01/01':
            continue
        obs.append({'data_utc': '2024-01-01', 'hora_utc': row['Hora UTC'][:2] + ':00', **{
            k: None if row[v] in ('', '-9999') else float(row[v].replace(',', '.'))
            for k, v in COLUMNS.items()
        }})
    assert len(obs) == 24 and [r['hora_utc'] for r in obs] == [f'{h:02}:00' for h in range(24)]
    assert all(r['temperatura_c'] is not None and r['umidade_pct'] is not None for r in obs)
    # Página física 9 do PDF separado = página impressa 183 do relatório.
    pdf = DATA / 'cetesb-2021-apendice4-original.pdf'
    meta = json.loads((DATA / 'cetesb-proveniencia.json').read_text())
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == meta['raw_sha256'], 'Original CETESB alterado'
    table = subprocess.check_output(['pdftotext', '-f', '9', '-l', '9', '-layout', str(pdf), '-'], text=True)
    assert '2021' in table and 'TABELA D' in table
    air = []
    for station in STATIONS:
        line = next(s for s in table.splitlines() if re.search(r'(?<!\w)' + re.escape(station) + r'\s', s))
        values = line.split()[-9:]
        assert values[0] in ('S', 'N') and len(values) == 9
        air.append({'estacao': station, 'ano': 2021, 'poluente': 'MP2,5',
                    'metodo': 'atenuação beta', 'representatividade_anual': values[0],
                    'n_dados_diarios': int(values[1]), 'media_publicada_ug_m3': int(values[2]),
                    'maior_media_24h_ug_m3': int(values[3])})
    return {'inmet-a701-2024-01-01.csv': make_csv(obs), 'cetesb-mp25-2021.csv': make_csv(air)}, obs, air


def main():
    outputs, obs, air = extract()
    check = '--check' in sys.argv
    for name, value in outputs.items():
        path = DATA / name
        if check:
            assert path.read_text() == value, f'Derivado diverge do original: {name}'
        else:
            path.write_text(value)
    # Verifica exemplos interpretativos; não substitui a validação técnica das redes.
    assert sum(r['radiacao_kj_m2'] is None for r in obs) == 10
    assert sum(r['precipitacao_mm'] for r in obs) == 0
    assert max(r['temperatura_c'] for r in obs) == 25.4
    assert max(r['maxima_hora_anterior_c'] for r in obs) == 26.5
    assert abs(sum(r['temperatura_c'] for r in obs) / 24 - 21.275) < 1e-10
    assert next(r for r in air if r['estacao'] == 'Ibirapuera')['representatividade_anual'] == 'S'
    assert next(r for r in air if r['estacao'] == 'São José do Rio Preto')['representatividade_anual'] == 'N'
    print('Exemplos conferidos: 24 observações INMET e 6 registros CETESB, extraídos dos originais.')


if __name__ == '__main__':
    main()
