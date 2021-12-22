#!/usr/bin/env python

from json import dumps, load
from functools import reduce
from os import getcwd
from glob import glob

baseDir = getcwd() + "/../selling-partner-api-models/models"

print("Looking in directory: {}".format(baseDir))

specs = glob("{}/**/*.json".format(baseDir), recursive=True)

jsonToDict = lambda f: load(open(f))

allSpecs = [jsonToDict(s) for s in specs if "merged" not in s]

if len(allSpecs):
    print("\n\t".join(["Using the following specs:"] + specs))
else:
    print("[ERROR] No specs found")
    exit(1)

updateAndReturn = lambda acc, d: acc.update(d) or acc

mergeKeyInto = lambda obj, key: reduce(updateAndReturn, map(lambda spec: spec[key], allSpecs), obj)

updateForKeyAndReturn = lambda acc, key, d: acc[key].update(d) or acc

keysToMerge = ['definitions', 'paths']

merged = reduce(lambda res, key: res[key].update(mergeKeyInto(res[key], key)) or res, keysToMerge, allSpecs[0])

outputFile = "merged.json"
with open(outputFile, 'w') as f:
    f.write(dumps(merged, indent=4))
