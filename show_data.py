import matplotlib.pyplot as plt #install via pip install matplotlib
import numpy as np

velocity = 300 #Edit the velocity here from 60-360 (multiples of 30) 

scores = np.load(f"data/scores_vs{velocity}.npy")  #file name to load
extent = [-27, 26.5, 3.5, 52]  # [xmin, xmax, ymin, ymax]

#cmap = color coding of map
plt.imshow(scores, cmap='inferno', interpolation='nearest', origin='lower', extent=extent)
plt.colorbar(label="Score")
plt.xlabel("x_c (cm)")
plt.ylabel("y_c (cm)")
plt.title(f"Score Heatmap for v_s = {velocity}")
plt.show()