using BLE_Data_Receiver;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using Windows.Devices.Enumeration;
using Windows.UI.Xaml;

namespace UWPHello
{
    public class CSensor
    {
        private String __deviceName;
        private String __serviceGUID;

        List<float> lAccelXVals = new List<float>();
        List<float> lAccelYVals = new List<float>();
        List<float> lAccelZVals = new List<float>();

        List<float> lGyroXVals = new List<float>();
        List<float> lGyroYVals = new List<float>();
        List<float> lGyroZVals = new List<float>();


        private DeviceInformation __deviceInfo;

        public CSensor(DeviceInformation p_oDeviceInfo, string p_sServiceGUID)
        {
            //this.__deviceName = p_sDeviceName;
            this.__deviceInfo = p_oDeviceInfo;
            this.__serviceGUID = p_sServiceGUID;   
        }

        public void getAccelValues(string p_sAccelXGUID, string p_sAccelYGUID, string p_sAccelZGUID,
                                                string p_sGyroXGUID, string p_sGyroYGUID, string p_sGyroZGUID)
        {
            CSensorAttribute oAccelX = new CSensorAttribute(__serviceGUID, p_sAccelXGUID, __deviceName, this.__deviceInfo);
            CSensorAttribute oAccelY = new CSensorAttribute(__serviceGUID, p_sAccelYGUID, __deviceName, this.__deviceInfo);
            CSensorAttribute oAccelZ = new CSensorAttribute(__serviceGUID, p_sAccelZGUID, __deviceName, this.__deviceInfo);

            CSensorAttribute oGyroX = new CSensorAttribute(__serviceGUID, p_sGyroXGUID, __deviceName, this.__deviceInfo);
            CSensorAttribute oGyroY = new CSensorAttribute(__serviceGUID, p_sGyroYGUID, __deviceName, this.__deviceInfo);
            CSensorAttribute oGyroZ = new CSensorAttribute(__serviceGUID, p_sGyroZGUID, __deviceName, this.__deviceInfo);

            oAccelX.Initialize();
            oAccelY.Initialize();
            oAccelZ.Initialize();

            oGyroX.Initialize();
            oGyroY.Initialize();
            oGyroZ.Initialize();
            

            while(true) 
            {
                List<float> lTempAccelXVals = oAccelX.Values;
                List<float> lTempAccelYVals = oAccelY.Values;
                List<float> lTempAccelZVals = oAccelZ.Values;

                //todo: make the gyro

                lAccelXVals.AddRange(lTempAccelXVals);
                lAccelYVals.AddRange(lTempAccelYVals);
                lAccelZVals.AddRange(lTempAccelZVals);

                lGyroXVals.AddRange(oGyroX.Values);
                lGyroYVals.AddRange(oGyroY.Values);
                lGyroZVals.AddRange(oGyroZ.Values);


                if (lTempAccelXVals.Count > 0)
                {
                    foreach (float nValue in lTempAccelXVals)
                        Debug.Write(nValue + ", ");
                    Debug.WriteLine("");
                }
                if (lTempAccelYVals.Count > 0)
                {
                    foreach (float nValue in lTempAccelYVals)
                        Debug.Write(nValue + ", ");
                    Debug.WriteLine("");
                }
                if (lTempAccelZVals.Count > 0)
                {
                    foreach (float nValue in lTempAccelZVals)
                        Debug.Write(nValue + ", ");
                    Debug.WriteLine("");
                }


                /*Debug.WriteLine(lGyroXVals);
                Debug.WriteLine(lGyroYVals);
                Debug.WriteLine(lGyroZVals);*/

            }
        }
    }
}
