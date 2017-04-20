import fileinput
import numpy as np
import pandas as pd

amazon = fileinput.FileInput('/Users/Chenny/Documents/aml_homework/amazon-meta.txt')

def extraWord(s):
    s = ''.join([i for i in s if not i.isdigit()])
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace(' & ', ' ')
    wordList = s.strip().split('|')
    for i in range(len(wordList)):
        wordList[i] = wordList[i].strip()
    while '' in wordList:
        wordList.remove('')
    left_word = wordList[3:]
    for word in left_word:
        if len(word) < 2:
            left_word.remove(word)
    stri = " ".join(str(x) for x in left_word)
    return stri

def extraWord_ori(s):
    s = ''.join([i for i in s if not i.isdigit()])
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    wordList = s.strip().split('|')
    for i in range(len(wordList)):
        wordList[i] = wordList[i].strip()
    left_word = wordList[3:]
    for word in left_word:
        if len(word) < 2:
            left_word.remove(word)
    stri = " ".join(str(x) for x in left_word)
    return stri


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
    stri = "Books|" + stri
    return stri

dicts = {}
for line in amazon:
    line=line.strip().split(':')
    if line[0] == 'ASIN':
        dicts[line[1].strip()]={}
        var = line[1].strip()
    if line[0] == 'categories':
        dicts[var]['categories'] = []
    # Only append books
    if 'Books' in line[0]:
        # has cleaned book business category
        dicts[var]['categories'].append(line[0])
    if line[0] == 'similar':
        item = line[1].strip().split()
        dicts[var]['similar'] = item[2:]

business_word = []
i = 0
for ASIN in dicts:
    i += 1
    print i
    if 'similar' not in dicts[ASIN] or 'categories' not in dicts[ASIN]:
        continue
    if not dicts[ASIN]['similar']:
        continue
    ASIN_category_string = extraWord_ori(dicts[ASIN]['categories'])
    if 'Business' not in ASIN_category_string and 'Books' not in ASIN_category_string:
        continue

    similar_keyword = []
    for asin in dicts[ASIN]['similar']:
        if asin not in dicts:
            continue
        if 'categories' not in dicts[asin]:
            continue
        for asin_category in dicts[asin]['categories']:
            similar_keyword.append(extraWord(asin_category))
    similar_keyword_string = " ".join(str(x) for x in similar_keyword)
    if not similar_keyword:
        continue
    similar_keyword_string = similar_keyword_string.replace('General', '')
    similar_keyword_string = similar_keyword_string.replace('Business', '')

    for category in dicts[ASIN]['categories']:
        if 'Business' not in category:
            continue
        business_word.append([clean_title(category), similar_keyword_string])
        print [clean_title(category), similar_keyword_string]

gen_business = pd.DataFrame(business_word)
gen_business.columns = ['Category', 'Key words']
gen_business.to_csv('gen_business.csv', index=False)

#gen_business = pd.read_csv("/Users/Chenny/Documents/aml_homework/gen_business.csv")
b_words = gen_business['Key_words'].values.tolist()
b_words = " ".join(str(x) for x in b_words)
b_words = b_words.replace(' & ', ' ')
b_words = b_words.replace(' General', '')
b_words = b_words.strip().split(' ')

b_words_count = pd.Series(b_words).value_counts()
b_words_count.columns = ['word', 'word_number']
b_words_count.to_csv('b_words_count.csv')


business_count = pd.Series(gen_business)[:, 0].value_counts()
business_count.columns = ['word', 'word_number']
business_count.to_csv('parenting_count.csv')



dicts = {}
for line in amazon:
    line=line.strip().split(':')
    if line[0] == 'ASIN':
        dicts[line[1].strip()]={}
        var = line[1].strip()
    if line[0] == 'categories':
        dicts[var]['categories'] = []
    # Only append books
    if 'Video' in line[0] and 'DVD' not in line[0]:
        # has cleaned book business category
        dicts[var]['categories'].append(line[0])
    if line[0] == 'similar':
        item = line[1].strip().split()
        dicts[var]['similar'] = item[2:]

