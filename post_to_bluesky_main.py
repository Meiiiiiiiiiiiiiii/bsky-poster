import os
import requests
from atproto import Client, client_utils, models

def run():
    # GitHub Secrets から読み込み
    username = os.environ["BSKY_IDENTIFIER_MAIN"]
    password = os.environ["BSKY_APP_PASSWORD_MAIN"]

   client = Client()
    builder = client_utils.TextBuilder()
    builder.text("I am accepting commissions! I also am selling "
        "adoptable ponies! Check out my pinned post or Ko-fi if "
        "you are interested!\n")
    builder.link("https://ko-fi.com/metaruscarlet/commissions", "https://ko-fi.com/metaruscarlet/commissions")

    # 画像取得
    prices_img = requests.get("https://storage.ko-fi.com/cdn/generated/ase8uhaewtvcq/2025-09-11_rest-a65e26ee8ce63adca67cc7cd6fe129e0-jf8atzez.jpg").content

    # BlueSkyログイン
    client.login(username, password)

    # 画像アップロード
    priceblob = client.upload_blob(prices_img)

    # 埋め込み設定
    embed = models.AppBskyEmbedExternal.Main(
        external=models.AppBskyEmbedExternal.External(
            title="MetaruScarlet's Ko-fi Page",
            description="MetaruScarlet's commissions/adopts is OPEN!",
            uri="https://www.youtube.com/watch?v=BY_XwvKogC8",
            thumb=priceblob.blob
        )
    )
    
    # 投稿送信
    post = client.send_post(builder, embed=embed)

    print(f"Posted to Bluesky: {post.uri}")


if __name__ == "__main__":

    run()
