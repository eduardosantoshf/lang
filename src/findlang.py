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
        """ Predicts the language for a given target file"""
        
        files = glob.glob(f"{self.train}*")
        bits = []

        # for each of the languages calculate the number of bits
        for f in files:
            en = Fcm(f , self.k, self.alpha, 0)
            l = Lang(en)
            total_bits = l.compare_files(target)[0]
            bits.append(total_bits)

        # get the lower amount of bits
        lang = files[bits.index(min(bits))] 

        lang_name = lang.split("/")[-1].split(".")[0]

        # returns the name of the file that has the lower number of needed bytes to encode
        return lang_name

    def find_all(self, target_folder):
        """ Calculates the top 5 predicted language for each target in the target_folder"""
        
        targets = glob.glob(f"{target_folder}*.utf8")
        train = glob.glob(f"{self.train}*")
        
        target_m = [[] for _ in range(len(targets))]
        for i, tr in enumerate(train):
            
            en = Fcm(tr, self.k, self.alpha, 0)
            l = Lang(en)
            
            for j, ta in enumerate(targets):
                total_bits = l.compare_files(ta)[0]
                target_m[j].append((total_bits, tr))
            
        res = {}
        for i, x in enumerate(target_m):
            res[targets[i]] = [l[1] for l in sorted(target_m[i])[:5]]
            
        return res
                
if __name__ == "__main__":

    # python3 findlang.py -r "../langs/train/" -t "../langs/test/english.utf8"

    parser = argparse.ArgumentParser(description='Lang')
    parser.add_argument("-r","--reference", type=str, required=True)
    parser.add_argument("-t,","--target", type=str, default="../langs/test/test_english.utf8")
    parser.add_argument('-k', type=int,
                    help='size of the sequence', default=1)
    parser.add_argument('-a', '--alpha', type=float, default=0.01,
                    help='alpha parameter')

    args = vars(parser.parse_args())

    train_folder = args["reference"]

    f = Findlang(train_folder, args["k"], args["alpha"])
    language = f.find(args["target"])
    print("The selected text is predicted to have the " + language + " language.")
