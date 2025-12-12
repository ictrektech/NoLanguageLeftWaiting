import time
import nllw
from nllw.test_strings import src_0_en


def measure_latency(translator, text: str):
    """测量一次翻译调用的耗时，并返回 validated 与 buffer 结果。"""
    tokens = [nllw.TimedText(text)]
    translator.insert_tokens(tokens)

    start_time = time.perf_counter()
    validated, buffer = translator.process()
    end_time = time.perf_counter()

    latency = end_time - start_time
    return latency, validated, buffer


def main():
    # 加载模型
    model = nllw.load_model(
        src_langs=["eng_Latn", "zho_Hans"],
        nllb_backend="ctranslate2",  # 可改为 transformers
        nllb_size="600M",
        ctranslate2_compute_type="int8_bfloat16"
    )

    # 多组测试用例：覆盖不同长度与语言方向
    test_cases = [
        # ---------------- Chinese → English ----------------
        {
            "name": "ZH→EN | Short sentence",
            "translator": nllw.OnlineTranslation(model, ["zho_Hans"], ["eng_Latn"]),
            "text": "加载翻译模型并创建流式翻译器。"
        },
        {
            "name": "ZH→EN | Multiple sentences",
            "translator": nllw.OnlineTranslation(model, ["zho_Hans"], ["eng_Latn"]),
            "text": "今天天气很好。我们正在测试翻译延迟。请确保输出符合预期。"
        },
        {
            "name": "ZH→EN | Medium paragraph",
            "translator": nllw.OnlineTranslation(model, ["zho_Hans"], ["eng_Latn"]),
            "text": (
                "随着机器翻译技术的不断发展，实时翻译系统逐渐成为许多应用场景中的关键组件。"
                "在本次测试中，我们希望评估模型在不同输入长度下的处理延迟和稳定性。"
                "这些结果将有助于我们优化系统结构和参数配置。"
            )
        },
        # {
        #     "name": "ZH→EN | Long text",
        #     "translator": nllw.OnlineTranslation(model, ["zho_Hans"], ["eng_Latn"]),
        #     "text": "这是一个长文本。" * 200
        # },

        # ---------------- English → Chinese ----------------
        {
            "name": "EN→ZH | Short sentence",
            "translator": nllw.OnlineTranslation(model, ["eng_Latn"], ["zho_Hans"]),
            "text": "This is a test for translation latency."
        },
        {
            "name": "EN→ZH | Multiple sentences",
            "translator": nllw.OnlineTranslation(model, ["eng_Latn"], ["zho_Hans"]),
            "text": (
                "We are evaluating the speed of the online translation pipeline. "
                "Each sentence may produce different latency characteristics. "
                "The goal is to observe how the model behaves under various input sizes."
            )
        },
        # {
        #     "name": "EN→ZH | Medium paragraph",
        #     "translator": nllw.OnlineTranslation(model, ["eng_Latn"], ["zho_Hans"]),
        #     "text": " ".join(src_0_en)
        # },
        # {
        #     "name": "EN→ZH | Long text",
        #     "translator": nllw.OnlineTranslation(model, ["eng_Latn"], ["zho_Hans"]),
        #     "text": ("This is a long text for latency testing. " * 200)
        # },
    ]

    # ---------------- 执行所有测试 ----------------
    for case in test_cases:
        print(f"\n===== {case['name']} =====")
        latency, validated, buffer = measure_latency(case["translator"], case["text"])
        print(f"Processing time: {latency:.4f} seconds")
        print(f"Final validated translation:\n{validated}")
        print(f"Final buffer translation:\n{buffer}")


if __name__ == "__main__":
    main()
