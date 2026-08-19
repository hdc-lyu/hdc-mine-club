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

`categories` は活動の種類（お知らせ / 建築 / 探検 / イベント など）です。
活動一覧では看板の上にタグとして表示されます。

本文はMarkdownで書きます。1つ目の段落が一覧ページの抜粋になります。

## 部員を追加・変更する

`_data/members.yml` を編集します。1人分が1ブロックです。

```yaml
- name: 山田 太郎     # 氏名（必須）
  mcid: yamada_taro   # MinecraftのプレイヤーID（空欄なら非表示）
  joined: 2023-04     # 入社年月
  role: 建築班        # 役割（任意。氏名の横にバッジ表示）
  comment: ひとこと   # 任意
```

人数の表示は自動計算なので、追記するだけで反映されます。

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

サイト全体をドットフォントにしたい場合は `assets/main.scss` に次を追加します。

```scss
body { font-family: $mc-font; }
```

## 構成

| ファイル | 役割 |
|---|---|
| `_config.yml` | サイト名・説明・ナビの順番・記事URLの形式 |
| `_data/members.yml` | 部員一覧のデータ |
| `_posts/` | 活動記録 |
| `_layouts/home.html` | トップページ（最近の活動3件を表示） |
| `_includes/head.html` | フォント読み込み・検索避けの設定 |
| `assets/main.scss` | 配色・フォント・レイアウト |
| `.github/workflows/jekyll.yml` | 公開の自動化 |
