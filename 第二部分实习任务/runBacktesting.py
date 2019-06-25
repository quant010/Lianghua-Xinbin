"""
展示如何执行策略回测。
"""
from vnpy.trader.app.ctaStrategy import BacktestingEngine
import pandas as pd
from vnpy.trader.utils import htmlplot
import json
import os
from Strategy import Strategy

# 
if __name__ == '__main__':
    # 创建回测引擎
    engine = BacktestingEngine()
    engine.setDB_URI("mongodb://localhost:27017")

    # Bar回测
    engine.setBacktestingMode(engine.BAR_MODE)
    engine.setDatabase('VnTrader_1Min_Db')

    # Tick回测
    # engine.setBacktestingMode(engine.TICK_MODE)
    # engine.setDatabase('VnTrader_1Min_Db', 'VnTrader_Tick_Db')

    # 设置回测用的数据起始日期，initHours 默认值为 0
    engine.setStartDate('20160603 10:00:00',initHours=10)
    # engine.setStartDate('20180202 10:00:00',initHours=10)
    # engine.setStartDate('20181130 10:00:00',initHours=10)
<<<<<<< HEAD
    engine.setEndDate('20170225 23:00:00')
=======
    engine.setEndDate('20190225 23:00:00')
>>>>>>> 32bc7ca3246ff40d1b12bb96aeaf5e592b2a8b0e

    # 设置产品相关参数
    engine.setCapital(10000000)  # 设置起始资金，默认值是1,000,000
    contracts = [{
                    "symbol":"J88:CTP",
                    "size" : 1, # 每点价值
                    "priceTick" : 1, # 最小价格变动
                    "rate" : 0.7/10000, # 单边手续费
                    "slippage" : 0 # 滑价
                    },] 

    engine.setContracts(contracts)
    engine.setLog(True, "./logJ88")
    # 获取当前绝对路径
    
    path = os.path.split(os.path.realpath(__file__))[0]
    with open(path+"//CTA_setting.json") as f:
        setting = json.load(f)[0]

    # Bar回测
    engine.initStrategy(Strategy, setting)
    
    # 开始跑回测
    engine.runBacktesting()
    
    # 显示回测结果
    engine.showBacktestingResult()
    engine.showDailyResult()
    
    ### 画图分析
    
    chartLog = pd.DataFrame(engine.strategy.chartLog).set_index('datetime')
    mp = htmlplot.getMultiPlot(engine, freq="15m")
    mp.set_line(line=chartLog[['envMa', 'fastMa', 'slowMa']].reset_index(), colors={"envMa": "green","fastMa": "red",'slowMa':'blue'}, pos=0)
    mp.show()
    