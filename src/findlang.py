from fcm import Fcm
from lang import Lang
import glob
import argparse
class Findlang:
    
    def __init__(self, train, k, alpha):
        self.k = k
        self.alpha = alpha
        self.languages = {
                            'eng.utf8': 'English',
                            'pt_pt.utf8': 'Portuguese',
                            'spanish.utf8': 'Spanish'
                        }
        self.train = train
        self.bits = []

    def find(self, target):

        files = glob.glob(f"{self.train}*")

        # for each of the languages calculate the number of bits
        for f in files:
            en = Fcm(f , self.k, self.alpha, 0)
            l = Lang(en)
            total_bits = l.compare_files(target)[0]
            self.bits.append(total_bits)

        # get the lower amount of bits
        lang = files[self.bits.index(min(self.bits))] 

        lang_name = self.languages[lang.rsplit("/", 1)[1]]

        # returns the name of the file that has the lower number of needed bytes to encode
        return lang_name


if __name__ == "__main__":

    # python3 findlang.py -r "../langs/train/" -t "../langs/test/test_english.utf8"

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
