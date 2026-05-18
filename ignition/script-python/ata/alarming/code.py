##### Import AlarmListener library
from com.inductiveautomation.ignition.common.alarming import AlarmListener
#### Create MyAlarmListener Class
class MyAlarmListener(AlarmListener):
	##### When the MyAlarmListener class is created print to the gateway 'Constructing Object' 
	def __init__(self):
		system.util.getLogger("MyAlarmListener").info("Constructing Object")
	
	##### Alarm acknowledged function	
	def onAcknowledge(self,evt):
		pass
#		system.util.getLogger("MyAlarmListener").info("OnAcknowledge")
#		system.util.sendMessage(project="SAB",messageHandler="onAcknowledge",payload = {"event":evt},scope = "C")
	
	##### Alarm active function
	def onActive(self,evt):
		##### Print to the gateway 'OnActive'
		system.util.getLogger("MyAlarmListener").info("OnActive")
		##### Send a message to the client message handler 'onActive'
		system.util.sendMessage(project="SAB",messageHandler="onActive",payload = {"event":evt},scope = "C")
	
	##### Alarm cleared function 		
	def onClear(self,evt):
		pass
#		system.util.getLogger("MyAlarmListener").info("OnClear")
#		system.util.sendMessage(project="SAB",messageHandler="onClear",payload = {"event":evt},scope = "C")