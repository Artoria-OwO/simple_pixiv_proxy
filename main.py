import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.responses import Response
from aiohttp import ClientSession

HOST = "" #local host here
PORT =  #local port
base_url = "https://i.pximg.net/"
p_headers = {
    "Referer": 'https://www.pixiv.net',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
}

app = FastAPI()

@app.get("/{pixiv_path:path}")
async def read_root(pixiv_path: str):
    path = base_url + pixiv_path
    img_name = path.split("/")[-1]
    async with ClientSession() as c:
        async with c.get(path, headers=p_headers) as rep:
            content = await rep.read()
            if rep.status == 200:
                headers = {
                    "cache-control": "no-cache",
                    "Content-Type": rep.headers['Content-Type'],
                    "Content-Disposition": f'''inline; filename="{img_name}"'''
                }
                return Response(content, headers=headers, media_type="stream")
            return Response("Invalid request", status_code=400)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host=HOST, port=PORT, reload=True)
