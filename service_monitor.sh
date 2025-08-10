#!/bin/bash

# iDotMatrix Web Controller Service Monitor

case "$1" in
    status)
        echo "📊 Service Status:"
        sudo systemctl status idotmatrix-web --no-pager
        ;;
    logs)
        echo "📋 Recent Logs:"
        sudo journalctl -u idotmatrix-web -n 50 --no-pager
        ;;
    live)
        echo "🔴 Live Logs (Ctrl+C to exit):"
        sudo journalctl -u idotmatrix-web -f
        ;;
    restart)
        echo "🔄 Restarting service..."
        sudo systemctl restart idotmatrix-web
        echo "✅ Service restarted"
        ;;
    stop)
        echo "⏹️ Stopping service..."
        sudo systemctl stop idotmatrix-web
        echo "✅ Service stopped"
        ;;
    start)
        echo "▶️ Starting service..."
        sudo systemctl start idotmatrix-web
        echo "✅ Service started"
        ;;
    *)
        echo "iDotMatrix Web Controller Service Monitor"
        echo ""
        echo "Usage: $0 {status|logs|live|restart|stop|start}"
        echo ""
        echo "Commands:"
        echo "  status   - Show current service status"
        echo "  logs     - Show recent logs"
        echo "  live     - Show live logs (real-time)"
        echo "  restart  - Restart the service"
        echo "  stop     - Stop the service"
        echo "  start    - Start the service"
        ;;
esac