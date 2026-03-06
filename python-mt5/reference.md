# Python MetaTrader 5 - API Reference

## Bảng hàm API

### Kết nối

| Hàm | Tham số | Trả về | Ghi chú |
|-----|---------|--------|---------|
| `initialize()` | `path`, `login`, `password`, `server`, `timeout`, `portable` | bool | Kết nối terminal, timeout mặc định 60000ms |
| `login(login, password, server)` | Số tài khoản, mật khẩu, tên server | bool | Đăng nhập tài khoản |
| `shutdown()` | - | None | Đóng kết nối |
| `version()` | - | tuple | (major, minor, build) |
| `last_error()` | - | tuple | (code, message) |

### Thông tin

| Hàm | Tham số | Trả về | Ghi chú |
|-----|---------|--------|---------|
| `account_info()` | - | namedtuple | balance, currency, leverage, margin, profit... |
| `terminal_info()` | - | namedtuple | connected, trade_allowed, path... |

### Symbol

| Hàm | Tham số | Trả về | Ghi chú |
|-----|---------|--------|---------|
| `symbols_total()` | - | int | Tổng số symbol |
| `symbols_get()` | - | tuple | Danh sách symbol |
| `symbol_info(symbol)` | symbol | namedtuple/None | point, digits, volume_min, visible... |
| `symbol_info_tick(symbol)` | symbol | namedtuple/None | bid, ask, last, volume, time |
| `symbol_select(symbol, enable)` | symbol, bool | bool | Thêm/xóa khỏi MarketWatch |

### Market Depth

| Hàm | Tham số | Trả về | Ghi chú |
|-----|---------|--------|---------|
| `market_book_add(symbol)` | symbol | bool | Đăng ký nhận Market Depth |
| `market_book_get(symbol)` | symbol | tuple | BookInfo entries |
| `market_book_release(symbol)` | symbol | bool | Hủy đăng ký |

### Bars (OHLC)

| Hàm | Tham số | Trả về | Ghi chú |
|-----|---------|--------|---------|
| `copy_rates_from(symbol, timeframe, date_from, count)` | symbol, timeframe, datetime, int | numpy array/None | Bars từ ngày |
| `copy_rates_from_pos(symbol, timeframe, start_pos, count)` | symbol, timeframe, int, int | numpy array/None | Bars từ index |
| `copy_rates_range(symbol, timeframe, date_from, date_to)` | symbol, timeframe, datetime, datetime | numpy array/None | Bars trong khoảng |

### Ticks

| Hàm | Tham số | Trả về | Ghi chú |
|-----|---------|--------|---------|
| `copy_ticks_from(symbol, date_from, count, flags)` | symbol, datetime, int, COPY_TICKS | numpy array/None | Ticks từ ngày |
| `copy_ticks_range(symbol, date_from, date_to, flags)` | symbol, datetime, datetime, COPY_TICKS | numpy array/None | Ticks trong khoảng |

### Giao dịch

| Hàm | Tham số | Trả về | Ghi chú |
|-----|---------|--------|---------|
| `order_check(request)` | dict | MqlTradeCheckResult | Kiểm tra trước khi gửi |
| `order_send(request)` | dict | MqlTradeResult | Gửi lệnh |
| `order_calc_margin(type, symbol, volume, price)` | ORDER_TYPE, symbol, volume, price | float | Tính margin |
| `order_calc_profit(type, symbol, volume, price_open, price_close)` | ... | float | Tính lợi nhuận |

### Orders & Positions

| Hàm | Tham số | Trả về | Ghi chú |
|-----|---------|--------|---------|
| `orders_total()` | - | int | Số lệnh chờ |
| `orders_get(symbol="...", ticket=...)` | symbol hoặc ticket | tuple | Lệnh chờ |
| `positions_total()` | - | int | Số vị thế |
| `positions_get(symbol="...", group="...", ticket=...)` | symbol/group/ticket | tuple | Vị thế mở |

### Lịch sử

