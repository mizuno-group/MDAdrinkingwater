# 最終版の図作成Notebook

2冊を同じディレクトリにまとめています。ファイル名・解析処理・Fig名・保存済み出力は移動前から維持しています。

| Notebook | 役割 | 図の保存先 |
| --- | --- | --- |
| main_fig.ipynb | 最終版の主図・補足図。Fig 2eは記入済みの異常パッチ比率から描画 | results/main_fig/ |
| fig_submisson_HEandAD.ipynb | 異常パッチ比率の算出、病理特徴量PCA、異常領域マップ、画像切り出し | results/histopathology/ |

## 実行条件

カーネルの作業ディレクトリはnotebooksではなくリポジトリルートに設定してください。main_figは同梱のnotebooks/utilsを参照します。環境の記録はenvironment/env.txtにあります。

main_figのdata_rootはリポジトリのdataを参照し、raw/とreferences/から読み込みます。統計表はresults/tables/へ保存します。病理解析の元画像・特徴量・外部data_handlerは未同梱です。詳細は../data/README.mdを参照してください。

今回Notebookは再実行していません。保存済みの図は移動前の結果です。既知のデータ誤記や解析上の不整合はルートREADMEを参照してください。

## 病理画像Notebookの従来の説明

病理画像解析のNotebookを原ファイル名のまま移動しています。Fig 2eの異常パッチ比率の算出、病理特徴量のPCA、異常領域マップ、切り出し画像の処理を参照できます。変更点は、図の出力先の設定と、冒頭にあったパッケージインストールのログ出力の削除だけです。入力データの所在と実行条件は、ルートのREADMEとdata/README.mdを参照してください。


## Figure inventory

[figure_inventory.csv](figure_inventory.csv) lists the 34 file-save targets in main_fig.ipynb. The notebook column is relative to the repository root; cell_index_0based is the zero-based cell position, not the execution count. The content descriptions are in English. Histopathology outputs are not yet included in this inventory.
