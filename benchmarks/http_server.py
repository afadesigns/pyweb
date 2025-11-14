import asyncio
from aiohttp import web
import os

async def handle(request):
    file_path = os.path.join(os.path.dirname(__file__), 'test_page.html')
    with open(file_path, 'r') as f:
        content = f.read()
    return web.Response(text=content, content_type='text/html')

async def main():
    app = web.Application()
    app.router.add_get('/test_page.html', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8000)
    await site.start()
    print("Server started on http://127.0.0.1:8000")
    # Keep the server running indefinitely until interrupted
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")