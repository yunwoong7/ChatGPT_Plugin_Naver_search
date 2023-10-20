import os
import json
import requests

import quart
import quart_cors
from quart import request, Response

# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# 네이버 API에 요청을 보내기 위한 기본 URL 및 헤더 정보
HOST_URL = "https://openapi.naver.com/v1/search"

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret,
}


@app.route("/news")
async def get_news():
    query = request.args.get("query")
    display = request.args.get("display")
    start = request.args.get("start")
    sort = request.args.get("sort")

    params = {"query": query,
              "display": display,
              "start": start,
              "sort": sort}
    res = requests.get(f"{HOST_URL}/news", headers=headers, params=params)
    body = res.json()

    return Response(response=json.dumps(body), status=res.status_code, mimetype="application/json")


@app.route("/blog")
async def get_blog_posts():
    query = request.args.get("query")
    display = request.args.get("display")
    start = request.args.get("start")
    sort = request.args.get("sort")

    params = {"query": query,
              "display": display,
              "start": start,
              "sort": sort}
    res = requests.get(f"{HOST_URL}/blog", headers=headers, params=params)
    body = res.json()

    return Response(response=json.dumps(body), status=res.status_code, mimetype="application/json")


@app.route("/image")
async def get_images():
    query = request.args.get("query")
    display = request.args.get("display")
    start = request.args.get("start")
    sort = request.args.get("sort")
    filter = request.args.get("filter")

    params = {"query": query,
              "display": display,
              "start": start,
              "sort": sort,
              "filter": filter}
    res = requests.get(f"{HOST_URL}/image", headers=headers, params=params)
    body = res.json()

    return Response(response=json.dumps(body), status=res.status_code, mimetype="application/json")


@app.route("/shop")
async def search_shop():
    query = request.args.get('query')
    display = request.args.get('display')
    start = request.args.get('start')
    sort = request.args.get('sort')
    filter = request.args.get('filter')
    exclude = request.args.get('exclude')

    params = {
        'query': query,
        'display': display,
        'start': start,
        'sort': sort,
        'filter': filter,
        'exclude': exclude
    }

    res = requests.get(f"{HOST_URL}/shop", headers=headers, params=params)  # 비동기가 아닌 동기 호출을 사용합니다.
    body = res.json()

    return Response(response=json.dumps(body), status=res.status_code, mimetype="application/json")


@app.route("/kin")
async def search_kin():
    query = request.args.get('query')
    display = request.args.get('display')
    start = request.args.get('start')
    sort = request.args.get('sort')
    params = {
        'query': query,
        'display': display,
        'start': start,
        'sort': sort
    }

    res = requests.get(f"{HOST_URL}/kin", headers=headers, params=params)
    body = res.json()

    return Response(response=json.dumps(body), status=res.status_code, mimetype="application/json")

@app.route("/local", methods=['GET'])
async def get_local():
    query = request.args.get('query')
    display = request.args.get('display')
    start = request.args.get('start')
    sort = request.args.get('sort')
    params = {
        'query': query,
        'display': display,
        'start': start,
        'sort': sort
    }

    res = requests.get(f"{HOST_URL}/local", headers=headers, params=params)
    body = res.json()

    return Response(response=json.dumps(body), status=res.status_code, mimetype="application/json")


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="localhost", port=5002)


if __name__ == "__main__":
    main()