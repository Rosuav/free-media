import json
import yaml # ImportError? pip install pyyaml

with open("filelist.yaml") as f:
	files = list(yaml.safe_load_all(f))

# TODO: Validate
# Ensure that the files all exist
# Ensure that no files exist in media/ that are not listed
# Check that every file has the appropriate four attributes
# Check that the Type is a valid type

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
