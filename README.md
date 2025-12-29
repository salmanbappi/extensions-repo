# SalmanBappi's Aniyomi Extensions Repository

This is a dedicated repository for custom Aniyomi/Anikku extensions, primarily focusing on BDIX-based streaming services and local content providers.

## How to Add to Aniyomi / Anikku

To use these extensions in Aniyomi or Anikku:

1.  Open **Aniyomi** or **Anikku**.
2.  Go to **Settings** -> **Browse** -> **Extension repositories**.
3.  Click **Add**.
4.  Enter the following URL:
    ```
    https://raw.githubusercontent.com/salmanbappi/extensions-repo/main/index.min.json
    ```
5.  After adding, you can find the extensions in the **Extensions** tab under the **Anime** category.

## Available Extensions

Currently, this repository hosts the following extensions:

- **DhakaFlix / Dhakadev**: Support for DhakaFlix (BDIX) streaming.
- **DhakaFlix 2**: Updated version for new DhakaFlix infrastructure.
- **FtpBd**: Support for FtpBd.net.
- **Dflix**: Support for Dflix streaming.
- **Nagordola**: Support for Nagordola content.
- **Udvash**: Support for Udvash educational content.

## Technical Information

- **Repository Website**: [https://github.com/salmanbappi/extensions-repo](https://github.com/salmanbappi/extensions-repo)

## Maintenance

This repository is automatically updated via GitHub Actions. When a new version of an extension is built in its respective repository, it is pushed here, and the `index.min.json` is regenerated.