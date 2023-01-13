from py_topping.general_use import lazy_LINE

# Create Class
# Pelayanan Umum Token
# token = 'obhJ7x4aa7tsDJ8awbUckLGNLRaLwi8TF5F3BznFZfU'
# Perki Aachen Token
token = 'tR5VANICCGGEcH2Vg9zj8CacFUxxdSORvp1OZPveapV'
# Mita Token
# token = '6iveKXRAOsMumXqa2U1kfDKBmcqlTHDKLOYJfG8e12L'
line = lazy_LINE(token=token)

# Send message
# line.send('',
#           notification=True)

import datetime

print(datetime.datetime.now().hour)

hour = datetime.datetime(2022, 10, 20, 23, 10, 00).hour
if 0 <= hour < 11:
    greeting = 'pagi'
elif 11 <= hour <= 15:
    greeting = 'siang'
elif 15 < hour < 18:
    greeting = 'sore'
else:
    greeting = 'malam'

print(greeting)