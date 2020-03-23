import os
from tools.alpha_vantage import AlphaVantage
from backtesting.backtest import Backtester
from financial_assets.financial_assets import Stock
from backtesting.portfolio import Portfolio
from backtesting.broker.brokers import InteractiveBrokers
from strategy.sma_crossover import AverageCrossOver
from datetime import datetime

portfolio = Portfolio(500, "USD")
ib = InteractiveBrokers()
alpha_vantage = AlphaVantage(os.environ['AlphaVantage_APItoken'])
sma_strategy = AverageCrossOver("SMA crossover", short=20, long=50)


# Equinor stocks
equinor = Stock("Equinor Energy", "EQNR", "USD")
equinor_bars = alpha_vantage.query_stocks("TIME_SERIES_DAILY", "EQNR", ascending=True, outputsize="full")
exxon_bars = alpha_vantage.query_stocks("TIME_SERIES_DAILY", "XON", ascending=True, outputsize="full")

equinor.set_bars(equinor_bars)
equinor.add_data_object("exxon_bars", exxon_bars)
sma_strategy.link(equinor)

backtester = Backtester(portfolio, ib, [equinor], [sma_strategy], "daily", run_to=datetime(2020, 1, 1))
backtester.run()