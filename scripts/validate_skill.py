#!/usr/bin/env python3
"""Compatibility wrapper for older docs."""

from skill_funding import main


if __name__ == "__main__":
    main(["validate", "--repo-root", "."])

