import json
import asyncio
import websockets
from nllw.test_strings import src_0_en
import time

# async def test_client():
#     uri = "ws://localhost:8765"
#     async with websockets.connect(uri) as ws:
#         await ws.send("Hello, this is a streaming")
#         response = await ws.recv()
#         print(json.loads(response))
#         await ws.send("translation example in real time.")
#         response = await ws.recv()
#         print(json.loads(response))

# asyncio.run(test_client())

# async def test_long_text():
#     uri = "ws://localhost:8765"
#     for text in src_0_en:
#         start_time = time.perf_counter()
#         async with websockets.connect(uri) as ws:
#             await ws.send(text)
#             response = await ws.recv()
#             end_time = time.perf_counter()
#             print(json.loads(response))
#         print(f"Processing time for text of length {len(text)}: {end_time - start_time:.4f} seconds")

# asyncio.run(test_long_text())

async def test_long_text():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        for text in src_0_en:
            start_time = time.perf_counter()
            await ws.send(text)
            response = await ws.recv()
            end_time = time.perf_counter()
            print(json.loads(response))
            print(f"Processing time for text of length {len(text)}: {end_time - start_time:.4f} seconds")

asyncio.run(test_long_text())