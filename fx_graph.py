import os # パス結合
import pandas as pd # pandasデータフレームを使用

# Googleドライブのマイドライブのパス
mydrive = 'C:/Users/hiro2/OneDrive/Documents/python/fx_graph/data/'

# フォルダ名
hst_dir = 'hst_20210117'

# 入力ファイル名
input_csv = 'USDJPY_20210117.csv'

# CSVファイルをPandasデータフレームに読み込む
df = pd.read_csv(os.path.join(mydrive, hst_dir, input_csv))

# DateTime列をdatatime型に変換→インデックスに設定して、元の列は削除する
df = df.set_index(pd.to_datetime(df['DateTime'])).drop('DateTime', axis=1)

from backtesting import Backtest, Strategy # バックテスト実行、ストラテジー作成
from backtesting.lib import crossover
from backtesting.test import SMA # SMAインジケータ使用

class myStrategy(Strategy):
    n1 = 10 # 終値のSMA（単純移動平均）の期間
    n2 = 30 # 終値のSMA（単純移動平均）の期間

    def init(self): # ストラテジーの事前処理
        self.sma1 = self.I(SMA, self.data.Close, self.n1) # 終値のSMA（単純移動平均）をインジケータとして追加
        self.sma2 = self.I(SMA, self.data.Close, self.n2) # 終値のSMA（単純移動平均）をインジケータとして追加

    def next(self): # ヒストリカルデータの行ごとに呼び出される（データの2行目から開始）
        if crossover(self.sma1, self.sma2): # sma1がsma2を上回った時
            self.buy() # 現在のポジションを閉じて、所持金分買う

        elif crossover(self.sma2, self.sma1):
            self.sell() # 現在のポジションを閉じて、所持金分売る

# バックテストを設定
bt = Backtest(
    df, # ヒストリカルデータ
    myStrategy, # ストラテジー
    cash=10000, # 所持金
    commission=0.0005, # 取引手数料（為替価格に対する倍率で指定、為替価格100円でcommission=0.0005なら0.05円）
    margin=1.0, # 取引金額に対する所持金の割合、cash=10000でmargin=0.2なら50000分取引する
    trade_on_close=True # True：現在の終値で取引する、False：次の時間の始値で取引する
)

output = bt.run() # バックテスト実行
print(output) # 実行結果を表示
bt.plot() # 実行結果のグラフを表示
