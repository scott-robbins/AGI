import time
import os


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def cmd(command, show):
    os.system('%s >> cmd.txt' % command)
    data = []
    for line in open('cmd.txt', 'r').readlines():
        data.append(line)
    if show:
        content = ''
        for e in data:
            content += e
        print content
    os.remove('cmd.txt')
    return data


def load_words(verbose):
    words = swap('/etc/dictionaries-common/words', False)
    if verbose:
        print '%d Unique Words Found ' % len(words)
    return words

