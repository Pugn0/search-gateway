# Search Gateway

A Python tool for analyzing websites to detect payment gateways and security protections.

## Features

- 🔍 Detects multiple payment gateways (PayPal, Stripe, Adyen, and many more)
- 🛡️ Identifies security protections like Cloudflare and reCAPTCHA
- 📊 Provides detailed analysis of website security measures
- 📝 Supports both single URL analysis and batch processing from a file
- 🔄 URL Filter addon for mitmproxy to automatically collect URLs

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

3. Install mitmproxy certificate:
   - Run mitmproxy once to generate the certificate:
   ```bash
   mitmproxy
   ```
   - The certificate will be generated in:
     - Windows: `%USERPROFILE%\.mitmproxy\mitmproxy-ca-cert.cer`
     - Linux/Mac: `~/.mitmproxy/mitmproxy-ca-cert.cer`
   - Install the certificate in your system:
     - Windows: Double-click the certificate file and follow the installation wizard
     - Linux: Copy to system certificates directory
     - Mac: Double-click and add to System keychain

## Usage

### Main Tool

The tool can be used in two ways:

1. **Single URL Analysis**
   - Run the script and choose option 1
   - Enter the URL you want to analyze

2. **Batch Analysis**
   - Create a `sites.txt` file with one URL per line
   - Run the script and choose option 2
   - The tool will analyze all URLs in the file

### URL Filter Addon

The URL Filter addon automatically collects URLs while browsing:

1. Start mitmproxy with the URL filter addon:
```bash
mitmproxy -s url_filter.py
```

2. Configure your browser/system to use the proxy:
   - Proxy address: 127.0.0.1
   - Port: 8080

3. Browse websites normally - the addon will automatically:
   - Collect URLs from visited pages
   - Save them to `sites.txt`
   - Skip common domains (Google, Facebook, etc.)

## Configuration

- `gates.json`: Contains the list of payment gateways to detect
- `sites.txt`: List of URLs to analyze in batch mode
- `url_filter.py`: Configuration for URL collection (modify `ignored_domains` to customize)

## Output

The tool provides detailed information about:
- HTTP Status Code
- Security Protections (Cloudflare, reCAPTCHA)
- Detected Payment Gateways
- reCAPTCHA details (version, key, host) when present

## Requirements

- Python 3.6+
- Required packages listed in `requirements.txt`
- System configured to trust mitmproxy certificate

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.