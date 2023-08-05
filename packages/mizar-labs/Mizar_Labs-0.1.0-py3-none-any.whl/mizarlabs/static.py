"""
Static variables that we do not expect to change
"""
import itertools

# Tick data column properties
TIMESTAMP_UNIT = "ms"

# Time bars column names
OPEN = "open"
LOW = "low"
HIGH = "high"
CLOSE = "close"
BASE_ASSET_VOLUME = "base_asset_volume"
BASE_ASSET_BUY_VOLUME = "base_asset_buy_volume"
BASE_ASSET_SELL_VOLUME = "base_asset_sell_volume"
QUOTE_ASSET_VOLUME = "quote_asset_volume"
BUY_QUANTITY = "buy_quantity"
SELL_QUANTITY = "sell_quantity"
BUY_QUOTE_QUANTITY = "buy_quote_quantity"
SELL_QUOTE_QUANTITY = "sell_quote_quantity"

FIRST_TIMESTAMP = "first_timestamp"
TIMESTAMP = "time"  # will be in ms

# Column names for trading
SIZE = "size"
SIDE = "side"
NUMBER_EXPIRATION_BARS_COLUMN = "num_expiration_bars"
EVENT_END_TIME = "event_end_time"
DAILY_VOL = "daily_vol"
STOP_LOSS = "stop_loss"
PROFIT_TAKING = "profit_taking"
RETURN = "return"
LABEL = "label"
T_VALUE = "t_value"

# barrier hit state
EXPIRED = "expired"

# Columns names for strategy trades info
IS_CLOSED = "is_closed"
OPEN_DATETIME = "open_datetime"
CLOSE_DATETIME = "close_datetime"
IS_LONG = "is_long"
OPEN_PRICE = "open_price"
SIGNAL_SIZE = "signal_size"
PROFIT_TAKING_VALUE = "profit_taking_value"
STOP_LOSS_VALUE = "stop_loss_value"
EXPIRATION_DATETIME = "expiration_datetime"
CLOSE_PRICE = "close_price"
EXPIRED = "expired"
DATETIME = "datetime"
DATA = "data"

# slack icons
ALERT_ICON = "https://image.flaticon.com/icons/svg/497/497738.svg"

# redis suffix
CREATOR_SUFFIX = "creator"
BARS_SUFFIX = "bars"
LAST_PUBLISHED_TICK = "last_published_tick"
TICK_SANITISATION_WARMED_UP_CACHE_KEY = "tick_sanitisation_warmed_up"
TICK_SANITISATION_LAST_TIMESTAMP_ALIVE_CACHE_KEY = "tick_sanitisation_last_alive"

LIVE_INGESTION_LAST_TIMESTAMP_ALIVE_CACHE_KEY = "live_ingestion_last_alive"
LIVE_INGESTION_WARMED_UP_CACHE_KEY = "live_ingestion_warmed_up"

INGESTED_STREAMS_CACHE_KEY = "ingested_streams"
SANITISED_STREAMS_CACHE_KEY = "sanitised_streams"

# pubsub suffix
BINANCE_INGESTED = "binance_ingested"

# bars and transformers
BAR_TYPES = [
    {
        "bar_transformer_class": bar_transformer_class,
        "bar_transformer_subclass": bar_transformer_subclass,
    }
    for (bar_transformer_class, bar_transformer_subclass) in (
            list(itertools.product(["run"], ["volume", "dollar", "tick"]))
            + list(itertools.product(["volume", "dollar", "tick"], ["dynamic"]))
    )
]

WINDOW_THRESHOLD_CALCULATION = 30
# the fraction below is used for tick, volume and dollar
FRACTION_OF_DAILY_AVERAGE = 1 / 50


