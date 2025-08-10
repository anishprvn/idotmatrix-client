# iDotMatrix Command Reference

Complete reference for all available commands and scripts in the iDotMatrix Web Controller.

## Web Server Commands

### Start Web UI (HTTP - Localhost)
```bash
./start_web_ui.sh
```
- Starts HTTP server on `http://localhost:8080`
- No SSL certificates required
- Best for local development

### Start Web UI (HTTPS - Domain/IP)
```bash
# Using config file
./start_web_ui_ip.sh

# With custom domain
./start_web_ui_ip.sh mydomain.com

# With Let's Encrypt
./start_web_ui_ip.sh mydomain.com user@email.com
```
- Uses HTTPS with SSL certificates
- Automatically uses Let's Encrypt for domains
- Falls back to self-signed certificates for IP addresses

### Manual Web Server Start
```bash
# HTTP (localhost)
python3 web_server.py --no-browser

# HTTPS with domain
python3 web_server.py --no-browser --domain mydomain.com --email user@email.com --port 443
```

## Service Management Commands

### Install Auto-Start Service
```bash
sudo ./install_service.sh
```
- Installs systemd service
- Enables auto-start on boot
- Starts the service immediately

### Service Monitoring
```bash
# Check service status
./service_monitor.sh status

# View recent logs
./service_monitor.sh logs

# View live logs (real-time)
./service_monitor.sh live

# Restart service
./service_monitor.sh restart

# Stop service
./service_monitor.sh stop

# Start service
./service_monitor.sh start
```

### Direct Systemd Commands
```bash
# Service status
sudo systemctl status idotmatrix-web

# Start service
sudo systemctl start idotmatrix-web

# Stop service
sudo systemctl stop idotmatrix-web

# Restart service
sudo systemctl restart idotmatrix-web

# Enable auto-start
sudo systemctl enable idotmatrix-web

# Disable auto-start
sudo systemctl disable idotmatrix-web

# View logs
sudo journalctl -u idotmatrix-web -f

# View logs from last hour
sudo journalctl -u idotmatrix-web --since "1 hour ago"
```

## Device Control Commands

### Basic Device Commands
```bash
# Scan for devices
./run_in_venv.sh --scan

# Sync time
./run_in_venv.sh --address MAC_ADDRESS --sync-time

# Set custom time
./run_in_venv.sh --address MAC_ADDRESS --sync-time --set-time 18-12-2023-19:10:10

# Screen control
./run_in_venv.sh --address MAC_ADDRESS --screen on
./run_in_venv.sh --address MAC_ADDRESS --screen off

# Reset device
./run_in_venv.sh --address MAC_ADDRESS --reset

# Flip screen
./run_in_venv.sh --address MAC_ADDRESS --flip-screen true
```

### Clock Commands
```bash
# Set clock style (0-7)
./run_in_venv.sh --address MAC_ADDRESS --clock 0

# Clock with date
./run_in_venv.sh --address MAC_ADDRESS --clock 0 --clock-with-date

# 24-hour format
./run_in_venv.sh --address MAC_ADDRESS --clock 0 --clock-24h

# Clock color (R-G-B format)
./run_in_venv.sh --address MAC_ADDRESS --clock 0 --clock-color 255-0-0
```

### Text Display Commands
```bash
# Basic text
./run_in_venv.sh --address MAC_ADDRESS --set-text "Hello World"

# Text with options
./run_in_venv.sh --address MAC_ADDRESS --set-text "Hello World" \
  --text-size 10 \
  --text-mode 1 \
  --text-speed 50 \
  --text-color 255-255-255 \
  --text-bg-color 0-0-255
```

### Timer Commands
```bash
# Stopwatch control (0=reset, 1=start, 2=pause, 3=continue)
./run_in_venv.sh --address MAC_ADDRESS --chronograph 1

# Countdown (0=disable, 1=start, 2=pause, 3=restart)
./run_in_venv.sh --address MAC_ADDRESS --countdown 1 --countdown-time 5-30
```

### Color Commands
```bash
# Fullscreen color
./run_in_venv.sh --address MAC_ADDRESS --fullscreen-color 255-255-255

# Single pixel color (X-Y-R-G-B)
./run_in_venv.sh --address MAC_ADDRESS --pixel-color 10-10-255-255-255
```

### Image Commands
```bash
# Display image
./run_in_venv.sh --address MAC_ADDRESS --image true --set-image ./images/demo_32.png

# Process and display image
./run_in_venv.sh --address MAC_ADDRESS --image true --set-image ./images/demo_512.png --process-image 32

# Display GIF
./run_in_venv.sh --address MAC_ADDRESS --set-gif ./images/demo.gif

# Process and display GIF
./run_in_venv.sh --address MAC_ADDRESS --set-gif ./images/demo.gif --process-gif 32
```

### Scoreboard Commands
```bash
# Set scoreboard (Player1-Player2)
./run_in_venv.sh --address MAC_ADDRESS --scoreboard 21-12
```

## Configuration Files

### Server Configuration (`server_config.json`)
```json
{
  "domain": "yourdomain.com",
  "email": "your@email.com"
}
```

### Web Configuration (`web_config.json`)
```json
{
  "saved_mac_address": "XX:XX:XX:XX:XX:XX"
}
```

## Environment Setup Commands

### Virtual Environment
```bash
# Create virtual environment
./create_venv.sh

# Run command in virtual environment
./run_in_venv.sh [COMMAND_ARGS]
```

### SSL Certificate Management
```bash
# Generate Let's Encrypt certificate
sudo certbot certonly --standalone --email your@email.com -d yourdomain.com

# Check certificate
openssl x509 -in server.crt -text -noout

# Test SSL connection
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

## Troubleshooting Commands

### Check Service Status
```bash
# Is service running?
systemctl is-active idotmatrix-web

# Is service enabled for auto-start?
systemctl is-enabled idotmatrix-web

# Check if ports are in use
sudo netstat -tlnp | grep :443
sudo netstat -tlnp | grep :8080
```

### Network Testing
```bash
# Test domain resolution
nslookup yourdomain.com

# Test HTTP connection
curl -I http://localhost:8080

# Test HTTPS connection (ignore certificate)
curl -k -I https://localhost:443
```

### Log Analysis
```bash
# View all service logs
sudo journalctl -u idotmatrix-web --no-pager

# View logs with timestamps
sudo journalctl -u idotmatrix-web -o short-iso

# View only errors
sudo journalctl -u idotmatrix-web -p err

# Follow logs in real-time
sudo journalctl -u idotmatrix-web -f
```

## Quick Reference

### Most Common Commands
```bash
# Start for local use
./start_web_ui.sh

# Start for remote access with HTTPS
sudo ./start_web_ui_ip.sh

# Install as service
sudo ./install_service.sh

# Check service status
./service_monitor.sh status

# View live logs
./service_monitor.sh live
```

### Emergency Commands
```bash
# Stop all Python processes (if stuck)
sudo pkill -f python3

# Restart networking (if connection issues)
sudo systemctl restart networking

# Check system resources
htop
df -h
free -h
```