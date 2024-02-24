import json
good = {
    "a": "1", 
    "b": "2",
    "c": "3"
}

a = 1

good["d"] = "4"

with open("violation_points.json", "w") as f:
    json.dump(good, f)

print(good)