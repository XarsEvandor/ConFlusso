using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Printing;
using System.Runtime.CompilerServices;
using System.Security.Cryptography.X509Certificates;
using System.Threading;
using System.Threading.Tasks;

using Microsoft.AspNetCore.SignalR;


namespace ConsoleSignalRServer
{
    public class CDataHub : Hub
    {
        public int MaxRetries = 4;
        public int RetryDelayMSecs = 250;

        // ----------------------------------------------------------------------------------------------------------
        // Do stuff when a client connects to the hub
        public async override Task OnConnectedAsync()
        {
            CDeviceDataQueue.Instance.Start();

            // Wait for some time so that the queue will have some collected data
            Thread.Sleep(1000);

            // Send a message back to the caller client
            await Clients.Caller.SendAsync("DoAfterConnected", DateTime.Now.ToString());
            await base.OnConnectedAsync();
            Console.WriteLine("Client Connected", Clients.Caller);
        }
        // ----------------------------------------------------------------------------------------------------------
        // Do stuff when a client disconnects from the hub
        public override async Task OnDisconnectedAsync(Exception? exception)
        {
            Debug.WriteLine("Disconnecting...");
            await base.OnDisconnectedAsync(exception);
        }
        // ----------------------------------------------------------------------------------------------------------
        // Simple API method that receives an integer parameter and returns an integer result
        public async Task<int> PlusPlus(int p_nNumber)
        {
            Debug.WriteLine("Incoming Message:", p_nNumber);

            return p_nNumber + 1;
        }
        // ----------------------------------------------------------------------------------------------------------
        // This is an API method that gets an argument count from the stream recipient client and yields serialized CDeviceData object
        public async IAsyncEnumerable<CDeviceData> OpenStream(int count, [EnumeratorCancellation] CancellationToken cancellationToken)
        {
            Console.WriteLine($"Queued item count {CDeviceDataQueue.Instance.Count}");
            for (int nStreamItemNumber=1; nStreamItemNumber<=count; nStreamItemNumber++)
            {
                Debug.WriteLine($"Streaming Queued Item:{nStreamItemNumber}/{count}");
                CDeviceData oDeviceData = null;

                bool bHasItem = CDeviceDataQueue.Instance.TryDequeue(out oDeviceData);
                if (!bHasItem)
                {
                    int nRetryCount = 0;
                    while((!bHasItem) && (nRetryCount < this.MaxRetries))
                    {
                        Thread.Sleep(this.RetryDelayMSecs);
                        bHasItem = CDeviceDataQueue.Instance.TryDequeue(out oDeviceData);
                        nRetryCount++;
                    }
                }

                if (!bHasItem)
                    oDeviceData = new CDeviceData() { EndOfStream = true };


                // We check the cancellation token that would be raised when the client disconnects, to throw an exception that forces this loop to terminate
                cancellationToken.ThrowIfCancellationRequested();
                
                yield return oDeviceData;

                // Delay for the next stream object and also forwards the cancellationToken to other APIs (that wait for it).
                await Task.Delay(0, cancellationToken);

                if (!bHasItem)
                    break;
            }
        }
        // ----------------------------------------------------------------------------------------------------------

    }
}
