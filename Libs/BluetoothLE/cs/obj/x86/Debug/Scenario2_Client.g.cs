﻿#pragma checksum "C:\Users\giorg\Desktop\Programing\Thesis\Development\Libs\BluetoothLE\shared\Scenario2_Client.xaml" "{8829d00f-11b8-4213-878b-770e8597ac16}" "13E70446FAD9E7ABB5FB0939D2AB635DA2B9781A7665EE2F6F1E5DE8B8DF0E39"
//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace SDKTemplate
{
    partial class Scenario2_Client : 
        global::Windows.UI.Xaml.Controls.Page, 
        global::Windows.UI.Xaml.Markup.IComponentConnector,
        global::Windows.UI.Xaml.Markup.IComponentConnector2
    {

        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 0.0.0.0")]
        [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
        private class Scenario2_Client_obj1_Bindings :
            global::Windows.UI.Xaml.Markup.IDataTemplateComponent,
            global::Windows.UI.Xaml.Markup.IXamlBindScopeDiagnostics,
            global::Windows.UI.Xaml.Markup.IComponentConnector,
            IScenario2_Client_Bindings
        {
            private global::SDKTemplate.Scenario2_Client dataRoot;
            private bool initialized = false;
            private const int NOT_PHASED = (1 << 31);
            private const int DATA_CHANGED = (1 << 30);

            // Fields for each control that has bindings.
            private global::Windows.UI.Xaml.Controls.Button obj2;
            private global::Windows.UI.Xaml.Controls.ComboBox obj3;
            private global::Windows.UI.Xaml.Controls.ComboBox obj4;
            private global::Windows.UI.Xaml.Controls.Button obj8;
            private global::Windows.UI.Xaml.Controls.Button obj9;
            private global::Windows.UI.Xaml.Controls.Button obj10;
            private global::Windows.UI.Xaml.Controls.Button obj11;

            // Fields for each event bindings event handler.
            private global::Windows.UI.Xaml.RoutedEventHandler obj2Click;
            private global::Windows.UI.Xaml.Controls.SelectionChangedEventHandler obj3SelectionChanged;
            private global::Windows.UI.Xaml.Controls.SelectionChangedEventHandler obj4SelectionChanged;
            private global::Windows.UI.Xaml.RoutedEventHandler obj8Click;
            private global::Windows.UI.Xaml.RoutedEventHandler obj9Click;
            private global::Windows.UI.Xaml.RoutedEventHandler obj10Click;
            private global::Windows.UI.Xaml.RoutedEventHandler obj11Click;

            // Static fields for each binding's enabled/disabled state

            public Scenario2_Client_obj1_Bindings()
            {
            }

            public void Disable(int lineNumber, int columnNumber)
            {
                if (lineNumber == 33 && columnNumber == 62)
                {
                    this.obj2.Click -= obj2Click;
                }
                else if (lineNumber == 35 && columnNumber == 23)
                {
                    this.obj3.SelectionChanged -= obj3SelectionChanged;
                }
                else if (lineNumber == 37 && columnNumber == 23)
                {
                    this.obj4.SelectionChanged -= obj4SelectionChanged;
                }
                else if (lineNumber == 46 && columnNumber == 57)
                {
                    this.obj8.Click -= obj8Click;
                }
                else if (lineNumber == 47 && columnNumber == 56)
                {
                    this.obj9.Click -= obj9Click;
                }
                else if (lineNumber == 39 && columnNumber == 80)
                {
                    this.obj10.Click -= obj10Click;
                }
                else if (lineNumber == 41 && columnNumber == 99)
                {
                    this.obj11.Click -= obj11Click;
                }
            }

            // IComponentConnector

            public void Connect(int connectionId, global::System.Object target)
            {
                switch(connectionId)
                {
                    case 2: // Scenario2_Client.xaml line 33
                        this.obj2 = (global::Windows.UI.Xaml.Controls.Button)target;
                        this.obj2Click = (global::System.Object p0, global::Windows.UI.Xaml.RoutedEventArgs p1) =>
                        {
                            this.dataRoot.ConnectButton_Click();
                        };
                        ((global::Windows.UI.Xaml.Controls.Button)target).Click += obj2Click;
                        break;
                    case 3: // Scenario2_Client.xaml line 34
                        this.obj3 = (global::Windows.UI.Xaml.Controls.ComboBox)target;
                        this.obj3SelectionChanged = (global::System.Object p0, global::Windows.UI.Xaml.Controls.SelectionChangedEventArgs p1) =>
                        {
                            this.dataRoot.ServiceList_SelectionChanged();
                        };
                        ((global::Windows.UI.Xaml.Controls.ComboBox)target).SelectionChanged += obj3SelectionChanged;
                        break;
                    case 4: // Scenario2_Client.xaml line 36
                        this.obj4 = (global::Windows.UI.Xaml.Controls.ComboBox)target;
                        this.obj4SelectionChanged = (global::System.Object p0, global::Windows.UI.Xaml.Controls.SelectionChangedEventArgs p1) =>
                        {
                            this.dataRoot.CharacteristicList_SelectionChanged();
                        };
                        ((global::Windows.UI.Xaml.Controls.ComboBox)target).SelectionChanged += obj4SelectionChanged;
                        break;
                    case 8: // Scenario2_Client.xaml line 46
                        this.obj8 = (global::Windows.UI.Xaml.Controls.Button)target;
                        this.obj8Click = (global::System.Object p0, global::Windows.UI.Xaml.RoutedEventArgs p1) =>
                        {
                            this.dataRoot.CharacteristicWriteButtonInt_Click();
                        };
                        ((global::Windows.UI.Xaml.Controls.Button)target).Click += obj8Click;
                        break;
                    case 9: // Scenario2_Client.xaml line 47
                        this.obj9 = (global::Windows.UI.Xaml.Controls.Button)target;
                        this.obj9Click = (global::System.Object p0, global::Windows.UI.Xaml.RoutedEventArgs p1) =>
                        {
                            this.dataRoot.CharacteristicWriteButton_Click();
                        };
                        ((global::Windows.UI.Xaml.Controls.Button)target).Click += obj9Click;
                        break;
                    case 10: // Scenario2_Client.xaml line 39
                        this.obj10 = (global::Windows.UI.Xaml.Controls.Button)target;
                        this.obj10Click = (global::System.Object p0, global::Windows.UI.Xaml.RoutedEventArgs p1) =>
                        {
                            this.dataRoot.CharacteristicReadButton_Click();
                        };
                        ((global::Windows.UI.Xaml.Controls.Button)target).Click += obj10Click;
                        break;
                    case 11: // Scenario2_Client.xaml line 41
                        this.obj11 = (global::Windows.UI.Xaml.Controls.Button)target;
                        this.obj11Click = (global::System.Object p0, global::Windows.UI.Xaml.RoutedEventArgs p1) =>
                        {
                            this.dataRoot.ValueChangedSubscribeToggle_Click();
                        };
                        ((global::Windows.UI.Xaml.Controls.Button)target).Click += obj11Click;
                        break;
                    default:
                        break;
                }
            }

            // IDataTemplateComponent

            public void ProcessBindings(global::System.Object item, int itemIndex, int phase, out int nextPhase)
            {
                nextPhase = -1;
            }

            public void Recycle()
            {
                return;
            }

            // IScenario2_Client_Bindings

            public void Initialize()
            {
                if (!this.initialized)
                {
                    this.Update();
                }
            }
            
            public void Update()
            {
                this.Update_(this.dataRoot, NOT_PHASED);
                this.initialized = true;
            }

            public void StopTracking()
            {
            }

            public void DisconnectUnloadedObject(int connectionId)
            {
                throw new global::System.ArgumentException("No unloadable elements to disconnect.");
            }

            public bool SetDataRoot(global::System.Object newDataRoot)
            {
                if (newDataRoot != null)
                {
                    this.dataRoot = (global::SDKTemplate.Scenario2_Client)newDataRoot;
                    return true;
                }
                return false;
            }

            public void Loading(global::Windows.UI.Xaml.FrameworkElement src, object data)
            {
                this.Initialize();
            }

            // Update methods for each path node used in binding steps.
            private void Update_(global::SDKTemplate.Scenario2_Client obj, int phase)
            {
                if (obj != null)
                {
                }
            }
        }
        /// <summary>
        /// Connect()
        /// </summary>
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 0.0.0.0")]
        [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
        public void Connect(int connectionId, object target)
        {
            switch(connectionId)
            {
            case 2: // Scenario2_Client.xaml line 33
                {
                    this.ConnectButton = (global::Windows.UI.Xaml.Controls.Button)(target);
                }
                break;
            case 3: // Scenario2_Client.xaml line 34
                {
                    this.ServiceList = (global::Windows.UI.Xaml.Controls.ComboBox)(target);
                }
                break;
            case 4: // Scenario2_Client.xaml line 36
                {
                    this.CharacteristicList = (global::Windows.UI.Xaml.Controls.ComboBox)(target);
                }
                break;
            case 5: // Scenario2_Client.xaml line 44
                {
                    this.CharacteristicWritePanel = (global::Windows.UI.Xaml.Controls.StackPanel)(target);
                }
                break;
            case 6: // Scenario2_Client.xaml line 49
                {
                    this.CharacteristicLatestValue = (global::Windows.UI.Xaml.Controls.TextBlock)(target);
                }
                break;
            case 7: // Scenario2_Client.xaml line 45
                {
                    this.CharacteristicWriteValue = (global::Windows.UI.Xaml.Controls.TextBox)(target);
                }
                break;
            case 10: // Scenario2_Client.xaml line 39
                {
                    this.CharacteristicReadButton = (global::Windows.UI.Xaml.Controls.Button)(target);
                }
                break;
            case 11: // Scenario2_Client.xaml line 41
                {
                    this.ValueChangedSubscribeToggle = (global::Windows.UI.Xaml.Controls.Button)(target);
                }
                break;
            case 12: // Scenario2_Client.xaml line 31
                {
                    this.SelectedDeviceRun = (global::Windows.UI.Xaml.Documents.Run)(target);
                }
                break;
            default:
                break;
            }
            this._contentLoaded = true;
        }

        /// <summary>
        /// GetBindingConnector(int connectionId, object target)
        /// </summary>
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 0.0.0.0")]
        [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
        public global::Windows.UI.Xaml.Markup.IComponentConnector GetBindingConnector(int connectionId, object target)
        {
            global::Windows.UI.Xaml.Markup.IComponentConnector returnValue = null;
            switch(connectionId)
            {
            case 1: // Scenario2_Client.xaml line 13
                {                    
                    global::Windows.UI.Xaml.Controls.Page element1 = (global::Windows.UI.Xaml.Controls.Page)target;
                    Scenario2_Client_obj1_Bindings bindings = new Scenario2_Client_obj1_Bindings();
                    returnValue = bindings;
                    bindings.SetDataRoot(this);
                    this.Bindings = bindings;
                    element1.Loading += bindings.Loading;
                    global::Windows.UI.Xaml.Markup.XamlBindingHelper.SetDataTemplateComponent(element1, bindings);
                }
                break;
            }
            return returnValue;
        }
    }
}

