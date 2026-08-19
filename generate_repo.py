import json
import os
import hashlib
import sys

# Definitive Source IDs as INTEGERS (Longs)
SOURCE_MAP = {
    "eu.kanade.tachiyomi.animeextension.all.dhakaflix2": [
        {"name": "DhakaFlix (Hindi & South Indian)", "lang": "all", "id": "5181466391484419941", "baseUrl": "http://172.16.50.14"},
        {"name": "DhakaFlix (TV & Web Series)", "lang": "all", "id": "5181466391484419942", "baseUrl": "http://172.16.50.12"},
        {"name": "DhakaFlix (Anime & Documentary)", "lang": "all", "id": "5181466391484419943", "baseUrl": "http://172.16.50.9"},
        {"name": "DhakaFlix (English & International)", "lang": "all", "id": "5181466391484419944", "baseUrl": "http://172.16.50.7"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.dhakaflix": [
        {"name": "DhakaFlix", "lang": "all", "id": 5181466391484419841, "baseUrl": "http://172.16.50.9"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.dflix": [
        {"name": "Dflix", "lang": "all", "id": 5181466391484419844, "baseUrl": "https://dflix.discoveryftp.net"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.dflixbackup": [
        {"name": "Dflix backup", "lang": "all", "id": 5181466391484419844, "baseUrl": "https://dflix.discoveryftp.net"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.ftpbd": [
        {"name": "FtpBd", "lang": "all", "id": 23418800222257732, "baseUrl": "https://server3.ftpbd.net"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.amaderftp": [
        {"name": "Amader FTP", "lang": "all", "id": 84769302158234567, "baseUrl": "http://amaderftp.net:8096"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.iccftp": [
        {"name": "IccFtp", "lang": "all", "id": 84726193058274619, "baseUrl": "http://10.16.100.244"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.cineplexbd": [
        {"name": "Cineplex BD", "lang": "all", "id": 5181466391484419848, "baseUrl": "http://cineplexbd.net"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.jellyfinbijoy": [
        {"name": "Jellyfin Bijoy", "lang": "all", "id": 73658291047123456, "baseUrl": "http://10.20.30.50"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.agnisys": [
        {"name": "AgniSYS", "lang": "all", "id": 84759302158234567, "baseUrl": "http://182.252.81.180:8096"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.roarzone": [
        {"name": "RoarZone", "lang": "all", "id": 84769302158234568, "baseUrl": "http://10.16.100.200"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.basplay": [
        {"name": "Bas play", "lang": "all", "id": 5181466391484419847, "baseUrl": "http://103.87.212.46"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.nagordola": [
        {"name": "Nagordola", "lang": "all", "id": 5181466391484419845, "baseUrl": "https://cdn.nagordola.com.bd"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.udvash": [
        {"name": "Udvash", "lang": "all", "id": 5181466391484419846, "baseUrl": "https://online.udvash-unmesh.com"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.nepu": [
        {"name": "Nepu", "lang": "all", "id": 5181466391484419855, "baseUrl": "https://nepu.to"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.fmftp": [
        {"name": "FM FTP", "lang": "all", "id": 7214566391484419847, "baseUrl": "https://fmftp.net"}
    ],
    "eu.kanade.tachiyomi.animeextension.en.toonworld4all": [
        {"name": "ToonWorld4All", "lang": "en", "id": 5181466391484419850, "baseUrl": "https://toonworld4all.me"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.infomedia": [
        {"name": "InfoMedia", "lang": "all", "id": 3615736726452648083, "baseUrl": "http://103.225.94.27/mediaserver"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.fanush": [
        {"name": "Fanush", "lang": "all", "id": 5181466391484419852, "baseUrl": "http://103.132.95.221:8096"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.livesports": [
        {"name": "Live Sports", "lang": "all", "id": 8246513271928475192, "baseUrl": "http://10.20.30.40"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.bdixlivetv": [
        {"name": "BDIX Live TV", "lang": "all", "id": 4519283712345678910, "baseUrl": "http://172.16.29.28"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.mangolivetv": [
        {"name": "Mango Live TV", "lang": "all", "id": 8519283712345678910, "baseUrl": "http://10.114.130.254"}
    ],
    "eu.kanade.tachiyomi.animeextension.all.moviebox": [
        {"name": "MovieBox", "lang": "all", "id": 3508466391484419848, "baseUrl": "https://moviebox.ph"}
    ]
}

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
            elif "infomedia" in pkg:
                name = "Aniyomi: InfoMedia"
            elif "fanush" in pkg:
                name = "Aniyomi: Fanush"
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
            elif "agnisys" in pkg:
                name = "Aniyomi: AgniSYS"
            elif "roarzonetv" in pkg:
                name = "Aniyomi: Roar zone tv"
            elif "roarzone" in pkg:
                name = "Aniyomi: RoarZone"
            elif "basplay" in pkg:
                name = "Aniyomi: Bas Play"
            elif "nagordola" in pkg:
                name = "Aniyomi: Nagordola"
            elif "udvash" in pkg:
                name = "Aniyomi: Udvash"
            elif "nepu" in pkg:
                name = "Aniyomi: Nepu"
            elif "fmftp" in pkg:
                name = "Aniyomi: FM FTP"
            elif "livesports" in pkg:
                name = "Aniyomi: Live Sports"
            elif "bdixlivetv" in pkg:
                name = "Aniyomi: BDIX Live TV"
            elif "mangolivetv" in pkg:
                name = "Aniyomi: Mango Live TV"
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
            
            if pkg in SOURCE_MAP:
                item["sources"] = SOURCE_MAP[pkg]
            
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
            "name": "SalmanBappi extension repo",
            "shortName": "salmanbappi",
            "website": "https://github.com/salmanbappi/extensions-repo",
            "signingKeyFingerprint": "c7ebe223044970f2f9738f600dc25c180d3ed03994e088aaf5709338c57b93af"
        }
    }
    with open("repo.json", "w") as f:
        json.dump(repo_info, f, indent=2)

if __name__ == "__main__":
    generate()
