import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

L = 2.870                           # m
l_in = [L-1.1, L-0.9, L-0.6, L-0.3] # m
l_out = [1.1, 0.9, 0.6, 0.3]        # m

strgauge = pd.DataFrame(data=np.abs([[L-1.1, L-1.1, L-0.9, L-0.9, L-0.6, L-0.6, L-0.3, L-0.3,
                               1.1, 1.1, 0.9, 0.9, 0.6, 0.6, 0.3, 0.3], 
                              [0, 0.4, 0, 0.4, 0, 0.4, 0, 0.4, 
                               0, 0.4, 0, 0.4, 0, 0.4, 0, 0.4]]).T,
                        index=["in SG 1", "in SG 2", "in SG 3", "in SG 4", "in SG 5", "in SG 6", "in SG 7", "in SG 8",
                               "out SG 1", "out SG 2", "out SG 3", "out SG 4", "out SG 5", "out SG 6", "out SG 7", "out SG 8"],
                        columns=["Horizontal Placement [m]", "Vertical Placement [m]"])



print(strgauge.head())