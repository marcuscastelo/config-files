import os
import json

VSCodeProductPath = "/usr/lib/code/product.json"

if not os.path.exists(VSCodeProductPath) or not os.access(VSCodeProductPath, os.W_OK):
    print("ERROR: Insuficient permissions or did not find VSCode Product file:", VSCodeProductPath)
    exit(1)

VSCodeProduct = open(VSCodeProductPath, "r")
data = json.load(VSCodeProduct)

# We need to ensure the extensionAllowedProposedApi has the following array:
extensionsToAdd = [
        "ms-vsliveshare.vsliveshare",
        "ms-vscode.node-debug",
        "ms-vscode.node-debug2"
]
print("Before:", data["extensionAllowedProposedApi"])

for extension in extensionsToAdd:
    if extension not in data["extensionAllowedProposedApi"]:
        data["extensionAllowedProposedApi"].append(extension)

print("After:", data["extensionAllowedProposedApi"])
print("Rewriting to file:", VSCodeProductPath)

VSCodeProduct = open(VSCodeProductPath, "w")
json.dump(data, VSCodeProduct,  indent=4)