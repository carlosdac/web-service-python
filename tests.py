import re

test_string = '/messages/440f/'

matched = re.match("/messages/\d+/$", test_string)
is_match = bool(matched)

print(is_match)