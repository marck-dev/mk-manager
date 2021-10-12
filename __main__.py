import os
import display_gui
import auto_import
import argparse

parse = argparse.ArgumentParser('Display manager', 'mk-manager [options]',
                                "Script to help with the display managenment")
parse.add_help
parse.add_argument('-g','--gui', help='Use the prompt system to set up display', action='store_true')
parse.add_argument('-a','--auto', help='Auto load the config file', action='store_true')
parse.add_argument('-l','--list', help='List ports and show status', action='store_true')

args = parse.parse_args()

if args.gui:
    data = display_gui.main()
    os.system('clear')
    choice = input('You want to save the configuration [y/n]:')
    if choice == 'y':
        auto_import.save_config(**data)
elif args.auto:
    auto_import.load_config()
elif args.list:
    display_gui.print_device_list(display_gui.get_devices())