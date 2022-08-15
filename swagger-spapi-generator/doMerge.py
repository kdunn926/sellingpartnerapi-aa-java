#!/usr/bin/env python

from json import dumps, load
from functools import reduce
from os import getcwd
from glob import glob
from sys import argv

baseDir = getcwd() + "/../selling-partner-api-models/models"

print("Looking in directory: {}".format(baseDir))

specs = []
try:
    specs = glob("{}/**/*.json".format(baseDir), recursive=True)
    specs = specs + glob("{}/../lib/*.json".format(getcwd()), recursive=True)
except TypeError:
    # This is used by Jitpack
    from subprocess import check_output
    specs = check_output("ls -r {}/**/*.json".format(baseDir), shell=True).splitlines()
    specs = specs + check_output("ls -r {}/../lib/*.json".format(getcwd()), shell=True).splitlines()

jsonToDict = lambda f: load(open(f))

specsToInclude = argv[1].split(",")
shouldInclude = lambda s: reduce(lambda res, spec: spec in s or res, specsToInclude, False)

print("\n\t".join(["Specs to include:"] + specsToInclude))

allSpecs = [jsonToDict(s) for s in specs if shouldInclude(s)]

if len(allSpecs):
    print("\n\t".join(["Using the following specs:"] + specs))
else:
    print("[ERROR] No specs found")
    exit(1)

updateAndReturn = lambda acc, d: acc.update(d) or acc

mergeKeyInto = lambda obj, key: reduce(updateAndReturn, map(lambda spec: spec.get(key, {}), allSpecs), obj)

updateForKeyAndReturn = lambda acc, key, d: acc.get(key, {}).update(d) or acc

keysToMerge = ['definitions', 'paths', 'parameters']

# Ensure all necessary keys are in the base spec
emptySpec = { k: dict() for k in keysToMerge if k not in allSpecs[0].keys() }
allSpecs[0].update(emptySpec)

merged = reduce(lambda res, key: res.get(key, {}).update(mergeKeyInto(res.get(key, {}), key)) or res,
                keysToMerge,
                allSpecs[0]
)

merged.update({ "consumes": ["application/json"] })
merged.update({ "produces": ["application/json"] })

outputFile = "merged.json"
with open(outputFile, 'w') as f:
    f.write(dumps(merged, indent=4))
