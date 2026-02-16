#!/usr/bin/env python3
"""
OpenClaw Workspace - Hello World Example
Created: 2026-02-16
"""

def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to OpenClaw."

def main():
    """Main function."""
    names = ["World", "OpenClaw", "GitHub"]
    for name in names:
        print(greet(name))

if __name__ == "__main__":
    main()
