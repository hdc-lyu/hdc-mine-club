"""サイトのアイコン（ファビコン）と、共有プレビュー用の既定画像を生成します。

どちらも草ブロック風の自作ドット絵です（ゲームのテクスチャは使っていません）。

    python3 _tools/site_icons.py

生成されるファイル:
    assets/favicon.svg           ブラウザのタブのアイコン
    assets/favicon-32.png        SVGに対応していないブラウザ向け
    assets/apple-touch-icon.png  iPhoneのホーム画面に追加したときのアイコン
    assets/images/og-default.png LINE・Teamsなどで共有したときのプレビュー画像
"""
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PALETTE = {
    "G": (0x6b, 0xbd, 0x46), "g": (0x5a, 0xa9, 0x3a), "h": (0x86, 0xcf, 0x5c),
    "d": (0x86, 0x60, 0x43), "D": (0x6b, 0x4a, 0x30), "e": (0x9b, 0x76, 0x53),
}

GRASS_BLOCK = [
    "GGhGGGGgGGGhGGGG",
    "GgGGGhGGGgGGGGgG",
    "GGGgGGGGhGGGgGGG",
    "gGGGGgGGGGGGGGhG",
    "GdGgdGGdGgGdGGdG",
    "ddDdGddDdGddeddD",
    "dedddDdddddDdded",
    "dddDdddeddddDddd",
    "DdddeddDddedddDd",
    "ddeddddddDdddddd",
    "dDdddDeddddedDdd",
    "ddddddddDddddddd",
    "deddDdddddedddDd",
    "ddDdddedDddddedd",
    "dddddddddddDdddd",
    "DddeddDddeddddDd",
]


def hexcolor(rgb):
    return "#%02x%02x%02x" % rgb


def write_png(path, width, height, pixel):
    """pixel(x, y) -> (r, g, b) で画像を書き出します（外部ライブラリ不要）。"""
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        for x in range(width):
            raw += bytes(pixel(x, y))

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)
    print(f"{path.relative_to(ROOT)}  {width}x{height}  {len(png) / 1024:.0f}KB")


def block_color(x, y):
    return PALETTE[GRASS_BLOCK[y][x]]


def favicon_svg():
    rects = []
    for y, row in enumerate(GRASS_BLOCK):
        x = 0
        while x < 16:
            c, start = row[x], x
            while x < 16 and row[x] == c:
                x += 1
            rects.append(f'<rect x="{start}" y="{y}" width="{x - start}" height="1" '
                         f'fill="{hexcolor(PALETTE[c])}"/>')
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" '
           'shape-rendering="crispEdges">' + "".join(rects) + "</svg>\n")
    path = ROOT / "assets" / "favicon.svg"
    path.write_text(svg, encoding="utf-8")
    print(f"{path.relative_to(ROOT)}  {len(svg) / 1024:.1f}KB")


def scaled_icon(path, size, pad):
    scale = (size - pad * 2) // 16
    offset = (size - scale * 16) // 2
    bg = (0x1a, 0x4f, 0x9c)

    def pixel(x, y):
        bx, by = (x - offset) // scale, (y - offset) // scale
        if 0 <= bx < 16 and 0 <= by < 16 and x >= offset and y >= offset:
            return block_color(bx, by)
        return bg

    write_png(path, size, size, pixel)


def og_image(path):
    """1200x630。会社色の青空に草ブロックを置き、下を地層にした構図です。"""
    width, height, scale = 1200, 630, 20
    sky_top, sky_bottom = (0x13, 0x3b, 0x76), (0x3a, 0x74, 0xc4)
    ground = 470                     # 地表の高さ
    bx0 = (width - 16 * scale) // 2  # 草ブロックの左上
    by0 = ground - 16 * scale + 40

    def layer(y):
        # 地表から下: 草 → 土 → 石
        if y < ground + 20:
            return (0x6b, 0xbd, 0x46) if (y // 10) % 2 == 0 else (0x5a, 0xa9, 0x3a)
        if y < ground + 90:
            return (0x86, 0x60, 0x43)
        return (0x7d, 0x7d, 0x7d)

    def pixel(x, y):
        bx, by = (x - bx0) // scale, (y - by0) // scale
        if 0 <= x - bx0 < 16 * scale and 0 <= y - by0 < 16 * scale:
            return block_color(bx, by)
        if y >= ground:
            base = layer(y)
            # 20pxのマス目で明暗をつけて、ドット絵の地面に見せます
            shade = ((x // 20) * 7 + (y // 20) * 13) % 5
            k = (0.92, 1.0, 0.96, 1.04, 0.9)[shade]
            return tuple(min(255, int(c * k)) for c in base)
        t = y / ground
        return tuple(int(a + (b - a) * t) for a, b in zip(sky_top, sky_bottom))

    write_png(path, width, height, pixel)


def main():
    favicon_svg()
    scaled_icon(ROOT / "assets" / "favicon-32.png", 32, 0)
    scaled_icon(ROOT / "assets" / "apple-touch-icon.png", 180, 10)
    og_image(ROOT / "assets" / "images" / "og-default.png")


if __name__ == "__main__":
    main()
