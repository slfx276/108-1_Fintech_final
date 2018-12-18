# 範例用一般MA
def myStrategy(pastData, currPrice):
    import numpy as np
    param = [0, 19]
    windowSize = 296
    alpha = param[0]
    beta = param[1]
    action = 0
    dataLen = len(pastData)
    if dataLen == 0:
        return 0
    if dataLen < windowSize:
        ma = np.mean(pastData)
        return 0
    windowedData = pastData[-windowSize:]
    ma = np.mean(windowedData)
    if (currPrice-alpha) > ma:
        action = 1
    elif (currPrice+beta) < ma:
        action = -1
    else:
        action = 0
    return action

# 用各種MA，就沒有使用到open high low price。
# MA 黃金、死亡交叉可以考慮用兩個均線試試看 ??????????????????????????????
def MA(pastData , currPrice , windowSize):
    import numpy as np
    import talib
    dataLen = len(pastData)
    # parameter selecte
    param = [0, 19]
    alpha = param[0]
    beta = param[1]

    if dataLen == 0 :
        return 0
    pastData = np.insert(pastData , dataLen , values = currPrice , axis = 0)
    currPrice = float(currPrice)
    pastData = np.array(pastData , dtype = "float")
    # 各種MA測試
    SMA = talib.MA(pastData , windowSize , matype = 0)[-1] # winSize=295,return=2.0688 [0,19]
    EMA = talib.MA(pastData , windowSize , matype=1)[-1] # winSize=347 return=1.9824 [0,19]
    WMA = talib.MA(pastData , windowSize , matype=2)[-1] # winSize=348 return=2.2064 [0,19]
    DEMA = talib.MA(pastData , windowSize , matype=3)[-1] #winSize=211 return=2.4753 [0,19]
    TEMA = talib.MA(pastData , windowSize , matype=4)[-1] #winSize=181 return=2.8288 [0,19]   

    currPrice = talib.MA(pastData , 5 , matype = 0)[-1] # winSize=295,return=2.0688 [0,19]
    # 用兩條移動均線
    # SMA，winSize=41 return=2.2393
    # EMA，winSize=34 return=2.4653
    # TEMA，winSize=158 return=1.0018


    # 低於移動平均
    if currPrice - alpha > EMA:
        return 1
    elif currPrice + beta < EMA:
        return -1
    else:
        return 0


# RSI 用來測量買壓賣壓
# RSI 常用週期14日
# new data，winSize=17 return=1.05 [30,70]
# new data，winSize=17 return=1.4977 [10,61]
def RSI(pastData , currPrice , windowSize , alpha , beta):
    import numpy as np
    import talib
    dataLen = len(pastData)
    param = [ alpha , beta ]
    alpha = param[0]
    beta = param[1]
    
    if dataLen == 0 :
        return 0
    pastData = np.insert(pastData , dataLen , values = currPrice , axis = 0)
    pastData = np.array(pastData , dtype="double")
    # winSize=32 return=2.6846 [30,70] 
    # 已確定parameter
    # 得到RSI
    rsi = talib.RSI(pastData , windowSize)[-1]
    if rsi < alpha:
        return 1
    elif rsi > beta:
        return -1
    else:
        return 0

# new data，winSize=6 return=3.5124 deviation=[3,1.6]
def BBAND(pastData , currPrice , windowSize ):
    import matplotlib.pyplot as plt
    import numpy as np
    import talib
    dataLen = len(pastData)
    # currPrice 插入 pastData 最後一項，用來計算MA等指標
    pastData = np.insert(pastData , dataLen , values = currPrice , axis = 0)
    pastData = np.array(pastData , dtype = float)
    # windowSize = 6
    if dataLen < windowSize :
        return 0
    param = [ 3 , 1.6 ]
    alpha = param[0]
    beta = param[1]
    # 算出布林通道 uppertBound=上方壓力線 lowerBound=下方支撐線 SMA=均線
    upperBound , SMA , lowerBound = talib.BBANDS(pastData , timeperiod = windowSize , matype = talib.MA_Type.T3 , nbdevup = alpha , nbdevdn = beta)
    if dataLen == 3690:
        plt.plot(upperBound)
        plt.plot(SMA)
        plt.plot(lowerBound)
        plt.grid()
        # plt.show()

    currPrice = float(currPrice)
    # print(type(currPrice) , type(lowerBound[-1]) , type(SMA[-1]) , type(upperBound[-1]))
    # print(currPrice , lowerBound[-1] , upperBound[-1])
    # 判斷買點
    if currPrice < lowerBound[-1]:
        return 1
    elif pastData[-2] < SMA[-2] and currPrice > SMA[-1] :
        return 1
    #optional
    elif SMA[-1] < currPrice < upperBound[-1] and SMA[-1] < pastData[-1] < upperBound[-1]:
        return 1
    # 判斷賣點
    elif currPrice > upperBound[-1]:
        return -1
    elif pastData[-2] > SMA[-2] and currPrice < SMA[-1] :
        return -1
    #optional
    elif currPrice < upperBound[-1] and pastData[-2] > upperBound[-2]:
        return -1
    else:
        return 0

