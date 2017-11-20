morse_alphabet = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", " ": "/", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----"}

reverse_morse_alphabet = {value: key for key, value in morse_alphabet.iteritems()}


def possible_decode(morse):
    to_compute = [('', morse)]
    final = []
    first_letter = ''
    while len(to_compute) != 0:
        begin, morse = to_compute.pop()
        if len(begin) > 0 and begin[0] != first_letter:
            first_letter = begin[0]
            print("Working on {}".format(first_letter))
        if len(morse) == 0:
            final.append(begin)
            continue
        for i in xrange(min(5, len(morse))):
            if morse[:i + 1] in reverse_morse_alphabet:
                to_compute.append((begin + reverse_morse_alphabet[morse[:i + 1]], morse[i + 1:]))
    with open('output', 'w+') as f:
        f.write(str(final))
    complete_final = []
    for word in final:
        if len(word) == 11:
            complete_final.append(word)
    with open('output_11', 'w+') as f:
        f.write(str(complete_final))
    has_flag = []
    for word in complete_final:
        if 'FLAG' in word:
            has_flag.append(word)
    with open('output_11_flag', 'w+') as f:
        f.write(str(has_flag))


possible_decode("...--.--.-----..-..-...---.")
