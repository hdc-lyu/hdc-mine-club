---
layout: page
title: 保守情報
permalink: /admin/
noindex: true
---

サイト管理者向けの手順書です。ナビゲーションには表示していません。

> **注意**
> このページは静的サイトの一部であり、認証はかかっていません。
> URLを知っていれば誰でも閲覧できます（リポジトリも公開されています）。
> パスワード、サーバーの接続情報、個人の連絡先などは書かないでください。

## 次回の活動を更新する

トップページの「次回の活動」は `_data/next_event.yml` で管理しています。

```yaml
date: 2026-09-19
title: ウィザー討伐
# note: ひとこと（任意）
```

日付を過ぎると自動で表示されなくなります。次の予定が決まったら書き換えてください。

## 活動記録を追加する

`_posts/` に `YYYY-MM-DD-タイトル.markdown` という名前でファイルを作成します。
ファイル名の日付が公開日になります。冒頭には次の front matter を書いてください。

```yaml
---
layout: post
title:  "記事のタイトル"
date:   2026-08-15 10:00:00 +0900
categories: 建築
---
```

`categories` は活動の種類です。活動一覧では看板の上にタグとして表示され、
次の4種類はアイテムのアイコンが付きます。

| 種類 | アイコン |
|---|---|
| 探検 | コンパス |
| 建築 | レンガ |
| イベント | ケーキ |
| お知らせ | 本 |

これ以外の種類も使えますが、アイコンは付かず文字だけになります。
アイコンを増やす・直すときは `_tools/item_icons.py` のドット絵を編集し、
`python3 _tools/item_icons.py` を実行してください（16×16の自作ドット絵です。
ゲームのテクスチャは著作権があるため使っていません）。

### 進捗の表示（任意）

front matter に `advancement` を1行書くと、記事の冒頭にゲームの
「進捗を達成しました！」風の通知が表示されます。アイコンは記事の種類で決まります。

```yaml
advancement: エンドの入口を見つけた
```

書かなければ表示されません。

本文はMarkdownで書きます。1つ目の段落が一覧ページの抜粋になります。

## 活動記録に写真を載せる

### 1. 画像を置く

`assets/images/posts/` の下に、**記事ごとのフォルダ**を作って入れます。
フォルダ名・ファイル名は半角英数字とハイフンにしてください。

```
assets/images/posts/2026-08-25-event/entrance.jpg
                                     /work-1.jpg
                                     /work-2.jpg
```

### 2. 記事に書く

写真を1枚、大きく載せる場合です。`src` は `assets/images/posts/` から先の部分だけ書きます。

```liquid
{% raw %}{% include photo.html src="2026-08-25-event/entrance.jpg" caption="完成したエントランス" %}{% endraw %}
```

`caption`（説明文）は省略できます。写真は本文と同じ幅に広がり、
縦長の写真は高さが頭打ちになるので、画面を占有しません。

こまかい写真を横に並べる場合は `photo-grid` で囲みます。
画面が狭いときは自動で縦積みになります。

```liquid
<div class="photo-grid">
{% raw %}{% include photo.html src="2026-08-25-event/work-1.jpg" caption="資材の準備" %}
{% include photo.html src="2026-08-25-event/work-2.jpg" caption="足場を組んだところ" %}{% endraw %}
</div>
```

### 3. 活動一覧にサムネイルを出す（任意）

front matter に `thumbnail` を書くと、活動一覧とトップページの看板に
写真が貼られます。書かなければ今までどおり文字だけの看板になります。

```yaml
---
layout: post
title:  "夏のイベントを開催しました"
date:   2026-08-25 18:00:00 +0900
categories: イベント
thumbnail: 2026-08-25-event/entrance.jpg
---
```

### 文章とのバランスのコツ

- **段落と段落の間に写真を置く**と流れが切れません。見出しの直後より、
  ひと段落説明してから見せるほうが読みやすくなります
- **1枚だけ大きく**見せたいもの以外は、2〜3枚を横に並べたほうが締まります
- 説明文（caption）を付けると、写真と本文の間にワンクッション入って読みやすくなります
- 1記事に大きい写真を何枚も並べるより、**代表を1枚＋並べて2〜3枚**が目安です

### 画像のサイズ

そのままだとスマートフォンの通信量を圧迫するので、**長辺1600px程度・1枚500KB以下**に
縮めてから置いてください。Macなら次のコマンドで縮小できます（元ファイルが上書きされるので
コピーしてから実行してください）。

```bash
sips -Z 1600 assets/images/posts/2026-08-25-event/*.jpg
```

## 部員を追加・変更する

