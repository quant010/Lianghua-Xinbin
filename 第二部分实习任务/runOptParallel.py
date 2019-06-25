from vnpy.trader.utils import optimize
from Strategy import Strategy
from datetime import datetime
import os
import json

def setConfig(root=None):
    # 设置策略类
    optimize.strategyClass = Strategy
    # 设置缓存路径，如果不设置则不会缓存优化结果。
    optimize.root = root
    # 设置引擎参数
    optimize.engineSetting = {
        "startDate": "20160603 10:00:00",
        "endDate": "20190225 23:00:00",
        "dbName": "VnTrader_1Min_Db",
        "contract":[{
                    "slippage": 0,
                    "rate": 0
                    }]
    }
    # 设置策略固定参数
    optimize.globalSetting = {
        "symbolList": ["RB88:CTP"],
        "barPeriod": 150,#往前推的初始数据值
        "timeframeMap" :{"envPeriod": "15m", "signalPeriod": "15m","ATRPeriod":"60m"},
        "barPeriod":150,"envPeriod": 100,"stoplossPct":0.02,"atrPeriod":20,"lot" :10
    }
    # 设置策略优化参数
    optimize.paramsSetting = {
            "fastPeriod": range(1,21,1),
            "slowPeriod": range(5,31,1)
    }
    path = os.path.split(os.path.realpath(__file__))[0]
    with open(path+"//CTA_setting.json") as f:
        globalSetting = json.load(f)[0]
    optimize.globalSetting = globalSetting
    optimize.initOpt()

# 并行优化 无缓存
def runSimpleParallel():
    start = datetime.now()
    print("run simple | start: %s -------------------------------------------" % start)
    setConfig()
    optimize.runParallel() #并行优化，返回回测结果
    report = optimize.runParallel()
    report.sort_values(by = 'sharpeRatio', ascending=False, inplace=True)
    # 将结果保存成csv
    report.to_csv('opt_RB88.csv')    
    end = datetime.now()
    print("run simple | end: %s | expire: %s -----------------------------" % (end, end-start))

def main():
    runSimpleParallel()

if __name__ == '__main__':
    main()
