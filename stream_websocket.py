import asyncio
import websockets
import nllw
import logging
import json
from urllib.parse import urlparse, parse_qs

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Language code mappings
LANG_CODE_MAP = {
    "en": "eng_Latn",
    "zh": "zho_Hans",
    "eng_Latn": "eng_Latn",
    "zho_Hans": "zho_Hans"
}

model = nllw.load_model(
    src_langs=["eng_Latn", "zho_Hans"],
    nllb_backend="ctranslate2",
    nllb_size="600M"
)

async def translate_stream(websocket):
    logger.info(f"Client connected: {websocket.remote_address}")

    # Parse URL parameters from request path
    request_path = websocket.request.path if hasattr(websocket, 'request') else websocket.path
    parsed_url = urlparse(request_path)
    query_params = parse_qs(parsed_url.query)

    # Get language parameters with defaults
    src_lang = query_params.get('src_lang', ['en'])[0].lower()
    target_lang = query_params.get('target_lang', ['zh'])[0].lower()

    # Map language codes
    src_lang_mapped = LANG_CODE_MAP.get(src_lang, src_lang)
    target_lang_mapped = LANG_CODE_MAP.get(target_lang, target_lang)

    logger.info(f"Translation mode: {src_lang_mapped} -> {target_lang_mapped}")

    # Validate language codes
    available_langs = ["eng_Latn", "zho_Hans"]
    if src_lang_mapped not in available_langs or target_lang_mapped not in available_langs:
        await websocket.send(json.dumps({
            "type": "error",
            "message": f"Unsupported language pair. Available: en, zh (mapped to {available_langs})"
        }))
        await websocket.close()
        return

    translator = nllw.OnlineTranslation(
        model,
        input_languages=[src_lang_mapped],
        output_languages=[target_lang_mapped]
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
    logger.info("Streaming translation server running at ws://0.0.0.0:8097/ws/transcribe")
    async with websockets.serve(translate_stream, "0.0.0.0", 8097):
        await asyncio.Future()

asyncio.run(main())
