#/usr/bin/python

from termcolor import colored, cprint

# Ref: https://pypi.python.org/pypi/termcolor

print_warning = lambda x: cprint(x, 'yellow')
print_error = lambda x: cprint(x, 'red', attrs=['bold'])
print_info = lambda x: cprint(x, 'green')

yellow_text = lambda x: colored(x, 'yellow')
red_text = lambda x: colored(x, 'red')
green_text = lambda x: colored(x, 'green')
