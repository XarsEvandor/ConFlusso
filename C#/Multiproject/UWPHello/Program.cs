using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Windows.ApplicationModel.Activation;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;

namespace UWPHello
{
    public class Program : Application
    {
        static void Main(string[] args)
        {
            Start(_ => new Program());


        }

        protected override void OnLaunched(LaunchActivatedEventArgs args)
        {
            base.OnLaunched(args);

            //CDeviceWatcher.EnumerateDevicesAsync();
            CDeviceWatcher oWatcher = new CDeviceWatcher();

            while (oWatcher.ArduinoDeviceInfo == null) { }


            CSensor oSensor = new CSensor(oWatcher.ArduinoDeviceInfo, "1101");
            oSensor.getAccelValues("2101", "2102", "2103", "2104", "2105", "2106");
            

            /*Window.Current.Content = new TextBlock
            {
                Text = "Hello world!",
                VerticalAlignment = VerticalAlignment.Center,
                HorizontalAlignment = HorizontalAlignment.Center,
                FontSize = 40

            };*/
            Window.Current.Activate();
        }
    }
}
