import asyncio
import time


from mllib.net import CNetDataClient
from mllib.net import CNetDataItem

from TimeSequenceDeviceData import CTimeSequenceDeviceData
import numpy as np
import matplotlib.pyplot as plt
from mllib.system.FileStore import CFileStore
from pickle import NONE

  
  
  

# =======================================================================================================================
class CDataHubClient(CNetDataClient):
  # --------------------------------------------------------------------------------------
  def __init__(self, p_sURL, p_nVerboseLevel=0):
    super(CDataHubClient, self).__init__(p_sURL, p_nVerboseLevel)
    # ................................................................
    # // Fields \\
    self.HasMoreStreamItems = False
    self.StartTime          = None
    self.EndTime            = None
    self.CollectedData      = CTimeSequenceDeviceData()
    # ................................................................    
    
    # Example of registering an API event handler 
    self.Connection.on("DoAfterConnected", self.DoAfterConnect)
  # --------------------------------------------------------------------------------------
  # Example of incoming API event handling
  def DoAfterConnect(self, p_sValue):
    print("Initializing after connection to data hub", p_sValue)
  # --------------------------------------------------------------------------------------
  # Example of invoking a Signal R Core API method
  async def PlusPlus(self, p_nNumber):
    nResult = await self.Connection.invoke("PlusPlus", [p_nNumber])
    return nResult
  # --------------------------------------------------------------------------------------
  # Example of opening a Signal R stream of objects via an API method, using a handler  
  # for the next data object and a specific limit of received objects.
  async def OpenStream(self, p_nMaxItems):
    self.HasMoreStreamItems = True
    await self.Connection.stream("OpenStream", [p_nMaxItems], self.NextDataItem)
  # --------------------------------------------------------------------------------------
  # Example of processing an incoming object that has been received by the stream
  def NextDataItem(self, p_dDataItem):
    if self.HasMoreStreamItems:
      try:
        oDataItem = CNetDataItem(p_dDataItem)
        if oDataItem.EndOfStream:
          print("End of stream!")
          self.EndTime = time.time()
          self.HasMoreStreamItems = False
        else:
          self.CollectedData.Add(oDataItem)
          print("Incoming data: Timestamp:%s X=%.2f" % (oDataItem.TimeStamp, oDataItem.X))
      except Exception as E:
        print(E)
  # --------------------------------------------------------------------------------------
  # This is an example of a Signal R core stream generator that returns batches of data
  # when it is used in a for-each loop
  async def DeviceDataStream(self, p_nPacketCount=25):
    while True:
      await self.OpenStream(p_nPacketCount)
      nData = self.CollectedData.ToNumpy()
      if nData is not None:
        # Create an empty object
        self.CollectedData = CTimeSequenceDeviceData()
        yield nData
      else:
        break
       
  # --------------------------------------------------------------------------------------
  
  # /////////////// EXAMPLE LOGIC \\\\\\\\\\\\\\\\

  # --------------------------------------------------------------------------------------
  async def TestServerStreamBatches(self, p_nBatchSize):
    nStartTime  = time.time()
    
    # Example of an iteration on a generator that brings batches of data
    oDeviceDataGenerator = self.DeviceDataStream(p_nBatchSize)
    oDataBatches = []
    nIndex = 0
    async for nDataBatch in oDeviceDataGenerator:
      print("Batch #%d Shape:%s" % (nIndex + 1, nDataBatch.shape))
      if nDataBatch is not None:
        #PlotData(nDataBatch, nIndex*p_nBatchSize, (nIndex+1)*p_nBatchSize)
        oDataBatches.append(nDataBatch)
      nIndex+=1
    
    if len(oDataBatches) > 0:
      nData = np.concatenate(oDataBatches, axis=0)
      
      nElapsed = time.time() - nStartTime
      nSecsPerStep = nElapsed / nData.shape[0]
      print("Secs/Step:%.6f" % nSecsPerStep)      
    else:
      nData = None
    
    return nData           
  # --------------------------------------------------------------------------------------
  async def TestClientRequests(self, p_nClientRequestCount):
    dStartTime = time.time()
    
    nValue = 0
    while nValue < p_nClientRequestCount:
      
      # Invoke a invoke (wait for return value)
      nValue = await self.PlusPlus(nValue)
      
      if nValue % 100 == 0:
        print("Requests finished:", nValue)   
        
    nElapsed = time.time() - dStartTime
    nSecsPerStep = nElapsed / p_nClientRequestCount
    print("Secs/Step:%.6f" % nSecsPerStep)   
  # --------------------------------------------------------------------------------------     
  async def TestServerStream(self, p_nStreamItemCount):
    self.StartTime = time.time()
    
    await self.OpenStream(p_nStreamItemCount)
   
    nElapsed = time.time() - self.StartTime
    nSecsPerStep = nElapsed / p_nStreamItemCount
    print("Secs/Step:%.6f" % nSecsPerStep)   
    
    return self.CollectedData.ToNumpy()
  # --------------------------------------------------------------------------------------
  # Helper method that plots a numpy array of data points that correspond to
  # discrete time moments from p_nStartIndex to p_nEndIndex
  def PlotData(self, p_nCollectedData, p_nStartIndex, p_nEndIndex):
    x = np.arange(p_nStartIndex, p_nEndIndex, dtype=np.int32)
    print("Plot data shape:", p_nCollectedData.shape)
    plt.plot(x, p_nCollectedData[:,0], label="X")
    plt.plot(x, p_nCollectedData[:,1], label="Y")
    plt.plot(x, p_nCollectedData[:,2], label="Z")
    plt.plot(x, p_nCollectedData[:,3], label="AccelX")
    plt.plot(x, p_nCollectedData[:,4], label="AccelY")
    plt.plot(x, p_nCollectedData[:,5], label="AccelZ")
    plt.legend()
    plt.show()  
  # --------------------------------------------------------------------------------------
  
# =======================================================================================================================



 
 

# --------------------------------------------------------------------------------------
async def main():
  nData = None
  
  sHost       = "localhost"
  nPort       = 5000
  sSignalRHub = "DataHub"
      
      
  oClient = CDataHubClient(f"http://{sHost}:{nPort}/{sSignalRHub}")
  try:
    await oClient.Connect()
    
    
    #await oClient.TestClientRequests(1000)
    #nData = await oClient.TestServerStream(100)
    nData = await oClient.TestServerStreamBatches(25)
  finally:
    await oClient.Disconnect()
    
        
  if nData is not None:
    oClient.PlotData(nData, 0, nData.shape[0])
    oFileStore = CFileStore(r"C:\Temp\DataCollection")
    oFileStore.Serialize("data.pkl", nData)
    
        
# --------------------------------------------------------------------------------------
  

          

asyncio.run(main())
  