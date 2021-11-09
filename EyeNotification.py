import time
from datetime import datetime
from plyer import notification

# autostart (run it only once!)
# import getpass
# USER_NAME = getpass.getuser()
# def add_to_startup(file_path=""):
# 	if file_path == "":
# 		file_path = os.path.dirname(os.path.realpath(__file__))
# 	bat_path = r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME
# 	with open(bat_path + '\\' + "EyeNotification.bat", "w+") as bat_file:
# 		bat_file.write(r"cmd /c 'python %s'" % file_path)
# add_to_startup(r"C:\Users\Philipp\Documents\EyeNotification.py")

# notification every 15 minutes
timeinterval = 60*15
def ScreenBreak():
	notification.notify(app_name="Bildschirmpause Notification", 
						title="Bildschirmpause", message="Mach eine Pause und schau in die Ferne.", 
						timeout=10) 
def showCurrentTime():
	current_time = datetime.now().strftime("%H:%M:%S")
	return current_time
print(f"Program gestartet um: {showCurrentTime()} ")	


if __name__ == "__main__":
	while True:
		time.sleep(timeinterval)
		ScreenBreak()
		print(f"Letzte Meldung : {showCurrentTime()}")