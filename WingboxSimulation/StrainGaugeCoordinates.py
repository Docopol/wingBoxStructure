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

# pairs = pd.DataFrame(index=["Horizontal Placement [m]", "Vertical Placement [m]"])
# for i in strgauge.index:
#     pairs.at["Horizontal Placement [m]", i] = strgauge.at[i, "Horizontal Placement [m]"]
#     pairs.at["Vertical Placement [m]", i] = strgauge.at[i, "Vertical Placement [m]"]
#
# print(strgauge)
# print(pairs)

# plt.scatter(pairs.loc["Horizontal Placement [m]"], pairs.loc["Vertical Placement [m]"], )

# pairs.plot.scatter("Horizontal Placement [m]", "Vertical Placement [m]")


#plt.scatter(strgauge["Horizontal Placement [m]"], strgauge["Vertical Placement [m]"], label=strgauge.index)
strgauge.plot.scatter("Horizontal Placement [m]", "Vertical Placement [m]")
for i in strgauge.index:
    if strgauge.at[i, "Vertical Placement [m]"] < 0.2:
        disp = 0.01
    else:
        disp = -0.02
    plt.text(strgauge.at[i, "Horizontal Placement [m]"] - 0.02,
             strgauge.at[i, "Vertical Placement [m]"] + disp, i.strip("out in SG"))
plt.show()

#print(strgauge.head())