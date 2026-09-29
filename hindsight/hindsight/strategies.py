import pandas as pd

def candles_to_dataframe(raw: list[list[float]]) -> pd.DataFrame:        # Joaquin
    """[[timestamp_ms, open, high, low, close, volume], ...] -> DataFrame indexed by
    UTC datetime, columns open/high/low/close/volume as floats."""


def fetch_ohlcv(symbol="BTC/USD", timeframe="1d", exchange_id="kraken"):  # Joaquin
    """Network call via CCXT, then candles_to_dataframe(). Drops the still-forming candle."""


def save_candles(df, symbol, timeframe) -> None:     # Cesar
    pass               

def load_candles(symbol, timeframe, start=None, end=None) -> pd.DataFrame:  #Joaquin
    pass

def get_candles(symbol, timeframe="1d", refresh=False) -> pd.DataFrame:     # Cesar
    """Serve from the cache; download only when missing, stale, or refresh=True."""