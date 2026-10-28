import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path


def run_command(command: str) -> str:
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def load_json_safe(content: str):
    if not content:
        return None
    try:
        return json.loads(content)
    except Exception as e:
        print(f"Warning: Failed to parse JSON: {e}")
        return None


def get_old_index(before_sha: str | None) -> list[dict] | None:
    # 1. Try to fetch and show from before_sha if given and valid
    if before_sha and before_sha != "0000000000000000000000000000000000000000":
        print(f"Attempting to fetch previous commit: {before_sha}")
        run_command(f"git fetch origin {before_sha} --depth=1")
        old_str = run_command(f"git show {before_sha}:index.min.json")
        data = load_json_safe(old_str)
        if data is not None:
            return data

    # 2. Try HEAD~1 if commit depth permits
    rev_count_str = run_command("git rev-list --count HEAD")
    try:
        rev_count = int(rev_count_str)
    except Exception:
        rev_count = 1

    if rev_count > 1:
        print("Falling back to HEAD~1...")
        old_str = run_command("git show HEAD~1:index.min.json")
        data = load_json_safe(old_str)
        if data is not None:
            return data

    return None


def send_discord_message(
    target_url: str,
    headers: dict,
    embed: dict,
    apk_path: Path | None = None,
) -> bool:
    payload = {"embeds": [embed]}

    # Check if we should attach the APK file
    should_attach = (
        apk_path is not None
        and apk_path.is_file()
        and apk_path.stat().st_size <= 24 * 1024 * 1024  # Discord upload limit < 25MB
    )

    if should_attach:
        boundary = uuid.uuid4().hex
        post_headers = {
            **headers,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        }
        body = bytearray()
        # JSON Payload part
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(b'Content-Disposition: form-data; name="payload_json"\r\n')
        body.extend(b"Content-Type: application/json\r\n\r\n")
        body.extend(json.dumps(payload).encode())
        body.extend(b"\r\n")

        # File part
        try:
            with apk_path.open("rb") as f:
                file_bytes = f.read()

            body.extend(f"--{boundary}\r\n".encode())
            body.extend(
                f'Content-Disposition: form-data; name="files[0]"; filename="{apk_path.name}"\r\n'.encode()
            )
            body.extend(b"Content-Type: application/vnd.android.package-archive\r\n\r\n")
            body.extend(file_bytes)
            body.extend(b"\r\n")
            body.extend(f"--{boundary}--\r\n".encode())

            req = urllib.request.Request(target_url, data=body, headers=post_headers, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"Sent with attachment ({apk_path.name}): HTTP {resp.status}")
                return True
        except Exception as e:
            print(f"Attachment upload failed ({e}), falling back to embed only...")

    # Fallback / Embed-only send
    post_headers = {
        **headers,
        "Content-Type": "application/json",
    }
    try:
        req = urllib.request.Request(
            target_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=post_headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"Sent embed: HTTP {resp.status}")
            return True
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')}")
        return False
    except Exception as e:
        print(f"Network error: {e}")
        return False


