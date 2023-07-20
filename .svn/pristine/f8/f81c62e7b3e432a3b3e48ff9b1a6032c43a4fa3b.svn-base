using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Channels;
using System.Threading.Tasks;
using System.Threading;

namespace ConsoleSignalRServer
{
    public class CChannelStreaming
    {
        // ----------------------------------------------------------------------------
        public ChannelReader<int> Counter(int count, int delay, CancellationToken cancellationToken)
        {
            var channel = Channel.CreateUnbounded<int>();

            // We don't want to await WriteItemsAsync, otherwise we'd end up waiting 
            // for all the items to be written before returning the channel back to
            // the client.
            _ = WriteItemsAsync(channel.Writer, count, delay, cancellationToken);

            return channel.Reader;
        }
        // ----------------------------------------------------------------------------
        private async Task WriteItemsAsync( ChannelWriter<int> writer ,int count, int delay, CancellationToken cancellationToken)
        {
            Exception localException = null;
            try
            {
                for (var i = 0; i < count; i++)
                {
                    await writer.WriteAsync(i, cancellationToken);

                    // Use the cancellationToken in other APIs that accept cancellation
                    // tokens so the cancellation can flow down to them.
                    await Task.Delay(delay, cancellationToken);
                }
            }
            catch (Exception ex)
            {
                localException = ex;
            }
            finally
            {
                writer.Complete(localException);
            }
        }
        // ----------------------------------------------------------------------------
    }
}
