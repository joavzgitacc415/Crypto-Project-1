### Library and global var declarations ###
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/candles")
TIME_COL = "timestamp"

def candles_to_dataframe(raw: list[list[float]]) -> pd.DataFrame:        # Joaquin
    """[[timestamp_ms, open, high, low, close, volume], ...] -> DataFrame indexed by
    UTC datetime, columns open/high/low/close/volume as floats."""


def fetch_ohlcv(symbol="BTC/USD", timeframe="1d", exchange_id="kraken"):  # Joaquin
    """Network call via CCXT, then candles_to_dataframe(). Drops the still-forming candle."""

def _candles_path(symbol: str, timeframe: str) -> Path:
    safe_symbol = symbol.replace("/", "-").replace(":", "-")
    return DATA_DIR / f"{safe_symbol}_{timeframe}.csv"

def _read_cache(path: Path) -> pd.DataFrame:
    candles = pd.read_csv(path, index_col = TIME_COL)
    candles.index = pd.to_datetime(candles.index, utc = True)
    return candles

def save_candles(df: pd.DataFrame, symbol: str, timeframe: str) -> None:     # Cesar

    if df.empty:
        return

    candles = df if TIME_COL in df.columns else df.reset_index()
    if not isinstance(df.index, pd.DatetimeIndex) or df.index.tz is None:
        raise ValueError("df needs a UTC DatetimeIndex (Check candles_to_dataframe)") 

    path = _candles_path(symbol, timeframe)   
    path.parent.mkdir(parents=True, exist_ok=True)  

    candles = pd.concat([_read_cache(path), df]) if path.exists() else df
    candles = candles[~candles.index.duplicated(keep="last")].sort_index()

    tmp_path = path.with_name(path.name + ".tmp")
    candles.to_csv(tmp_path, index_label=TIME_COL)
    tmp_path.replace(path)

def load_candles(symbol, timeframe, start=None, end=None) -> pd.DataFrame:  #Joaquin
    pass

def get_candles(symbol, timeframe="1d", refresh=False) -> pd.DataFrame:     # Cesar
    """Serve from the cache; download only when missing, stale, or refresh=True."""
    if refresh or _needs_download(symbol, timeframe):
        save_candles(fetch_ohlcv(symbol, timeframe), symbol, timeframe)
    return load_candles(symbol, timeframe)

def _needs_download(symbol: str, timeframe: str) -> bool:
    path = _candles_path(symbol, timeframe)
    if not path.exists():
        return True

    period = pd.Timedelta(seconds=ccxt.Exchange.parse_timeframe(timeframe))
    last_open = _read_cache(path).index.max()
    return pd.Timestamp.now(tz="UTC") >= last_open + 2 * period