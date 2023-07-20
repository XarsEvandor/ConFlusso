using SignalRServer;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Text;
using System.Threading;

namespace ConsoleSignalRServer
{
    public class CDeviceDataQueue: ConcurrentQueue<CDeviceData>
    {
        // ...........................................................................
        // Singleton \\
        private static CDeviceDataQueue __instance = null;
        public static CDeviceDataQueue Instance
        {
            get
            {
                if (__instance == null)
                    __instance = new CDeviceDataQueue();
                return __instance;
            }
        }
        // ...........................................................................

        private CDataGenerationThread __datagen = null;

        // ------------------------------------------------------------------------------------------------
        private CDeviceDataQueue()
        {
        }
        // ------------------------------------------------------------------------------------------------
        public void Start()
        {
            // Replace this with the startup of the Bluetooth listener thread that connects and handles input data, providing the queue to it
            if (__datagen == null)
            { 
                __datagen = new CDataGenerationThread(this);
                __datagen.Start();
            }
        }
        // ------------------------------------------------------------------------------------------------

    }
}
