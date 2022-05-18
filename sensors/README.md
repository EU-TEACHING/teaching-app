# sensors
Project for all the sensors that can be instantiated, from "file" sensors to cameras and wearables.

# How to use Bluetooth on the iMX8
The shimmer devices need bluetooth to communicate with the board.

You need to:
- install `hciconfig`
- `hciconfig hci0 up` to activate bluetooth
- `hcitool scan` will give you the MAC address
- `rfcomm bind 0 MAC-ADDRESS`
- Now you should be able to see the device in `/dev`. This is the device that you need to add in the yaml config of your application.
