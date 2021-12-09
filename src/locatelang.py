import glob
from lang import Lang
from fcm import Fcm

class LocateLang:
    
    
    def __init__(self, target, threshold, window_size):
        self.target = target
        self.threshold = threshold
        self.window_size = window_size
        
        
    def locate(self):

        positions = {}    # {Lang : Positions[]}
        files = glob.glob("../langs/train/*")
        
        # TODO: use all files
        for f in files[:5]:
            fcm = Fcm(f, 3, 0.00001, 0)
            l = Lang(fcm)
            _, stream = l.compare_files(self.target)

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
       

if __name__ == "__main__":
    
    l = LocateLang("../example/maias.txt", 2, 5)
    pos = l.locate()
    print(pos.keys())
    