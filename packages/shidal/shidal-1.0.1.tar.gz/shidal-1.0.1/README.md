# Shidal - Simple hid action listener

A library intended to be used with qmk keyboards. QMK keyboards are able to send raw hid data.<br>This library is able to intercept that data and work as a kind of action listener.<br>

## HID Data
The sent hid data needs to be in the following format:
- First byte is the 'command'
- Second byte is the 'subcommand'
- Rest of the data can be any data