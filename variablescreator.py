from ubidots import ApiClient

api = ApiClient(token='RBgwxE0fSTaFS7IH7EqIya2Nl6yVek')
ctrlVarFloraBox=api.create_datasource({"name":"Ctrl floraBox"})
ctrlActFloraBox=api.create_datasource({"name":"Ctrl Actuators floraBox"})
varFloraBox=api.create_datasource({"name":"Variables floraBox"})

#Ctrl Actuadores

ctrlActFloraBox.create_variable({"description":"CAACR 1","unit":"bool","name":"Ctrl Air Circulation"})
ctrlActFloraBox.create_variable({"description":"CAAHE 1","unit":"bool","name":"Ctrl Air Heater"})
ctrlActFloraBox.create_variable({"description":"CAAHU 1","unit":"bool","name":"Ctrl Air Humidifier"}) 
ctrlActFloraBox.create_variable({"description":"CAAVE 1","unit":"bool","name":"Ctrl Air Ventilation"}) 
ctrlActFloraBox.create_variable({"description":"CALMI 1","unit":"bool","name":"Ctrl Light Mother"}) 
ctrlActFloraBox.create_variable({"description":"CALPN 1","unit":"bool","name":"Ctrl Light Panel 1"})
ctrlActFloraBox.create_variable({"description":"CALPN 2","unit":"bool","name":"Ctrl Light Panel 2"})

#Ctrl Variables

ctrlVarFloraBox.create_variable({"description":"CSACO 1","unit":"ppp","name":"Ctrl CO2"})
ctrlVarFloraBox.create_variable({"description":"CSAHU 1","unit":"%","name":"Ctrl Air Humidity"})
ctrlVarFloraBox.create_variable({"description":"CSATM 1","unit":"°C","name":"Ctrl Air Temp"})
ctrlVarFloraBox.create_variable({"description":"CSWEC 1","unit":"mS/cm","name":"Ctrl Water EC"})
ctrlVarFloraBox.create_variable({"description":"CSWPH 1","unit":"PH","name":"Ctrl Water PH"})

#Variables

varFloraBox.create_variable({"description":"AACR 1","unit":"bool","name":"Air Circulation"})
varFloraBox.create_variable({"description":"AAHE 1","unit":"bool","name":"Air Heater"})
varFloraBox.create_variable({"description":"AAHU 1","unit":"bool","name":"Air Humidifier"}) 
varFloraBox.create_variable({"description":"AAVE 1","unit":"bool","name":"Air Ventilation"}) 
varFloraBox.create_variable({"description":"ALMI 1","unit":"bool","name":"Light Mother"}) 
varFloraBox.create_variable({"description":"ALPN 1","unit":"bool","name":"Light Panel 1"})
varFloraBox.create_variable({"description":"ALPN 2","unit":"bool","name":"Light Panel 2"}) 
varFloraBox.create_variable({"description":"SACO 1","unit":"ppp","name":"CO2"})
varFloraBox.create_variable({"description":"SAHU 1","unit":"%","name":"Air Humidity"})
varFloraBox.create_variable({"description":"SAHU 2","unit":"%","name":"Air Humidity (CO2)"})
varFloraBox.create_variable({"description":"SATM 1","unit":"°C","name":"Air Temp"})
varFloraBox.create_variable({"description":"SATM 2","unit":"°C","name":"Air Temp (CO2)"})
varFloraBox.create_variable({"description":"SGSO 1","unit":"bool","name":"Shell Open"})
varFloraBox.create_variable({"description":"SGWO 1","unit":"bool","name":"Window Open"})
varFloraBox.create_variable({"description":"SLIN 1","unit":"lux","name":"Light Intensity"})
varFloraBox.create_variable({"description":"SLPA 1","unit":"umol/(s*m^2)","name":"Photosynthetically Active Radiation"})
varFloraBox.create_variable({"description":"SWEC 1","unit":"mS/cm","name":"Water EC"})
varFloraBox.create_variable({"description":"SWPH 1","unit":"PH","name":"Water PH"})
varFloraBox.create_variable({"description":"SWTM 1","unit":"°C","name":"Water Temp"})
