def handle_command(msg: str):
    if msg == "help":
        return "可用命令：help, exit"
    return f"你输入的是：{msg}"


def main():
    print("AI Agent CLI 已启动（输入 exit 退出）")

    while True:
        try:
            msg = input(">>> ").strip()

            if msg.lower() == "exit":
                print("Bye")
                break

            print(handle_command(msg))

        except (KeyboardInterrupt, EOFError):
            print("\nBye")
            break


if __name__ == "__main__":
    main()