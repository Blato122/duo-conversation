import get_data, llmcall

if __name__ == "__main__":
    # dok
    get_data.update()
    while True:
        user_message = input()
        assistant_message = llmcall.answer(user_message)
        print(assistant_message)