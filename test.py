
data = open("/home/domdf/Downloads/test sound.csv").read().split("\n")
data = [float(x) for x in data if x]
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
# plt.plot(data[::100])
# plt.plot(data[:10])
plt.plot(data)
# plt.axis('off')
print(data)
plt.show()