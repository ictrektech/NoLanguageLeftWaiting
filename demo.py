import nllw
import time
from nllw.test_strings import src_0_en

# 1. 加载翻译模型（支持英文作为源语言)
model = nllw.load_model(
    src_langs=["eng_Latn"],
    nllb_backend="ctranslate2",
    # nllb_backend="transformers",
    nllb_size="600M"  
)

# 2. 创建流式翻译器（英文到中文）
translator = nllw.OnlineTranslation(  
    model,  
    input_languages=["eng_Latn"],
    output_languages=["zho_Hans"]
)

# print original test strings
for i, text in enumerate(src_0_en):
    print(f"Test string {i+1}: {text}")


for text in src_0_en:
    start_time = time.perf_counter()
    tokens = [nllw.TimedText(text)]
    translator.insert_tokens(tokens)
    validated, buffer = translator.process()
    print(f"Input length: {len(text)} | validated: {validated} | buffer: {buffer}")
    end_time = time.perf_counter()
    print(f"Processing time: {end_time - start_time:.4f} seconds")

# # 3. 流式翻译示例 - 第一段输入  
# start_time = time.perf_counter()
# tokens = [nllw.TimedText('Hello, this is a streaming')]
# translator.insert_tokens(tokens)  
# validated, buffer = translator.process()  
# print(f"validated: {validated} | buffer: {buffer}")
# end_time = time.perf_counter()
# print(f"Processing time: {end_time - start_time:.4f} seconds")
  
# # 4. 继续输入第二段  
# start_time = time.perf_counter()
# tokens = [nllw.TimedText('translation example in real time.')]
# translator.insert_tokens(tokens)  
# validated, buffer = translator.process()  
# print(f"validated: {validated} | buffer: {buffer}")
# end_time = time.perf_counter()
# print(f"Processing time: {end_time - start_time:.4f} seconds")