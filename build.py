#!/usr/bin/env python3
# To install: ln -s ../../build.py .git/hooks/pre-commit
import json
import os
import mimetypes
import sys
import yaml # ImportError? pip install pyyaml

class Loader(yaml.SafeLoader):
	"""Modified version of SafeLoader that retains line numbers"""
	def construct_mapping(self, node, deep=False):
		mapping = super().construct_mapping(node, deep=deep)
		mapping["_line"] = node.start_mark.line + 1
		return mapping

with open("filelist.yaml") as f:
	files = list(yaml.load_all(f, Loader))

# Validate. Check that every YAML entry has the necessary attributes, and that
# the files and YAML entries correspond correctly.

media = {f: False for f in os.listdir("media")}

for f in files:
	if not isinstance(f, dict) or "_line" not in f:
		print("filelist.yaml:1: Malformed YAML entry", file=sys.stderr)
		import pprint; pprint.pprint(f, stream=sys.stderr)
		sys.exit(1)
	if {"Filename", "License", "Description"} - set(f):
		print("filelist.yaml:%d: YAML entry lacks key attribute" % f["_line"], file=sys.stderr)
		import pprint; pprint.pprint(f, stream=sys.stderr)
		sys.exit(1)
	if f["Filename"] not in media:
		print("filelist.yaml:%d: File does not exist: %r" % (f["_line"], f["Filename"]), file=sys.stderr)
		sys.exit(1)
	if media[f["Filename"]]:
		print("filelist.yaml:%d: File listed twice in YAML: %r" % (f["_line"], f["Filename"]), file=sys.stderr)
		sys.exit(1)
	mimetype, enc = mimetypes.guess_type(f["Filename"])
	if not mimetype:
		print("filelist.yaml:%d: MIME type detection failed: %r" % (f["_line"], f["Filename"]), file=sys.stderr)
		sys.exit(1)
	f["MIMEType"] = mimetype # Not currently using the encoding, prob not necessary for audio/video files
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
		"mimetype": f["MIMEType"],
		"description": f["Description"],
	}
	for f in files
]}
with open("filelist.json", "w") as f:
	json.dump(data, f, indent=4)
# TODO: If being called as git hook, validate the version being committed,
# then git add the resulting json file.
