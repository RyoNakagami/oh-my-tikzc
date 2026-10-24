[← 描画エンジン](../description.md)

# 座標と形状

種別：リーフ．解析コミット `32ac110`．

座標式の解釈と，ノード形状の幾何（[render/coordinates.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/coordinates.rs)，[render/geometry.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/geometry.rs)，[src/transform.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/transform.rs)）．

- `coordinate`，`read_point`，`calc`：`(1,2)`，`(a.north)`，`($(a)!0.5!(b)$)` などを点に変換する．
- `basis`，`transform`：`scale` / `shift` / `rotate` などの変換を `Matrix` で適用する．
- `Point`，`Bounds`，`Node::anchor`，`Node::border`：アンカー位置と境界点．パスはノードの境界で切られる．

## ソース

- [src/render/coordinates.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/coordinates.rs)
- [src/render/geometry.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/geometry.rs)
- [src/transform.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/transform.rs)
