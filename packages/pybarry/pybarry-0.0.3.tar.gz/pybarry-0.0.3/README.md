# pybarry 
Python3 library for [Barry](https://barry.energy/dk).

Get electricity consumption price.

## Install
```
pip3 install pybarry
```

## Example:

```python
from pybarry import Barry
access_token = '<your barry token>'
barry_connection = Barry(access_token=access_token)
latest_price = barry_connection.update_price_data()
print(latest_price)
```