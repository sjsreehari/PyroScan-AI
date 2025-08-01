import re

def coordinates(path):
    nums = re.findall(r"-?\d+\.\d+", path)
    return {
        "longitude": nums[0],
        "lattitude": nums[1]
    }

