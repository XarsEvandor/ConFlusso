import matplotlib.pyplot as plt
from mllib import CFileStore

oFileStore = CFileStore(r"C:\Temp\DataCollection")
nData = oFileStore.Deserialize("data.pkl")

plt.plot(nData[:,0])
plt.plot(nData[:,1])
plt.show()
