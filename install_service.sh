#!/bin/bash

# Install iDotMatrix Web Controller as systemd service

echo "🔧 Installing iDotMatrix Web Controller service..."

# Copy service file to systemd directory
sudo cp idotmatrix-web.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable idotmatrix-web.service

# Start the service
sudo systemctl start idotmatrix-web.service

echo "✅ Service installed and started!"
echo ""
echo "Service commands:"
echo "  sudo systemctl status idotmatrix-web    # Check status"
echo "  sudo systemctl stop idotmatrix-web      # Stop service"
echo "  sudo systemctl start idotmatrix-web     # Start service"
echo "  sudo systemctl restart idotmatrix-web   # Restart service"
echo "  sudo systemctl disable idotmatrix-web   # Disable auto-start"