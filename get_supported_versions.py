#!/usr/bin/env python3
"""
Script to determine supported Ubuntu versions from the endoflife.date API.
Logic: Support the first ubuntu version and the first two LTS versions.
If the first version is an LTS version, only support the latest 2 LTS versions.
"""

import json
import sys
import urllib.request
from datetime import datetime
from typing import List, Dict, Any


def fetch_ubuntu_versions() -> List[Dict[str, Any]]:
    """Fetch Ubuntu versions from the endoflife.date API."""
    url = "https://endoflife.date/api/ubuntu.json"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        return data
    except Exception as e:
        print(f"Error fetching Ubuntu versions: {e}", file=sys.stderr)
        sys.exit(1)


def get_supported_versions(versions: List[Dict[str, Any]]) -> List[str]:
    """
    Determine supported Ubuntu versions based on the logic:
    - Support the first ubuntu version and the first two LTS versions
    - If the first version is an LTS version, only support the latest 2 LTS versions
    """
    if not versions:
        return []

    # Sort versions by release date (most recent first)
    sorted_versions = sorted(
        versions,
        key=lambda x: datetime.fromisoformat(x['releaseDate']),
        reverse=True
    )

    # Get the first (most recent) version
    first_version = sorted_versions[0]

    # Get all LTS versions, sorted by release date (most recent first)
    lts_versions = [v for v in sorted_versions if v.get('lts', False)]

    supported_versions = []

    if first_version.get('lts', False):
        # If the first version is LTS, support the latest 2 LTS versions
        supported_versions = lts_versions[:2]
    else:
        # Support the first version and the first two LTS versions
        supported_versions.append(first_version)
        supported_versions.extend(lts_versions[:2])

    # Extract codenames and convert to lowercase (removing spaces)
    codenames = []
    for version in supported_versions:
        codename = version.get('codename', '').lower().split()[0]  # Take first word and lowercase
        if codename:
            codenames.append(codename)

    return codenames


def main():
    """Main function to fetch and print supported Ubuntu versions as JSON for GitHub Actions."""
    versions = fetch_ubuntu_versions()
    supported = get_supported_versions(versions)

    # Output only the JSON array needed for GitHub Actions
    print(json.dumps(supported))


if __name__ == "__main__":
    main()
