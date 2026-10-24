[← 描画エンジン](../description.md)

# パス拡張機能

種別：リーフ．解析コミット `32ac110`．

パス構築から呼ばれる TikZ ライブラリ相当の機能をまとめた要素．各機能は独立しており，内部の相互作用は少ないため 1 つの葉にした．

- [render/plot.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/plot.rs)：`plot` による関数の標本化と plot mark．
- [render/intersections.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/intersections.rs)：`name path` と `name intersections`．パスを折れ線に平坦化して交点を求める．
- [render/markings.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/markings.rs)：`decorations.markings` の `mark=at position ... with {...}`．
- [render/shading.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/shading.rs)：線形・放射グラデーション．

## ソース

- [src/render/plot.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/plot.rs)
- [src/render/intersections.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/intersections.rs)
- [src/render/markings.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/markings.rs)
- [src/render/shading.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/shading.rs)
