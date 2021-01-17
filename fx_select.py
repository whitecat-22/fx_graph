import os # パス結合
import pandas as pd # pandasデータフレームを使用

# Googleドライブのマイドライブのパス
mydrive = 'C:/Users/hiro2/OneDrive/Documents/python/fx_graph/data/'

# フォルダ名
hst_dir = 'hst_20210117'

# 入力ファイル名
input_csv = 'USDJPY.csv'

# CSVファイルをPandasデータフレームに読み込む
df = pd.read_csv(os.path.join(mydrive, hst_dir, input_csv))

# DateTime列をdatatime型に変換→インデックスに設定して、元の列は削除する
df = df.set_index(pd.to_datetime(df['DateTime'])).drop('DateTime', axis=1)

# 指定した期間のデータを抽出する（参考として指定方法を数パターン書いています）
#df = df['2019-09-30 0:00' : '2019-09-30 6:00'] # 期間を日時で指定
df = df['2020-01' : '2021-01'] # 期間を年月で指定
#df = df['2019-09-20' : '2019-09-30'] # 期間を日で指定
#df = df['2019'] # 年で指定
#df = df['2019-09'] # 年月で指定
#df = df['2020-01-01'] # 年月日で指定
#df = df[:100] # 先頭からの行数で指定
#df = df[100:200] # 期間を行数で指定

# 抽出結果の表示
print('行数:%d' % len(df)) # 行数
#display(df.head(1)) # データの先頭1行を表示
#display(df.tail(1)) # データの末尾頭1行を表示
print(df.head(1)) # データの先頭1行を表示
print(df.tail(1)) # データの末尾頭1行を表示

# 出力ファイル名
output_csv = 'USDJPY_20210117.csv'

# CSVファイルに保存
df.to_csv(os.path.join(mydrive, hst_dir, output_csv))
