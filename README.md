# ai-wordle-solver

The ai wordle solver uses information theory and statistical entropy to make the best guesses on a random wordle word. This program allows the user to challenge the ai guesser and see if they can beat the machine! After each guess, the program will return the expected bit rate of the ai's guess and the bit rate of the user guess. Based on these results, the user may view how efficient their guesses are. At the end, the program will print out the most efficient game that could have been played based on expected bit rate.




A few clarifications should be made about this program:
------------------------------------------------------------------------------------------------------------------------------------------------------
- In the context of this application, bit rate refers to the amount of information that is revealed/removed when a certain guess is made. If a guess cuts the possible remaining words in half, it is said to have a bit rate of 1. If it cuts the remaining words into a quarter, it is said to have a bit rate of 2. 
- When a guess is made, there are nearly 3^5 possible unique feedbacks that can be returned. This is due to the fact that each letter has 3 possible feedbacks, green, yellow, or gray, and there are 5 letters. Because some masks are not possible, for example, 4 green letters and a yellow letter, the number of possible masks is a little less than 3^5.
- The ai calculates the expected bit rate of each word by creating all of its masks. Then, the ai places all of the other words in the word list into whichever maks they fit into. Next, the probability of each mask is found by dividing the number of words in a mask by the toal number of words in the word list. This probability, p, is then multiplied by the log base 2 (1/p). Lastly, the product that was just found is calculated for each mask and the sum of all of those products yields the expected information/bit rate for a certain guess. The ai does this for each word in the word list and the word with the highest bit rate is chosen as the guess.
- After the guess is made, the program compares the guess to the secret word, and feedback, green, yellow, and gray tiles, is given.
- The word list is then updated to only contain the words in the mask which corresponds to the feedback given after the previous guess had been made.
- It should be noted that a guess can be the secret word but still not be a wise or optimal guess, which is why a correct answer may be in a low percentile. This is because the ai relies on expected information. Sometimes the actual information yield may be higher or lower than the expected information yield but the expected information yield is the most efficient method in the long run.
- Concerning a returned percentile, the max percnetile is 100. A higher percentile is better while a lower percentile is worse.
