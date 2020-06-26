import Adafruit_DHT

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

	parsed_temps.update(external = (t2))
	parsed_temps.update(enclosure = (t1))

	# parsed_temps.update(test = (random.uniform(99,101),100))
	# parsed_temps.update(test2 = (random.uniform(199,201),200))
	# parsed_temps.update(test3 = (random.uniform(55,57),None))
	return parsed_temps

__plugin_name__ = "OctoPrint-DHT22"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_version__ = "0.1.0"
__plugin_hooks__ = {
	"octoprint.comm.protocol.temperatures.received": (callback, 1)
}