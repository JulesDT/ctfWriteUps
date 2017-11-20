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