category_word = []
length = 0
i = 0
for ASIN in dicts:
    i += 1
    print i
    if 'similar' not in dicts[ASIN] or 'categories' not in dicts[ASIN]:
        continue
    if not dicts[ASIN]['similar']:
        continue

    similar_keyword = []
    for asin in dicts[ASIN]['similar']:
        if asin not in dicts:
            continue
        if 'categories' not in dicts[asin]:
            continue
        for asin_category in dicts[asin]['categories']:
            similar_keyword.append(extraWord(asin_category))
    similar_keyword_string = " ".join(str(x) for x in similar_keyword)

    for category in dicts[ASIN]['categories']:
        if 'Parenting' not in category:
            continue
        category_word.append([category, similar_keyword_string])
        print [category, similar_keyword_string]

gen_parenting = pd.DataFrame(category_word)
gen_parenting.columns = ['Category', 'Key_words']
gen_parenting.to_csv('gen_parenting.csv', index=False)



gen_parenting = pd.read_csv("/Users/Chenny/Documents/aml_homework/gen_parenting.csv")
p_words = gen_parenting['Key_words'].values.tolist()


p_words = " ".join(str(x) for x in p_words)
p_words = p_words.replace(' & ', ' ')
p_words = p_words.replace(' General', '')
p_words = p_words.strip().split(' ')

p_words_count = pd.Series(p_words).value_counts()
p_words_count.columns = ['word', 'word_number']
p_words_count.to_csv('p_words_count.csv')


def clean_title(s):
    s = ''.join([i for i in s if not i.isdigit()])
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace(' & ', ' ')
    wordList = s.strip().split('|')
    for i in range(len(wordList)):
        wordList[i] = wordList[i].strip()
    while '' in wordList:
        wordList.remove('')
    left_word = wordList[3:]
    for word in left_word:
        if len(word) < 2:
            left_word.remove(word)
    stri = " ".join(str(x) for x in left_word)
    return stri

#gen_parenting = pd.read_csv("/Users/Chenny/Documents/aml_homework/gen_parenting.csv")
parenting_count = gen_parenting['Category'].values.tolist()
parenting_count = [clean_title(x) for x in parenting_count]


parenting_count = " ".join(clean_title(x) for x in parenting_count)
parenting_count = parenting_count.replace(' & ', ' ')
parenting_count = parenting_count.strip().split(' ')


parenting_count = pd.Series(parenting_count).value_counts()
parenting_count.columns = ['word', 'word_number']
parenting_count.to_csv('parenting_count.csv')



dicts = {}
for line in amazon:
    line=line.strip().split(':')
    if line[0] == 'ASIN':
        dicts[line[1].strip()]={}
        var = line[1].strip()
    if line[0] == 'categories':
        dicts[var]['categories'] = []
    # Only append books
    if 'Music' in line[0]:
        # has cleaned book business category
        dicts[var]['categories'].append(line[0])
    if line[0] == 'similar':
        item = line[1].strip().split()
        dicts[var]['similar'] = item[2:]

