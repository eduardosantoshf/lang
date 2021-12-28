from lang import Lang, Fcm
import matplotlib.pyplot as plt

def chart_average_bits_compare(target, reference, ks, alphas):
    
    l = Lang(None)
    target_e = []
    reference_e = []
    for k in ks:
        fcm = Fcm(reference, k, 0, 0)
        for a in alphas:
            fcm.alpha = a
            l.fcm = fcm
            
            total_bits, stream = l.compare_files(target)
            target_e.append(total_bits/ (len(stream) + k)) 
            reference_e.append(l.fcm.calculate_global_entropy())
    
    plt.plot(ks, target_e, label="target")
    plt.plot(ks, reference_e, label="reference")
    plt.legend()
    plt.show()
    


chart_average_bits_compare("../langs/test/test_pt_br.utf8", "../langs/train/pt_pt.utf8", [2,3,4,5,6], [0.0001])

