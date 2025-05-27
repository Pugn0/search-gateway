# Search Gateway

A Python tool for analyzing websites to detect payment gateways and security protections.

## Features

- 🔍 Detects multiple payment gateways (PayPal, Stripe, Adyen, and many more)
- 🛡️ Identifies security protections like Cloudflare and reCAPTCHA
- 📊 Provides detailed analysis of website security measures
- 📝 Supports both single URL analysis and batch processing from a file

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pugn0/search-gateway.git
cd search-gateway
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The tool can be used in two ways:

1. **Single URL Analysis**
   - Run the script and choose option 1
   - Enter the URL you want to analyze

2. **Batch Analysis**
   - Create a `sites.txt` file with one URL per line
   - Run the script and choose option 2
   - The tool will analyze all URLs in the file

## Configuration

- `gates.json`: Contains the list of payment gateways to detect
- `sites.txt`: List of URLs to analyze in batch mode

## Output

The tool provides detailed information about:
- HTTP Status Code
- Security Protections (Cloudflare, reCAPTCHA)
- Detected Payment Gateways
- reCAPTCHA details (version, key, host) when present

## Requirements

- Python 3.6+
- Required packages listed in `requirements.txt`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.