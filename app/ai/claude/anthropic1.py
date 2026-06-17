import anthropic

client = anthropic.Anthropic()
# model="claude-sonnet-4-6",
#
message = client.messages.create(
  model="claude-haiku-4-5-20251001",
  max_tokens=1024,
  messages=[{
    "role": "user",
    "content": "Hello, Claude"
  }]
)
print(message.content[0].text)