| Hàm | Tham số | Trả về | Ghi chú |
|-----|---------|--------|---------|
| `history_orders_total(from_date, to_date)` | datetime, datetime | int | Số lệnh trong khoảng |
| `history_orders_get(from_date, to_date, group="...", ticket=..., position=...)` | ... | tuple | Lệnh lịch sử |
| `history_deals_total(from_date, to_date)` | datetime, datetime | int | Số deal |
| `history_deals_get(from_date, to_date, group="...", ticket=..., position=...)` | ... | tuple | Deals |

---

## Enumerations

### TIMEFRAME

| Hằng số | Mô tả |
|---------|-------|
| TIMEFRAME_M1 | 1 phút |
| TIMEFRAME_M2, M3, M4, M5, M6, M10, M12, M15, M20, M30 | 2–30 phút |
| TIMEFRAME_H1, H2, H3, H4, H6, H8, H12 | 1–12 giờ |
| TIMEFRAME_D1 | 1 ngày |
| TIMEFRAME_W1 | 1 tuần |
| TIMEFRAME_MN1 | 1 tháng |

### TRADE_ACTION_*

| Hằng số | Mô tả |
|---------|-------|
| TRADE_ACTION_DEAL | Lệnh thị trường (mở/đóng ngay) |
| TRADE_ACTION_PENDING | Đặt lệnh chờ |
| TRADE_ACTION_SLTP | Sửa SL/TP vị thế |
| TRADE_ACTION_MODIFY | Sửa lệnh chờ |
| TRADE_ACTION_REMOVE | Xóa lệnh chờ |
| TRADE_ACTION_CLOSE_BY | Đóng bằng vị thế ngược chiều |

### ORDER_TYPE_*

| Hằng số | Mô tả |
|---------|-------|
| ORDER_TYPE_BUY | Mua thị trường |
| ORDER_TYPE_SELL | Bán thị trường |
| ORDER_TYPE_BUY_LIMIT | Lệnh mua giới hạn |
| ORDER_TYPE_SELL_LIMIT | Lệnh bán giới hạn |
| ORDER_TYPE_BUY_STOP | Lệnh mua dừng |
| ORDER_TYPE_SELL_STOP | Lệnh bán dừng |
| ORDER_TYPE_BUY_STOP_LIMIT | Mua dừng giới hạn |
| ORDER_TYPE_SELL_STOP_LIMIT | Bán dừng giới hạn |

### ORDER_TYPE_FILLING

| Hằng số | Mô tả |
|---------|-------|
| ORDER_FILLING_FOK | Fill or Kill - toàn bộ hoặc hủy |
| ORDER_FILLING_IOC | Immediate or Cancel - phần có sẵn |
| ORDER_FILLING_RETURN | Return - chấp nhận khớp một phần |

### ORDER_TYPE_TIME

| Hằng số | Mô tả |
|---------|-------|
| ORDER_TIME_GTC | Good till Cancel |
| ORDER_TIME_DAY | Chỉ trong ngày |
| ORDER_TIME_SPECIFIED | Đến thời điểm cụ thể |
| ORDER_TIME_SPECIFIED_DAY | Đến cuối ngày chỉ định |

### COPY_TICKS

| Hằng số | Mô tả |
|---------|-------|
| COPY_TICKS_ALL | Tất cả ticks |
| COPY_TICKS_INFO | Bid/Ask thay đổi |
| COPY_TICKS_TRADE | Last/Volume thay đổi |

### TRADE_RETCODE_DONE

`10009` = lệnh thực thi thành công.

---

## Cấu trúc MqlTradeRequest (dict)

