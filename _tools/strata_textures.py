"""フッターの地層（土・石・深層岩・岩盤）のドット絵テクスチャを生成します。

Minecraft のテクスチャは使わず、色味を寄せた16x16の模様を乱数で自作しています
（乱数の種を固定しているので、何度実行しても同じ模様になります）。
色を変えたら次のコマンドで _sass/strata-textures.scss を作り直してください。

    python3 _tools/strata_textures.py
"""
import random
from pathlib import Path
from urllib.parse import quote

SIZE = 16

# base: 地の色 / spots: (色, 割合) / streak: 横に伸びる筋を入れるか（深層岩の層の感じ）
LAYERS = {
    "dirt": {"base": "#866043", "spots": [("#6b4a30", 0.20), ("#9b7653", 0.14), ("#5a3d27", 0.06)]},
    "stone": {"base": "#7d7d7d", "spots": [("#6b6b6b", 0.20), ("#8f8f8f", 0.14), ("#5f5f5f", 0.05)]},
    # 文字を載せる層なので、明るい粒を控えめにして文字とのコントラストを確保しています
    "deepslate": {"base": "#4a4a4f", "spots": [("#3e3e43", 0.22), ("#54545a", 0.12), ("#36363a", 0.06)],
                  "streak": True},
    "bedrock": {"base": "#3a3a3a", "spots": [("#1f1f1f", 0.26), ("#6b6b6b", 0.14), ("#555555", 0.12)]},
}


def texture_svg(name, layer):
    rng = random.Random(f"hdc-mine-club-{name}")
    grid = [[layer["base"]] * SIZE for _ in range(SIZE)]
    for color, ratio in layer["spots"]:
        for _ in range(int(SIZE * SIZE * ratio)):
            x, y = rng.randrange(SIZE), rng.randrange(SIZE)
            grid[y][x] = color
            if layer.get("streak") and rng.random() < 0.5:
                grid[y][(x + 1) % SIZE] = color  # 横に1マス伸ばして筋っぽく
    rects = []
    for y, row in enumerate(grid):
        x = 0
        while x < SIZE:
            c, start = row[x], x
            while x < SIZE and row[x] == c:
                x += 1
            if c != layer["base"]:
                rects.append(f'<rect x="{start}" y="{y}" width="{x - start}" height="1" fill="{c}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" '
            f'shape-rendering="crispEdges"><rect width="{SIZE}" height="{SIZE}" fill="{layer["base"]}"/>'
            + "".join(rects) + "</svg>")


def main():
    lines = [
        "// フッターの地層テクスチャ（_tools/strata_textures.py で自動生成。直接編集しないでください）",
        "",
    ]
    for name, layer in LAYERS.items():
        uri = "data:image/svg+xml," + quote(texture_svg(name, layer), safe=" =:/,")
        lines.append(f'$tex-{name}: url("{uri}");')
    path = Path(__file__).resolve().parent.parent / "_sass" / "strata-textures.scss"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{path} を生成しました（{len(LAYERS)}層）")


if __name__ == "__main__":
    main()
