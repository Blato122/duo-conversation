import get_data, llmcall

context = []

if __name__ == "__main__":
    get_data.update()
    while True:
        user_message = input()
        context.append({"role": "user", "content": user_message})
        assistant_message = llmcall.answer(context)
        context.append({"role": "assistant", "content": assistant_message})
        print(assistant_message)