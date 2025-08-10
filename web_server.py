#!/usr/bin/env python3
"""
Simple web server for iDotMatrix Web Controller
Serves the HTML interface and handles command execution
"""

import asyncio
import json
import os
import subprocess
import sys
import ssl
import ipaddress
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class iDotMatrixHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    

    
    def do_POST(self):
        """Handle POST requests for command execution"""
        if self.path == '/execute':
            self.handle_execute()
        elif self.path == '/save-address':
            self.handle_save_address()
        else:
            self.send_error(404, "Not Found")
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/web_ui.html'
        elif self.path == '/load-address':
            self.handle_load_address()
            return
        super().do_GET()
    
    def handle_execute(self):
        """Execute iDotMatrix commands"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Get command arguments
            args = data.get('args', [])
            if not args:
                self.send_error(400, "No command arguments provided")
                return
            
            # Execute command
            result = self.execute_command(args)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(result.encode('utf-8'))
            
        except Exception as e:
            logger.error(f"Error handling execute request: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def handle_save_address(self):
        """Save MAC address to config file"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            address = data.get('address', '')
            if address:
                config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web_config.json')
                config = {'saved_mac_address': address}
                
                with open(config_file, 'w') as f:
                    json.dump(config, f)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'saved'}).encode('utf-8'))
            else:
                self.send_error(400, "No address provided")
        except Exception as e:
            logger.error(f"Error saving address: {e}")
            self.send_error(500, f"Error saving address: {str(e)}")
    
    def handle_load_address(self):
        """Load MAC address from config file"""
        try:
            config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web_config.json')
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                address = config.get('saved_mac_address', '')
            else:
                address = ''
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'address': address}).encode('utf-8'))
        except Exception as e:
            logger.error(f"Error loading address: {e}")
            self.send_error(500, f"Error loading address: {str(e)}")
    
    def execute_command(self, args):
        """Execute the iDotMatrix command"""
        try:
            # Determine the correct script to run
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Check if we should use the virtual environment
            venv_script = os.path.join(script_dir, 'run_in_venv.sh')
            if os.path.exists(venv_script):
                # Use the virtual environment script
                cmd = ['bash', venv_script] + args
            else:
                # Fall back to direct python execution
                app_script = os.path.join(script_dir, 'app.py')
                cmd = [sys.executable, app_script] + args
            
            logger.info(f"Executing command: {' '.join(cmd)}")
            
            # Execute the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                cwd=script_dir
            )
            
            # Combine stdout and stderr
            output = result.stdout
            if result.stderr:
                output += f"\nErrors: {result.stderr}"
            
            if result.returncode != 0:
                output += f"\nCommand failed with return code: {result.returncode}"
            
            return output or "Command executed successfully"
            
        except subprocess.TimeoutExpired:
            return "Command timed out after 30 seconds"
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return f"Error executing command: {str(e)}"
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"{self.address_string()} - {format % args}")

def setup_letsencrypt_cert(domain, email):
    """Setup Let's Encrypt certificate using certbot"""
    try:
        # Check if certbot is installed
        subprocess.run(['certbot', '--version'], check=True, capture_output=True)
        
        # Run certbot to get certificate
        cmd = [
            'certbot', 'certonly', '--standalone',
            '--non-interactive', '--agree-tos',
            '--email', email,
            '-d', domain
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            cert_path = f'/etc/letsencrypt/live/{domain}/fullchain.pem'
            key_path = f'/etc/letsencrypt/live/{domain}/privkey.pem'
            
            if os.path.exists(cert_path) and os.path.exists(key_path):
                print(f"✅ Let's Encrypt certificate obtained for {domain}")
                return cert_path, key_path
            else:
                print("❌ Certificate files not found after certbot run")
                return None, None
        else:
            print(f"❌ Certbot failed: {result.stderr}")
            return None, None
            
    except subprocess.CalledProcessError:
        print("❌ Certbot not installed. Install with: sudo apt install certbot")
        return None, None
    except Exception as e:
        print(f"❌ Error setting up Let's Encrypt: {e}")
        return None, None

def create_self_signed_cert(cert_file, key_file):
    """Create a self-signed certificate for HTTPS"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(u"localhost"),
                x509.IPAddress(ipaddress.IPv4Address(u"127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write certificate
        with open(cert_file, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Write private key
        with open(key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print(f"✅ Created self-signed certificate: {cert_file}, {key_file}")
        
    except ImportError:
        # Fallback to openssl command if cryptography is not available
        print("📦 cryptography library not found, using openssl...")
        subprocess.run([
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-keyout', key_file,
            '-out', cert_file, '-days', '365', '-nodes', '-subj', '/CN=localhost'
        ], check=True)
        print(f"✅ Created self-signed certificate: {cert_file}, {key_file}")
    except Exception as e:
        print(f"❌ Failed to create certificate: {e}")
        print("Please install cryptography: pip install cryptography")
        sys.exit(1)

def start_server(port=8080, open_browser=True, domain=None, email=None):
    """Start the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, iDotMatrixHandler)
    
    # Auto-detect if we should use HTTPS
    use_https = domain is not None and domain != 'localhost'
    protocol = "https" if use_https else "http"
    
    if use_https:
        cert_file = 'server.crt'
        key_file = 'server.key'
        
        # Try Let's Encrypt for real domains
        if email:
            letsencrypt_cert, letsencrypt_key = setup_letsencrypt_cert(domain, email)
            if letsencrypt_cert and letsencrypt_key:
                cert_file = letsencrypt_cert
                key_file = letsencrypt_key
            else:
                print("⚠️  Falling back to self-signed certificate")
                if not os.path.exists(cert_file) or not os.path.exists(key_file):
                    create_self_signed_cert(cert_file, key_file)
        else:
            # Use self-signed certificate for IP addresses
            if not os.path.exists(cert_file) or not os.path.exists(key_file):
                create_self_signed_cert(cert_file, key_file)
        
        # Wrap socket with SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                  iDotMatrix Web Controller                   ║
╠══════════════════════════════════════════════════════════════╣
║  Server started successfully!                                ║
║                                                              ║
║  🌐 Open your browser and go to:                            ║
║     {protocol}://localhost:{port}                                   ║
║                                                              ║
║  📱 Or from another device on your network:                 ║
║     {protocol}://YOUR_IP_ADDRESS:{port}                            ║
║                                                              ║
║  Press Ctrl+C to stop the server                            ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Auto-open browser
    if open_browser:
        import threading
        import webbrowser
        import time
        
        def open_browser_delayed():
            time.sleep(1)  # Wait a second for server to be ready
            try:
                webbrowser.open(f'{protocol}://localhost:{port}')
                print("🌐 Browser opened automatically!")
            except Exception as e:
                print(f"Could not open browser automatically: {e}")
        
        threading.Thread(target=open_browser_delayed, daemon=True).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        httpd.shutdown()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='iDotMatrix Web Controller Server')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on (default: 8080)')
    parser.add_argument('--no-browser', action='store_true', help='Do not automatically open browser')
    parser.add_argument('--domain', type=str, help='Domain name or IP address (auto-detects HTTPS need)')
    parser.add_argument('--email', type=str, help='Email address for Let\'s Encrypt certificate')
    args = parser.parse_args()
    
    start_server(args.port, not args.no_browser, args.domain, args.email)