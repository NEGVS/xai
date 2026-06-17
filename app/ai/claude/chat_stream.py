import anthropic

def chat_stream(prompt: str):
    client = anthropic.Anthropic()
    try:
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
        print()
    except Exception as e:
        print(f"错误: {e}")

# 使用
if __name__ == '__main__':
    chat_stream("你好，Claude")