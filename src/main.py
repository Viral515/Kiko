import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tray_icon import TrayIcon

if __name__ == "__main__":
    tray = TrayIcon()
    tray.run()