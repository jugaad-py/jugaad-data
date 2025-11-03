#!/usr/bin/env python3
"""
Version checker script for jugaad-data package.
Checks if the current version in pyproject.toml already exists on PyPI.
"""

import sys
import tomllib
import requests
from pathlib import Path


def get_current_version():
    """Read version from pyproject.toml"""
    try:
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    except Exception as e:
        print(f"❌ Error reading pyproject.toml: {e}")
        sys.exit(1)


def check_pypi_version(package_name, version):
    """Check if version exists on PyPI"""
    url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True  # Version exists
        elif response.status_code == 404:
            return False  # Version doesn't exist
        else:
            print(f"⚠️  Warning: Unexpected response from PyPI (HTTP {response.status_code})")
            return None
    except requests.RequestException as e:
        print(f"❌ Error checking PyPI: {e}")
        return None


def main():
    package_name = "jugaad-data"
    
    # Get current version
    current_version = get_current_version()
    print(f"📦 Current version in pyproject.toml: {current_version}")
    
    # Check PyPI
    print("🔍 Checking PyPI...")
    exists = check_pypi_version(package_name, current_version)
    
    if exists is True:
        print(f"❌ ERROR: Version {current_version} already exists on PyPI!")
        print("🔧 Please update the version in pyproject.toml before deploying.")
        print(f"🌐 View existing versions: https://pypi.org/project/{package_name}/#history")
        sys.exit(1)
    elif exists is False:
        print(f"✅ Version {current_version} is available on PyPI. Safe to deploy!")
        sys.exit(0)
    else:
        print("⚠️  Could not verify PyPI status. Proceed with caution.")
        sys.exit(2)


if __name__ == "__main__":
    main()