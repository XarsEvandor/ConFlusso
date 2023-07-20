# ......................................................................................
# MIT License

# Copyright (c) 2020-2023 Pantelis I. Kaplanoglou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ......................................................................................

import asyncio

from signalrcore_async.hub_connection_builder import HubConnectionBuilder
from signalrcore_async.protocol.json import JsonHubProtocol


# =========================================================================================================================
class CNetDataClient(object):
  # --------------------------------------------------------------------------------------
  def __init__(self, p_sURL, p_nVerboseLevel=1):
    # ................................................................
    # // Fields \\
    self.URL            = p_sURL
    self.VerboseLevel   = p_nVerboseLevel
    self.Connection     = None
    self.IsConnected    = False
    # ................................................................
    
    oOptions = {"verify_ssl": False}
    pConnectionInitializer = CSignalRClientInitializer().get_dictionary()

    if p_nVerboseLevel > 1:
      self.Connection = HubConnectionBuilder()\
                  .with_url(self.URL, options=oOptions)\
                  .with_hub_protocol(JsonHubProtocol())\
                  .configure_logging(1)\
                  .with_automatic_reconnect(pConnectionInitializer).build()
    else:
      self.Connection = HubConnectionBuilder()\
                  .with_hub_protocol(JsonHubProtocol())\
                  .with_url(self.URL, options=oOptions)\
                  .with_automatic_reconnect(pConnectionInitializer).build()
    


  # --------------------------------------------------------------------------------------
  async def Connect(self):
    if not self.IsConnected:
      await self.Connection.start()
      if self.VerboseLevel >= 1:
        print("(>) Connected to %s" % self.URL)
      self.IsConnected = True    
  # --------------------------------------------------------------------------------------
  async def Disconnect(self):
    if self.IsConnected:
      self.IsConnected = False
      if self.VerboseLevel >= 1:
        print("(x) Disconnecting from %s" % self.URL)    
      await self.Connection.stop()
        
  # --------------------------------------------------------------------------------------    
# =========================================================================================================================

  
  
  
  
  
  
# =======================================================================================================================
class CSignalRClientInitializer:
  # ----------------------------------------------------------------------------------------
  def __init__(self, con_type="raw", int_keep_alive=10, recon_interval=5, max_attemps=5):
    self.type = con_type
    self.keep_alive_interval = int_keep_alive
    self.reconnect_interval = recon_interval
    self.max_attempts = max_attemps
  # ----------------------------------------------------------------------------------------
  def get_dictionary(self):
    return {
        'type'                : self.type,
        'keep_alive_interval' : self.keep_alive_interval,
        'reconnect_interval'  : self.reconnect_interval,
        'max_attempts'        : self.max_attempts
    }
# =======================================================================================================================








 
# --------------------------------------------------------------------------------------
async def main():
  sHost       = "localhost"
  nPort       = 5000
  sSignalRHub = "DataHub"
      
  oClient = CNetDataClient(f"http://{sHost}:{nPort}/{sSignalRHub}")
  try:
    await oClient.Connect()
  finally:
    await oClient.Disconnect()
# --------------------------------------------------------------------------------------
  

          
if __name__ == "__main__":
  asyncio.run(main())
  
          
            