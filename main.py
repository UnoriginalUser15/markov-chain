import string
import random



def tokenise_data():
    with open("input.txt", encoding="utf8") as f:
        # reads txt
        raw_text = f.read().lower()

        lower_case_raw = raw_text.lower()
        # creates list of all the words in the text
        words = lower_case_raw.split()
        # strips the punctuation for the words
        words = [
            w.strip(string.punctuation)
            for w in lower_case_raw.split()
            if w.strip(string.punctuation)
        ]
    
    return words


def create_ngram_transition(transitions: dict, words: list, order: int):
    """
    Takes in a list of the words in the corpus (text) and creates a transition
    matrix from it.\n
    -----------------------
    Takes in 2 arguments:\n
    transitions = dict\n
    words = list\n
    order = int\n
    'order' is refering to how many words it looks back in the text
    """
    
    state: tuple
    next_word: str

    for i in range(len(words) - order):
        state = tuple(words[i : i + order])
        next_word = words[i + order]

        # creates dict entry if word(s) doesn't already exist
        if state not in transitions:
            transitions[state] = []
        
        transitions[state].append(next_word)
    
    return transitions


def generate_text(transitions: dict, order: int, num_word: int):
    output_list = []
    
    # gets a random word to start with
    key_list = list(transitions.keys())
    state = random.choice(key_list)


    for i in range(num_word - order):
        if state not in transitions:
            state = random.choice(
                list(transitions.keys())
            )
            output_list.extend(list(state))
        else:
            output_list.append(random.choice(transitions[state]))
            # slide the window forward
            state = tuple(output_list[-order:])

    return " ".join(output_list)

### HELPER FUNCTIONS ###

def print_transitions(transitions: dict):
    for word, followers in transitions.items():
        print(f"{word} -> {followers}")

    print(f"\nnum of unique keys: {len(transitions)}")



if __name__ == "__main__":

    words = tokenise_data()
    # determines how many words back it looks when generating the text e.g 2 = 2 words back
    # imagine it as how much 'context' it gets
    nth_order = 2

    transitions = {}

    transitions = create_ngram_transition(transitions, words, nth_order)

    output = generate_text(transitions, nth_order, 50)

    # writes the output to a text file
    with open("output.txt", "w", encoding="utf8") as f:
        f.write(output)
