import json
import pprint
import re

str = open("module.txt").readline()

count = 0
index = 0
prevLast = -1
substrings = []

for char in str:
    index += 1
    assert not (char == "}" and count == 0)

    if char == "{":
        count += 1
    elif char == "}":
        count -= 1

    if char == "}" and count == 0:
        first = prevLast + 1
        substring = str[first:index]
        substrings.append(substring)
        prevLast = index

# You can't stop me, LinkedIn...
for i in range(len(substrings)):
    substring = substrings[0]
    cleaned = re.match(".*?(\{.*)$", substring).group(1)
    try:
        fn = "./json/%i.json" % i
        fh = open(fn, "w")
        data = json.loads(cleaned)
        text = pprint.pformat(data)
        fh.write(text)
        fh.close()
        print "Converted element %i." % i
    except:
        print "Failed to convert element %i." % i
