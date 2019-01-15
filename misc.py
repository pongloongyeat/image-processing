# Written by: Pong Loong Yeat
# Last modified: 15/1/2019
# Dependencies: -

from difflib import SequenceMatcher
import numpy as np


##################################################
# Description: Separates a combined string       #
#              into separate strings in a list.  #
# Input:                                         #
#        @result: List or str. String to be      #
#        separated.                              #
# Output:                                        #
#        @: List. List of separated string.      #
# Usage:  separate('toilet\nhospital')           #
# Expect: ['toilet', 'hospital']                 #
##################################################
def separate(result):

    return str(result).splitlines()


##################################################
# Description: Checks similarity between two     #
#              strings.                          #
# Input:                                         #
#        @a,b: Str. Two strings to be checked    #
#              against.                          #
# Output:                                        #
#        @: Float. Similarity score (0 to 1)     #
#           between strings @a and @b.           #
# Usage:  similar('toilet', 'toilei')            #
# Expect: 0.8                                    #
##################################################
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


##################################################
# Description: Returns index value of the most   #
#              similar word.                     #
# Input:                                         #
#        @input_word: Str. Word to be checked    #
#                     against.                   #
#        @input_list: List. List to be checked   #
#                     against.                   #
# Output:                                        #
#        @max_index: Int. Index value of         #
#                    @input_list that has the    #
#                    most similar word.          #
# Usage:  choose_word('toy', ['tok', 'abc')]     #
# Expect: 0                                      #
##################################################
def choose_word(input_word, input_list):

    score = []
    for i in range(0, len(input_list)):
        score.append(similar(input_list[i], input_word))

    max_index = np.argmax(score)
    # print(detected_dir[max_index])
    return max_index
