# This Python program gets an integer input from a user and outputs the same integer in words
# for example: 89,475,872,465 -->
# eighty nine billion, four hundred and seventy five million, eight hundred and seventy two thousand, four hundred and sixty five

# Get input from a user

from functools import reduce

# get integer from user input
x = input('Please enter a positive integer less than 10**18: \n')
x = int(x)

# ------------------------------------------------------------
# Initialize

# highest power of 10 this program can deal with
power = 17

# dictionary of powers of 1000 in words
powers_in_words = {(0,1,2): '', (3,4,5): 'thousand', (6,7,8): 'million', (9,10,11): 'trillion', (12,13,14): 'gazillion', (15,16,17): 'super - gazillion'}

small_dict = {0: '', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
              6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
              11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
              16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen'}

big_dict = {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty', 6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'}

# this number remembers the 10th multiple so that we can add it to the ones multiple
combined_num = 0

# list of integers that make up the input integer x
# initialize to empty list
int_list = []

# word is only the word for a multiple of thousand, ex. five hundred and fifty three million
word = []
# combined_word is the combined list of all the words composing the entire integer, all the multiples of thousand
# that's the word representing the entire input integer x
combined_word = []

# ------------------------------------------------------------
# Define functions

def int_to_word_decider(largest_remaining_multiple_of_10, largest_power_of_10):
    '''This function decides what word an integer corresponds to,
        based on it's power of 10 and the integer       
    '''
    word = []
    # this number remembers the 10th multiple so that we can add it to the ones multiple
    global combined_num    

    if largest_power_of_10 == 2:
        word.append(small_dict[largest_remaining_multiple_of_10])
        word.append('hundred')
    elif largest_power_of_10 == 1:
        if largest_remaining_multiple_of_10 == 1:
            combined_num += 10
        elif largest_remaining_multiple_of_10 > 1:
            word.append(big_dict[largest_remaining_multiple_of_10])
    else:
        combined_num += largest_remaining_multiple_of_10
        word.append(small_dict[combined_num])

    return word


def hundreds_to_words(int_list):
    '''This function converts a list of integers, representing a number less than 1000 into words.
        Input: int_list
        a list of integers representing a positive integer less than 1000
        this list must be non-empty and only of length 1 or 2 or 3
        the index of each integer represents a power of 10
        ex. a list [6,5,9] represents a number 956

        Output: a string, the integer that the list represents, in words, ex. nine hundred and fifty six
    '''

    word = []
    
    while int_list != []:

        #largest_remaining_multiple_of_10 is the largest multiple of 10 element left in int_list
        largest_remaining_multiple_of_10 = int_list[0]

        #largest_power_of_10 is the power of 10 that largest_remaining_multiple_of_10 is a multiple of
        #or just it's index in the int_list
        largest_power_of_10 = len(int_list)-1

        #update the word represending the integer
        word.append(int_to_word_decider(largest_remaining_multiple_of_10, largest_power_of_10))

        # remove the first element from the remaining int_list that you just took and put into a word
        int_list.pop(0)

    return word

def flatten(nested_list):
    '''This function flattens a list,
    Input: nested list of lists or a flat list (any list)
    Output: a list composed of lowers level elements ex. strings or integers '''

    flat_list = []

    for e in nested_list:
        if isinstance(e, list):
            for i in e:
                if isinstance(i, list):
                    flatten(i)
                else:
                    flat_list.append(i)
        else:
            flat_list.append(e)

    return flat_list

def rm_leading_zeros(int_list):
    '''This function removes leading zeroes from a list of integers
    If the input is a list of all zeroes, the output will be an empty list'''

    while int_list[0] == 0:
        int_list.pop(0)
        if int_list == []:
            break

    return int_list

def rm_trailing_empties(strings_list):
    '''This finction takes a list of strings as input and removes any empty strings
    at the end of the list, returning a new list, such that the last element is a non-empty string
    if strings_list is empty, or contains only empty strings, it returns an empty list'''

    if strings_list == []:
        return strings_list

    strings_list.reverse()
    
    while strings_list[0] == '':
        strings_list.pop(0)
        if strings_list == []:
            break

    strings_list.reverse()
        
    return strings_list
  
def list_to_string(word_list):
    '''This function takes a list of words as input and converts it to a proper sentence with ands ans spaces in the right places'''

    sentence = []
    word_list = rm_trailing_empties(word_list)

    for i in range(len(word_list)):

        e = word_list[i]
        e_is_last = (i == len(word_list)-1)
        
        if e != '':
            sentence.append(e)

            if e_is_last:
                break
   
            if e in powers_in_words.values():
                #if there are only 1 or 2 elements left in word_list after e
                if i >= len(word_list)- 3:
                    sentence.append(' and ')
                else:
                    sentence.append(', ')
            elif e == 'hundred':
                #if the next element is thousand, million, trillion,...
                if word_list[i+1] in powers_in_words.values():
                    sentence.append(' ')
                else:
                    sentence.append(' and ')
            else:
                sentence.append (' ')

    sentence = reduce(lambda x,y: x+y, sentence)
            
    return sentence

# ------------------------------------------------------------
# Convert the input integer x into a list of integers it is composed of int_list
# the index of an integer in int_list corresponds to the power of 10 that it's a multiple of

for p in range(power,-1,-1):
    power_of_10 = x//10**p
    x = x%10**p
    int_list.append(power_of_10)

# remove leading zeroes from int_list
int_list = rm_leading_zeros(int_list)

int_list.reverse()

# ------------------------------------------------------------
# Extract groups of multiples of thousand from the input integer x

# largest power of 10 that x is divisible by
power = len(int_list)-1

# define groups of powers of 1000 of the components of x
group_index = list(range(0,len(int_list),3))


# loop though group_index to group the integers composing x into powers of 1000
i=0

while i< len(group_index)-1:
    
    sub_int_list = int_list[group_index[i]: group_index[i+1]]
    sub_int_list.reverse()
    #remove leading zeros from sub_int_list
    sub_int_list = rm_leading_zeros(sub_int_list)
    powers_tuple = tuple(range(group_index[i], group_index[i+1]))
    
    i += 1
    
    #pass sub_int_list to the hundreds_to_words function and get the <= hundreds number in words  
    word = hundreds_to_words(sub_int_list)
    word = flatten(word)

    if word != []:
        combined_word.append(powers_in_words[powers_tuple])
        combined_word.append(word)
        
    combined_num = 0
        
# get the remaining biggest powers of 10 composing the input integer x
sub_int_list = int_list[group_index[i]:]
sub_int_list.reverse()
#remove leading zeros from sub_int_list
sub_int_list = rm_leading_zeros(sub_int_list)

powers_tuple = tuple(range(group_index[i], group_index[i]+3))

#pass sub_int_list to the hundreds_to_words function and get the <= hundreds number in words
word = hundreds_to_words(sub_int_list)
word = flatten(word)

combined_word.append(powers_in_words[powers_tuple])
combined_word.append(word)
combined_word.reverse()

combined_word = flatten(combined_word)
sentence = list_to_string(combined_word)

print(sentence)
