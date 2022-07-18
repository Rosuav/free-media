#!/usr/bin/env python3
# To install: ln -s ../../build.py .git/hooks/pre-commit
import json
import os
import sys
import yaml # ImportError? pip install pyyaml

with open("filelist.yaml") as f:
	files = list(yaml.safe_load_all(f))

# Validate. Check that every YAML entry has the necessary attributes, and that
# the files and YAML entries correspond correctly.

media = {f: False for f in os.listdir("media")}

for f in files:
	if {"Filename", "License", "Type", "Description"} - set(f):
		print("filelist.yaml:1: YAML entry lacks key attribute", file=sys.stderr)
		import pprint; pprint.pprint(f, stream=sys.stderr)
		sys.exit(1)
	if f["Filename"] not in media:
		print("filelist.yaml:1: File listed in YAML but not found: %r" % f["Filename"], file=sys.stderr)
		sys.exit(1)
	if media[f["Filename"]]:
		print("filelist.yaml:1: File listed twice in YAML: %r" % f["Filename"], file=sys.stderr)
		sys.exit(1)
	if f["Type"] not in {"Image", "Audio"}:
		# Does Video also need to be represented separately?
		print("filelist.yaml:1: File has invalid type: %r -> %r" % (f["Filename"], f["Type"]), file=sys.stderr)
		sys.exit(1)
	media[f["Filename"]] = True
	
for fn, seen in media.items():
	if not seen:
		print("filelist.yaml:1: File not listed in YAML: %r" % fn, file=sys.stderr)
		sys.exit(1)

# Write out the JSON file
data = {"files": [
	{
		"filename": f["Filename"],
		"license": f["License"],
		"type": f["Type"].lower(),
		"description": f["Description"],
	}
	for f in files
]}
with open("filelist.json", "w") as f:
	json.dump(data, f, indent=4)
# TODO: If being called as git hook, validate the version being committed,
# then git add the resulting json file.
