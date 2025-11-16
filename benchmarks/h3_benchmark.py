import asyncio
import timeit
import argparse
from rust_scraper import scrape_urls_concurrent, scrape_urls_concurrent_h3
from http_server import run_server, URLS_H1, URLS_H3

async def run_scrape_http1():
    await scrape_urls_concurrent(URLS_H1, "p", 100)

async def run_scrape_http3():
    await scrape_urls_concurrent_h3(URLS_H3, "p", 100)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--http3", action="store_true")
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_process = loop.run_until_complete(run_server())

    try:
        if args.http3:
            print("Running benchmark with HTTP/3")
            run_scrape = run_scrape_http3
        else:
            print("Running benchmark with HTTP/1.1")
            run_scrape = run_scrape_http1

        times = timeit.repeat(
            lambda: loop.run_until_complete(run_scrape()),
            number=1,
            repeat=10,
        )

        print(f"Average time: {sum(times) / len(times):.2f}s")

    finally:
        if hasattr(server_process, "shutdown"):
            loop.run_until_complete(server_process.shutdown())
        elif hasattr(server_process, "close"):
            server_process.close()
            loop.run_until_complete(server_process.wait_closed())
        else:
            server_process.terminate()
            loop.run_until_complete(server_process.wait())

if __name__ == "__main__":
    main()