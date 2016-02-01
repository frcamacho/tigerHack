import json
import re

def buildSubstrings(node):
    content = str(node)
    count = 0
    index = 0
    prevLast = -1
    substrings = []

    for char in content:
        index += 1
        assert not (char == "}" and count == 0)

        if char == "{":
            count += 1
        elif char == "}":
            count -= 1

        if char == "}" and count == 0:
            first = prevLast + 1
            substring = content[first:index]
            substrings.append(substring)
            prevLast = index

    return substrings

def extract(node, index):
    substrings = buildSubstrings(node)
    substring = substrings[index]
    cleaned = re.match(".*?(\{.*)$", substring).group(1)
    payload = json.loads(cleaned)
    return payload 

def traverse(node, depth=0):
    if isinstance(node, list):
        for child in node:
            traverse(child, depth + 1)
    elif isinstance(node, dict):
        for key in node.keys():
            print str(depth) + (" " * depth) + key
            child = node[key]
            traverse(child, depth + 1)
    else:
        try:
            if isinstance(node, str):
                node = re.sub("\n", " ", node)
                if len(node) > 10:
                    node = node[0:10] + "..."
            print str(depth) + (" ") * depth + str(node)
        except(UnicodeEncodeError):
            node = node.encode("ascii", "ignore")
            print str(depth) + (" ") * depth + str(node)