部員1人につきファイルを1つ、`_members/` に作ります。
**このファイルがそのまま自己紹介ページになります。**
ファイル名がURLになるので、半角英数字とハイフンで付けてください
（`yamada-taro.md` → `/members/yamada-taro/`）。

```markdown
---
title: 山田 太郎        # 名前
joined: 2021-10         # 入社年月（YYYY-MM）
department: 開発部      # 部署
platform: Java版        # プラットフォーム（Java版 / 統合版 / Switch など）
---

はじめまして、山田太郎です。
会社の社屋をマイクラで再現するのが目標です。

## 好きな建築

レッドストーン回路を使った自動装置を作るのが好きです。
```

上の `---` で挟まれた部分が一覧カードに表示される情報、
その下が自己紹介ページの本文（Markdownで自由に書けます）です。

- `title` 以外の項目は、空欄にすると表示されません
- 本文を空にすると、一覧に「自己紹介」ボタンが出ません（書いた人だけボタンが出ます）
- 一覧は入社年月の古い順に並びます
- 人数は自動計算なので、ファイルを置くだけで反映されます
- 退部した場合はファイルを削除します

## 固定ページを追加する

リポジトリ直下に `ページ名.markdown` を作り、front matter に
`layout: page` / `title` / `permalink` を書きます。
ヘッダーのナビに出すかどうかは `_config.yml` の `header_pages` で決めます。
このページのようにナビに出したくない場合は、そこに追加しないでください。
あわせて `noindex: true` を書くと検索避けになります。

## ローカルで確認する

```bash
bundle exec jekyll serve
```

http://localhost:4000/hdc-mine-club/ で確認できます。
`_config.yml` を編集したときだけ、サーバーの再起動が必要です。

## 公開する

`main` ブランチにpushすると、GitHub Actions が自動でビルドして公開します。

```bash
git push origin main
```

- 実行状況: リポジトリの Actions タブ
- 公開URL: <https://hdc-lyu.github.io/hdc-mine-club/>
- 反映まで1〜2分かかります

## 見た目を変える

配色・フォントサイズは `assets/main.scss` の先頭にある変数にまとまっています。

| 変数 | 用途 |
|---|---|
| `$hdc-blue` | 会社色の青（ヘッダー・リンク） |
| `$mc-green` | マイクラの草の緑（アクセント・主ボタン） |
| `$mc-wood` | 活動一覧の看板の木の色 |
| `$mc-font` | ドットフォント（DotGothic16） |
| `$fs-page-title` 他 | フォントサイズのスケール |

フォントサイズはドットフォントが綺麗に出るよう8の倍数で揃えています。
変更するときも8の倍数（16 / 24 / 32 / 40）に揃えてください。

ドットフォント DotGothic16 は外部CDNを使わず `assets/fonts/` に同梱しています。
社内など外部通信が制限された環境でも同じ見た目で表示されます。
ライセンスは SIL Open Font License 1.1（`assets/fonts/dotgothic16/OFL.txt`）で、
再配布にあたりライセンス全文を同梱する必要があるため削除しないでください。

サイト全体をドットフォントにしたい場合は `assets/main.scss` に次を追加します。

```scss
body { font-family: $mc-font; }
```

## 構成

| ファイル | 役割 |
|---|---|
| `_config.yml` | サイト名・説明・ナビの順番・記事URLの形式 |
| `_members/` | 部員1人につき1ファイル。自己紹介ページを兼ねる |
| `assets/images/posts/` | 活動記録に載せる写真 |
| `_includes/photo.html` | 写真を1枚表示する部品 |
| `_posts/` | 活動記録 |
| `_layouts/home.html` | トップページ（最近の活動3件を表示） |
| `_layouts/member.html` | 部員の自己紹介ページの体裁 |
| `_includes/head.html` | 検索避けなどのhead設定 |
| `_sass/dotgothic16.scss` | 同梱フォントの定義（自動生成・手編集不可） |
| `assets/fonts/` | 同梱フォント本体とライセンス |
| `_layouts/post.html` | 記事ページ（進捗の表示を含む） |
| `_includes/item-icon.html` | 活動の種類のアイコン（自動生成・手編集不可） |
| `_sass/strata-textures.scss` | フッターの地層の模様（自動生成・手編集不可） |
| `_tools/` | 上の2つとファビコン・共有画像を作り直すスクリプト（`python3 _tools/ファイル名.py`） |
| `_plugins/thumbnail_image.rb` | 記事の thumbnail を共有プレビュー画像に使う設定 |
| `_data/next_event.yml` | トップの「次回の活動」 |
| `404.html` | 存在しないページを開いたときの画面 |
| `assets/main.scss` | 配色・フォント・レイアウト |
| `.github/workflows/jekyll.yml` | 公開の自動化 |
