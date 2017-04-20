import fileinput
import numpy as np
import pandas as pd

amazon = fileinput.FileInput('amazon-meta.txt')


def clean_title(s):
    s = ''.join([i for i in s if not i.isdigit()])
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    wordList = s.strip().split('|')
    for i in range(len(wordList)):
        wordList[i] = wordList[i].strip()
    for word in wordList:
        if len(word) < 2:
            wordList.remove(word)
    while '' in wordList:
        wordList.remove('')
    left_word = wordList[2:]
    stri = "|".join(str(x) for x in left_word)
    return stri



book = []
music = []
dvd = []
video = []
for (i, line) in enumerate(amazon):
    line = line.strip()
    if 'Books' in line and 'group:' not in line:
        book.append(clean_title(line))
    if 'Music' in line and 'group:' not in line:
        music.append(clean_title(line))
    if 'DVDs' in line and 'group:' not in line:
        dvd.append(clean_title(line))
    if 'Videos' in line and 'group:' not in line:
        video.append(clean_title(line))

book_count = pd.Series(book).value_counts()
#book_count.columns = ['book', 'book_number']
#book_count = book_count[:5]
book_count.columns = ['book_category', 'book_count']
book_count.to_csv('book_count.csv')


music_count = pd.Series(music).value_counts()
#music_count.columns = ['music', 'music_number']
#music_count = music_count[:5]
music_count.columns = ['music_category', 'music_count']
music_count.to_csv('music_count.csv')


dvd_count = pd.Series(dvd).value_counts()
#dvd_count.columns = ['dvd', 'dvd_number']
#dvd_count = dvd_count[:5]
dvd_count.columns = ['dvd_category', 'dvd_count']
dvd_count.to_csv('dvd_count.csv')

video_count = pd.Series(video).value_counts()
video_count.columns = ['video_category', 'video_count']
video_count.to_csv('video_count.csv')

subcategories = pd.concat([book_count, music_count, dvd_count, video_count], axis=1)
subcategories.to_csv('subcategories.csv')
