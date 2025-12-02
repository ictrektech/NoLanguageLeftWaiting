import asyncio
import websockets
import nllw
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = nllw.load_model(
    src_langs=["eng_Latn"],
    nllb_backend="ctranslate2",
    nllb_size="600M"
)

async def translate_stream(websocket):
    logger.info(f"Client connected: {websocket.remote_address}")

    translator = nllw.OnlineTranslation(
        model,
        input_languages=["eng_Latn"],
        output_languages=["zho_Hans"]
    )

    try:
        async for message in websocket:
            logger.info(f"Received message: {message}")
            print(f"Received message: {message}")

            if not isinstance(message, str):
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid message format. Expected a string."
                }))
                continue

            payload = message.strip()
            if not payload:
                continue

            if len(payload) > 500:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Message too long (max 500 chars)."
                }))
                continue

            try:
                tokens = [nllw.timed_text.TimedText(payload)]
                translator.insert_tokens(tokens)
                validated, buffer = translator.process()

                await websocket.send(json.dumps({
                    "type": "translation",
                    "validated": validated.text if validated else "",
                    "buffer": buffer.text if buffer else ""
                }))
            except Exception as e:
                logger.error(f"Translation error: {e}", exc_info=True)
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": str(e)
                }))

    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client disconnected: {websocket.remote_address}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        logger.info(f"Connection closed: {websocket.remote_address}")


async def main():
    logger.info("Streaming translation server running at ws://localhost:8765")
    async with websockets.serve(translate_stream, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
