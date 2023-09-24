from ChartInk import ChartInk as ci
import pandas as pd
# Instantiate a ChartInk object

# Get the stocks that match the conditions
cond = "( {cash} ( latest ema ( latest close , 21 ) >= latest ema ( latest close , 50 ) and latest ema ( close,10 ) / latest ema ( close,21 ) <= 1.03 and latest ema ( close,10 ) / latest ema ( close,21 ) > 1 and latest ema ( close,21 ) / latest ema ( close,30 ) <= 1.03 and latest ema ( close,21 ) / latest ema ( close,30 ) > 1 and latest ema ( close,30 ) / latest ema ( close,50 ) <= 1.03 and latest ema ( close,30 ) / latest ema ( close,50 ) > 1 and latest close >= weekly max ( 52 , weekly high ) * 0.75 and latest close >= weekly max ( 52 , weekly low ) * 1 and latest close > 30 and latest sma ( latest volume , 50 ) > 10000 and market cap >= 1000 and latest close > 30 and latest ema ( latest close , 10 ) > latest ema ( latest close , 21 ) and latest ema ( latest close , 21 ) > latest ema ( latest close , 50 ) and latest ema ( latest close , 50 ) > latest ema ( latest close , 100 ) and latest close > latest ema ( latest close , 50 ) and 1 quarter ago foreign institutional investors percentage >= 2 quarter ago foreign institutional investors percentage and quarterly foreign institutional investors percentage >= 1 quarter ago foreign institutional investors percentage and quarterly indian public percentage <= 1 quarter ago indian public percentage and 1 quarter ago indian public percentage <= 2 quarter ago indian public percentage and weekly ema ( weekly close , 50 ) >= weekly ema ( weekly close , 100 ) and 2 quarter ago indian public percentage <= 3 quarter ago indian public percentage ) ) "
df = pd.DataFrame(ci.get_stocks(cond=cond))

df.to_csv("try1.csv")