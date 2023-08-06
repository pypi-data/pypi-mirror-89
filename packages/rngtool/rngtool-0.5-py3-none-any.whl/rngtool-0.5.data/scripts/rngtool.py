import argparse
import sys
import random 

def main():

    def rollDice():
        n = random.randint(1,6)
        print('You rolled a',n)

    def coinToss():
        n = random.randint(1,2)
        if n  == 1:
            print('You flipped Heads!')
        elif n == 2:
            print('You flipped Tails!')

    def randOptions():
        n = random.randint(int(sys.argv[2]), int(sys.argv[3]))
        print('You got',n)

    def help():
        print(''' 
        / RNG Tool v0.5 /
        
        ~ Random number generator tool for Linux ~ 

        .Command Index:

            dice: gives number between 1 and 6(Rolling dice)
            
            coin: gives number between 1 and 2(Heads or Tails)

            opt [starting number] [ending number]: gives number between given starting number and ending numbers

                Ex: opt 1 100(output  = number between 1 and 100)
        
        .About:

         Made by: Ayub Farah
         Version: 0.5
         Email: razortyphon@gmail.com
         Repo: https://github.com/ayubf/rngtool

        Thank you for installing!
        
        ''')
    
    if sys.argv[1] == 'dice':
        rollDice()
    elif sys.argv[1] == 'coin':
        coinToss() 
    elif sys.argv[1] == 'opt':
        randOptions()
    elif sys.argv[1] == 'help':
        help()