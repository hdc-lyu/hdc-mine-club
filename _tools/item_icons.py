"""活動の種類ごとのアイテムアイコン（16x16のドット絵）を生成します。

Minecraft のテクスチャは使わず、雰囲気を寄せて自作しています。
アイコンを直したり種類を増やしたりしたら、次のコマンドで
_includes/item-icon.html を作り直してください。

    python3 _tools/item_icons.py
"""
from pathlib import Path

# 1文字 = 1ピクセル。"." は透明
ICONS = {
    "探検": {  # コンパス
        "palette": {"K": "#2f2f2f", "g": "#8c8c8c", "w": "#ececec", "r": "#d42a2a", "k": "#4a4a4a"},
        "pixels": [
            "................",
            ".....KKKKKK.....",
            "...KKggggggKK...",
            "..KggwwwwwwggK..",
            "..KgwwwwwwrwgK..",
            ".KgwwwwwwrrwwgK.",
            ".KgwwwwwrrrwwgK.",
            ".KgwwwwrrrwwwgK.",
            ".KgwwwkkkwwwwgK.",
            ".KgwwkkkwwwwwgK.",
            ".KgwwkkwwwwwwgK.",
            "..KgwkwwwwwwgK..",
            "..KggwwwwwwggK..",
            "...KKggggggKK...",
            ".....KKKKKK.....",
            "................",
        ],
    },
    "建築": {  # レンガ
        "palette": {"m": "#d9d0c3", "r": "#b0513a", "R": "#8a3a28"},
        "pixels": [
            "mmmmmmmmmmmmmmmm",
            "rrrrrrrmrrrrrrrm",
            "rRrrrrrmrrrRrrrm",
            "rrrrRrrmrrrrrrRm",
            "mmmmmmmmmmmmmmmm",
            "rrrmrrrrrrrmrrrr",
            "rrRmrrrRrrrmrrRr",
            "rrrmrrrrrrrmrrrr",
            "mmmmmmmmmmmmmmmm",
            "rrrrrrrmrrrrrrrm",
            "rrrRrrrmrRrrrrrm",
            "rrrrrrRmrrrrrRrm",
            "mmmmmmmmmmmmmmmm",
            "rrrmrrrrrrrmrrrr",
            "rRrmrrrrRrrmrrrr",
            "rrrmrrrrrrrmrrrr",
        ],
    },
    "イベント": {  # ケーキ
        "palette": {"K": "#3b2414", "W": "#f7f4ec", "w": "#d9d2c2", "r": "#d42a2a",
                    "b": "#c07a3f", "B": "#8f5428"},
        "pixels": [
            "................",
            "................",
            "................",
            "..KKKKKKKKKKKK..",
            ".KWWWWrWWWWWWWK.",
            ".KWWwWWWWWrWWWK.",
            ".KWWWWWWWWWWwWK.",
            ".KWWWrWWwWWWWWK.",
            ".KWbWWbWWWbWWbK.",
            ".KbbbbbbbbbbbbK.",
            ".KbBbbbbbBbbbbK.",
            ".KbbbbbBbbbbbBK.",
            ".KbbbbbbbbbbbbK.",
            ".KBBBBBBBBBBBBK.",
            "..KKKKKKKKKKKK..",
            "................",
        ],
    },
    "予定": {  # 時計（トップの「次回の活動」で使います）
        "palette": {"K": "#3a2a05", "y": "#f2c230", "Y": "#c99612", "b": "#2f5fb8",
                    "s": "#f6e27a", "k": "#1f1f1f"},
        "pixels": [
            "................",
            ".....KKKKKK.....",
            "...KKYyyyyYKK...",
            "..KYyyssssyyYK..",
            "..KyysbbbbsyyK..",
            ".KYysbbbbbbsyYK.",
            ".KyysbbkbbbsyyK.",
            ".KyysbbkbbbsyyK.",
            ".KyysbbkkkbsyyK.",
            ".KyysbbbbbbsyyK.",
            ".KYysssssssyyYK.",
            "..KyyyyyyyyyyK..",
            "..KYYyyyyyyYYK..",
            "...KKYYYYYYKK...",
            ".....KKKKKK.....",
            "................",
        ],
    },
    "お知らせ": {  # 本
        "palette": {"K": "#2e1a0b", "b": "#7d4a22", "d": "#5e3617", "y": "#e3c35f",
                    "p": "#f4ecd8", "P": "#d6c9ab"},
        "pixels": [
            "................",
            "...KKKKKKKKKK...",
            "..KdbbbbbbbbbK..",
            "..KdbbbbbbbbbK..",
            "..KdbbyyyyybbK..",
            "..KdbbyyyyybbK..",
            "..KdbbbbbbbbbK..",
            "..KdbbbbbbbbbK..",
            "..KdbbbbbbbbbK..",
            "..KdbbbbbbbbbK..",
            "..KdbbbbbbbbbK..",
            "..KdbbbbbbbbbK..",
            "..KdppppppppppK.",
            "..KdPPPPPPPPPPK.",
            "...KKKKKKKKKKK..",
            "................",
        ],
    },
}


def svg_paths(icon):
    """同じ色の横に連続するピクセルをまとめて、色ごとの path にします。"""
    rows = icon["pixels"]
    assert len(rows) == 16, "縦は16行にしてください"
    runs = {}
    for y, row in enumerate(rows):
        assert len(row) == 16, f"{y + 1}行目が16文字ではありません: {row!r}"
        x = 0
        while x < 16:
            c = row[x]
            if c == ".":
                x += 1
                continue
            start = x
            while x < 16 and row[x] == c:
                x += 1
            runs.setdefault(c, []).append(f"M{start} {y}h{x - start}v1h-{x - start}z")
    return "".join(
        f'<path fill="{icon["palette"][c]}" d="{"".join(d)}"/>' for c, d in runs.items()
    )


def main():
    out = [
        "{%- comment -%}",
        "  活動の種類（category）に応じたアイテムアイコンを表示します。",
        "  使い方: {% include item-icon.html name=\"探検\" %}",
        "  対応していない種類のときは何も表示しません。",
        "",
        "  このファイルは _tools/item_icons.py で自動生成しています。直接編集しないでください。",
        "{%- endcomment -%}",
    ]
    for i, (name, icon) in enumerate(ICONS.items()):
        out.append(f'{{%- {"if" if i == 0 else "elsif"} include.name == "{name}" -%}}')
        out.append(
            '<svg class="item-icon" width="16" height="16" viewBox="0 0 16 16" '
            'shape-rendering="crispEdges" aria-hidden="true" focusable="false">'
            + svg_paths(icon) + "</svg>"
        )
    out.append("{%- endif -%}")
    path = Path(__file__).resolve().parent.parent / "_includes" / "item-icon.html"
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{path} を生成しました（{len(ICONS)}種類）")


if __name__ == "__main__":
    main()
