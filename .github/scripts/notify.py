import json
import os
import subprocess
import sys
import urllib.request
import uuid
from pathlib import Path

def run_command(command: str) -> str:
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(result.stderr.strip())
        return ""
    return result.stdout.strip()

def main():
    before_sha = os.environ.get("BEFORE_SHA")
    after_sha = os.environ.get("AFTER_SHA", "HEAD")
    discord_token = os.environ.get("DISCORD_BOT_TOKEN")
    channel_id = "1517517856231919687"
    
    if not discord_token:
        print("DISCORD_BOT_TOKEN environment variable not set.")
        sys.exit(0)
        
    print(f"Comparing before_sha={before_sha} and after_sha={after_sha}")
    
    # Load old index
    old_index = []
    if before_sha and before_sha != "0000000000000000000000000000000000000000":
        # Fetch the before_sha to make sure it's available locally
        run_command(f"git fetch origin {before_sha} --depth=1")
        old_index_str = run_command(f"git show {before_sha}:index.min.json")
        if old_index_str:
            try:
                old_index = json.loads(old_index_str)
            except Exception as e:
                print("Failed to parse old index JSON:", e)
    else:
        # Fallback to HEAD~1 if before_sha is missing/invalid
        old_index_str = run_command("git show HEAD~1:index.min.json")
        if old_index_str:
            try:
                old_index = json.loads(old_index_str)
            except Exception as e:
                print("Failed to parse HEAD~1 index JSON:", e)

    # Load new index (from local workspace)
    new_index_path = Path("index.min.json")
    if not new_index_path.exists():
        print("index.min.json not found in current directory.")
        sys.exit(0)
        
    with new_index_path.open(encoding="utf-8") as f:
        try:
            new_index = json.load(f)
        except Exception as e:
            print("Failed to parse new index JSON:", e)
            sys.exit(1)

    old_pkgs = {x["pkg"] for x in old_index}
    new_extensions = [item for item in new_index if item["pkg"] not in old_pkgs]
    
    if not new_extensions:
        print("No new extensions found.")
        sys.exit(0)
        
    print(f"Found {len(new_extensions)} new extension(s) to send to Discord.")
    
    for item in new_extensions:
        apk_name = item["apk"]
        apk_path = Path("apk") / apk_name
        
        message_content = (
            f"🆕 **New Extension Added!**\n"
            f"**Name:** {item['name']}\n"
            f"**Package:** `{item['pkg']}`\n"
            f"**Language:** `{item['lang'].upper()}`\n"
            f"**Version:** `{item['version']}`\n"
            f"**NSFW:** {'Yes 🔞' if item['nsfw'] == 1 else 'No'}"
        )
        
        if apk_path.exists():
            print(f"Sending {apk_name} to Discord channel {channel_id}...")
            boundary = uuid.uuid4().hex
            url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
            
            headers = {
                "Authorization": f"Bot {discord_token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            
            try:
                with apk_path.open("rb") as f:
                    file_data = f.read()
                
                payload = json.dumps({"content": message_content})
                
                body = bytearray()
                body.extend(f"--{boundary}\r\n".encode())
                body.extend(f'Content-Disposition: form-data; name="payload_json"\r\n'.encode())
                body.extend(b'Content-Type: application/json\r\n\r\n')
                body.extend(f"{payload}\r\n".encode())
                
                body.extend(f"--{boundary}\r\n".encode())
                body.extend(f'Content-Disposition: form-data; name="files[0]"; filename="{apk_name}"\r\n'.encode())
                body.extend(b'Content-Type: application/octet-stream\r\n\r\n')
                body.extend(file_data)
                body.extend(b'\r\n')
                
                body.extend(f"--{boundary}--\r\n".encode())
                
                req = urllib.request.Request(url, data=body, headers=headers, method="POST")
                with urllib.request.urlopen(req) as response:
                    print(f"Successfully sent {apk_name} to Discord: {response.read().decode()}")
            except Exception as e:
                print(f"Failed to send {apk_name} to Discord: {e}")
                if hasattr(e, 'read'):
                    try:
                        print("Response details:", e.read().decode())
                    except Exception:
                        pass
        else:
            print(f"Apk path not found: {apk_path}")

if __name__ == "__main__":
    main()