# new data，return=1..6762
def KD(pastData , currPrice , windowSize):
    import numpy as np
    import pandas as pd
    import talib
    import matplotlib.pyplot as plt

    df = pd.read_csv("ohlcv_daily.csv")
    df["high"] = df["high"].astype("float64")
    df["low"] = df["low"].astype("float64")
    df["close"] = df["close"].astype("float64")
    high = df["high"].values
    low = df["low"].values
    close = df["close"].values
    dataLen = len(pastData)
    # currPrice 插入 pastData 最後一項，用來計算指標
    pastData = np.insert(pastData , dataLen , values = currPrice , axis = 0)
    pastData = np.array(pastData , dtype = float)
    currPrice = float(currPrice)
    if dataLen == 0 :
        return 0
        
    dataLen = len(pastData)
    # return type 是tuple 
    K , D = talib.STOCH(high[:dataLen] , low[:dataLen] , pastData )

    if K[-1] < 20 or D[-1] < 20:
        return 1
    elif K[-1] > 80 or D[-1] > 80:
        return -1
    else:
        return 0

# new data ，winSize=14 return=0.77 沒有最佳化參數的情況
# new data ，winSize=10 return=0.296 沒有最佳化參數的情況
# new data，winSize=8 return=1.1496
def WILLR(pastData , currPrice , windowSize):
    import numpy as np
    import pandas as pd
    import talib
    import matplotlib.pyplot as plt

    df = pd.read_csv("ohlcv_daily.csv")
    df["high"] = df["high"].astype("float64")
    df["low"] = df["low"].astype("float64")
    df["close"] = df["close"].astype("float64")
    high = df["high"].values
    low = df["low"].values
    close = df["close"].values

    dataLen = len(pastData)
    # currPrice 插入 pastData 最後一項，用來計算指標   ##### 資料前處理 #####
    pastData = np.insert(pastData , dataLen , values = currPrice , axis = 0)
    pastData = np.array(pastData , dtype = float)
    currPrice = float(currPrice)

    if dataLen == 0:
        return 0

    dataLen = len(pastData)
    WILLRArray = talib.WILLR(high[:dataLen] , low[:dataLen] , pastData , timeperiod = windowSize)


    # if dataLen == 3690:
    #     plt.plot(pastData)
    #     plt.plot(WILLRArray)
    #     plt.show()

    if WILLRArray[-1] < -80:
        return 1
    # 超買
    elif WILLRArray[-1] > -20:
        return -1
    else:
        return 0

# new data，目前策略只能用到return=0.7906
def MACD(pastData , currPrice , windowSize):
    import numpy as np
    import pandas as pd
    import talib
    import matplotlib.pyplot as plt
    dataLen = len(pastData)
    # currPrice 插入 pastData 最後一項，用來計算指標   ##### 資料前處理 #####
    pastData = np.insert(pastData , dataLen , values = currPrice , axis = 0)
    pastData = np.array(pastData , dtype = float)
    currPrice = float(currPrice)

    if dataLen == 0:
        return 0
    DIF , DEA , MACDArray = talib.MACD(pastData , fastperiod = 12 , slowperiod = 26 , signalperiod = 9)


    if dataLen == 3690:
        plt.plot(pastData)
        plt.show()


    # MACD 由負轉正
    if MACDArray[-1] > 0 and MACDArray[-4] < 0:
        return 1
    # DIF 由下而上穿越 DEA
    elif DIF[-2] < DEA[-2] and DIF[-1] > DEA[-1]:
        return 1
    # MACD 由正轉負
    elif MACDArray[-1] < 0 and MACDArray[-4] > 0:
        return -1
    # DIF 由上而下穿越 DEA
    elif DIF[-2] > DEA[-2] and DIF[-1] < DEA[-1]:
        return -1
    else:
        return 0


