# 🌐 iDotMatrix Web Controller

A modern, user-friendly web interface for controlling your iDotMatrix pixel displays. This web-based UI provides an intuitive alternative to the command-line interface and complements the existing PyQt5 GUI.

## ✨ Features

### 🎯 Easy-to-Use Interface
- **Modern Design**: Clean, responsive web interface that works on desktop and mobile
- **Visual Controls**: Color pickers, sliders, and dropdown menus for easy configuration
- **Real-time Console**: See command output and status updates in real-time
- **Device Management**: Scan for and connect to multiple devices

### 🔧 Complete Control Set
- **Basic Controls**: Screen on/off, time sync, device reset
- **Clock Settings**: Multiple styles, colors, date/time formats
- **Text Display**: Custom text with animations, colors, and effects
- **Color Controls**: Fullscreen colors and pixel-level control
- **Timers**: Stopwatch and countdown functionality
- **Scoreboard**: Two-player score tracking
- **File Upload**: Images and GIFs (with processing options)

### 📱 Cross-Platform Compatibility
- Works on any device with a web browser
- No additional software installation required
- Access from phones, tablets, laptops, or desktops
- Network access allows remote control

## 🚀 Quick Start

### Option 1: Using the Launcher Scripts

**Linux/macOS:**
```bash
./start_web_ui.sh
```

**Windows:**
```batch
start_web_ui.bat
```

### Option 2: Manual Start

1. **Activate virtual environment** (if using one):
   ```bash
   source my-venv/bin/activate  # Linux/macOS
   # or
   my-venv\Scripts\activate.bat  # Windows
   ```

2. **Start the web server**:
   ```bash
   python3 web_server.py
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:8080
   ```

## 🔧 Configuration

### Custom Port
To run on a different port:
```bash
python3 web_server.py --port 9000
```

### Network Access
To access from other devices on your network:
1. Find your computer's IP address
2. Start the server as usual
3. Access from other devices using: `http://YOUR_IP_ADDRESS:8080`

## 📖 Usage Guide

### 1. Device Connection
1. **Enter Device Address**: Type your device's MAC address or use "auto" for auto-discovery
2. **Scan for Devices**: Click the scan button to find nearby devices
3. **Connect**: Click connect to establish connection

### 2. Basic Controls
- **Sync Time**: Synchronize device time with your computer
- **Screen On/Off**: Control display power
- **Reset Device**: Reset the device to clear any glitches

### 3. Clock Settings
- **Style**: Choose from 8 different clock styles
- **Color**: Pick custom colors for the clock display
- **Options**: Enable date display and 24-hour format

### 4. Text Display
- **Text Input**: Enter any text to display
- **Size & Mode**: Choose text size and animation effects
- **Colors**: Set text and background colors
- **Speed**: Adjust animation speed with the slider

### 5. Timers
- **Stopwatch**: Start, pause, and reset functionality
- **Countdown**: Set minutes and seconds for countdown timer

### 6. Scoreboard
- Set scores for two players (0-999 each)

### 7. File Upload
- **Images**: Upload PNG/JPG files with automatic resizing
- **GIFs**: Upload animated GIFs with processing options

## 🔍 Troubleshooting

### Common Issues

**"Connection refused" or server won't start:**
- Check if port 8080 is already in use
- Try a different port: `python3 web_server.py --port 9000`
- Ensure Python 3 is installed and accessible

**Commands not executing:**
- Verify the device address is correct
- Check that the device is powered on and in range
- Ensure Bluetooth is enabled on your computer

**File uploads not working:**
- File upload requires the files to be accessible to the server
- Large files may take time to process
- Ensure the file format is supported (PNG, JPG, GIF)

**Web interface not loading:**
- Clear your browser cache
- Try a different browser
- Check the console for JavaScript errors

### Debug Mode
For detailed logging, check the server console output. All commands and their results are logged there.

## 🔒 Security Notes

- The web server runs locally by default (localhost only)
- When enabling network access, ensure you're on a trusted network
- The server has basic security measures but is intended for local/trusted network use

## 🆚 Comparison with Other UIs

| Feature | Web UI | PyQt5 GUI | Command Line |
|---------|--------|-----------|--------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Mobile Access** | ✅ | ❌ | ❌ |
| **Remote Access** | ✅ | ❌ | ✅ |
| **Visual Feedback** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Advanced Features** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Setup Required** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🤝 Contributing

The web UI is designed to be easily extensible. To add new features:

1. **Add UI elements** in `web_ui.html`
2. **Add JavaScript functions** for the new controls
3. **Update the server** in `web_server.py` if needed
4. **Test thoroughly** with actual hardware

## 📝 Technical Details

### Architecture
- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)
- **Backend**: Python HTTP server with command execution
- **Communication**: REST API with JSON payloads
- **Command Execution**: Calls existing `app.py` script

### Files
- `web_ui.html`: Main web interface
- `web_server.py`: Python web server
- `start_web_ui.sh`: Linux/macOS launcher
- `start_web_ui.bat`: Windows launcher

### Dependencies
- Python 3.x (standard library only)
- Existing iDotMatrix project dependencies
- Modern web browser

## 📄 License

This web UI follows the same license as the main iDotMatrix project (GNU General Public License).

---

**Enjoy controlling your iDotMatrix displays with the new web interface! 🎉**