import matplotlib.pyplot as plt
import glob

def plot_locations(positions, reference_folder):
    
    #files = glob.glob(f"{reference_folder}*")
    #files = [f.split("/")[-1].split(".")[0] for f in files]
    #print(positions.keys())
    cmap = plt.cm.get_cmap("hsv", len(positions)+1)
    for i, lang in enumerate(positions.keys()):
        for pos in positions[lang]:
            plt.plot(pos, (i,i), c=cmap(i))
    plt.yticks(range(i + 1), [x.split("/")[-1].split(".")[0] for x in positions.keys()])
    plt.xlabel("Position")
    plt.show()
    
def add_entropy_to_plot(stream, threshold, lang, show=False):
    
    if show:
        plt.legend()
        plt.show()
        return
    
    temp = [s for s in stream if s < 5]
    plt.scatter(range(len(temp)), temp)
    
    plt.plot(range(len(stream)), [threshold for _ in range(len(stream))], label=lang)