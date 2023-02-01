using System;
using System.IO;
using System.Text.Json;

namespace Lib.files
{
    // ===============================================================================================================================
    public class CJSONFile
    {

        public Type ClassType { get; set; }
        public string FileName { get; set; }


        // -----------------------------------------------------------------------------------------------------------------------------         
        public CJSONFile(string p_sFileName)
        {
            this.FileName = p_sFileName;
        }
        // -----------------------------------------------------------------------------------------------------------------------------         
        #region //IFileStore\\
        
        // ------------------------------------------------------------------------------------------------
        public object Load()
        {
            object oResult;

            if (File.Exists(this.FileName))
            {
                string sJSON = File.ReadAllText(this.FileName);
                oResult = JsonSerializer.Deserialize(sJSON, this.ClassType); 
            }
            else
                oResult = null;

            return oResult;
        }
        // ------------------------------------------------------------------------------------------------
        public void Save(object p_oSourceObject)
        {
            // We create an options object to modify the default behaviour allowing indented json file (more readable).
            // When JSON needs to be transferred through the web we need to minify it, thus we leave WriteIndented = false.
            JsonSerializerOptions oOptions = new JsonSerializerOptions();
            oOptions.WriteIndented = true;

            string sJSON = JsonSerializer.Serialize(p_oSourceObject, oOptions);
            File.WriteAllText(this.FileName, sJSON);
        }
        // -----------------------------------------------------------------------------------------------------------------------------         
        #endregion
        // -----------------------------------------------------------------------------------------------------------------------------         
    }
    // ===============================================================================================================================
}