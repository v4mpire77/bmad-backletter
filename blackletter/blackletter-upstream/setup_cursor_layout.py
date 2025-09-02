#!/usr/bin/env python3
"""
Cursor IDE Layout Setup Script
Sets up the AI chat panel on the left side of Cursor IDE
"""

import time
import sys

def print_step(step_num, description, shortcut=None):
    """Print a formatted step with optional shortcut"""
    print(f"\n{step_num}. {description}")
    if shortcut:
        print(f"   Shortcut: {shortcut}")

def main():
    print("🎯 Cursor IDE Layout Setup")
    print("=" * 40)
    print("This script will guide you through setting up the AI chat panel on the left.")
    
    input("\nPress Enter to continue...")
    
    print_step(1, "Open Cursor IDE", "Launch Cursor application")
    print_step(2, "Open AI Chat Panel", "Ctrl+I (or Cmd+I on Mac)")
    print_step(3, "Pin Chat to Left Side", "Look for pin/dock icon in chat header")
    print_step(4, "Adjust Panel Width", "Drag divider to ~1/3 screen width")
    print_step(5, "Verify Layout", "Chat left, editor middle, explorer right")
    
    print("\n🎉 Layout should now match the reference image!")
    print("\nIf the chat panel won't stay open:")
    print("- Check your Cursor subscription/plan")
    print("- Restart Cursor if AI features seem disabled")
    print("- Make sure you're in a Cursor workspace")

if __name__ == "__main__":
    main()
