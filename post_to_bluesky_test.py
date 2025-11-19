import os
import requests
from atproto import Client, client_utils, models

def run():
    # GitHub Secrets から読み込み
    username = os.environ["BSKY_IDENTIFIER"]
    password = os.environ["BSKY_APP_PASSWORD"]

    client = Client()
    builder = client_utils.TextBuilder()
    builder.text("This is API test. This post is supposed to be posted automatically.\n")
    builder.link("https://www.youtube.com/watch?v=BY_XwvKogC8", 
                 "https://www.youtube.com/watch?v=BY_XwvKogC8")

    # 画像取得
    prices_img = requests.get("https://i.ytimg.com/vi/BY_XwvKogC8/maxresdefault.jpg").content

    # BlueSkyログイン
    client.login(username, password)

    # 画像アップロード
    priceblob = client.upload_blob(prices_img)

    # 埋め込み設定
    embed = models.AppBskyEmbedExternal.Main(
        external=models.AppBskyEmbedExternal.External(
            title="CHIHIRO - BILLIE EILISH (Official Music Video)",
            description="YOU MUST LISTEN",
            uri="https://www.youtube.com/watch?v=BY_XwvKogC8",
            thumb=priceblob.blob
        )
    )

    # 投稿送信
    post = client.send_post(builder, embed=embed)

    print(f"Posted to Bluesky: {post.uri}")


if __name__ == "__main__":
    run()