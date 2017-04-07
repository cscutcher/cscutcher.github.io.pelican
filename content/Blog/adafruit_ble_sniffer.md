Title: Using the Adafruit Bluetooth LE Sniffer with modern distro
Tags: notes, research, bluetooth, ble

I'm currently doing a lot of work with BLE and so was looking for ways to
analyse traffic on the wire. While wireshark can do sniffing with your standard
bluetooth dongle, it can only sniff traffic that the bluetooth controller is
directly involved with, and the indirection between bluetooth bluez, host and
controller, made me distinctly suspect that I wasn't seeing the complete picture
even then.

After some research I discovered
[this device from adafruit](https://www.adafruit.com/product/2269)
which is capable of sniffing without being directly involved in the dialogues.

After getting hold of one however, I found that it's linux support on a modern
distros is shaky at best, mostly due to being built for older version of
wireshark.

To help any other fellow travellers here's what I did to get it mostly working.

### Collecting the traffic ###
To make the initial pcap trace clone [this repo](https://github.com/adafruit/Adafruit_BLESniffer_Python);

```bash
git clone https://github.com/adafruit/Adafruit_BLESniffer_Python.git
```

The tool we're interested in is `sniffer.py`.
To run this tool **make sure you use python 2 and have pyserial installed**.

Collect traffic from a particular address with a command like this;

```bash
python2 sniffer.py -t AA:BB:CC:DD:EE:FF -l sniffed.pcap /dev/ttyUSB0
```

where `AA:BB:CC:DD:EE:FF` is the address of the device you want to sniff and
`/dev/ttyUSB0` is the path to the serial device that appears when you plug the
BLE sniffer stick in. Look at `dmesg` after plugging the stick in to find the
latter.

This will output the sniffed packets to `sniffed.pcap`.


### Dissecting the traffic with wireshark ###
This bit was slightly more awkward. Unfortunately modern wireshark
(I'm using 2.2.5) doesn't have a dissector for the sniffed packets.

The repo above does contain some c implementations of a dissector but no
instructions on how to build.

I had a bit more luck with [this repo](https://github.com/ambrice/nordic_ble)
which has some cmake for building and installing the dissector (although note
the path it installs to is `.wireshark/plugins` when it should be
`.config/wireshark/plugins`) but it became obvious that this dissector was
written for an older version of Wireshark.

What saved me was
[this repo with a lua implementation of the dissector](https://github.com/tewarid/wireshark-nordic-ble-lua).

Clone this to a sensible location and add the following to
`.config/wireshark/init.lua`:

```
dofile("/path/to/nordic_ble.lua")
```

When you next open wireshark you should be able to read the pcap file generated
above and see a sensible dissection.

### Notes and caveats ###
I've not been able to validate that the dissector or the sniffer produces
correct results yet.
The lua repo seems quite fresh, but there's no guarantee that it's
dissector implementation is as correct as the c reference implementation.

I didn't realise it at first but there also seems a reasonable python API in the
same repo as `sniffer.py` (indeed the sniffer seems to exists just to
demonstrate this api). It looks pretty handy so I'd like to get the chance to
play with that too.

There also seems to be some hint that the dissectors were eventually merged into
the main wireshark codebase but I can't find anything to confirm that.
Perhaps they were merged in under a different name?

### Links ###
* [Adafruit product page](https://www.adafruit.com/product/2269)
* [Adafruit docs on the sniffer](https://learn.adafruit.com/introducing-the-adafruit-bluefruit-le-sniffer)
* [Python API for Bluefruit LE Sniffer](https://github.com/adafruit/Adafruit_BLESniffer_Python)
* [C based wireshark dissectors with Cmake](https://github.com/ambrice/nordic_ble)
* [Lua wireshark dissector](https://github.com/tewarid/wireshark-nordic-ble-lua)
* [Docs from Nordic who make the sniffer chip](https://devzone.nordicsemi.com/blogs/750/ble-sniffer-in-linux-using-wireshark/)
* [Relevant question on nordic help forum](https://devzone.nordicsemi.com/question/67447/wireshark-201-and-nrfsniffer/)
* [Another relevant question on nordic help forum](https://devzone.nordicsemi.com/question/79845/nrf-sniffer-support-for-wireshark-v203/)