def main():
    before_sha = os.environ.get("BEFORE_SHA")
    after_sha = os.environ.get("AFTER_SHA", "HEAD")
    discord_token = os.environ.get("DISCORD_BOT_TOKEN")
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    channel_id = os.environ.get("DISCORD_CHANNEL_ID", "1517517856231919687")
    force_all = os.environ.get("FORCE_NOTIFY_ALL", "").strip().lower() in {"true", "1", "yes"}

    if not discord_token and not webhook_url:
        print("Neither DISCORD_BOT_TOKEN nor DISCORD_WEBHOOK_URL is set. Exiting.")
        sys.exit(0)

    # Determine endpoint & authorization
    if webhook_url:
        target_url = webhook_url if "?" in webhook_url else f"{webhook_url}?wait=true"
        headers = {
            "User-Agent": "AniZen-Extension-Notifier/2.0",
        }
    else:
        target_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bot {discord_token}",
            "User-Agent": "AniZen-Extension-Notifier/2.0",
        }

    # Load current index
    new_index_path = Path("index.min.json")
    if not new_index_path.exists():
        print("index.min.json not found in current directory.")
        sys.exit(0)

    with new_index_path.open(encoding="utf-8") as f:
        try:
            new_index = json.load(f)
        except Exception as e:
            print(f"Failed to parse index.min.json: {e}")
            sys.exit(1)

    # Load old index
    old_index = get_old_index(before_sha)

    if old_index is None:
        if force_all:
            print("Force notify requested. Processing current extensions...")
            old_index = []
        else:
            print(
                "Notice: Unable to locate previous commit index for diff comparison "
                "(initial commit or forced push). Skipping bulk notifications to avoid spam."
            )
            sys.exit(0)

    old_map = {item["pkg"]: item for item in old_index if "pkg" in item}
    new_map = {item["pkg"]: item for item in new_index if "pkg" in item}

    # Detect additions and updates
    added_items = []
    updated_items = []

    for pkg, item in new_map.items():
        if pkg not in old_map:
            added_items.append(item)
        else:
            old_item = old_map[pkg]
            code_changed = item.get("code") != old_item.get("code")
            ver_changed = item.get("version") != old_item.get("version")
            apk_changed = item.get("apk") != old_item.get("apk")
            if code_changed or ver_changed or apk_changed:
                updated_items.append((item, old_item))

    total_changes = len(added_items) + len(updated_items)
    print(f"Diff Summary: {len(added_items)} added, {len(updated_items)} updated.")

    if total_changes == 0:
        print("No new or updated extensions found.")
        sys.exit(0)

    # Process additions
    for item in added_items:
        pkg = item["pkg"]
        apk_name = item.get("apk", "")
        apk_path = Path("apk") / apk_name
        apk_raw_url = f"https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/apk/{apk_name}"
        icon_url = f"https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/icon/{pkg}.png"

        sources_count = len(item.get("sources", []))
        source_note = f" • {sources_count} source(s)" if sources_count > 0 else ""

        embed = {
            "title": f"🆕 {item.get('name', pkg)} [{item.get('lang', 'all').upper()}]",
            "description": f"**New Extension Added!**\nDirect Download: [`{apk_name}`]({apk_raw_url})",
            "color": 0x10B981,  # Emerald Green
            "thumbnail": {"url": icon_url},
            "fields": [
                {
                    "name": "Version",
                    "value": f"`v{item.get('version', '1.0')}` (Code `{item.get('code', 0)}`){source_note}",
                    "inline": True,
                },
                {
                    "name": "Language",
                    "value": f"`{item.get('lang', 'all').upper()}`",
                    "inline": True,
                },
                {
                    "name": "Rating",
                    "value": "18+ 🔞" if item.get("nsfw") == 1 else "Safe ✅",
                    "inline": True,
                },
                {
                    "name": "Package",
                    "value": f"`{pkg}`",
                    "inline": False,
                },
            ],
            "footer": {
                "text": "SalmanBappi Extensions • AniZen / Aniyomi",
            },
        }

        print(f"Sending notification for new extension: {item.get('name')}")
        send_discord_message(target_url, headers, embed, apk_path)
        time.sleep(1)

    # Process updates
    for item, old_item in updated_items:
        pkg = item["pkg"]
        apk_name = item.get("apk", "")
        apk_path = Path("apk") / apk_name
        apk_raw_url = f"https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/apk/{apk_name}"
        icon_url = f"https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/icon/{pkg}.png"

        old_ver = old_item.get("version", "?")
        new_ver = item.get("version", "?")
        old_code = old_item.get("code", "?")
        new_code = item.get("code", "?")

        sources_count = len(item.get("sources", []))
        source_note = f" • {sources_count} source(s)" if sources_count > 0 else ""

        embed = {
            "title": f"🔄 {item.get('name', pkg)} [{item.get('lang', 'all').upper()}]",
            "description": (
                f"**Extension Updated!**\n"
                f"Upgrade: `v{old_ver}` (Build `{old_code}`) ➔ `v{new_ver}` (Build `{new_code}`)\n"
                f"Direct Download: [`{apk_name}`]({apk_raw_url})"
            ),
            "color": 0x7C3AED,  # Royal Violet
            "thumbnail": {"url": icon_url},
            "fields": [
                {
                    "name": "Latest Version",
                    "value": f"`v{new_ver}` (Code `{new_code}`){source_note}",
                    "inline": True,
                },
                {
                    "name": "Language",
                    "value": f"`{item.get('lang', 'all').upper()}`",
                    "inline": True,
                },
                {
                    "name": "Rating",
                    "value": "18+ 🔞" if item.get("nsfw") == 1 else "Safe ✅",
                    "inline": True,
                },
                {
                    "name": "Package",
                    "value": f"`{pkg}`",
                    "inline": False,
                },
            ],
            "footer": {
                "text": "SalmanBappi Extensions • AniZen / Aniyomi",
            },
        }

        print(f"Sending notification for updated extension: {item.get('name')}")
        send_discord_message(target_url, headers, embed, apk_path)
        time.sleep(1)


if __name__ == "__main__":
    main()