def KD_BBAND(pastData , currPrice , windowSize):
    import numpy as np
    import pandas as pd
    import talib
    import matplotlib.pyplot as plt

    df = pd.read_csv("ohlcv_daily.csv")
    df["high"] = df["high"].astype("float64")
    df["low"] = df["low"].astype("float64")
    df["close"] = df["close"].astype("float64")
    high = df["high"].values
    low = df["low"].values
    close = df["close"].values
    dataLen = len(pastData)
    # currPrice 插入 pastData 最後一項，用來計算指標   ##### 資料前處理 #####
    pastData = np.insert(pastData , dataLen , values = currPrice , axis = 0)
    pastData = np.array(pastData , dtype = float)
    currPrice = float(currPrice)


    if dataLen == 0 :
        return 0
    # 造出KD值，return type 是tuple 
    # K , D = talib.STOCH(high , low , close , fastk_period=9 , slowk_period=3 , slowk_matype=0 , slowd_period=3 , slowd_matype=0)
    K , D = talib.STOCH(high , low , close )


    param = [ 3 , 1.6 ]
    alpha = param[0]
    beta = param[1]
    # 算出布林通道 uppertBound=上方壓力線 lowerBound=下方支撐線 SMA=均線
    upperBound , SMA , lowerBound = talib.BBANDS(pastData , timeperiod = windowSize , matype = talib.MA_Type.T3 ,
                                    nbdevup = alpha , nbdevdn = beta)

    print(dataLen)
    # 判斷 KD 的決定
    KD_decision = 0
    BBAND_decision = 0
    if K[dataLen] < 20 or D[dataLen] < 80:
        KD_decision =  1
    elif K[dataLen] > 20 or D[dataLen] > 80:
        KD_decision = -1
    else:
        KD_decision = 0

    # 判斷 BBAND 的決定
    if currPrice < lowerBound[-1]:
        BBAND_decision = 1
    elif pastData[-2] < SMA[-2] and currPrice > SMA[-1] :
        BBAND_decision = 1
    elif SMA[-1] < currPrice < upperBound[-1] and SMA[-1] < pastData[-1] < upperBound[-1]:
        BBAND_decision = 1
    # 判斷賣點
    elif currPrice > upperBound[-1]:
        BBAND_decision = -1
    elif pastData[-2] > SMA[-2] and currPrice < SMA[-1] :
        BBAND_decision = -1
    elif currPrice < upperBound[-1] and pastData[-2] > upperBound[-2]:
        BBAND_decision = -1
    else:
        BBAND_decision = 0

    if KD_decision + BBAND_decision == 2:
        return 1
    elif KD_decision + BBAND_decision == -2:
        return -1
    else:
        return 0

# new data，MA winSize=4、RSI winSize=3、BBAND winSize=12 return=4.2213 [0,19][30,70][3,1.6]
def MA_RSI_BBAND(pastData , currPrice , p1 , p2 , p3):
    import numpy as np
    import pandas as pd
    import talib
    import matplotlib.pyplot as plt
    dataLen = len(pastData)

    # currPrice 插入 pastData 最後一項，用來計算指標   ##### 資料前處理 #####
    pastData = np.insert(pastData , dataLen , values = currPrice , axis = 0)
    pastData = np.array(pastData , dtype = float)
    currPrice = float(currPrice)

    if dataLen == 0:
        return 0
    
    MA_decision = 0
    RSI_decision = 0
    BBAND_decision = 0
    # MA
    SMA = talib.MA(pastData , p1 , matype = 0)[-1]
    if currPrice - 0 > SMA:
        MA_decision = 1
    elif currPrice + 19 < SMA:
        MA_decision = -1
    else:
        MA_decision = 0

    # RSI
    RSI = talib.RSI(pastData , p2)[-1]
    if RSI < 30:
        RSI_decision = 1
    elif RSI > 70:
        RSI_decision = -1
    else:
        RSI_decision = 0
    
    # BBAND
    upperBound , SMA , lowerBound = talib.BBANDS(pastData , timeperiod = p3 , matype = talib.MA_Type.T3 , nbdevup = 3 , nbdevdn = 1.6)
    if dataLen == 3690:
        plt.plot(upperBound)
        plt.plot(SMA)
        plt.plot(lowerBound)
        plt.grid()
        # plt.show()

    # 判斷買點
    if currPrice < lowerBound[-1]:
        BBAND_decision = 1
    elif pastData[-2] < SMA[-2] and currPrice > SMA[-1] :
        BBAND_decision = 1
    #optional
    elif SMA[-1] < currPrice < upperBound[-1] and SMA[-1] < pastData[-1] < upperBound[-1]:
        BBAND_decision = 1
    # 判斷賣點
    elif currPrice > upperBound[-1]:
        BBAND_decision = -1
    elif pastData[-2] > SMA[-2] and currPrice < SMA[-1] :
        BBAND_decision = -1
    #optional
    elif currPrice < upperBound[-1] and pastData[-2] > upperBound[-2]:
        BBAND_decision = -1
    else:
        BBAND_decision = 0

    if MA_decision + RSI_decision + BBAND_decision >= 2:
        return 1
    elif MA_decision + RSI_decision + BBAND_decision <= -2:
        return -1
    else:
        return 0



# 葛蘭碧八大法則
# regression
# 可以考慮使用open high low
# 吳推薦：KD + RSI + WILLR
# 指標參考 https://www.fmz.com/bbs-topic/1234