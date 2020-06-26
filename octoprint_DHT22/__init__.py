# coding=utf-8
from __future__ import absolute_import

import Adafruit_DHT

import octoprint.plugin
import octoprint.util


dht22_temp_arr = [0, 0]

# def callback(comm, parsed_temps):
# 	parsed_temps.update(test = (random.uniform(99,101),100))
# 	parsed_temps.update(test2 = (random.uniform(199,201),200))
# 	parsed_temps.update(test3 = (random.uniform(55,57),None))
# 	return parsed_temps

def callback(comm, parsed_temps):
	# DHT_SENSOR = Adafruit_DHT.DHT22

	# DHT_PIN = 23
	# DHT_PIN2 = 24

	# h1, t1 = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	# h2, t2 = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN2)

	# dht22_temp_arr = [t2, t1]

	#     if h1 is not None and t1 is not None:
	#         print("#1 enclosure: Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(t1, h1))
	#     if h2 is not None and t2 is not None: 
	#         print("#2 external: Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(t2, h2))

	parsed_temps.update(external = (dht22_temp_arr[0], None))
	parsed_temps.update(enclosure = (dht22_temp_arr[1], None))

	# parsed_temps.update(test = (random.uniform(99,101),100))
	# parsed_temps.update(test2 = (random.uniform(199,201),200))
	# parsed_temps.update(test3 = (random.uniform(55,57),None))
	return parsed_temps

class Dht22Plugin(octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin

    def __init__(self):
        self.timer = None
		self.startTimer()

    def doWork(self):
        # the_cmd = self._settings.get(["command"])
        # rc, output = self.run_command(the_cmd)
        # if self._settings.get(["verbose"]):
        #     self._logger.info("result code is %s. output: '%s'" % (rc, output))
		pass

	def startTimer(self):
        # interval = self._settings.get_float(["interval"])
		interval = 5
        # self._logger.info(
        #     "starting timer to run command '%s' every %s seconds" % (the_cmd, interval)
        # )
        self.timer = octoprint.util.RepeatedTimer(
            interval, self.doWork, run_first=True
        )
        self.timer.start()

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/DHT22.js"],
			css=["css/DHT22.css"],
			less=["less/DHT22.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			DHT22=dict(
				displayName="DHT22 Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="aerickson",
				repo="OctoPrint-DHT22",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/aerickson/OctoPrint-DHT22/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "DHT22 Plugin"
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Dht22Plugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.temperatures.received": (callback, 1)  # function and interval
	}

