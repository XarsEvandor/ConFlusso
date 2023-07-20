using ConsoleSignalRServer;
using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading;

namespace SignalRServer
{
    public class CDataGenerationThread
    {
        private Thread __thread = null;
        private CDeviceDataQueue __queue;
        
        // For testing purposes
        public int MaximumDataPointCount = 100*6;
        public int PeriodDataPointCount  = 100;
        public int SamplingWindowMSecs = 1;

        // ------------------------------------------------------------------------------------------------
        public CDataGenerationThread(CDeviceDataQueue p_oQueue) 
        {
            // This is a parameterized thread start, pushing the queue of data items inside the method that contains the thread loop
            __queue = p_oQueue;

        }
        // ------------------------------------------------------------------------------------------------
        public void Start()
        {
            __thread = new Thread(new ParameterizedThreadStart(GenerateSignalData));
            //__thread = new Thread(new ParameterizedThreadStart(GenerateSequenceData));
            __thread.Start(__queue);
        }
        // ------------------------------------------------------------------------------------------------
        // Test for checking the data points of signals
        private void GenerateSignalData(object? p_oParam)
        {
            CDeviceDataQueue oQueue = (CDeviceDataQueue)p_oParam ?? null;
            int nDataPointCount = 0;
            while (true)
            {
                for (int i = 1; i <= this.PeriodDataPointCount; i++)
                {
                   oQueue.Enqueue(new CDeviceData()
                    {
                        X = 2.0*Math.Sin(i/4.0),
                        Y = 3.0*Math.Sin(i/4.0 + 0.5),
                        Z = 4.0*Math.Sin(i/4.0 + 2.0)
                        ,
                        GyroX = Math.Log10(i),
                        GyroY = Math.Log10(i * 1.5),
                        GyroZ = Math.Log10(i * 2.0)
                    });
                    nDataPointCount++;

                    // Emulate a delay for the Bluetooth comms between Arduino and the data sink
                    //Thread.Sleep(this.SamplingWindowMSecs); // 1ms
                }

                // You should have a limit on the data points that will be added to the queue by the sampler
                if (nDataPointCount >= this.MaximumDataPointCount)
                { 
                    Console.WriteLine("Stopping data collection");
                    break;
                }
            }
        }
        // ------------------------------------------------------------------------------------------------
        // Test for checking the sequence of data points
        private void GenerateSequenceData(object? p_oParam)
        {
            CDeviceDataQueue oQueue = (CDeviceDataQueue)p_oParam ?? null;
            int nDataPointCount = 0;
            while (true)
            {
                for (int i = 1; i <= this.PeriodDataPointCount; i++)
                {
                    oQueue.Enqueue(new CDeviceData()
                    {
                        X = nDataPointCount,
                        Y = 3.0*Math.Sin(i/4.0 + 0.5),
                        Z = 4.0*Math.Sin(i/4.0 + 2.0),
                        GyroX = Math.Log10(i),
                        GyroY = Math.Log10(i * 1.5),
                        GyroZ = Math.Log10(i * 2.0)
                    });
                    nDataPointCount++;
                    // Emulate a delay for the Bluetooth comms between Arduino and the data sink
                    Thread.Sleep(this.SamplingWindowMSecs); // 1ms
                }

                // You should have a limit on the data points that will be added to the queue by the sampler
                if (nDataPointCount >= this.MaximumDataPointCount)
                {
                    Console.WriteLine("Stopping data collection");
                    break;
                }
            }
        }
        // ------------------------------------------------------------------------------------------------

    }
}
