from fcm import Fcm
import math
import argparse


class Lang:

    def __init__(self, fcm):
        self.fcm = fcm

    def compare_files(self, filename):
        
        alphabet = set()
        with open(filename, "r") as f:
            alphabet = set(f.read())
        alphabet_size = len(set(self.fcm.alphabet) | alphabet)
        

        with open(filename, "r") as f:
            total_bits = 0
            #table_total = self.fcm.total_counter + self.fcm.alpha * self.fcm.alphabet_size**(self.fcm.k+1)
            context = f.read(self.fcm.k)      # read k size
            stream = []
            
            while (next_char := f.read(1)):
            
                if context in self.fcm.filled_table:
                    row_sum = self.fcm.filled_table[context]["sum"] + self.fcm.alpha * alphabet_size
                    if next_char not in self.fcm.filled_table[context]:
                        prob = (self.fcm.alpha) / row_sum
                    else:
                        prob = (self.fcm.filled_table[context][next_char] + self.fcm.alpha) / row_sum
                    
                    #context_prob = (self.fcm.filled_table[context]["sum"] + self.fcm.alpha * alphabet_size) / table_total
                    stream.append(- math.log2(prob))
                    total_bits +=  - math.log2(prob)
                
                else:    
                    row_sum = self.fcm.alpha * alphabet_size
                    total_bits +=  -math.log2(self.fcm.alpha / row_sum)
                    stream.append(-math.log2(self.fcm.alpha / row_sum))
                    
                context = context[1:] + next_char

        return total_bits, stream



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument("--repfile", metavar="file", type=str, default="../langs/train/eng.utf8")
    parser.add_argument("--testfile", metavar="file", type=str, default="../langs/test/test_english.utf8")
    parser.add_argument('-a', '--alpha', type=float, default=0.000000000001, help='alpha parameter')

    args = vars(parser.parse_args())


    en = Fcm(args["repfile"] , 3, args["alpha"], 0)

    print("Total Entropy: ", en.calculate_global_entropy() * (en.total_counter + en.k))
    print("Mean Entropy: ", en.calculate_global_entropy())

    print("numero de cenas ", en.total_counter + en.k)

    l = Lang(en)

    print("Number of bits: ", l.compare_files(args["testfile"])[0])


