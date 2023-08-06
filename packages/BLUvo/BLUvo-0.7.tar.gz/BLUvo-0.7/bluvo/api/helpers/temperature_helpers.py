import decimal
from itertools import islice


def float_range(start, stop, step):
  while start <= stop:
    yield decimal.Decimal(start)
    start += decimal.Decimal(step)


def temp_code_to_celsius(code: str) -> decimal.Decimal:
    if code:
        hex_temp_index = code[0:2]
        temp_range = float_range(14, 30, 0.5)
        temp_index = int(hex_temp_index, 16)

        return next(islice(temp_range, temp_index, None))
    else:
        return decimal.Decimal(0.0)


def celsius_to_temp_code(temp: decimal.Decimal) -> str:
    temp_range = list(float_range(14, 30, 0.5))
    temp_index = temp_range.index(temp)
    return hex(temp_index).split('x')[-1].upper() + "H"
