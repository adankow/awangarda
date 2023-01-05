import os 
import numpy

words_dictionary = {}
WL_dicitonary = {}
words_count_total = 0
wiersze = []
for file_name in os.listdir("au"):
    if "BAN" == file_name[:3]:
        continue

    with open("au/" + file_name, 'r') as file:
        lines = file.readlines()
        words = []
        for line in lines:
            if len(line) == 0 or line[0].isdigit():
                continue

            filtered_line = line.replace(',', '').replace('.', '').replace('"', '').replace(':', '').replace('-', '') 
            words += filtered_line.split()

        words = [word.lower() for word in words]
        wiersze += [words]
        distinct_words = {}
        for word in words:
            words_dictionary[word] = words_dictionary.get(word, 0) + 1
            words_count_total += 1
            distinct_words[word] = distinct_words.get(word, 1)
        WL = len(distinct_words) / len(words)
        WL_dicitonary[file_name[:len(file_name) - 4]] = WL

words_distribution_dir = {word: (count / words_count_total) for word, count in words_dictionary.items()}
words_distribution_list = sorted([{"word": word, "prob": prob} for word, prob in words_distribution_dir.items()], key=(lambda d: -d["prob"]))
word_ranking = sorted([{"word": word, "count": count} for word, count in words_dictionary.items()], key=(lambda d: -d["count"]))
wl_ranking = sorted([{"title": title, "WL": wl} for title, wl in WL_dicitonary.items()], key = (lambda d: d["WL"]))
#print(word_ranking[20:30])

print(wiersze[:5])

def tri_gram(w1, w2, w3, L1, L2, L3, F):
    bi_next_counter = {}
    tri_next_counter = {}
    bi_cnt = 0
    tri_cnt = 0
    #bi-gram
    for wiersz in wiersze:
        for i in range(len(wiersz) - 2):
            if wiersz[i] == w2 and wiersz[i + 1] == w3:
                bi_next_counter[wiersz[i + 2]] = bi_next_counter.get(wiersz[i + 2], 0) + 1
                bi_cnt += 1
    #tri-gram
    for wiersz in wiersze:
        for i in range(len(wiersz) - 3):
            if wiersz[i] == w1 and wiersz[i + 1] == w2 and wiersz[i + 2] == w3:
                tri_next_counter[wiersz[i + 3]] = tri_next_counter.get(wiersz[i + 3], 0) + 1
                tri_cnt += 1
    #familiarity
    fam_total = 0
    fam_counter = {}
    for wiersz in wiersze:
        for i in range(len(wiersz) - 2):
            if wiersz[i] in [w1, w2, w3] or wiersz[i + 2] in [w1, w2, w3]:
                fam_counter[wiersz[i + 1]] = fam_counter.get(wiersz[i + 1], 0) + 1
                fam_total += 1
    best_prob = 0
    #second_prob = 0
    if bi_cnt == 0: 
        L2 = 0
        bi_cnt = 1
    if tri_cnt == 0:
        L3 = 0
        tri_cnt = 1
    if fam_total == 0:
        F = 0
        fam_total = 1
    print(bi_cnt,tri_cnt, fam_total)
    candidate_list = []
    for word, prob in words_distribution_dir.items():
        prob = L1 * prob + L2 * bi_next_counter.get(word, 0) / bi_cnt + L3 * tri_next_counter.get(word, 0) / tri_cnt + F * fam_counter.get(word, 0) / fam_total
        if (len(word) < 3 and len(w3) < 3) or word == w3 :
            prob = 0
        candidate_list += [(word, prob)]
    sort_list = sorted(candidate_list, key=(lambda x: -x[1]))
    print(sort_list[:5])
    num = int(numpy.random.geometric(0.8) - 1)
    if(num > len(sort_list)):
        num = len(sort_list) - 1
    return sort_list[num][0]
    
print("t:", words_distribution_dir["t"])
start_phrase = ["już", "głowę", "kwadratową"]

for i in range(70):
    w1 = start_phrase[i]
    w2 = start_phrase[i + 1]
    w3 = start_phrase[i + 2]
    w_next = tri_gram(w1, w2, w3, 1/9, 2/9, 1/3, 1/3)
    print(w_next)
    start_phrase += [w_next]

print(' '.join(start_phrase))

#1/12, 1/6, 1/4, 1/2
#jestem polakiem kurwa ja pierdole kurwa czy ja kurwa wyglądam na lokalnego przewodnika co się dzieje z prądem coś tego co się działo bo działo inaczej to jest to wszytko to jest to
#0.7,1/9, 2/9, 1/3, 1/3 
#jestem polakiem kurwa nie tak dużo dla ciebie jak nawet nie możesz sobie poradzić z przesłaniem tego na zawsze z lasu wygnamy! tego do tego że merkuriusz pojawił się po raz ostatni prostu

#znowu nie wyszło sogo? tak nie udało się bo nie ma nic oprócz tej pustki co wygląda na pszne wyraźnie długo tuszone zbyt długo nie zdążył ma się w nie choć tak i