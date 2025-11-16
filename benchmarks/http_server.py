import asyncio
from aiohttp import web
import os
import argparse
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3Connection, H3_ALPN
from aioquic.h3.events import H3Event, HeadersReceived, DataReceived
from urllib.parse import urlparse

ROOT = os.path.dirname(__file__)
PORT = 8000
URLS_H1 = [f"http://localhost:{PORT}/test_page.html" for _ in range(100)]
URLS_H3 = [f"https://localhost:{PORT}/test_page.html" for _ in range(100)]

async def handle(request):
    with open(os.path.join(ROOT, "test_page.html"), "r") as f:
        return web.Response(text=f.read(), content_type='text/html')

async def run_http1_server():
    app = web.Application()
    app.router.add_get('/test_page.html', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', PORT)
    await site.start()
    print(f"HTTP/1.1 server running at http://127.0.0.1:{PORT}")
    return runner

class H3RequestHandler(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http = H3Connection(self._quic)

    def quic_event_received(self, event):
        if isinstance(event, H3Event):
            self._http.handle_event(event)

    def http_event_received(self, event):
        if isinstance(event, HeadersReceived):
            headers = dict(event.headers)
            path = headers.get(b":path").decode()
            if path == "/test_page.html":
                with open(os.path.join(ROOT, "test_page.html"), "r") as f:
                    body = f.read().encode()
                response_headers = [
                    (b":status", b"200"),
                    (b"content-type", b"text/html"),
                    (b"content-length", str(len(body)).encode()),
                ]
                self._http.send_headers(event.stream_id, response_headers)
                self._http.send_data(event.stream_id, body, end_stream=True)

async def run_http3_server():
    configuration = QuicConfiguration(
        is_client=False,
        alpn_protocols=H3_ALPN,
    )
    configuration.load_cert_chain(
        os.path.join(ROOT, "ssl_cert.pem"),
        os.path.join(ROOT, "ssl_key.pem"),
    )
    server = await serve(
        "127.0.0.1",
        PORT,
        configuration=configuration,
        create_protocol=H3RequestHandler,
    )
    print(f"HTTP/3 server running at https://127.0.0.1:{PORT}")
    return server

async def run_server():
    parser = argparse.ArgumentParser()
    parser.add_argument("--http3", action="store_true")
    args = parser.parse_args()

    if args.http3:
        return await run_http3_server()
    else:
        return await run_http1_server()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(run_server())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()