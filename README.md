# KurumeTree
免疫染色データから決定木を作成するプログラム  
graphvizというライブラリを研究室のマシンに導入するのが(２年前は)難しかったため，WindowsPCでの実行を推奨  

# 実行環境
ライブラリバージョン
* python            3.6.13
* python-graphviz   0.16
* graphviz          2.38
* matplotlib        3.3.4
* numpy             1.19.2
* pandas            1.1.3
* pillow            8.2.0

# Graphvizのインストール
かなり前のことなので，正直よく覚えていないです．  
頑張ってインストールしてみてください．  
参考として，このページをみてインストールしたような覚えがあります．
>https://hytmachineworks.hatenablog.com/entry/2019/02/04/001411  

環境変数へのPathの登録が鍵だったような気もします．

Graphvizは木構造の図の描写のためで，自分で図をパワポなりで作れば済む話ではあるので，最悪インストールできなくても大丈夫です．(プログラムの該当の行をコメントアウトすればいいです．)

# ファイル構造
研究室のデータセットには保存されていません．
このプロジェクトのフォルダだけで完結します．
```
# 久留米大学からもらった状態のデータ 
Raw_data/
    ├ 1st
    |   ├ ML180001_180660.xlsx  (名前改変前)最初期のデータ
    |   ├ ML180001_180660.csv   (名前改変前)最初期のデータ
    |   └ Kurume_img_list.txt   (名前改変前)/Raw/_Kurume_Dataset/svs にあるsvsファイル一覧のデータ
    ├ 2nd
    |   ├ ML180001_180660.xlsx  (名前改変前)2021年5月？時点のデータ
    |   ├ ML180001_182700.csv   (名前改変前)2021年5月？時点のデータ
    |   └ Kurume_img_list.txt   (名前改変前)/Raw/_Kurume_Dataset/svs にあるsvsファイル一覧のデータ
    ├ 3rd
        ├ O_C_00001-02530.xlsx  (名前改変後)2021年11月時点のデータ
        ├ O_C_00001-02530.csv   (名前改変後)2021年11月時点のデータ
        └ Kurume_img_list.txt   (名前改変後)/Raw/_Kurume_Dataset/svs にあるsvsファイル一覧のデータ

# Source Code
Source/
    ├ GraphViz.py       # 木構造描写用プログラム
    ├ kurume_tree.py    # 久留米大学の基準の免疫染色の使用の有無で形態を分ける決定木のプログラム
    ├ make_add_flag.py  # add_flag_list.pyを作成するためのプログラム
    ├ makedataset.py    # datasetを作成するプログラム
    ├ normal_tree.py    # 情報エントロピーで分ける通常の決定木のプログラム
    └ utils.py          # 補助関数をまとめたプログラム
```

# 使い方
1. makedataset.py でオリジナルのデータから必要な要素だけを抽出した以下のファイルを作成
    * プログラム内の `data_option` 変数に0～2を入力して，どの(いつの)データかを選択
    * 番号とデータの対応は 0→1st, 1→2nd, 2→3rd となっている
    ```
        # makedataset.py make_add_flag.pyで作成されるデータ
        dataset/
            ├ 1st
            |   ├ Data_FullName.csv             病型1,2で記載した免疫染色データ
            |   ├ Data_FullName_svs.csv         ↑のsvsファイルが存在する症例のみを抽出したデータ
            |   ├ Data_SimpleName.csv           病型1で記載した免疫染色データ
            |   ├ Data_SimpleName_svs.csv       ↑のsvsファイルが存在する症例のみを抽出したデータ
            |   ├ Disease_FullName.csv          病型1,2で記載した病型の一覧データ
            |   ├ Disease_FullName_svs.csv      ↑のsvsファイルが存在する症例のみを抽出したデータ
            |   ├ Disease_SimpleName.csv        病型1で記載した病型の一覧データ
            |   ├ Disease_SimpleName_svs.csv    ↑のsvsファイルが存在する症例のみを抽出したデータ
            |   └ Stain_list.csv                免疫染色のリスト
            ├ 2nd
            |   ├ 同上
            |   └ add_flag_list.txt             1stから追加されたデータかどうかを示すデータ
            └ 3rd
                ├ 同上
                └ add_flag_list.txt             1stから追加されたデータかどうかを示すデータ
    ```

**`以降のプログラムでは基本的に svsファイルが存在するデータで実行している`**  
(プログラム中の`ReadCSV_svs`を`ReadCSV`に変えれば全てのデータでの決定木ができる)

2. normal_tree.py で 免疫染色の使用の有無による決定木を作成
    * 各ノードでサブタイプの確率からエントロピーを計算し，最もエントロピーが小さくなる免疫染色で分岐させる一般的な決定木
    * utils.py に補助的な関数を記載
    * GraphViz.py に決定木の描画に必要なプログラムを記載
    * 実行時の引数の説明
        ```
        mode            # 病型の名前(Simple/Full)を選択，情報エントロピーが変わり違う決定木になる
        depth           # 最大の深さを選択，その深さまでのデータが作られる
        weight_option   # データ数を疑似的にいじって計算する
            ├ 0:通常のエントロピーの計算
            ├ 1:データ数の正規化，全てのサブタイプで同じ症例数だと仮定して計算
            └ 2:特定のサブタイプのみ数を疑似的に増やして計算
        data            # データの指定(1st, 2nd, 3rd)
        ```
    * 結果は/resultsに保存される
        ```
        results/normal_tree_{weight_option}/{data}/{mode}
            ├ tree/             各深さにおける決定木の画像を保存
            └ unu_depth{x}/     深さごとに情報を保存
                ├ leafs_data/
                |   └leaf_{x}.csv           各葉に分岐したデータを保存(MILに使用)       
                ├ feature_importance.csv    データ数とエントロピーから計算される免疫染色の分岐の重要度を保存
                ├ hist_normal.csv           各葉ごとのサブタイプの確率(頻度)を保存
                ├ leaf_list_normal.csv      各葉に分岐した症例番号を保存(leaf_{x}.csvとほぼ重複)   
                └ Ptable_normal.csv         各症例のサブタイプの確率を保存(hist_normal.csvとほぼ重複)
        ```
3. kurume_tree.py で 免疫染色の使用の有無による決定木を作成
    * 久留米大学の先生に教えてもらったHE染色の判断手順をもとに，特定の免疫染色で分岐させる決定木のプログラム
    * かなり力技のプログラムでとても読みにくいです
    * utils.py に補助的な関数を記載
    * GraphViz.py に決定木の描画に必要なプログラムを記載
    * 実行時の引数の説明
        ```
        mode    # 病型の名前(Simple/Full)を選択できるが，どちらも同じ(↑とのディレクトリの整合性のため)
        data    # データの指定(1st, 2nd, 3rd)
        ```
    * 結果は/resultsに保存される
        ```
        results/kurume_tree/{data}/{mode}
            └ 同上
        ```

**名前改訂後のデータにはサブタイプ「META」のデータが削除されている**  
**今後，名前改訂後データでMILを実験する時は，METAを追加するか，CD20の分岐をなくしてFDCの分岐を行うのがいいかな**  
**FDCの分岐でMILを実験する場合はYOLOのアノテーションを作るところから始める必要がある**  

4. make_add_flag.py で追加されたどうかのフラグファイルを作成する
    * 特に引数などを指定する必要はなく，実行するだけで作成される