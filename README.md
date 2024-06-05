# Ddos-script
This is an advanced DDoS (Distributed Denial of Service) script for ethical testing purposes. The script allows you to conduct stress tests on network services using UDP, TCP, or HTTP protocols.

Features
Multi-Protocol Support: Supports UDP, TCP, and HTTP protocols.
Customizable Parameters: Adjust number of threads, packet size, attack duration, etc.
HTTP Support: Send GET or POST requests with a customizable payload.
Automatic URL Resolution: Resolve target URLs to IP addresses for HTTP attacks.
Error Handling: Comprehensive error handling for both socket errors and HTTP request exceptions.
Logging: Detailed logging of attack progress and errors.
Ethical Use: Designed for ethical testing and educational purposes.
Usage
Prerequisites
Python 3.x
Required Python libraries: requests
Installation
Clone the repository:

bash
Copier le code
git clone https://github.com/hydr0cher/ddos-script.git
cd ddos-script
Install dependencies:

Copier le code
pip install -r requirements.txt
Command Line Arguments
bash
Copier le code
usage: ddos.py [-h] [-t THREADS] [-s SIZE] [-d DURATION] [-p {tcp,udp,http}] [-r REQUEST_PATH] [-m {GET,POST}] target target_port

Advanced DDoS script for ethical testing purposes.

positional arguments:
  target                Target IP address or URL
  target_port           Target port

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        Number of attacking threads (default: 10)
  -s SIZE, --size SIZE  Size of packet payload (default: 1024 bytes)
  -d DURATION, --duration DURATION
                        Duration of the attack in seconds (default: None, indefinite)
  -p {tcp,udp,http}, --protocol {tcp,udp,http}
                        Protocol to use for the attack (default: udp)
  -r REQUEST_PATH, --request-path REQUEST_PATH
                        HTTP request path (default: /)
  -m {GET,POST}, --method {GET,POST}
                        HTTP method (default: GET)
Examples
UDP Attack
bash
Copier le code
python ddos.py 192.168.1.100 80 -t 20 -s 2048 -d 60 -p udp
TCP Attack
bash
Copier le code
python ddos.py 192.168.1.100 443 -t 15 -s 1024 -d 30 -p tcp
HTTP Attack
bash
Copier le code
python ddos.py http://example.com 80 -t 10 -s 512 -d 60 -p http -r /index.html -m GET
Disclaimer
This script is intended for educational and ethical testing purposes only. The author is not responsible for any misuse or damage caused by this script.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
Hydr0cher - GitHub
