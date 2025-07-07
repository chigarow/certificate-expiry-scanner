# CheckCertificate

CheckCertificate is a Python script that scans a directory for SSL certificate files (.crt and .pem) and checks their expiration status. It provides a simple way to monitor certificate validity and ensure that your certificates are up to date.

## Features

- Scans a specified directory (and its subdirectories) for certificate files.
- Checks the expiration date of each certificate.
- Reports expired certificates and those that will expire soon.

## Installation

To use CheckCertificate, you need to have Python installed on your system. You can install the required dependencies using pip or pip3.

### Using pip

1. Open your terminal or command prompt.
2. Navigate to the project directory where `check-certificate.py` is located.
3. Install the required packages by running:

```
pip install cryptography
```

### Using pip3

1. Open your terminal or command prompt.
2. Navigate to the project directory where `check-certificate.py` is located.
3. Install the required packages by running:

```
pip3 install cryptography
```

## Usage

You can run the script using Python or Python3 from the command line. 

### Using Python

To check certificates in the current directory, run:

```
python check-certificate.py
```

To specify a different directory, run:

```
python check-certificate.py /path/to/directory
```

### Using Python3

To check certificates in the current directory, run:

```
python3 check-certificate.py
```

To specify a different directory, run:

```
python3 check-certificate.py /path/to/directory
```

## Output

The script will output the status of each certificate found in the specified directory:

- **EXPIRED**: The certificate has expired.
- **EXPIRES SOON**: The certificate will expire within the next 365 days.
- **VALID**: The certificate is valid and will not expire soon.

If no expired certificates are found, the script will inform you accordingly.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

This project uses the `cryptography` library for handling certificate files.