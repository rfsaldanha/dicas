"""Confere conversões publicadas e casos de transição usando a base IANA local."""
from datetime import datetime, timezone
import json
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent


def main():
    document = json.loads((ROOT / 'data-raw/figures/conversoes-utc-cap4.json').read_text())
    source = (ROOT / 'chapters/part-1/04-espaco-tempo-qualidade.qmd').read_text()
    for row in document['rows']:
        zone = ZoneInfo(row['zone'])
        for entry in row['conversions']:
            instant = datetime.fromisoformat(entry['utc'])
            local = instant.astimezone(zone)
            assert local.isoformat() == entry['local'], (row['label'], entry)
            assert local.astimezone(timezone.utc) == instant
        assert row['markdown'] in source, row['label']
    # Série histórica: não aplicar o deslocamento atual a todo o passado.
    sao_paulo = ZoneInfo('America/Sao_Paulo')
    assert datetime(2018, 1, 29, tzinfo=timezone.utc).astimezone(sao_paulo).utcoffset().total_seconds() == -7200
    assert datetime(2026, 1, 29, tzinfo=timezone.utc).astimezone(sao_paulo).utcoffset().total_seconds() == -10800
    paris = ZoneInfo('Europe/Paris')
    spring = [datetime(2026, 3, 29, h, 30, tzinfo=timezone.utc).astimezone(paris) for h in [0, 1]]
    autumn = [datetime(2026, 10, 25, h, 30, tzinfo=timezone.utc).astimezone(paris) for h in [0, 1]]
    assert [x.hour for x in spring] == [1, 3]
    assert [x.hour for x in autumn] == [2, 2]
    assert autumn[0].utcoffset() != autumn[1].utcoffset()
    print('UTC: 16 conversões, mudança de dia, regra histórica e transições de Paris conferidas.')


if __name__ == '__main__':
    main()
