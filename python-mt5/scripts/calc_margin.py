#!/usr/bin/env python3
"""
Tính margin cần thiết cho lệnh.
Chạy: python scripts/calc_margin.py [SYMBOL] [LOT]
Ví dụ: python scripts/calc_margin.py EURUSD 0.1
"""
import sys

try:
    import MetaTrader5 as mt5
except ImportError:
    print("Lỗi: Chưa cài MetaTrader5. Chạy: pip install MetaTrader5")
    sys.exit(1)


def main():
    symbol = sys.argv[1] if len(sys.argv) > 1 else "EURUSD"
    try:
        lot = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    except ValueError:
        print("LOT phải là số (ví dụ: 0.1)")
        sys.exit(1)

    if not mt5.initialize():
        print("initialize() thất bại:", mt5.last_error())
        sys.exit(1)

    try:
        if not mt5.symbol_select(symbol, True):
            print(f"Không tìm thấy symbol {symbol}")
            sys.exit(1)

        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            print(f"Không lấy được giá {symbol}")
            sys.exit(1)

        account = mt5.account_info()
        margin_buy = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, lot, tick.ask)
        margin_sell = mt5.order_calc_margin(mt5.ORDER_TYPE_SELL, symbol, lot, tick.bid)

        if margin_buy is None or margin_sell is None:
            print("order_calc_margin thất bại:", mt5.last_error())
            sys.exit(1)

        currency = account.currency if account else "USD"
        print(f"{symbol} {lot} lot")
        print(f"  Buy margin:  {margin_buy:.2f} {currency}")
        print(f"  Sell margin: {margin_sell:.2f} {currency}")
        print(f"  Margin free: {account.margin_free:.2f} {currency}")
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()
