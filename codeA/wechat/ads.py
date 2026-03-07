from wechaty import Wechaty, Message

class MyBot(Wechaty):
    async def on_message(self, msg: Message):
        print(f"收到消息: {msg.text()}")

if __name__ == "__main__":
    bot = MyBot()
    bot.start()