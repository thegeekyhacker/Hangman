import re
import random
import operator

def get_word(filename):
    obj1 = open(f"{filename}","r")
    wordlist=obj1.read().split()
    index = random.randint(0,len(wordlist)-1)
    return wordlist[index],wordlist

def make_sec_word(word):
    length = len(word)
    sec_word = ""
    for i in range(length):
        sec_word = sec_word + "_"
    return sec_word

def find_occurrences(s,ch):
    return [i for i,letter in enumerate(s) if letter == ch]

def vowel_count(wordlist,guessed):
    voweld = {'a':0,'e':0,'i':0,'o':0,'u':0}
    for i in voweld:
        if i not in guessed:
            for j in wordlist:
                for k in j:
                    if k == i:
                        voweld[i] = voweld[i] + 1
    voweld = sorted(voweld.items(),key=operator.itemgetter(1),reverse=True)
    return voweld

def consonant_count(wordlist,guessed):
    consonantd = {'b':0,'c':0,'d':0,'f':0,'g':0,'h':0,'j':0,'k':0,'l':0,'m':0,'n':0,'p':0,'q':0,'r':0,'s':0,'t':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    for i in consonantd:
        if i not in guessed:
            for j in wordlist:
                for k in j:
                    if k == i:
                        consonantd[i] = consonantd[i]+1
    consonantd = sorted(consonantd.items(),key=operator.itemgetter(1),reverse=True)
    return consonantd

def wordlist_reduction(wordlist,sec_word):
    nwl = wordlist.copy()
    length = len(sec_word)
    for i in wordlist:
        if len(i) != length:
            nwl.remove(i)
    return nwl

def realted_reduction(wordlist,sec_word,guessed):
    strtemp = ""
    for i in sec_word:
        if i != "_":
            strtemp += i
    strtemp = strtemp.replace(" ","")
    for i in guessed:
        if i not in strtemp:
            strtemp += i
    regtemp = f"[a-z^{strtemp}]"
    sec_word = sec_word.replace("_",regtemp)
    sec_word = sec_word.replace(" ","")
    temp = list(sec_word)
    temp.insert(0,'^')
    temp.append('$')
    reg_exp = "".join(temp)
    new  = []
    # print(reg_exp)
    for i in wordlist:
        # print(i)
        if bool(re.match(reg_exp,i)) == True:
            new.append(i)
    return new  

def guess_char(guess,guessed,word):
    if guess not in guessed and guess in word:
        return True
    else:
        return False

def replace_occurences(word,guess,sec_word):
    l = find_occurrences(word,guess)
    for i in l:
        temp = list(sec_word)
        temp[i] = guess
        sec_word = "".join(temp)
    return sec_word

def main():
    check = False
    word,wl = get_word("words_250000_train.txt")
    sec_word = make_sec_word(word)
    guessed = []
    wl = wordlist_reduction(wl,sec_word)
    tries = 6
    print("the word is : ",word)
    for i in range(5):
        vowels = vowel_count(wl,guessed)
        guess = vowels[0][0]
        chk1 = guess_char(guess,guessed,word)
        if (chk1 == True):
            sec_word = replace_occurences(word,guess,sec_word)
            if sec_word == word:
                print(f"You have successfully guessed the word in {tries} tries and it was {sec_word}")
                check = True
                return check
            guessed.append(guess)
            wl = realted_reduction(wl,sec_word,guessed) 
        else:
            tries -= 1
            guessed.append(guess)
            if tries <= 0:
                check = False
                print(f"You were unable to guess the word {word} within 6 tries")
                return check
    
    wl = realted_reduction(wl,sec_word,guessed)
    print(sec_word)
    print("Og")
    print(wl)
    for i in range(21):
        consonants = consonant_count(wl,guessed)
        guess = consonants[0][0]
        chk2 = guess_char(guess,guessed,word)
        if chk2 == True:
            sec_word = replace_occurences(word,guess,sec_word)
            print(sec_word)
            if sec_word == word:
                check = True
                print(f"You have successfully guessed the word in {tries} tries and it was {sec_word}")
                return check
            guessed.append(guess)
            wl = realted_reduction(wl,sec_word,guessed)
            print(wl)
        else:
            tries -= 1
            guessed.append(guess)
            if tries<=0:
                check = False
                print(f"You were unable to guess the word {word} within 6 tries")
                return check
    print("Secret word : ",sec_word)
    print("Tries : ",tries)
    print("Guessed Characters : ",guessed)


success = 0
failure = 0
for i in range(100):
    print(i+1)
    check = main()
    if (check == True):
        success += 1
    else:
        failure += 1
print("Number of Success : ",success)
print("Number of Failure : ",failure)
print("Successs Percentage : ",(success/(success + failure))*100)