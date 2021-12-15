from fcm import Fcm
from lang import Lang
import glob
import argparse


class Findlang:
    
    def __init__(self, train, k, alpha):
        self.k = k
        self.alpha = alpha
        self.train = train

    def find(self, target):

        files = glob.glob(f"{self.train}*")
        bits = []
        for f in files:
            en = Fcm(f , self.k, self.alpha, 0)
            l = Lang(en)
            bits.append(l.compare_files(target)[0])

        lang = files[bits.index(min(bits))] 
        print(lang)
        # returns the name of the file that has the lower number of needed bytes to encode
        return lang   


if __name__ == "__main__":

    # python3 findlang.py -r "../langs/train/" -t "../langs/test/test_english.utf8"

    parser = argparse.ArgumentParser(description='Lang')
    parser.add_argument("-r","--reference", type=str, required=True)
    parser.add_argument("-t,","--target", type=str, required=True)
    parser.add_argument('-k', type=int,
                    help='size of the sequence', default=1)
    parser.add_argument('-a', '--alpha', type=float, default=0.01,
                    help='alpha parameter')

    args = vars(parser.parse_args())

    train_folder = args["reference"]

    f = Findlang(train_folder, args["k"], args["alpha"])
    f.find(args["target"])