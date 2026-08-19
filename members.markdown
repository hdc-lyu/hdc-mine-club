---
layout: page
title: 部員一覧
permalink: /members/
---

現在の部員は {{ site.data.members | size }} 名です。
入部希望・情報の修正は部長までご連絡ください。

<ul class="member-list">
{%- for member in site.data.members -%}
  <li class="member-card">
    <h2 class="member-name">
      {{ member.name }}
      {%- if member.role %} <span class="member-role">{{ member.role }}</span>{% endif -%}
    </h2>
    <dl class="member-meta">
      {%- if member.mcid %}
      <dt>MCID</dt>
      <dd>{{ member.mcid }}</dd>
      {%- endif %}
      {%- if member.joined %}
      <dt>入社</dt>
      <dd>{{ member.joined }}</dd>
      {%- endif %}
    </dl>
    {%- if member.comment %}
    <p class="member-comment">{{ member.comment }}</p>
    {%- endif %}
  </li>
{%- endfor -%}
</ul>
