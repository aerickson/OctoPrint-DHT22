# coding=utf-8
from __future__ import absolute_import

import adafruit_dht

import octoprint.plugin
import octoprint.util


class Dht22Plugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
):
    def initialize(self):
        self.startTimer()
        pass

    ##~~ StartupPlugin mixin

    def on_after_startup(self):
        self._logger.debug(self._settings.get(["debugging_enabled"]))
        self._logger.debug(self._settings.get(["pin_configuration"]))
        pass

    #~~ TemplatePlugin
    # def get_template_configs(self):
    #     return [dict(type="settings", custom_bindings=False)]

    ##~~ SettingsPlugin mixin
    def get_settings_defaults(self):
        return dict(
            debugging_enabled=False,
            pin_configuration="# example configuration<br>Enclosure,23<br>External,24"
        )

    def get_settings_restricted_paths(self):
        return dict(admin=[["debugging_enabled"], ["pin_configuration"],],
                    user=[],
                    never=[])

    def get_settings_version(self):
        return 1

    def __init__(self):
        # type of sensor we're using
        # self.DHT_SENSOR = Adafruit_DHT.DHT22

        # maps sensor name to pin
        self.sensors = {"enclosure": 23, "external": 24}
        self.sensor_objects = {}
        self.current_data = {}
        self.timer = None

        for name, pin in self.sensor_objects.items():
            self.sensor_objects[name] = adafruit_dht.DHT22(pin)
        
    # see https://docs.octoprint.org/en/maintenance/plugins/hooks.html?highlight=octoprint%20comm%20protocol#octoprint-comm-protocol-temperatures-received
    def callback(self, comm, parsed_temps):
        for sensor_name, temp_value in self.current_data.items():
            parsed_temps[sensor_name] = (temp_value, None)
        return parsed_temps

    def doWork(self):
        for name, sensor_obj in self.sensor_objects.items():
            try:
                self.current_data[name] = a_device.temperature
            except RuntimeError as error:
                logging.error(error.args[0])

    def startTimer(self):
        # interval = self._settings.get_float(["interval"])
        interval = 10
        # self._logger.info(
        #     "starting timer to run command '%s' every %s seconds" % (the_cmd, interval)
        # )
        self.timer = octoprint.util.RepeatedTimer(interval, self.doWork, run_first=True)
        self.timer.start()

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(js=["js/DHT22.js"], css=["css/DHT22.css"], less=["less/DHT22.less"])

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
                type="github_commit",
                user="aerickson",
                repo="OctoPrint-DHT22",
                current=self._plugin_version,
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "DHT22 Plugin"
__plugin_pythoncompat__ = ">=2.7,<4"  # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Dht22Plugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        # https://docs.octoprint.org/en/maintenance/plugins/hooks.html?highlight=octoprint%20comm%20protocol#execution-order
        "octoprint.comm.protocol.temperatures.received": (
            __plugin_implementation__.callback,
            1,
        ),  # function and order
    }
