import unittest

from src.sector.sector_mapper import SectorMapper


class SectorClassificationTests(unittest.TestCase):
    def test_financial_services_symbol_is_classified(self):
        self.assertEqual(SectorMapper().get_sector("360ONE.NS"), "FINANCIAL_SERVICES")

    def test_unmapped_symbol_never_displays_unknown(self):
        self.assertEqual(SectorMapper().get_sector("NEWFOSYMBOL"), "DIVERSIFIED")
