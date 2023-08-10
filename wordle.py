import random
import math

from colorama import Fore, Back, Style, init
init(autoreset=True) #Ends color formatting after each print statement
from wordle_wordlist import get_word_list

def get_feedback(guess: str, secret_word: str) -> str:
    '''Generates a feedback string based on comparing a 5-letter guess with the secret word. 
       The feedback string uses the following schema: 
        - Correct letter, correct spot: uppercase letter ('A'-'Z')
        - Correct letter, wrong spot: lowercase letter ('a'-'z')
        - Letter not in the word: '-'

       For example:
        - get_feedback("lever", "EATEN") --> "-e-E-"
        - get_feedback("LEVER", "LOWER") --> "L--ER"
        - get_feedback("MOMMY", "MADAM") --> "M-m--"
        - get_feedback("ARGUE", "MOTTO") --> "-----"

        Args:
            guess (str): The guessed word
            secret_word (str): The secret word
        Returns:
            str: Feedback string, based on comparing guess with the secret word
    '''
    if len(guess) != 5 or len(secret_word) != 5:
        return ""
    
    guess = guess.lower()
    secret_word = secret_word.lower()
    secret_word_copy = ["-", "-", "-", "-", "-"]

    for i in range(len(secret_word)):
        secret_word_copy[i] = secret_word[i]

    feedback_string_list = ["-", "-", "-", "-", "-"]


    for i in range(len(secret_word)):
        if guess[i] == secret_word[i]:
            feedback_string_list[i] = guess[i].upper()
            secret_word_copy[i] = "-"


    for i in range(len(guess)):
        if guess[i] in secret_word_copy and guess[i] != secret_word[i]:
            feedback_string_list[i] = guess[i].lower()
            index = secret_word_copy.index(guess[i])
            secret_word_copy[index] = "-"

    feedback_string = ""
    for i in range(len(feedback_string_list)):
        feedback_string = feedback_string + feedback_string_list[i]

    return feedback_string


def get_AI_guess(word_list: list[str], guesses: list[str], feedback: list[str]) -> str:
    '''Analyzes feedback from previous guesses (if any) to make a new guess
        Args:
            word_list (list): A list of potential Wordle words
            guesses (list): A list of string guesses, could be empty
            feedback (list): A list of feedback strings, could be empty
        Returns:
         str: a valid guess that is exactly 5 uppercase letters
    '''
    '''---iterate through word list, for each word: find all masks, their probablility of occurence, and the amount of information they give.
        with that information find the average amount of expected information for each word in word list.
        ---guess that word and you will recieve a mask
        ---word list is restricted based on mask
        ---repeat this process until one word remains'''


    updated_word_list = []
    for i in range(len(guesses)):
        for e in word_list:
            if get_feedback(guesses[i], e) ==  feedback[i]:
                updated_word_list.append(e)
        word_list = updated_word_list[:]
        updated_word_list = []

    word_dict = {}
    information_dict = {}
    word_list_length = len(word_list)
    for word in word_list:
        word_dict[word] = {}
        for word2 in word_list:
            mask = get_feedback(word, word2)
            word_dict[word][mask] = word_dict[word].setdefault(mask, 0) + 1/word_list_length
    
    optimal_guess = word_list[0]
    for word in word_list:
        for mask in word_dict[word]:
            p = word_dict[word][mask]
            information_dict[word] = information_dict.setdefault(word, 0) + p*math.log(1/p, 2)
        if information_dict[word] > information_dict[optimal_guess]:
            optimal_guess = word  

    return optimal_guess, information_dict

def get_user_percentile(guess: str, information_dict: dict, ai_guess: str, out_of_list_information: float):
    

    if guess.upper() not in information_dict.keys():
        ai_information_bit = information_dict[ai_guess.upper()]

        bit_list = [i for i in information_dict.values()]
        bit_list.append(out_of_list_information)
        bit_list.sort(reverse=True)

        index_user_bit = bit_list.index(out_of_list_information)
        percentile = 100 - ((index_user_bit / len(bit_list)) * 100)

        return percentile, out_of_list_information, ai_information_bit, -1
    else:
        user_information_bit = information_dict[guess.upper()]
        ai_information_bit = information_dict[ai_guess.upper()]

        bit_list = [i for i in information_dict.values()]
        bit_list.sort(reverse=True)

        index_user_bit = bit_list.index(user_information_bit)
        percentile = 100 - ((index_user_bit / len(bit_list)) * 100)

        return percentile, user_information_bit, ai_information_bit, 0




