#!/usr/bin/python


################################################################################
#
# Created By : Egbie 
# Name Of The Program : Password_Generator.Py 
# Created on the 13/09/2015 at 06:10:58 hrs
# This is version : 1 
#
#
# File description 
#
# Generates random password as well as a pass phrase. The length of the password c
# an be between 3 and 22. The idea is to generate a random password that is random.
# The pass phrase is based on the letters of your password. 
#
# BUT A WORD OF CAUTION IF YOU USE THE RANDOMISED PASSWORD GENERATOR PROGRAM 
# TO GENERATE A PASSWORD. PLEASE REMEMBER YOUR PASS PHRASE BEFORE YOU DESTROY IT 
# OR KEEP IT SAFE OTHERWISE THERE IS NO WAY TO UNLOCK THE PASSWORD AND ANY DATA 
# YOU SAVED USING THE PASSWORD WILL BE LOST.
#
################################################################################

import random
import string
import os
from optparse import OptionParser
from time import sleep

LETTERS = string.uppercase

class Dictionary(object):

    def __init__(self, dictionary_file):
        self._words = self.load(dictionary_file)
        self.words_dict = {}
        self.word_dict  = {char: [] for char in LETTERS} # lookup will be used to generate pass phrase

        # create a word dictionary with the length of the word as key and the
        # word as value. e.g {1 : [a], 5:[apple]}
        for word in self._words:
            word = word.strip()
            num = len(word)

            if num not in self.words_dict:
                self.words_dict.setdefault(num, [word])
            else:
                self.words_dict[num].append(word)

            self.word_dict[word[0]].append(word)

    def load(self, f):
        """loads a file into memory"""

        try:
            with open(f, "r") as f:
                dictionary = f.readlines()
                return dictionary
        except IOError:
            exit("[!] The file could not be located, exiting program")

class PasswordGenerator(Dictionary):
    """Generates a random password along with a rememeber pass phrase"""

    def __init__(self, dic_file="dictionary.txt"):
        Dictionary.__init__(self, dic_file)

    def _shuffle_str(self, string):
        """shuffle_str(str) -> return(list)
        Takes a string and shuffles it

        >>> shuffle_str('word')
        'rowd'
        """

        chars = list(string)   # turn the string into a list
        random.shuffle(chars)  # shuffle the chars in the list
        return "".join(chars)

    # private method
    def _get_word(self, num):
        """get_word(int) -> return(str)
        Returns a word of length x
        """
        words = self.words_dict.get(num, None)
        if words:
        	return random.choice(words)  # select a random word
        exit("\nThe mimimum length of the password is 3 and the maximum is 22")

    # private method
    def _gen_pass_phrase(self, password):
        """_gen_pass_phrase(str) -> return(str)
        Takes a random string and generates a pass phrase

        >>> _gen_pass_phrase(superman)
        'SUCCOR  UNABBREVIATED  PERSEVERED  EJECTS  RECOGNITIONS  MACKINAW  AIRDROPS  NONPERISHABLE '
        """

        pass_phrase = []

        for char in password:
            if char.isalpha():

                word = random.choice(self.word_dict[char.upper()])
                if char.islower():
                	word = word.lower()
                
                pass_phrase.append(" ")
                pass_phrase.append(word)
                pass_phrase.append(" ")
            else:
                pass_phrase.append(char)
                
        return "".join(pass_phrase)

    def gen_passwd(self, num):
        """gen_passwd(int) -> return(tuple)
        Generates a password of len n with along with a pass phrase.

        The first part of the tuple is the password and the second part is the
        pass phrase.

        >>> generated(5)
        ('8R5T97tis31E2406', '8 ROUNDED 5 TIPPING 97 TRANSFORM  INVARIANTS  SHASTA 31 EXCLAIMER 2406')
        """

        numbers = "0123456789"
        word = self._get_word(num)

        # make the first half of the word lower cases and the other half uppercase
        first_part, second_part = word[0: (num/2)], word[(num/2):]
        word = first_part.lower() + second_part

        # shuffle the words and numbers in the string
        word, numbers = self._shuffle_str(word), self._shuffle_str(numbers)

        # join the word with number and shuffle again, generate a pass phrase    
        password    = self._shuffle_str(word + numbers)
        pass_phrase = self._gen_pass_phrase(password)
        return password, pass_phrase

# The main program takes in command lines
def main():

    parser = OptionParser("usage%prog -d <dictionary_file> -n < password length>")
    parser.add_option("-n", "--number", dest="pass_num", type=str, help="Length of chars for the password")
    parser.add_option("-d", "--dictionary", dest="dictionary_file", type=str, help="Enter the dictionary file")

    options, args = parser.parse_args()

    if not (options.dictionary_file and options.pass_num and options.pass_num.isdigit()):
        print parser.usage
    else:
       
        pass_num = int(options.pass_num)

        if os.path.exists(options.dictionary_file): # check if the dictionary file exists

            dictionary_obj = Dictionary(options.dictionary_file)
            password_gen   = PasswordGenerator(options.dictionary_file)
            password, pass_phrase = password_gen.gen_passwd(pass_num)

            print"\n[+] Generating password with {} chars along with randomised numbers, please wait....".format(pass_num)
            sleep(0.5)
            print"[+] Generating pass phrase, please wait...."
            sleep(0.5)
            print"[+] Done, password and pass phrase generated"
            sleep(0.5)
            print"\n[+] Your generated random password  is {}".format(password)
            sleep(0.5)
            print"[+] Your generated random pass phrase is :\n\t --> '{}' <--".format(pass_phrase.strip())
            sleep(0.5)
            print"\n[+] Remember to throughly memorise your pass phrase before destroying it or keep it in a safe place!!\n"
            sleep(1)
            print"[+] Goodbye!!"
  

if __name__ == '__main__':
    main()



