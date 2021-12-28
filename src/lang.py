from fcm import Fcm
import math
import argparse

class Lang:

    def __init__(self, fcm):
        self.fcm = fcm
        self.alphabet = set()
        self.alphabet_size = 0

    def compare_files(self, filename):
        
        # calculate alphabet size
        with open(filename, "r") as f:
            self.alphabet = set(f.read())
        self.alphabet_size = len(set(self.fcm.alphabet) | self.alphabet)
        

        with open(filename, "r") as f:
            total_bits = 0
            #table_total = self.fcm.total_counter + self.fcm.alpha * self.fcm.alphabet_size**(self.fcm.k+1)
            context = f.read(self.fcm.k)      # read k size
            stream = []
            
            while (next_char := f.read(1)):
            
                if context in self.fcm.filled_table:
                    row_sum = self.fcm.filled_table[context]["sum"] + self.fcm.alpha * self.alphabet_size
                    if next_char not in self.fcm.filled_table[context]:
                        prob = (self.fcm.alpha) / row_sum
                    else:
                        prob = (self.fcm.filled_table[context][next_char] + self.fcm.alpha) / row_sum
                    
                    #context_prob = (self.fcm.filled_table[context]["sum"] + self.fcm.alpha * alphabet_size) / table_total
                    stream.append(- math.log2(prob))
                    total_bits -= math.log2(prob)
                
                else:    
                    row_sum = self.fcm.alpha * self.alphabet_size
                    total_bits -= math.log2(self.fcm.alpha / row_sum)
                    stream.append(- math.log2(self.fcm.alpha / row_sum))
                    
                context = context[1:] + next_char

        return total_bits, stream



if __name__ == "__main__":
    # python3 lang.py -r "../langs/train/eng.utf8" -t "../langs/test/test_english.utf8"
    parser = argparse.ArgumentParser(description='Lang')
    parser.add_argument("-r","--reference", type=str, default="../langs/train/eng.utf8")
    parser.add_argument("-t,","--target", type=str, default="../langs/test/test_english.utf8")
    parser.add_argument('-k', type=int,
                    help='size of the sequence', default=1)
    parser.add_argument('-a', '--alpha', type=float, default=0.01,
                    help='alpha parameter')

    args = vars(parser.parse_args())
    
    target = args["target"]
    reference = args["reference"]
    
    en = Fcm(reference, args["k"], args["alpha"], 0)
    print(f"Average entropy: {en.calculate_global_entropy():.3f}")
    print("Reference Text size: ", en.total_counter + en.k)
    print(f"Total average entropy: {en.calculate_global_entropy()*(en.total_counter + en.k):.3f}")
    l = Lang(en)
    total_bits, stream = l.compare_files(target)
    print(f"Average bits to encode: {total_bits/(len(stream) + en.k):.3f}")
    print(f"Target Text Size: {len(stream) + en.k}")
    print(f"Number of bits to encode: {total_bits:.3f}")
