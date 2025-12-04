import nllw
import time
from nllw.test_strings import src_0_en

model = nllw.load_model(
    src_langs=["eng_Latn","zho_Hans"],
    nllb_backend="ctranslate2",
    # nllb_backend="transformers",
    nllb_size="600M"
)

# 中译英翻译器
translator = nllw.OnlineTranslation(
    model,
    input_languages=["zho_Hans"],
    output_languages=["eng_Latn"]
)

start_time = time.perf_counter()
text = "加载翻译模型并创建流式翻译器。"
tokens = [nllw.TimedText(text)]
translator.insert_tokens(tokens)
validated, buffer = translator.process()
end_time = time.perf_counter()
print(f"Processing time: {end_time - start_time:.4f} seconds")
print(f"Final validated translation: {validated}")
print(f"Final buffer translation: {buffer}")

# 英译中翻译器
translator = nllw.OnlineTranslation(
    model,
    input_languages=["eng_Latn"],
    output_languages=["zho_Hans"]
)

start_time = time.perf_counter()
text = " ".join(src_0_en)
tokens = [nllw.TimedText(text)]
translator.insert_tokens(tokens)
validated, buffer = translator.process()
end_time = time.perf_counter()
print(f"Processing time: {end_time - start_time:.4f} seconds")
print(f"Final validated translation: {validated}")
print(f"Final buffer translation: {buffer}")