def play_game(word_list: list[str], guess_list: list[str], feedback_list: list[str]):
    original_word_list = word_list[:]
    guesses = 0
    secret_word = random.choice(get_word_list())
    output = Back.WHITE + "       " + Style.RESET_ALL + '\n' + Back.WHITE + ' ' + Style.RESET_ALL
    while True:
        guess = input("What is your guess?")
        guess = guess.upper()
        while len(guess) != 5:
            print("Your guess must be 5 letters long. Please try again.")
            guess = input("What is your guess?")
            guess = guess.upper()
        while guess not in original_word_list:
            print("Your guess must be a real word. Please try again")
            guess = input("What is your guess?")
            guess = guess.upper()        
            
        ai_guess, information_dict = get_AI_guess(word_list, guess_list, feedback_list)
        

        guesses += 1
        feedback = get_feedback(guess, secret_word)
        feedback_list.append(feedback)
        guess_list.append(guess)
        updated_word_list = []
        for e in word_list:
           if get_feedback(guess, e) ==  feedback_list[-1]:
               updated_word_list.append(e)
        previous_word_list = word_list[:]
        word_list = updated_word_list[:]
        word = ''

        out_of_list_p = len(word_list) / len(previous_word_list)
        out_of_list_information = math.log(1/out_of_list_p, 2)

        percentile, user_information_bit, ai_information_bit, sub_optimal_checker = get_user_percentile(guess, information_dict, ai_guess, out_of_list_information)




        for i in range(len(feedback)):
            if feedback[i] == '-':
                word += Back.LIGHTBLACK_EX + guess[i].upper() + Style.RESET_ALL
            elif feedback[i] == feedback[i].upper():
                word += Back.GREEN + guess[i].upper() + Style.RESET_ALL
            elif feedback[i] == feedback[i].lower():
                word += Back.YELLOW + guess[i].upper() + Style.RESET_ALL
        output += word + Back.WHITE  + ' ' + Style.RESET_ALL + '\n' + Back.WHITE + ' ' + Style.RESET_ALL
        print(output + Back.WHITE + '      ' + Style.RESET_ALL)

        if user_information_bit >= ai_information_bit and ai_information_bit != 0 and guess.lower() != ai_guess.lower():
            print("You made a sub-optimal guess. Given the feedback from your previous guesses, your guess could not have been the correct answer.")
            print(f"Despite this, your guess had an actual bit rate of {user_information_bit}!")
            print(f"The most optimal guess had an expected bit rate of {ai_information_bit}")
            print("While your guess yielded a higher bit rate than the expected bit rate of the optimal guess, your guess was not the most optimal guess, given its expected bit rate.")
        elif ai_information_bit == 0 and guess.lower() != secret_word.lower():
            print("You made a sub-optimal guess. Given the feedback from your previous guesses, your guess could not have been the correct answer.")
            print(f"Your guess had an actual bit rate of {user_information_bit}!")
            print(f"The most optimal guess had an expected bit rate of {ai_information_bit} because the ai has narrowed it down to a single word.")
        else:
            if sub_optimal_checker == -1:
                if user_information_bit == 0:
                    print("You made a sub-optimal guess. Given the feedback from your previous guesses, your guess could not have been the correct answer.")
                    print(f"Your guess' actual bit rate was {user_information_bit}.")
                    print(f"The most optimal guess had an expected bit rate of {ai_information_bit}")
                else:
                    print("You made a sub-optimal guess. Given the feedback from your previous guesses, your guess could not have been the correct answer.")
                    print(f"Despite this, your guess was in the {percentile} percentile of guesses and its actual bit rate was {user_information_bit}!")
                    print(f"The most optimal guess had an expected bit rate of {ai_information_bit}")
            else:
                print(f"Your guess was in the {percentile} percentile of guesses and its expected bit rate was {user_information_bit}!")
                print(f"The most optimal guess had an expected bit rate of {ai_information_bit}")


        if user_information_bit == ai_information_bit and ai_information_bit != 0:
            if ai_information_bit == 1 and guess.lower() != secret_word.lower():
                pass
            else:
                 print("You made the most optimal guess!")
            


        if guess.lower() == secret_word.lower():
            print("You won in " + str(guesses) + " guesses!")
            break
        if guesses >= 6:
            print("Too many guesses, you lose.")
            break



    word_list = original_word_list
    guess_list = []
    feedback_list = []
    guesses = 0

    print("This is the most optimal game:")
    output = Back.WHITE + "       " + Style.RESET_ALL + '\n' + Back.WHITE + ' ' + Style.RESET_ALL
    while True:
        guess, information_dict = get_AI_guess(word_list, guess_list, feedback_list)
        guesses += 1
        feedback = get_feedback(guess, secret_word)
        feedback_list.append(feedback)
        guess_list.append(guess)
        updated_word_list = []
        for e in word_list:
           if get_feedback(guess, e) ==  feedback_list[-1]:
               updated_word_list.append(e)
        word_list = updated_word_list[:]
        word = ''
        for i in range(len(feedback)):
            if feedback[i] == '-':
                word += Back.LIGHTBLACK_EX + guess[i].upper() + Style.RESET_ALL
            elif feedback[i] == feedback[i].upper():
                word += Back.GREEN + guess[i].upper() + Style.RESET_ALL
            elif feedback[i] == feedback[i].lower():
                word += Back.YELLOW + guess[i].upper() + Style.RESET_ALL
        output += word + Back.WHITE  + ' ' + Style.RESET_ALL + '\n' + Back.WHITE + ' ' + Style.RESET_ALL
        print(output + Back.WHITE + '      ' + Style.RESET_ALL)
        if guess.lower() == secret_word.lower():
            print("The AI won in " + str(guesses) + " guesses!")
            break
        if guesses >= 6:
            print("The AI was not able to win.")
            break
        

if __name__ == "__main__":
    play_game(get_word_list(), [], [])
