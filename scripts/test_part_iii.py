#!/usr/bin/env python3
"""Testes de aceite da especificação; não é um pipeline de dados de saúde.

Os casos de fronteira são entradas técnicas de teste, não observações empíricas.
A única conferência empírica usa a resposta real do SIDRA arquivada no projeto.
Requer PyYAML, também utilizado pelas ferramentas editoriais Python do projeto.
"""
import calendar
import csv
from datetime import date, timedelta
from decimal import Decimal
import hashlib
from io import StringIO
import json
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "indicators/protocols"
SPEC = yaml.safe_load((PROTOCOL / "parte-iii.yml").read_text())


def ratio(numerator, denominator, scale=100):
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return scale * numerator / denominator


def age_band(value):
    """Oráculo dos limites documentados do campo IDADE/SIM."""
    if not isinstance(value, str) or not re.fullmatch(r"\d{3}", value):
        return None
    unit, quantity = int(value[0]), int(value[1:])
    if unit in (0, 1, 2, 3):
        return 0 if 1 <= quantity <= {0: 59, 1: 23, 2: 29, 3: 11}[unit] else None
    if unit not in (4, 5):
        return None
    years = quantity + (100 if unit == 5 else 0)
    return min(years // 5, 17)


def cause_in(code, ranges):
    code = re.sub(r"[.\s]", "", code.upper())
    if not re.fullmatch(r"[A-Z]\d{2}[A-Z0-9]*", code):
        return False
    code = code[:3]
    return any((r.split("-")[0] <= code <= r.split("-")[-1]) for r in ranges)


def complete_conformity(values, evidence=True):
    if not evidence or not values or any(v not in ("sim", "nao") for v in values):
        return None
    return all(v == "sim" for v in values)


def risk_current(review, assessment):
    year = assessment.year - SPEC["coleta_local"]["ris_anos"]
    start = date(year, assessment.month,
                 min(assessment.day, calendar.monthrange(year, assessment.month)[1]))
    return start <= review <= assessment


class PartIII(unittest.TestCase):
    def test_card_set_and_retirements(self):
        cards = {}
        for path in (ROOT / "indicators/data").glob("*.yml"):
            obj = yaml.safe_load(path.read_text())
            cards.update((x["codigo"], x) for x in obj.get("indicators", [obj]))
        active = {c for c in cards if c.startswith(("EXP-", "EFE-", "RES-"))}
        self.assertEqual(active, set(SPEC["fichas_parte_iii"]))
        self.assertEqual(len(active), 12)
        self.assertEqual(len(cards), 64)
        for code in active:
            self.assertTrue(cards[code]["capitulo_fichas"].startswith("chapters/part-4/"))
            self.assertEqual(cards[code]["protocolo_versao"], SPEC["versao"])
        chapters = "\n".join(p.read_text() for p in (ROOT / "chapters/part-4").glob("*.qmd"))
        for code in SPEC["codigos_reservados"]:
            self.assertNotIn(code, cards)
            self.assertIn("{#sec-" + code.lower() + "}", chapters)
            self.assertFalse((ROOT / "indicators/includes" / (code.lower()+".qmd")).exists())

    def test_official_sidra_response_and_provenance(self):
        folder = ROOT / "data-raw/parte-iii"
        evidence = json.loads((folder / "verificacao.json").read_text())
        raw = (folder / evidence["arquivo"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), evidence["sha256"])
        values = {}
        for variable in json.loads(raw):
            for result in variable["resultados"]:
                classes = {c["id"]: next(iter(c["categoria"])) for c in result["classificacoes"]}
                self.assertEqual(classes["63"], "95826")
                self.assertEqual(classes["125"], "2932")
                series = result["series"][0]
                self.assertEqual(series["localidade"]["id"], "3304557")
                values[(variable["id"], classes["1975"])] = Decimal(series["serie"]["2022"])
        result = ratio(values["381", "73090"], values["381", "73086"])
        self.assertEqual(result.quantize(Decimal("0.01")), values["1000381", "73090"])
        self.assertEqual(values["381", "73090"], Decimal("80536"))
        self.assertEqual(values["381", "73086"], Decimal("2436966"))
        h = SPEC["habitacao"]
        self.assertEqual((h["tabela"], h["variavel"], h["classificacao"], h["numerador"], h["denominador"]),
                         (9933, 381, 1975, 73090, 73086))

    def test_empty_and_zero_denominators(self):
        self.assertEqual(SPEC["habitacao"]["sinais"]["-"], 0)
        for symbol in ["X", "...", "..", ""]:
            self.assertIsNone(SPEC["habitacao"]["sinais"][symbol])
        self.assertIsNone(ratio(0, 0))
        self.assertIsNone(ratio(1, None))
        self.assertIsNone(ratio(None, 100))
        self.assertEqual(ratio(0, 100), 0)
        # Desconhecido e não respondente não são ausência de problema.
        self.assertIsNone(complete_conformity(["sim", "ignorado"]))
        self.assertIsNone(complete_conformity(["nao", ""]))
        self.assertIsNone(complete_conformity(["sim"], evidence=False))
        self.assertFalse(complete_conformity(["sim", "nao"]))
        self.assertTrue(complete_conformity(["sim", "sim"]))

    def test_who_weights_and_age_boundaries(self):
        weights = list(csv.DictReader(StringIO((PROTOCOL / "pesos-oms-2001.csv").read_text())))
        expected = "8.86 8.69 8.60 8.47 8.22 7.93 7.61 7.15 6.59 6.04 5.37 4.55 3.72 2.96 2.21 1.52 0.91 0.63".split()
        self.assertEqual([r["percentual_publicado"] for r in weights], expected)
        self.assertEqual(sum(map(Decimal, expected)), Decimal("100.03"))
        self.assertEqual([int(r["idade_min"]) for r in weights], list(range(0, 90, 5)))
        self.assertEqual(weights[-1]["idade_max"], "")
        self.assertLess(abs(sum(Decimal(r["peso_normalizado"]) for r in weights)-1), Decimal("1e-13"))
        for r in weights:
            self.assertLess(abs(Decimal(r["peso_normalizado"])-Decimal(r["percentual_publicado"])/Decimal("100.03")), Decimal("1e-14"))
        cases = {"001": 0, "059": 0, "123": 0, "229": 0, "311": 0,
                 "400": 0, "404": 0, "405": 1, "409": 1, "410": 2,
                 "480": 16, "484": 16, "485": 17, "499": 17, "500": 17,
                 "999": None, "000": None, "060": None, "124": None, "": None}
        for value, expected_band in cases.items():
            with self.subTest(idade=value): self.assertEqual(age_band(value), expected_band)
        # Uma faixa ausente/zero impede a soma; não renormalizar as restantes.
        self.assertTrue(any(ratio(1, p) is None for p in [1, None]))
        self.assertTrue(any(ratio(1, p) is None for p in [1, 0]))

    def test_cid_and_aih_continuation(self):
        m = SPEC["mortalidade"]["causas"]
        self.assertEqual(m, {"cardiovasculares": ["I00-I99"], "respiratorias_cronicas": ["J30-J35", "J37-J98"]})
        for c in ["J30", "j35.9", "J37", "J98"]: self.assertTrue(cause_in(c, m["respiratorias_cronicas"]))
        for c in ["J29", "J36", "J99", "", "999"]: self.assertFalse(cause_in(c, m["respiratorias_cronicas"]))
        self.assertTrue(cause_in("I99", m["cardiovasculares"]))
        h = SPEC["internacoes"]
        self.assertEqual(h["tipo_aih_incluir"], "1")
        self.assertEqual(h["tipo_aih_excluir"], "5")
        self.assertEqual(h["ano"], "ANO_CMPT")
        self.assertEqual(h["grupos"], {"neoplasias": ["C00-C97", "D46"], "diabetes": ["E10-E14"],
                         "hipertensivas": ["I10-I15"], "isquemicas": ["I20-I25"],
                         "cerebrovasculares": ["I60-I69"], "pneumonia": ["J12-J18"]})
        self.assertTrue(cause_in("D46.9", h["grupos"]["neoplasias"]))
        self.assertFalse(cause_in("D45", h["grupos"]["neoplasias"]))
        self.assertFalse(cause_in("J19", h["grupos"]["pneumonia"]))

    def test_local_dates_and_empty_templates(self):
        assessment = date(2026, 10, 6)
        start, end = [assessment-timedelta(days=n) for n in SPEC["coleta_local"]["janela_dias_anteriores"]]
        self.assertEqual((start, end), (date(2026, 9, 29), date(2026, 10, 5)))
        self.assertEqual((end-start).days+1, 7)
        self.assertFalse(start <= assessment <= end)
        self.assertTrue(risk_current(date(2021, 10, 6), assessment))
        self.assertFalse(risk_current(date(2021, 10, 5), assessment))
        self.assertFalse(risk_current(assessment+timedelta(days=1), assessment))
        self.assertTrue(risk_current(date(2019, 2, 28), date(2024, 2, 29)))
        dictionary = (PROTOCOL / "coleta-local.qmd").read_text()
        for name in ["avaliacao-local-modelo.csv", "universo-local-modelo.csv"]:
            rows = list(csv.reader(StringIO((PROTOCOL / name).read_text())))
            self.assertEqual(len(rows), 1, "Modelo deve conter apenas cabeçalho, sem dados fictícios.")
            self.assertEqual(len(rows[0]), len(set(rows[0])))
        header = next(csv.reader(StringIO((PROTOCOL / "avaliacao-local-modelo.csv").read_text())))
        fields = list(SPEC["coleta_local"]["metadados"])
        for group, questions in SPEC["coleta_local"]["grupos"].items():
            fields += list(questions)+[group+"_evidencia"]
        self.assertEqual(header, fields)
        for field in header: self.assertIn("`"+field+"`", dictionary)
        self.assertEqual(len([g for g in SPEC["coleta_local"]["grupos"] if g.startswith("was_")]), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
