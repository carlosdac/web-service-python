import re

test_string = '/messages/4/'

matched = re.match("/messages/$", test_string)
is_match = bool(matched)

print(is_match)