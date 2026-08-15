---
layout: page
title: 活動一覧
permalink: /activities/
---

これまでの活動記録です（全 {{ site.posts | size }} 件）。

{% assign date_format = site.minima.date_format | default: "%Y年%-m月%-d日" %}

<ul class="post-list activity-list">
{%- for post in site.posts -%}
  <li>
    <span class="post-meta">{{ post.date | date: date_format }}</span>
    <h2>
      <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
    </h2>
    {%- if post.categories.size > 0 -%}
    <p class="activity-tags">
      {%- for category in post.categories -%}
      <span class="activity-tag">{{ category }}</span>
      {%- endfor -%}
    </p>
    {%- endif -%}
    {{ post.excerpt }}
  </li>
{%- endfor -%}
</ul>

新しい活動記録は `_posts/YYYY-MM-DD-タイトル.markdown` として追加してください。
