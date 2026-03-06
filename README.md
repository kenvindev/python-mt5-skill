# Python MetaTrader 5 – Agent Skill

Agent Skill hướng dẫn tích hợp Python với MetaTrader 5: kết nối terminal, lấy dữ liệu OHLC/ticks, gửi lệnh, quản lý vị thế. Dùng khi làm việc với MetaTrader5, MT5, giao dịch thuật toán, backtest hoặc automation trading.

---

## Cài đặt

```bash
pip install MetaTrader5
```

**Yêu cầu:** MetaTrader 5 terminal đã cài và chạy trên máy.

---

## Scripts tiện ích

Chạy từ thư mục gốc project:

| Script | Mô tả | Ví dụ |
|--------|-------|-------|
| `check_connection.py` | Kiểm tra kết nối MT5 | `python scripts/check_connection.py` |
| `calc_margin.py` | Tính margin cho symbol/lot | `python scripts/calc_margin.py EURUSD 0.1` |
| `export_rates.py` | Export bars OHLC ra CSV | `python scripts/export_rates.py EURUSD H4 1000 out.csv` |

`export_rates.py` hỗ trợ `--dry-run` để mô phỏng không ghi file.

---

## Luồng cơ bản

1. `initialize()` để kết nối terminal
2. Thực hiện thao tác (lấy dữ liệu, giao dịch)
3. `shutdown()` khi kết thúc

**Kiểm tra lỗi:** Gọi `last_error()` sau mỗi thao tác thất bại (trả về tuple `(code, message)`).

---

## Tài liệu

| File | Nội dung |
|------|----------|
| [SKILL.md](SKILL.md) | Hướng dẫn chi tiết: connection, market data, trading, positions, error handling |
| [examples.md](examples.md) | Mẫu code: kết nối, OHLC, ticks, mở/đóng lệnh, sửa SL/TP |
| [reference.md](reference.md) | API, constants, structures |

---

## Cấu trúc thư mục

```
python-mt5/
├── README.md
├── SKILL.md
├── examples.md
├── reference.md
└── scripts/
    ├── check_connection.py
    ├── calc_margin.py
    └── export_rates.py
```
