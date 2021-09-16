# OctoPrint-DHT22

DEPRECATED: Please use a different sensor. I never got this to work well. Please see https://github.com/aerickson/OctoPrint-HTU31.

Reads DHT22 sensors and adds the data to OctoPrint's temperature data.

## Setup

Install libgpiod2.

`sudo apt-get install libgpiod2`

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/aerickson/OctoPrint-DHT22/archive/master.zip

## Graphing

Install https://github.com/jneilliii/OctoPrint-PlotlyTempGraph to display the data.

## Configuration

**TODO:** Pin configuration is hard-coded currently.
