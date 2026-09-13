---
layout: page
title: 部員一覧
permalink: /members/
---

現在の部員は {{ site.members | size }} 名です。
参加を希望される方・掲載内容の修正は、部員までご連絡ください。

{% assign members = site.members | sort: "joined" %}

<ul class="member-list">
{%- for member in members -%}
  <li class="member-card">
    <h2 class="member-name">
      {{ member.title }}
      {%- if member.platform %} <span class="member-platform">{{ member.platform }}</span>{% endif -%}
    </h2>
    <dl class="member-meta">
      {%- if member.joined %}
      <dt>入社</dt>
      <dd>{{ member.joined }}</dd>
      {%- endif %}
      {%- if member.department %}
      <dt>部署</dt>
      <dd>{{ member.department }}</dd>
      {%- endif %}
    </dl>
    {%- assign intro = member.content | strip %}
    {%- if intro != "" %}
    <p class="member-link">
      <a class="mc-button mc-button--small" href="{{ member.url | relative_url }}">自己紹介</a>
    </p>
    {%- endif %}
  </li>
{%- endfor -%}
</ul>
