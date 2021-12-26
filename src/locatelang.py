import glob
from lang import Lang
from fcm import Fcm
import argparse
import utils
import math

class LocateLang:
    
    
    def __init__(self, train_folder, target, threshold_type, window_size, noise):
        self.train_folder = train_folder
        self.target = target
        self.threshold_type = threshold_type
        self.window_size = window_size
        self.noise = noise
        
    def locate(self, orders, show_entropies=False):

        positions = {}    # {Lang : Positions[]}
        files = glob.glob(f"{self.train_folder}*")
        #files = ["../langs/train/pt_pt.utf8", "../langs/train/ita.utf8", "../langs/train/spanish.utf8", "../langs/train/eng.utf8"]
        # TODO: use all files
        for f in files:
            print(f)
            streams = []
            entropies = []
            for order in orders:
                fcm = Fcm(f, order, 0.001, 0)
                l = Lang(fcm)
                _, stream = l.compare_files(self.target)
                streams.append(stream)
                entropies.append(fcm.calculate_global_entropy())
            
            if self.threshold_type == "max":
                self.threshold = max(entropies)
            elif self.threshold_type == "mean":
               self.threshold = sum(entropies)/len(entropies)
            elif self.threshold_type == "entropy":  
                self.threshold = math.log2(fcm.alphabet_size)/2
            else:
                self.threshold = self.threshold_type

            stream = self._average_stream(streams, orders)
            if show_entropies:                       
                utils.add_entropy_to_plot(stream, self.threshold, f.split("/")[-1].split(".")[0])     
            
            initial_pos = 0
            lower = False
            # sliding window of size window_size
            for b in range(0, len(stream) - self.window_size):
            
                # calculates the mean for the values inside the window
                mean = 0
                for i in range(self.window_size):
                    mean += stream[b + i]
                mean /= self.window_size

                # saves start and end position when below the threshold
                if mean <= self.threshold:
                    if not lower:
                        lower = True
                        initial_pos = b
                else:
                    if lower and mean >= self.threshold * self.noise:
                        lower = False
                        positions.setdefault(f, [])
                        positions[f].append((initial_pos, b))
                        initial_pos = b + self.window_size            
        
        return positions       
       
    def _average_stream(self, streams, orders):
        
        # sort streams according to orders
        streams = [s for _,s  in sorted(zip(orders, streams))]
        orders.sort()
       
        temp = [0 for _ in range(len(streams[0]))]
        times = [0 for _ in range(len(streams[0]))]
        for i in range(len(streams)):
            d = orders[i] - orders[0]
            for j, s in enumerate(streams[i]):
                temp[j + d] += s
                times[j + d] += 1

        for i,s in enumerate(temp):
            temp[i] = s/times[i]

        return temp
    
if __name__ == "__main__":
    
    # python3 locatelang.py -r "../langs/train/" -t "../langs/test/test.txt" -w 3 -o 2 3 4

    parser = argparse.ArgumentParser(description='Lang')
    parser.add_argument("-r","--reference", type=str, required=True)
    parser.add_argument("-t,","--target", type=str, required=True)
    parser.add_argument('-o', "--orders", nargs='+', type=int,
                    help='size of the sequence', default=[2])
    parser.add_argument('-a', '--alpha', type=float, default=0.01,
                    help='alpha parameter')
    parser.add_argument("--threshold", default="entropy")
    parser.add_argument("-w","--window_size", type=int, default=3)
    parser.add_argument("--noise", type=float, default=1)
    parser.add_argument("--show_langs", action="store_true")
    parser.add_argument("--show_entropies", action="store_true")
    

    args = vars(parser.parse_args())

    threshold = args["threshold"]
    if args["threshold"] not in ("max", "mean", "entropy"):
        
        try:
            threshold = float(args["threshold"])
        except:
            print("Threshold type needs to be either mean, max, entropy or a float value representing the threshold.")
            exit(1)

    l = LocateLang(args["reference"], args["target"], threshold, args["window_size"], args["noise"])
    pos = l.locate(args["orders"], args["show_entropies"])
    
    if args["show_entropies"]:
        utils.add_entropy_to_plot(None, None, None, True)
    if args["show_langs"]:
        utils.plot_locations(pos, args["reference"])