category_word = []
i = 0
for ASIN in dicts:
    i += 1
    print i
    if 'similar' not in dicts[ASIN] or 'categories' not in dicts[ASIN]:
        continue
    if not dicts[ASIN]['similar']:
        continue

    similar_keyword = []
    for asin in dicts[ASIN]['similar']:
        if asin not in dicts:
            continue
        if 'categories' not in dicts[asin]:
            continue
        for asin_category in dicts[asin]['categories']:
            similar_keyword.append(extraWord(asin_category))
    if not similar_keyword:
        continue
    similar_keyword_string = " ".join(str(x) for x in similar_keyword)
    similar_keyword_string = similar_keyword_string.replace('Music', '')
    similar_keyword_string = similar_keyword_string.replace('Classical', '')
    similar_keyword_string = similar_keyword_string.replace('General', '')
    similar_keyword_string = similar_keyword_string.replace('featured', '')
    similar_keyword_string = similar_keyword_string.replace('Featured', '')
    similar_keyword_string = similar_keyword_string.replace('composers', '')
    similar_keyword_string = similar_keyword_string.replace('Composers', '')
    similar_keyword_string = similar_keyword_string.replace('categories', '')
    similar_keyword_string = similar_keyword_string.replace('Categories', '')
    similar_keyword_string = similar_keyword_string.replace('works', '')
    similar_keyword_string = similar_keyword_string.replace('Works', '')
    similar_keyword_string = similar_keyword_string.replace('historical', '')
    similar_keyword_string = similar_keyword_string.replace('Historical', '')
    similar_keyword_string = similar_keyword_string.replace('forms', '')
    similar_keyword_string = similar_keyword_string.replace('Forms', '')
    similar_keyword_string = similar_keyword_string.replace('outlet', '')
    similar_keyword_string = similar_keyword_string.replace('Outlet', '')
    similar_keyword_string = similar_keyword_string.replace('period', '')
    similar_keyword_string = similar_keyword_string.replace('Period', '')
    similar_keyword_string = similar_keyword_string.replace('genre', '')
    similar_keyword_string = similar_keyword_string.replace('Genre', '')
    similar_keyword_string = similar_keyword_string.replace('Genres', '')
    similar_keyword_string = similar_keyword_string.replace('all', '')
    similar_keyword_string = similar_keyword_string.replace('All', '')
    similar_keyword_string = similar_keyword_string.replace('under', '')
    similar_keyword_string = similar_keyword_string.replace('Under', '')
    similar_keyword_string = similar_keyword_string.replace('title', '')
    similar_keyword_string = similar_keyword_string.replace('century', '')
    similar_keyword_string = similar_keyword_string.replace('Century', '')
    similar_keyword_string = similar_keyword_string.replace('modern', '')
    similar_keyword_string = similar_keyword_string.replace('Modern', '')
    similar_keyword_string = similar_keyword_string.replace('Bargains', '')
    similar_keyword_string = similar_keyword_string.replace('Bargain', '')
    similar_keyword_string = similar_keyword_string.replace('bargain', '')
    similar_keyword_string = similar_keyword_string.replace('bargains', '')
    similar_keyword_string = similar_keyword_string.replace('title', '')
    similar_keyword_string = similar_keyword_string.replace('Title', '')
    similar_keyword_string = similar_keyword_string.replace('cds', '')
    similar_keyword_string = similar_keyword_string.replace('Cds', '')
    similar_keyword_string = similar_keyword_string.replace('CDS', '')
    similar_keyword_string = similar_keyword_string.replace('nonopera', '')
    similar_keyword_string = similar_keyword_string.replace('Nonopera', '')
    similar_keyword_string = similar_keyword_string.replace('Composer', '')

    for category in dicts[ASIN]['categories']:
        if 'Classical' not in category:
            continue
        category_word.append([clean_title(category), similar_keyword_string])

gen_classical = pd.DataFrame(category_word)
gen_classical.columns = ['Category', 'Key_words']
gen_classical.to_csv('gen_classical.csv', index=False)


gen_classical = pd.read_csv("/Users/Chenny/Documents/aml_homework/gen_classical.csv")
classical_count = pd.Series(gen_classical['Category']).value_counts()
classical_count.columns = ['word', 'word_number']
classical_count.to_csv('classical_count.csv')


gen_classical= pd.read_csv("/Users/Chenny/Documents/aml_homework/gen_classical.csv")
c_words = gen_classical['Key_words'].values.tolist()


c_words = " ".join(str(x) for x in c_words)
c_words = c_words.replace(' & ', ' ')
c_words = c_words.replace(' General', '')
c_words = c_words.replace('Classical', '')
c_words = c_words.strip().split(' ')

c_words_count = pd.Series(c_words).value_counts()
c_words_count.columns = ['word', 'word_number']
c_words_count.to_csv('c_words_count.csv')
