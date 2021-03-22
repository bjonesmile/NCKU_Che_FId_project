import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(1,20,num=10)
y = np.linspace(3,40,num=10)
z = (x+y)/2
z_max = max(z)
z = z/z_max
print(z)

plt.scatter(x, y, marker='o',c=z)
plt.gray()
plt.show()