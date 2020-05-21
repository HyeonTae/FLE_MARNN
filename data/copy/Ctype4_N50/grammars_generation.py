import random
import numpy as np
import sys
import argparse
import string
import copy
import os

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--alphabet_size", default=4,
                    type=int, help="Alphabet Size")
parser.add_argument("-n", "--string_max_length", default=50,
                    type=int, help="String max length")
parser.add_argument("-m", "--data_size", default=100000,
                    type=int, help="Number of data")
args = parser.parse_args()

class DataGeneration():
    def __init__(self):
        self.alphabet_set = list(string.ascii_lowercase[:args.alphabet_size])

    def __call__(self):
        f = open("grammar_data.txt", 'w')
        words_list = []
        data_size = args.data_size
        for i in range(1, int(args.string_max_length/2)+1):
            cnt = 0
            max_cnt = int(data_size/(int(args.string_max_length/2)+1-i))
            while(True):
                self.printProgress(len(words_list), args.data_size, 'Progress', 'Complete')
                word = ""
                if cnt >= 4**i*(i*3+1) or cnt >= max_cnt:
                    data_size -= cnt
                    break
                for _ in range(i):
                    word += random.choice(self.alphabet_set)
                temp = ["0" for i in range(len(word))]
                label = ["0" for i in range(len(word))]
                label.extend(temp)
                result = list(word + word)
                result, label = self.error(result, label)
                if result not in words_list:
                    cnt += 1
                    words_list.append(result)
                    f.write("%s\t%s\n" % (
                        " ".join(result), " ".join(label)))
                else:
                    continue

    def Pe(self, n):
        p = [0.1]
        for i in range(n, 0, -1):
            p.append(0.9 * 2/(n * (n+1)) * i)
        return np.random.choice(n+1, 1, p=p)[0]

    def error(self, words, label):
        vocb = dict(zip(self.alphabet_set,range(1,len(self.alphabet_set)+1)))
        l = int(len(words)/2)
        if l is not 0:
            mpoint = len(words) - l
            pe = self.Pe(l)
            nerror = random.sample(range(mpoint, len(words)), pe)
            for i in nerror:
                s = copy.deepcopy(self.alphabet_set)
                s.remove(words[i])
                label[i] = str(vocb.get(words[i]))
                words[i] = random.choice(s)
        return "".join(words), "".join(label)

    def printProgress (self, iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 50):
        formatStr = "{0:." + str(decimals) + "f}"
        percent = formatStr.format(100 * (iteration / float(total)))
        filledLength = int(round(barLength * iteration / float(total)))
        bar = '#' * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix))
        if(iteration == total):
            sys.stdout.write('\n')
        sys.stdout.flush()

if __name__ == "__main__":
    # Data Generation
    dataGeneration = DataGeneration()
    dataGeneration()
    # Data Split
    os.system("shuf grammar_data.txt -o grammar_data_shuf.txt")
    os.system("split -l " + str(int(args.data_size/5*4)) + " grammar_data_shuf.txt")
    os.system("mv xaa data_train.txt")
    os.system("mv xab data_test.txt")
    # Test Data Length Split
    lines = open("data_test.txt").read().strip().split('\n')
    line = [l for l in lines]
    for l in line:
        for pair in [[s for s in l.split('\t')]]:
            length = len(pair[1].split(' '))
            fname = "dev_length/data_test_length_" + str(length) + ".txt"
            with open(fname, 'a') as f:
                f.write("%s\n" % l)

