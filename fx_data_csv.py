import os  # ディレクトリ作成、パス結合、ファイル削除
import datetime  # 日付取得
import requests  # ダウンロード処理
import zipfile  # zip解凍
import numpy as np  # 数値データ高速処理
import pandas as pd  # データ構造化

# 取得・作成したデータを保存するディレクトリのパス（Google Drive）
hst_dir = 'C:/Users/hiro2/OneDrive/Documents/python/fx_graph/data/hst_' + \
    datetime.datetime.today().strftime('%Y%m%d')
if not os.path.exists(hst_dir):  # ディレクトリが無い場合
    os.mkdir(hst_dir)  # ディレクトリを作成

# 取得する通貨ペアを指定
list = ['USDJPY', 'EURJPY']
for item in list:
    print(item)
    zip_url = 'https://tools.fxdd.com/tools/M1Data/' + item + '.zip'  # ダウンロード元url
    zip_file = os.path.join(hst_dir, item + '.zip')  # 保存先ファイル名
    req = requests.get(zip_url)
    with open(zip_file, 'wb') as f:
        f.write(req.content)
    print(' ：ダウンロード完了')

  # zipファイルを解凍する
    with zipfile.ZipFile(zip_file, 'r') as f:  # 読み込みモードで開く
        f.extractall(hst_dir)  # zip展開
        print(' ：zip解凍完了')

    # hstファイルをcsvファイルに保存する
    with open(os.path.join(hst_dir, item + '.hst'), 'rb') as f:
        # hstのヘッダ(148byte)からバージョン(先頭の4byte)を取得
        # dtype='i4':符号あり32ビット整数型
        ver = np.frombuffer(buffer=f.read(148)[:4], dtype='i4')
        if ver == 400:  # バージョンが400の場合
            # 1行のデータの並びを定義
            dtype = [
                ('DateTime', 'u4'),  # 'u4':符号なし32ビット整数型
                ('Open', 'f8'),      # 'f8':符号あり64ビット整数型
                ('Low', 'f8'),       #
                ('High', 'f8'),      #
                ('Close', 'f8'),     #
                ('Volume', 'f8')     #
            ]
        elif ver == 401:  # バージョンが401の場合
            # 1行のデータの並びを定義
            dtype = [
                ('DateTime', 'u8'),  # 'u8':符号なし32ビット整数型
                ('Open', 'f8'),      # 'f8':符号あり64ビット整数型
                ('Low', 'f8'),       #
                ('High', 'f8'),      #
                ('Close', 'f8'),     #
                ('Volume', 'f8'),    #
                ('Spread', 'i4'),    # 'i4':符号あり32ビット整数型
                ('RealVolume', 'i8')
            ]
        # バイナリデータをPandasのデータフレームに変換する
        df = pd.DataFrame(np.frombuffer(buffer=f.read(), dtype=dtype))
        # DateTime列を日付データに変換してインデックスに設定して、変換前の列を削除する
        df = df.set_index(pd.to_datetime(
            df['DateTime'], unit='s')).drop('DateTime', axis=1)

#        display(df.head(2))  # データの先頭2行を書き出す
#        display(df.tail(2))  # データの末尾2行を書き出す
        print(df.head(2))  # データの先頭2行を書き出す
        print(df.tail(2))  # データの末尾2行を書き出す

        #csvファイルに保存
        df.to_csv(os.path.join(hst_dir, item + '.csv'))
        print(' ：csvに変換完了')

    # ファイルを削除
    os.remove(zip_file)  # zipファイル削除
    os.remove(os.path.join(hst_dir, item + '.hst'))  # hstファイル削除
    print(' ：zip、hst削除完了')
