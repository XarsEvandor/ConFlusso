using System;

namespace ConsoleSignalRServer
{
    public class CDeviceData
    {
        public DateTime TimeStamp { get; set; }
        public double X { get; set; }
        public double Y { get; set; }
        public double Z { get; set; }  
        public double GyroX { get; set; } 
        public double GyroY { get; set; }
        public double GyroZ { get; set; }
        public bool EndOfStream { get; set; }
        public CDeviceData()
        {
            this.EndOfStream = false;
            TimeStamp = DateTime.Now;
        }

    }
}
