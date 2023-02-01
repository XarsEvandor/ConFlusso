using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System.IO;  // For class File
using System.Text.Json; // For class JsonSerializer
using M;


namespace JSON
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            
        }

        private void btnDeserialize_Click(object sender, EventArgs e)
        {
            string sFileName = "Prodigy-No Good.json";

            CMIDIFile oDeserializedObject;

            if (File.Exists(sFileName))
            {
                string sJSON = File.ReadAllText(sFileName);

                Type tClassType = typeof(CMIDIFile);
                oDeserializedObject = (CMIDIFile)JsonSerializer.Deserialize(sJSON, tClassType);
            }

        }
    }
}
