#!/usr/bin/env python3
"""
Export bars OHLC ra file CSV.
Chạy: python scripts/export_rates.py [SYMBOL] [TIMEFRAME] [COUNT] [OUTPUT]
Ví dụ: python scripts/export_rates.py EURUSD H4 1000 output.csv
       python scripts/export_rates.py EURUSD H4 1000 --dry-run  # Chỉ mô phỏng, không ghi file
"""
import sys
from datetime import datetime

try:
    import MetaTrader5 as mt5
except ImportError:
    print("Lỗi: Chưa cài MetaTrader5. Chạy: pip install MetaTrader5")
    sys.exit(1)

TIMEFRAMES = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
    "W1": mt5.TIMEFRAME_W1,
    "MN1": mt5.TIMEFRAME_MN1,
}


def main():
    dry_run = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--dry-run"]

    symbol = args[0] if len(args) > 0 else "EURUSD"
    tf_str = (args[1] if len(args) > 1 else "H4").upper()
    count = int(args[2]) if len(args) > 2 else 1000
    output = args[3] if len(args) > 3 else f"{symbol}_{tf_str}.csv"

    if tf_str not in TIMEFRAMES:
        print(f"TIMEFRAME không hợp lệ. Dùng: {list(TIMEFRAMES.keys())}")
        sys.exit(1)
    timeframe = TIMEFRAMES[tf_str]

    if not mt5.initialize():
        print("initialize() thất bại:", mt5.last_error())
        sys.exit(1)

    try:
        if not mt5.symbol_select(symbol, True):
            print(f"Không tìm thấy symbol {symbol}")
            sys.exit(1)

        # Lấy bars gần nhất (date_from=None sẽ lấy từ hiện tại ngược lại)
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None or len(rates) == 0:
            print("Không lấy được dữ liệu:", mt5.last_error())
            sys.exit(1)

        if dry_run:
            print(f"[DRY-RUN] Sẽ export {len(rates)} bars {symbol} {tf_str} -> {output}")
            print(f"  Mẫu: time={rates[0]['time']}, O={rates[0]['open']}, H={rates[0]['high']}, L={rates[0]['low']}, C={rates[0]['close']}")
            return

        # Đảo để thứ tự cũ nhất -> mới nhất (chuẩn cho CSV)
        rates = rates[::-1] if len(rates) > 1 else rates

        with open(output, "w") as f:
            f.write("time,open,high,low,close,tick_volume,spread,real_volume\n")
            for r in rates:
                f.write(f"{r['time']},{r['open']},{r['high']},{r['low']},{r['close']},{r['tick_volume']},{r['spread']},{r['real_volume']}\n")

        print(f"Đã export {len(rates)} bars -> {output}")
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()
