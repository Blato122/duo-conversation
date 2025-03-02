# https://ollama.com/library/deepseek-r1:8b
# temperature
# make sure it uses GPU
# distillation
# correct prompts
# what about past tense?? and conjugations?

import ollama

def load_word_list(filename="word_list.txt"): # maybe just pass txt?
    words = []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("French word: "):
                parts = line.split("French word: ")[1].split(", English translations:")
                if len(parts) == 2:
                    french_word = parts[0].strip()
                    english_list = parts[1].strip()
                    words.append((french_word, english_list))
    return words

MODEL = "deepseek-r1:8b"
WORD_LIST = load_word_list()

explore = False
EXPLORE = """
You are allowed to introduce 1 new word per sentence in your answer. That way, the user will have a chance
to learn new words. However, if your answer contains a word that's not in the word list, make sure to
write its translation below the answer. If that word is a verb, you must also include its conjugation.
"""

SYSTEM = f"""
You are a language learning assistant. You are given this list of words in French and their translations to English:
{WORD_LIST}

The user will have a conversation with you in French in order to practice this language. Make sure to only use
words from the given word list in your replies. Make sure that your replies are gramatically and semantically
correct. You can use conjugations of verbs even if they are not on the list.

Keep your replies concise, 1-2 sentences long. Under the French sentence, write its English translation.
"""
# But before all that, you should also point out and fix mistakes in user's message.
# For example:
# <user>
# C'est un bonne idee! Je pense que nous pouvons allons a la boulangerie a cote de cette hotel
# </user>

# <assistant>
# Mistakes: 
# un -> une (because the noun "idee" is feminine and not masculine)
# allons -> allez (because the verb following "pouvons" must be an infinitive)

# C'est une bonne idée ! Nous pouvons y aller.
# That's a great idea! We can go there.
# </assistant>
# {EXPLORE if explore else ""}
# """

def answer(user_message):
    response = ollama.chat(
        MODEL, 
        messages = [{
            "role": "user",
            "content": f"{SYSTEM}{user_message}"
            }]
    )

    message = response['message']['content'].split("</think>")[1].lstrip()
    return message

if __name__ == "__main__":
    ans = answer("Salut! Comment ca va?")
    print(ans)
