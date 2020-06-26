# coding=utf-8
from __future__ import absolute_import

import Adafruit_DHT

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

def callback(comm, parsed_temps):
	DHT_SENSOR = Adafruit_DHT.DHT22

	DHT_PIN = 23
	DHT_PIN2 = 24

	h1, t1 = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	h2, t2 = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN2)

	#     if h1 is not None and t1 is not None:
	#         print("#1 enclosure: Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(t1, h1))
	#     if h2 is not None and t2 is not None: 
	#         print("#2 external: Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(t2, h2))

	parsed_temps.update(external = (t2, None))
	parsed_temps.update(enclosure = (t1, None))

	# parsed_temps.update(test = (random.uniform(99,101),100))
	# parsed_temps.update(test2 = (random.uniform(199,201),200))
	# parsed_temps.update(test3 = (random.uniform(55,57),None))
	return parsed_temps

class Dht22Plugin(octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin

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
		"octoprint.comm.protocol.temperatures.received": (callback, 10)
	}

