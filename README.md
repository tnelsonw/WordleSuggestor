# Wordle Suggestor

If you are like me and get stuck coming up with words to enter when playing Wordle, then this is the program
for you!

## How to Run
To run this text-based Wordle Suggestor, clone the repository and run `python suggestor.py`. 
It runs with both 5-letter words and 6-letter words, so the first option it will ask you is if you are playing the traditional 
5-letter Wordle or the alternate 6-letter version. Type the respective length of the word to get started.

The program then suggests a couple of initial suggestions for the first word, but feel free to ignore them if you
already have a strategy in place. Type "1" to continue  or "2" for a different initial suggestion. 

For each word you input, the program will first ask for the letter and then the color of the letter, not the entire
word. For instance, if "irate" was your first guess, and "i" was yellow, "e" was green, and the rest of the letters
were blank, you would type:

`i`  
`yellow`  
`r`  
`blank`  
`a`  
`blank`  
`t`  
`blank`  
`e`  
`green`

Note that you can replace "yellow" with "y", "green" with "g", and "blank" with "b" for the same results. 

The program with then systematically eliminate words from the dictionary that are impossible based on the
letters and color values that were inputted and provide you a suggested word.

## Other Notes

This program does run in "hard mode", meaning you have to use the yellow and green letters from previous 
rounds in your next guess, or it will not provide a suggested word. 

The dictionary in this program is not Wordle's official dictionary, since some of the
words I ended up with as suggestions were not in the dictionary when actually playing Wordle. But to account 
for that, I added an option that lets you remove that word if Wordle won't take it. (If anyone does know of an official
Wordle dictionary, let me know). 

I've tested this program with quite an extensive list of words, so I'm fairly confident this program can handle
pretty much any word combination. If you do find bugs though, let me know. This is just a project done for fun
during my free time. 