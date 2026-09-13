# 記事の front matter に thumbnail があれば、その写真を共有プレビュー画像
# （og:image）として使います。jekyll-seo-tag は page.image を見るため、
# 描画の直前に thumbnail から image を設定しています。
Jekyll::Hooks.register :posts, :pre_render do |post|
  thumbnail = post.data["thumbnail"]
  post.data["image"] = "/assets/images/posts/#{thumbnail}" if thumbnail
end
