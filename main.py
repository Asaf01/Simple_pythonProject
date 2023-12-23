import random
import time

word_database = [
    "always,be,yourself", "keep,it,cool", "python,is,rock",
    "be,the,change", "all,is,hell", "believe,in,yourself",
    "cash,is,king, commit,or,quit", "do,it,yourself", "game,is,over"
]

def choose_word():
    return random.choice(word_database).split(',')

def display_word(words, guessed_letters):
   return ', '.join(''.join(l if l in guessed_letters else '_' for l in word)for word in words)

def guess_the_word():
    words_to_guess, guessed_letters, start_time, points, correct_guesses = choose_word(), set(), time.time(), 0, set()

    print("***Guess the Word???***")

    while True:
        elapsed_time = time.time() - start_time
        print("\nCurrent words:", display_word(words_to_guess, guessed_letters))
        guess = input("Enter a letter: ").lower()

        if guess == "quit":
            break

        if len(guess) != 1:
            print("Invalid input. Please renter a single letter.")
            continue

        guessed_letters.add(guess)

        if any(guess in word for word in words_to_guess):
            print("correct")
            points += 5 * sum(guess in word and guess not in correct_guesses for word in words_to_guess)
            correct_guesses.update(guess for word in words_to_guess if guess in word)
            if correct_guesses == set(letter for word in words_to_guess for letter in word):
                print("correct You guessed one of the words.")
                break
        else:
            points -= 1
            print(f"Wrong guess! Points: {points}")

    if correct_guesses == set(letter for word in words_to_guess for letter in word) and elapsed_time < 30:
        points += 100

    print(f"\nGame Over! Your total points: {points}")
    print("The correct words were:", ', '.join(words_to_guess))

if __name__ == "__main__":
    guess_the_word()
# change
