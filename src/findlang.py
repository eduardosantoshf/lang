from fcm import Fcm
from lang import Lang
import glob
import argparse


class Findlang:
    
    def __init__(self, k, alpha):
        self.k = k
        self.alpha = alpha

    def find(self, target):

        files = glob.glob("../langs/train/*")
        bits = []
        for f in files[:5]:
            en = Fcm(f , self.k, self.alpha, 0)
            l = Lang(en)
            bits.append(l.compare_files(target)[0])

        lang = files[bits.index(min(bits))] 
        print(lang)
        # returns the name of the file that has the lower number of needed bytes to encode
        return lang   


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument("--testfile", metavar="file", type=str, default="../langs/test/test_english.utf8")

    args = vars(parser.parse_args())

    f = Findlang(3, 0.000001)
    
    f.find(args["testfile"])