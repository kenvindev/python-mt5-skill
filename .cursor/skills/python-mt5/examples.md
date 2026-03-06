# Python MetaTrader 5 - Mẫu code

## Script tiện ích

Chạy từ thư mục project:

```bash
python .cursor/skills/python-mt5/scripts/check_connection.py
python .cursor/skills/python-mt5/scripts/calc_margin.py EURUSD 0.1
python .cursor/skills/python-mt5/scripts/export_rates.py EURUSD H4 1000 output.csv
python .cursor/skills/python-mt5/scripts/export_rates.py EURUSD H4 1000 --dry-run
```

---

## 1. Kết nối cơ bản

```python
import MetaTrader5 as mt5

# Kết nối (tự tìm terminal)
if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

# Kiểm tra kết nối
print("Terminal:", mt5.terminal_info())
print("Phiên bản:", mt5.version())
print("Tài khoản:", mt5.account_info().login)

# Luôn gọi shutdown khi kết thúc
mt5.shutdown()
```

---

## 2. Lấy bars OHLC

```python
from datetime import datetime
import pytz
import pandas as pd
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

# Dùng UTC để tránh lệch múi giờ
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2020, 1, 10, tzinfo=timezone)

# Lấy 100 nến H4 EURUSD từ 10/01/2020
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H4, utc_from, 100)
mt5.shutdown()

if rates is None:
    print("Không lấy được dữ liệu:", mt5.last_error())
else:
    # Chuyển sang DataFrame
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    print(df[["time", "open", "high", "low", "close"]].head())
```

---

## 3. Lấy ticks

```python
from datetime import datetime
import pytz
import pandas as pd
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2020, 1, 10, tzinfo=timezone)

# Lấy 1000 ticks EURUSD
ticks = mt5.copy_ticks_from("EURUSD", utc_from, 1000, mt5.COPY_TICKS_ALL)
mt5.shutdown()

if ticks is not None:
    df = pd.DataFrame(ticks)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    print(df[["time", "bid", "ask", "volume"]].head(10))
```

---

## 4. Mở lệnh market Buy

```python
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

symbol = "USDJPY"
lot = 0.1

# Kiểm tra symbol có sẵn
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(f"{symbol} không tìm thấy")
    mt5.shutdown()
    quit()

if not symbol_info.visible:
    mt5.symbol_select(symbol, True)

point = symbol_info.point
price = mt5.symbol_info_tick(symbol).ask

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,
    "tp": price + 100 * point,
    "deviation": 20,
    "magic": 234000,
    "comment": "python script",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}

# Kiểm tra trước khi gửi
check = mt5.order_check(request)
if check.retcode != 0:
    print("order_check thất bại:", check)
    mt5.shutdown()
    quit()

# Gửi lệnh
result = mt5.order_send(request)
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("order_send thất bại:", result.retcode, result.comment)
else:
    print("Mở vị thế thành công, ticket:", result.order)

mt5.shutdown()
```

---

## 5. Đóng vị thế

```python
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

symbol = "USDJPY"

# Lấy vị thế theo symbol
positions = mt5.positions_get(symbol=symbol)
if positions is None or len(positions) == 0:
    print("Không có vị thế", symbol)
    mt5.shutdown()
    quit()

# Đóng từng vị thế
for pos in positions:
    # Xác định type đóng (ngược với type mở)
    close_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
    price = mt5.symbol_info_tick(symbol).bid if close_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": pos.volume,
        "type": close_type,
        "position": pos.ticket,
        "price": price,
        "deviation": 20,
        "magic": pos.magic,
        "comment": "python close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print("Đóng vị thế", pos.ticket, "thành công")
    else:
        print("Đóng thất bại:", result.retcode, result.comment)

mt5.shutdown()
```

---

## 6. Đặt lệnh chờ (Buy Limit)

```python
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

symbol = "EURUSD"
lot = 0.1
offset_points = 50  # Cách giá hiện tại 50 points

symbol_info = mt5.symbol_info(symbol)
if symbol_info is None or not symbol_info.visible:
    mt5.symbol_select(symbol, True)

point = symbol_info.point
digits = symbol_info.digits
ask = mt5.symbol_info_tick(symbol).ask

# Buy Limit: giá đặt thấp hơn ask
price = round(ask - offset_points * point, digits)

request = {
    "action": mt5.TRADE_ACTION_PENDING,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY_LIMIT,
    "price": price,
    "deviation": 10,
    "magic": 234000,
    "comment": "python pending",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}

result = mt5.order_send(request)
if result.retcode == mt5.TRADE_RETCODE_DONE:
    print("Đặt lệnh chờ thành công, ticket:", result.order)
else:
    print("Thất bại:", result.retcode, result.comment)

mt5.shutdown()
```

---

## 7. Sửa SL/TP của vị thế

