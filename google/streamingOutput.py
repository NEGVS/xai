from google import genai

client = genai.Client(api_key="AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U")

response = client.models.generate_content_stream(
    model="gemini-2.0-flash", contents="总之，我拥有的是一种基于训练数据的，用于理解和生成文本的记忆能力，而不是像人类一样的个人记忆。翻译为意大利语"
)

# Streaming output
# By default, the model returns a response after completing the entire text generation process. You can achieve faster interactions by using streaming to return instances of GenerateContentResponse as they're generated.
for chunk in response:
    print(chunk.text, end="")

# Woof woof! I am dog! Happy to sniff butts and chase squirrels for you. How can I help you today? Maybe you want me to fetch something? Or just give you some happy licks? Arf!
# 汪汪！我是狗狗！很高兴为你闻屁屁和追松鼠。今天有什么我可以帮你的吗？也许你想让我去叼东西？或者只是给你一些快乐的舔舔？ 嗷呜！
