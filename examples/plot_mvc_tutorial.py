"""
Radiograph segmentation tutorial
===================================


"""


#%%
#Importing modules

import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import median, rank

#from xripl.data import shot
from xripl.reader import openRadiograph
from xripl.contrast import equalize
from xripl.clean import cleanArtifacts, flatten
from xripl.segmentation import detectShock
# import xripl.pltDefaults


#%%
# Plot

xData = np.arange(10)
yData = xData ** 2

plt.plot(xData, yData)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