| Trường | Kiểu | Bắt buộc khi | Mô tả |
|--------|------|--------------|-------|
| action | int | Luôn | TRADE_ACTION_* |
| symbol | str | Mở/đóng | Tên symbol |
| volume | float | Mở/đóng | Khối lượng (lots) |
| type | int | Mở | ORDER_TYPE_* |
| price | float | Mở (Instant/Request) | Giá |
| sl | float | Tùy chọn | Stop Loss |
| tp | float | Tùy chọn | Take Profit |
| deviation | int | Mở (Instant/Request) | Độ lệch (points) |
| magic | int | Tùy chọn | Magic number |
| comment | str | Tùy chọn | Ghi chú |
| type_filling | int | Mở | ORDER_FILLING_* |
| type_time | int | Tùy chọn | ORDER_TIME_* |
| expiration | datetime | type_time=SPECIFIED | Thời hạn |
| position | int | Đóng/Sửa SLTP | Ticket vị thế |
| position_by | int | CLOSE_BY | Ticket vị thế đối |
| order | int | Sửa/Xóa | Ticket lệnh chờ |
| stoplimit | float | Stop Limit | Giá limit |

**Trường bắt buộc theo loại:**

- **Market Execution (mở):** action, symbol, volume, type, type_filling
- **Instant/Request (mở):** + price, deviation, sl, tp (tùy)
- **Đóng vị thế:** action=DEAL, position, symbol, volume, type (ngược), price, deviation
- **SLTP:** action=SLTP, position, symbol, sl, tp
- **Pending:** action=PENDING, symbol, volume, type, price, type_filling, type_time
- **Modify pending:** action=MODIFY, order, price, sl, tp, deviation, type_time, expiration
- **Remove:** action=REMOVE, order
- **Close by:** action=CLOSE_BY, position, position_by

---

## Cấu trúc dữ liệu bars (numpy)

| Cột | Mô tả |
|-----|-------|
| time | Unix timestamp (seconds) |
| open | Giá mở |
| high | Giá cao nhất |
| low | Giá thấp nhất |
| close | Giá đóng |
| tick_volume | Khối lượng tick |
| spread | Spread |
| real_volume | Khối lượng thực |

---

## Cấu trúc ticks (numpy)

| Cột | Mô tả |
|-----|-------|
| time | Unix timestamp (seconds) |
| bid | Giá bid |
| ask | Giá ask |
| last | Giá last |
| volume | Khối lượng |
| time_msc | Milliseconds |
| flags | TICK_FLAG_* |
| volume_real | Khối lượng thực |

---

## Cấu trúc BookInfo (Market Depth)

| Trường | Mô tả |
|--------|-------|
| type | 1=Bid, 2=Ask |
| price | Giá |
| volume | Khối lượng (lots) |
| volume_dbl | Khối lượng (double) |

**Lưu ý:** Gọi `market_book_add(symbol)` trước `market_book_get()`, sau đó `market_book_release(symbol)` khi xong.

---

## Mã lỗi last_error()

| Code | Hằng số | Mô tả |
|------|---------|-------|
| 1 | RES_S_OK | Thành công |
| -1 | RES_E_FAIL | Lỗi chung |
| -2 | RES_E_INVALID_PARAMS | Tham số không hợp lệ |
| -3 | RES_E_NO_MEMORY | Thiếu bộ nhớ |
| -4 | RES_E_NOT_FOUND | Không tìm thấy (history) |
| -5 | RES_E_INVALID_VERSION | Phiên bản không hợp lệ |
| -6 | RES_E_AUTH_FAILED | Xác thực thất bại |
| -7 | RES_E_UNSUPPORTED | Phương thức không hỗ trợ |
| -8 | RES_E_AUTO_TRADING_DISABLED | Auto-trading tắt |
| -10000 | RES_E_INTERNAL_FAIL | Lỗi IPC chung |
| -10001 | RES_E_INTERNAL_FAIL_SEND | Gửi IPC thất bại |
| -10002 | RES_E_INTERNAL_FAIL_RECEIVE | Nhận IPC thất bại |
| -10003 | RES_E_INTERNAL_FAIL_INIT/CONNECT | Khởi tạo/kết nối IPC |
| -10005 | RES_E_INTERNAL_FAIL_TIMEOUT | Timeout |
