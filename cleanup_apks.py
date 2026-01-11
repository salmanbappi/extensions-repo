import os
import re

apk_dir = "extensions-repo/apk"
files = os.listdir(apk_dir)
files = [f for f in files if f.endswith(".apk")]

# Map pkg -> list of (version_code, filename)
packages = {}

# Regex to parse filename: {pkg}-v{version}-c{code}.apk
# Example: eu.kanade.tachiyomi.animeextension.all.roarzone-v14.1015-c1015.apk
pattern = re.compile(r"(.+)-v.*-c(\d+)\.apk")

for f in files:
    match = pattern.match(f)
    if match:
        pkg = match.group(1)
        code = int(match.group(2))
        if pkg not in packages:
            packages[pkg] = []
        packages[pkg].append((code, f))

# For each package, keep only highest code
for pkg, items in packages.items():
    # Sort descending by code
    items.sort(key=lambda x: x[0], reverse=True)
    
    if not items:
        continue
        
    latest = items[0]
    print(f"Keeping latest for {pkg}: {latest[1]} (code {latest[0]})")
    
    # Delete others
    for code, filename in items[1:]:
        path = os.path.join(apk_dir, filename)
        print(f"Deleting old version: {filename}")
        os.remove(path)
