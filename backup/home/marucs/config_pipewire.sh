pactl load-module module-null-sink media.class=Audio/Sink sink_name=virtual1 channel_map=surround-51 sink_properties=device.nick="virtual1"
pactl load-module module-null-sink media.class=Audio/Sink sink_name=virtual2 channel_map=surround-51 sink_properties=device.nick="virtual2"
pactl load-module module-null-sink media.class=Audio/Sink sink_name=virtual3 channel_map=surround-51 sink_properties=device.nick="virtual3"

pactl load-module module-loopback source=virtual1.monitor sink="alsa_output.pci-0000_00_1f.3.analog-stereo" sink_properties=device.description="v2toA"
pactl load-module module-loopback source=virtual1.monitor sink=virtual2
pactl load-module module-loopback source=virtual2.monitor sink=virtual3
pactl load-module module-loopback source="alsa_input.pci-0000_00_1f.3.analog-stereo" sink=virtual3
