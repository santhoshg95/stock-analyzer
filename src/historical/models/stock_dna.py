"""Backward-compatible name for the stock behavioural profile model."""

from .stock_dna_model import StockDNAModel


# HistoricalEngine was written against this public name.  Keeping the alias
# avoids two competing models and restores the historical-analysis path.
StockDNA = StockDNAModel
