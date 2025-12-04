import asyncio
import websockets
import json

async def test_connection():
    try:
        # Test English to Chinese
        uri = "ws://localhost:27100/ws/transcribe?src_lang=en&target_lang=zh"
        print(f"Connecting to: {uri}")

        async with websockets.connect(uri) as ws:
            print("Connected successfully!")

            # Send a simple test message
            test_message = "do you remember that era?"
            print(f"Sending: {test_message}")
            await ws.send(test_message)

            # Receive response
            response = await ws.recv()
            print(f"Received response: {response}")

            # Parse JSON response
            data = json.loads(response)
            print(f"Parsed response: {data}")

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

async def test_reverse():
    try:
        # Test Chinese to English
        uri = "ws://localhost:27100/ws/transcribe?src_lang=zh&target_lang=en"
        print(f"\nConnecting to: {uri}")

        async with websockets.connect(uri) as ws:
            print("Connected successfully!")

            # Send a simple test message
            test_message = "可以用以上命令来测试。"
            print(f"Sending: {test_message}")
            await ws.send(test_message)

            # Receive response
            response = await ws.recv()
            print(f"Received response: {response}")

            # Parse JSON response
            data = json.loads(response)
            print(f"Parsed response: {data}")

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

async def main():
    await test_connection()
    await test_reverse()

if __name__ == "__main__":
    asyncio.run(main())