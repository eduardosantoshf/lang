from fcm import Fcm
from lang import Lang
import glob


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

    f = Findlang(3, 0.000001)
    f.find("../langs/test/eng_AU.latn.Aboriginal_English.comb-test.utf8")