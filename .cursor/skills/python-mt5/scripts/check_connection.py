#!/usr/bin/env python3
"""
Kiểm tra kết nối MetaTrader 5.
Chạy: python scripts/check_connection.py
"""
import sys

try:
    import MetaTrader5 as mt5
except ImportError:
    print("Lỗi: Chưa cài MetaTrader5. Chạy: pip install MetaTrader5")
    sys.exit(1)


def main():
    if not mt5.initialize():
        err = mt5.last_error()
        print(f"initialize() thất bại: code={err[0]}, message={err[1]}")
        sys.exit(1)

    try:
        info = mt5.terminal_info()
        acc = mt5.account_info()
        ver = mt5.version()
        print("Kết nối thành công")
        print(f"  Terminal: {info.path if info else 'N/A'}")
        print(f"  Phiên bản: {ver}")
        print(f"  Tài khoản: {acc.login if acc else 'N/A'}")
        print(f"  Server: {acc.server if acc else 'N/A'}")
        print(f"  Balance: {acc.balance if acc else 0} {acc.currency if acc else ''}")
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()
