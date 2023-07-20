import numpy as np

# =======================================================================================================================
class CTimeSequenceDeviceData(object):
  # --------------------------------------------------------------------------------------
  def __init__(self):
    self.Data = [] 
  # --------------------------------------------------------------------------------------
  def Add(self, p_oDeviceData):
    '''
    # Fixed detection data points
    if len(self.Data) > 600:
      self.Data.pop(0)
    '''
    self.Data.append([p_oDeviceData.X,
                      p_oDeviceData.Y,
                      p_oDeviceData.Z,
                      p_oDeviceData.GyroX,
                      p_oDeviceData.GyroY,
                      p_oDeviceData.GyroZ])
  # --------------------------------------------------------------------------------------
  def ToNumpy(self):
    nResult = None
    if (len(self.Data) != 0):
      nResult = np.asarray(self.Data).astype(np.float32)
    return nResult
  # --------------------------------------------------------------------------------------
# =======================================================================================================================