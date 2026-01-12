import json
import os
import hashlib
import sys

def get_apk_size(file_path):
    return os.path.getsize(file_path)

def get_file_sha256(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def generate():
    repo_data = {}
    apk_dir = "apk"
    
    if not os.path.exists(apk_dir):
        os.makedirs(apk_dir)

    for apk_name in os.listdir(apk_dir):
        if not apk_name.endswith(".apk"):
            continue
            
        apk_path = os.path.join(apk_dir, apk_name)
        
        try:
            parts = apk_name.replace(".apk", "").split("-")
            pkg = parts[0]
            version_name = parts[1].replace("v", "")
            version_code = int(parts[2].replace("c", ""))
            
            if "dhakaflix2" in pkg:
                name = "Aniyomi: DhakaFlix 2"
            elif "dflixbackup" in pkg:
                name = "Aniyomi: Dflix backup"
            elif "dflix" in pkg:
                name = "Aniyomi: Dflix"
            elif "dhakaflix" in pkg:
                name = "Aniyomi: Dhakadev"
            elif "ftpbd" in pkg:
                name = "Aniyomi: FtpBd"
            elif "amaderftp" in pkg:
                name = "Aniyomi: Amader FTP"
            elif "iccftp" in pkg:
                name = "Aniyomi: ICC FTP"
            elif "cineplexbd" in pkg:
                name = "Aniyomi: Cineplex BD"
            elif "jellyfinbijoy" in pkg:
                name = "Aniyomi: Bijoy"
            elif "roarzone" in pkg:
                name = "Aniyomi: RoarZone"
            elif "basplay" in pkg:
                name = "Aniyomi: Bas Play"
            elif "nagordola" in pkg:
                name = "Aniyomi: Nagordola"
            elif "udvash" in pkg:
                name = "Aniyomi: Udvash"
            else:
                name = pkg
            
            item = {
                "name": name,
                "pkg": pkg,
                "apk": apk_name,
                "lang": "all",
                "code": version_code,
                "version": version_name,
                "nsfw": 0,
                "hasReadme": 0,
                "hasChangelog": 0,
                "icon": f"https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/icon/{pkg}.png"
            }
            
            item["size"] = get_apk_size(apk_path)
            item["sha256"] = get_file_sha256(apk_path)
            
            if pkg not in repo_data or version_code > repo_data[pkg]["code"]:
                repo_data[pkg] = item
        except Exception as e:
            print(f"Skipping {apk_name} due to naming convention error: {e}")

    final_data = sorted(repo_data.values(), key=lambda x: x["name"])

    with open("index.min.json", "w") as f:
        json.dump(final_data, f, separators=(',', ':'))

    repo_info = {
        "meta": {
            "name": "SalmanBappi Extensions Repo",
            "shortName": "salmanbappi",
            "website": "https://github.com/salmanbappi/extensions-repo",
            "signingKeyFingerprint": "17a9a43374e4951aadb5f33e6d8b10a21e231cdfda050a0473a50254494dc040"
        }
    }
    with open("repo.json", "w") as f:
        json.dump(repo_info, f, indent=2)

if __name__ == "__main__":
    generate()
