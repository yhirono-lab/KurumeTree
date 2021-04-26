# KurumeTree
1. makedataset.py でオリジナルのデータから必要な要素だけを抽出した以下のファイルを作成
    * Stain_list.csv : 免疫染色24種類のリスト
    * Disease_{Full/Simple}Name_list.csv : 病名ごとに何症例あるか記したファイル
    * Data_{Full/Simple}Name.csv : 決定木作成に必要な免疫染色の結果を記したファイル

2. using_tree.py で use/not useによる決定木を作成
    * Data_{Full/Simple}Name.csv が必要
    * utils.py に補助的な関数を記載
    * GraphViz.py に決定木の描画に必要なプログラムを記載
    * 結果を/resultに保存
        * /tree : 各深さにおける決定木の画像を保存
        * /unu_depth{x} : 以下のファイルに情報を保存
            * feature_importance.csv
            * hist_unu.csv
            * leaf_list_unu.csv
            * Ptable_unu.csv