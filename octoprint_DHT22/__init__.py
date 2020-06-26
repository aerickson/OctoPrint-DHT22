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



class Dht22Plugin(octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.TemplatePlugin):

    ##~~ SettingsPlugin mixin

    def __init__(self):
        # type of sensor we're using
        self.DHT_SENSOR = Adafruit_DHT.DHT22

        # maps sensor name to pin
        self.sensors = {'enclosure': 23, 'external': 24}
        self.current_data = {}

        self.timer = None
        self.startTimer()


    # see https://docs.octoprint.org/en/maintenance/plugins/hooks.html?highlight=octoprint%20comm%20protocol#octoprint-comm-protocol-temperatures-received
    def callback(self, comm, parsed_temps):
        self._logger.info("HAHAHAHA ANDDDDDYYYYYYYYYYYY HERE")
        for sensor_name, temp_value in self.current_data.items():
            parsed_temps.update(sensor_name = (temp_value, None))
            # parsed_temps.update(enclosure = (dht22_temp_arr[1], None))

        # parsed_temps.update(test = (random.uniform(99,101),100))
        # parsed_temps.update(test2 = (random.uniform(199,201),200))
        # parsed_temps.update(test3 = (random.uniform(55,57),None))
        return parsed_temps


    def doWork(self):
        # if self._settings.get(["verbose"]):
        #     self._logger.info("result code is %s. output: '%s'" % (rc, output))
        for name, pin in self.sensors.items():
            self.current_data[name] = Adafruit_DHT.read_retry(self.DHT_SENSOR, pin)


    def startTimer(self):
        # interval = self._settings.get_float(["interval"])
        interval = 10
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
        # https://docs.octoprint.org/en/maintenance/plugins/hooks.html?highlight=octoprint%20comm%20protocol#execution-order
        "octoprint.comm.protocol.temperatures.received": (__plugin_implementation__.callback, 1)  # function and order
    }

