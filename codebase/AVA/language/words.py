import numpy as np
import requests
import utils
import time
import sys
import os


def wikiparser(paragraphs):
    data_out = []
    return data_out


def web_search(link, verbose):
    DATA = {}
    if verbose:
        print '\033[3m Searching for %s\033[0m' % link
    data = requests.get('%s' % (link.replace(' ', '_')))
    headers = data.headers
    cookies = data.cookies
    content = data.content.split('<p>')
    if verbose:
        print 'Headers: %s' % headers
        print 'Cookies: %s' % cookies
        print '%ss Elapsed' % data.elapsed
    print '%d paragraphs received' % len(content)
    for P in range(1, len(content), 1):
        para = content[P]
        DATA[P] = wikiparser(para)
        for element in para.split(' '):
            if len(element.split('href=')) > 1:
                links.append(element.split('href=')[1])
    print '%d Embedded Links in Article' % len(links)
    print '=========================================================='
    print content[1:3]
    children = []
    # Recursively crawl links, as child of current link
    for l in links:
        if len(l.split('"/wiki/')) > 1:
            children.append(l)
    DATA['Links'] = children
    DATA['Headers'] = headers
    DATA['Cookies'] = cookies

    # TODO: FOR DEBUGGING
    file_name = '%s.txt' % link.split('.org/wiki/')[1]
    print 'Dumping to LogFile %s' % file_name
    os.system('touch %s' % file_name)
    dump = ''
    for par in content[1:]:
        for line in par.split('\n'):
            dump += line + '\n'
    open(file_name, 'w').write(dump)
    print '%s Bytes of RAW HTML DUMPED' % os.path.getsize(file_name)
    return DATA


def readfile(file_in, word_bag, verbose):
    data_out = []
    content = utils.swap(file_in, False)
    for line in content:
        for element in line.split(' '):
            if element.replace('.', '').replace(',', '').replace('"', '') not in word_bag:  # TODO: All special chars
                w = element.replace('\n', '')
                data_out.append(w)
                word_bag.append(w)
    if verbose:
        print '%d New Words Found' % len(data_out)
    return word_bag


def add_words(charstr, wordset):
    n_words = len(wordset)
    useful_files = utils.cmd('locate '+charstr, False)
    print '%d Files Found' % len(useful_files)
    for readme in useful_files:
        wordset = readfile(readme.replace('\n', ''), wordset, False)
    print '%d New Words Found [%d Total]' % (len(wordset) - n_words, len(words))
    return wordset


def pull_random_words(word_bag, n):
    rii = np.random.random_integers(0, len(word_bag), n)
    random_words = ''
    ii = 0
    for ind in rii:
        if ii < n - 1:
            random_words += word_bag[ind] + ' '
        else:
            random_words += word_bag[ind]
        ii += 1
    random_words += '.'
    return random_words


tic = time.time()
words = utils.load_words(True)
N_Words = int(len(words))
base = 'https://en.wikipedia.org/wiki/'


if len(sys.argv) >= 2 and '-s' in sys.argv:
    search = '%s%s' % (base, sys.argv[2])
    content = []
    links = []
    data = web_search(search, False)
    # TODO: Log the search, and the children links? (for crawling/connecting pages)
    log_file = search.split(base)[1]+'.txt'


if '-N' in sys.argv:
    if len(sys.argv) == 2:
        print '\033[1m\033[31mIncorrect Usage!\033[0m'
    random_words = pull_random_words(words, int(sys.argv[2]))
    print random_words
print '\033[1m[%ss Elapsed]\033[0m' % str(time.time()-tic)
