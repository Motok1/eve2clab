# eve2clab

EVE-NG で作成したトポロジ情報(.unl)を clab の config(.clab.yaml) に変更するためのツール

## Usage

1. EVE-NG から export した .unl を用意する。変換時にファイルの場所を指定するため、置く場所はどこでも良い。
2. `python3 converter.py -f <unl ファイル>` を実行する。実行後、`export-**` のディレクトリが生成され、ディレクトリ内に .clab.yaml も生成される。

※ `--mode` option で変換モードが指定できるようになっているが、現時点では unl → clab の変換のみで逆は NotIMprementedError となる。

## Caveats

**unl の instance type と clab の kind のマッピングについて**

`MAPPING` の辞書において、 instance type の変換表を保持している。
新規に変換を増やす場合や、mapping を変更したい場合は辞書の中を編集して対応を更新すること。

```py
MAPPING = {
    'EVE-NG instance prefix': 'Containerlab Kind'
}
 ```

**Links**

1. P2P のみのサポートで、L2 NW の変換はできません。
