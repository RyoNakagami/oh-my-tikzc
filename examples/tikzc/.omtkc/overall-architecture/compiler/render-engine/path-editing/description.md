[← 描画エンジン](../description.md)

# 編集ハンドル

種別：リーフ．解析コミット `32ac110`．

VSCode のキャンバスでパスの点をドラッグできるよう，点ごとに「元ソースのどの範囲を書き換えればよいか」と世界座標を記録する（[render/path_editing.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/path_editing.rs)）．モジュール冒頭のコメントどおり，範囲はコンパイラが検証したもの（compiler-verified）である．この情報は `Diagram.editing.objects[].pathPoints` などとして拡張の [canvas-editing](../../../../data-flow/canvas-editing/description.md) に届く．

## 他の視点での同じ要素

- [キャンバス編集](../../../../data-flow/canvas-editing/description.md)（`data-flow/canvas-editing`）

## ソース

- [src/render/path_editing.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/path_editing.rs)
