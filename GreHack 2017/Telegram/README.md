# GreHack 2017 - Telegram
### Crypto - 150 pts

    To all operators:

    Several operators from other companies have been complaining to us. There are often not able to decode our telegrams because some of you do not respect blanks properly. Therefore, we ask you to complete all your telegrams with a checksum: you are required to append the number of words followed by the number of letters the initial message contains at the end of each message you send.

    The Direction Board

    The flag format *is not* GH17{xxxxxx}
    
This challenge was given with an audio file. The audio sound like a morse code but hard to transcript. Indeed, it had no spaces between chars.

First step was to translate the sound to actual dots and lines. For this, I could have used audacity, but I used this [website](https://morsecode.scphillips.com/labs/audio-decoder-adaptive/)
After using that, we get the following "Morse" code: `...--.--.-----..-..-...---.    ....-    .----.----`

According to the challenge text, we can easily understand that there are 4 words. The second part can't be something else than 11. So 4 words, 11 letters.

My first step was to create an algorithm that would generate all possible values for the morse code that we got. Indeed the beginning `...` for example could either mean `EEE` or `EI` or `IE` or `S`.

Here is the code that generate all output. 2 files are created. Output has EVERYTHING, and output_11 has only the possibilites that have 11 chars. Seperating by words seemed hard to do and maybe not useful.

```python
morse_alphabet = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", " ": "/", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----"}

reverse_morse_alphabet = {value: key for key, value in morse_alphabet.iteritems()}


def possible_decode(morse):
    to_compute = [('', morse)]
    final = []
    first_letter = ''
    while len(to_compute) != 0:
        begin, morse = to_compute.pop()

        # Just to do a tiny logging to know where we're at
        if len(begin) > 0 and begin[0] != first_letter:
            first_letter = begin[0]
            print("Working on {}".format(first_letter))

        # Means we reached the end of the morse code to decode
        if len(morse) == 0:
            final.append(begin)
            continue

        # Morse chars are coded with 1 up to 5 "chars" i.e dots or lines
        for i in xrange(min(5, len(morse))):
            if morse[:i + 1] in reverse_morse_alphabet:
                to_compute.append((begin + reverse_morse_alphabet[morse[:i + 1]], morse[i + 1:]))

    # Output writing
    with open('output', 'w+') as f:
        f.write(str(final))
    complete_final = []
    for word in final:
        if len(word) == 11:
            complete_final.append(word)
    with open('output_11', 'w+') as f:
        f.write(str(complete_final))

possible_decode("...--.--.-----..-..-...---.")
```

Sadly, the output is huge (25 073 081 entries for `output`, 427 743 for `output_11`) and thus the flag is very hard to catch. I searched for `FLAG` and found a bunch of words finishing with `FLAG`, showing me I was on the right track.
At this point I was a bit lazy to check them all and decided I'll look at the challenge later on.

One of my teammates decided to try decoding the morse by hand. He ended up seeing a possible `I WA`. Which quickly ended up as `I WANT`. Running the code on the rest of the undecoded morse gave us pretty easily the right flag: `IWANTTOFLAG`.


## Alternative (and better) method

A method we could have used and I would like to talk about here is checking possibilities with an English Dictionnary. As I said, finding `FLAG` was pretty easy.
For this method, I use an English dictionnary of the 1000 most used English words found [on this gist](https://gist.github.com/deekayen/4148741) and increment the score of an entry every time a word in found in it.

Here is the little code snippet to do so:
```python
with open('output_11_flag', 'r') as f:
    possible_list = eval(f.read())

with open('english-dictionnary.txt', 'r') as f:
    word_list = f.readlines()

score = {}
max_score = 0
for entry in possible_list:
    score[entry] = 0
    for word in word_list:
        if word.strip().lower() in entry.lower():
            score[entry] += 1
    if score[entry] > max_score:
        flag = entry
        max_score = score[entry]

print "The most probable flag is: {}".format(flag)
```

This code directly gives us `IWANTTOFLAG`. The longer the flag is, the better this solution is obviously. The choice of the dictionnary also depends on the size of your "possible entries" list. The bigger this list is, the smaller the dictionnary should be in order to compute it in a reasonnable time.