```python
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

symbol = "EURUSD"
position_ticket = 123456789  # Thay bằng ticket thực tế

positions = mt5.positions_get(ticket=position_ticket)
if positions is None or len(positions) == 0:
    print("Không tìm thấy vị thế")
    mt5.shutdown()
    quit()

pos = positions[0]
symbol_info = mt5.symbol_info(pos.symbol)
point = symbol_info.point
digits = symbol_info.digits

# Tính SL/TP mới (ví dụ: ±50 points từ giá mở)
new_sl = round(pos.price_open - 50 * point, digits)
new_tp = round(pos.price_open + 50 * point, digits)

request = {
    "action": mt5.TRADE_ACTION_SLTP,
    "symbol": pos.symbol,
    "position": position_ticket,
    "sl": new_sl,
    "tp": new_tp,
}

result = mt5.order_send(request)
if result.retcode == mt5.TRADE_RETCODE_DONE:
    print("Sửa SL/TP thành công")
else:
    print("Thất bại:", result.retcode, result.comment)

mt5.shutdown()
```

---

## 8. Lấy lịch sử orders và deals

```python
from datetime import datetime, timedelta
import pytz
import pandas as pd
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

timezone = pytz.timezone("Etc/UTC")
to_date = datetime.now(timezone)
from_date = to_date - timedelta(days=7)

# Lịch sử orders
orders = mt5.history_orders_get(from_date, to_date)
if orders is not None:
    df_orders = pd.DataFrame([o._asdict() for o in orders])
    df_orders["time"] = pd.to_datetime(df_orders["time"], unit="s")
    print("Orders:", len(df_orders))
    print(df_orders[["ticket", "symbol", "volume", "price_open", "time"]].head())
else:
    print("Không có orders:", mt5.last_error())

# Lịch sử deals
deals = mt5.history_deals_get(from_date, to_date)
if deals is not None:
    df_deals = pd.DataFrame([d._asdict() for d in deals])
    df_deals["time"] = pd.to_datetime(df_deals["time"], unit="s")
    print("Deals:", len(df_deals))
    print(df_deals[["ticket", "symbol", "volume", "price", "profit", "time"]].head())
else:
    print("Không có deals:", mt5.last_error())

mt5.shutdown()
```

---

## 9. Market Depth (Depth of Market)

```python
import time
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

symbol = "EURUSD"

# Đăng ký nhận Market Depth - bắt buộc trước khi gọi market_book_get
if not mt5.market_book_add(symbol):
    print(f"market_book_add({symbol}) thất bại:", mt5.last_error())
    mt5.shutdown()
    quit()

try:
    # Lấy nội dung Market Depth
    items = mt5.market_book_get(symbol)
    if items:
        # type=1: Bid, type=2: Ask
        for it in items:
            side = "BID" if it.type == 1 else "ASK"
            print(f"  {side} | price={it.price:.5f} | volume={it.volume_dbl}")
    else:
        print("Không có dữ liệu DOM (một số symbol không hỗ trợ)")
finally:
    # Luôn hủy đăng ký khi xong
    mt5.market_book_release(symbol)

mt5.shutdown()
```

**Lưu ý:** DOM chỉ có sẵn cho một số symbol. Luôn gọi `market_book_release()` sau khi dùng xong.

---

## 10. Tính margin với order_calc_margin

```python
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

symbol = "EURUSD"
lot = 0.1
account = mt5.account_info()

# Lấy giá hiện tại
tick = mt5.symbol_info_tick(symbol)
if tick is None:
    print(f"Không lấy được tick {symbol}")
    mt5.shutdown()
    quit()

# Tính margin cho lệnh Buy 0.1 lot
margin_buy = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, lot, tick.ask)
margin_sell = mt5.order_calc_margin(mt5.ORDER_TYPE_SELL, symbol, lot, tick.bid)

if margin_buy is not None and margin_sell is not None:
    print(f"{symbol} {lot} lot - Buy margin: {margin_buy:.2f} {account.currency}")
    print(f"{symbol} {lot} lot - Sell margin: {margin_sell:.2f} {account.currency}")
    print(f"Margin free: {account.margin_free:.2f} {account.currency}")
else:
    print("order_calc_margin thất bại:", mt5.last_error())

mt5.shutdown()
```

---

## 11. Tính lợi nhuận với order_calc_profit

```python
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() thất bại:", mt5.last_error())
    quit()

symbol = "EURUSD"
lot = 0.1
price_open = 1.1000
price_close = 1.1050  # Giá đóng giả định

# Lợi nhuận nếu mua 0.1 lot ở 1.10 và bán ở 1.105
profit_buy = mt5.order_calc_profit(
    mt5.ORDER_TYPE_BUY, symbol, lot, price_open, price_close
)
# Lợi nhuận nếu bán 0.1 lot ở 1.10 và mua lại ở 1.105 (lỗ)
profit_sell = mt5.order_calc_profit(
    mt5.ORDER_TYPE_SELL, symbol, lot, price_open, price_close
)

if profit_buy is not None:
    account = mt5.account_info()
    print(f"Buy 0.1 @ {price_open} -> close @ {price_close}: {profit_buy:.2f} {account.currency}")
    print(f"Sell 0.1 @ {price_open} -> close @ {price_close}: {profit_sell:.2f} {account.currency}")

mt5.shutdown()
```
