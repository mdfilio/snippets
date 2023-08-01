import socket
import ssl
import argparse
import requests

def test_ssl(host, port):
    context = ssl.create_default_context()

    try:
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                print(f"Connection to {host} on port {port} using SSL is successful using system root CAs.")
                print(f"SSL protocol version being used is: {ssock.version()}")
    except Exception as e:
        print(f"System root CAs aren't updated for your {host} on port {port} using SSL.")

    try:
        response = requests.get(f"https://{host}:{port}")
        response.raise_for_status()
        print(f"GET request to https://{host}:{port} was successful. Response status code was: {response.status_code}")
    except Exception as e:
        print(f"System root CAs are being ignored. Check your application for options to point to a certificate.")

def main():
    parser = argparse.ArgumentParser(description='Test SSL connection and GET request to specified host and port.')
    parser.add_argument('host', type=str, help='Host to connect to.')
    parser.add_argument('port', type=int, help='Port to connect to.')

    args = parser.parse_args()

    test_ssl(args.host, args.port)

if __name__ == "__main__":
    main()

