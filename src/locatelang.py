import glob
from lang import Lang
from fcm import Fcm
import argparse

class LocateLang:
    
    
    def __init__(self, train_folder, target, threshold, window_size):
        self.train_folder = train_folder
        self.target = target
        self.threshold = threshold
        self.window_size = window_size
        
        
    def locate(self, orders):

        positions = {}    # {Lang : Positions[]}
        files = glob.glob(f"{self.train_folder}*")
        files = ["../langs/train/pt_pt.utf8", "../langs/train/pt_br.utf8", "../langs/train/eng.utf8"]
        # TODO: use all files
        for f in files:
            print(f)
            streams = []
            entropies = []
            for order in orders:
                fcm = Fcm(f, order, 0.00001, 0)
                l = Lang(fcm)
                _, stream = l.compare_files(self.target)
                streams.append(stream)
                entropies.append(fcm.calculate_global_entropy())
            
            self.threshold = min(entropies) #sum(entropies)/len(entropies)
            stream = self._average_stream(streams, orders)
                            
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
                    if lower:
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
    
    # python3 locatelang.py -r "../langs/train/" -t "../example/test.txt" -w 3 -o 2 3 4

    parser = argparse.ArgumentParser(description='Lang')
    parser.add_argument("-r","--reference", type=str, required=True)
    parser.add_argument("-t,","--target", type=str, required=True)
    parser.add_argument('-o', "--orders", nargs='+', type=int,
                    help='size of the sequence', default=[2])
    parser.add_argument('-a', '--alpha', type=float, default=0.01,
                    help='alpha parameter')
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("-w","--window_size", type=int, default=3)

    args = vars(parser.parse_args())
    
    l = LocateLang(args["reference"], args["target"], args["threshold"], args["window_size"])
    pos = l.locate(args["orders"])
    print(pos)
    