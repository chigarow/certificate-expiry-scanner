import os
import datetime
import argparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from zoneinfo import ZoneInfo

def check_certificate_expiry(cert_path):
    """
    Checks the expiration date of a single certificate file.

    Args:
        cert_path (str): The full path to the certificate file.

    Returns:
        A tuple containing the certificate status (str) and expiration date (datetime).
        Returns (None, None) if the file is not a valid certificate.
    """
    try:
        with open(cert_path, 'rb') as f:
            cert_data = f.read()
            
        # The cryptography library can handle both PEM and DER formats.
        # It will raise a ValueError if the format is not recognized.
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        
        expiration_date = cert.not_valid_after_utc
        now = datetime.datetime.now(datetime.timezone.utc)
        time_until_expiry = expiration_date - now

        if time_until_expiry.days < 0:
            return "EXPIRED", expiration_date
        elif time_until_expiry.days <= 365:
            return "EXPIRES SOON", expiration_date
        else:
            return "VALID", expiration_date
            
    except ValueError:
        # This error is often raised for files that are not valid certificates
        # or are password-protected without providing a password.
        # We can safely ignore these files.
        return None, None
    except Exception as e:
        print(f"Error processing {os.path.basename(cert_path)}: {e}")
        return None, None

def check_certs_in_directory(directory):
    """
    Scans a directory (and subdirectories) for .crt and .pem files 
    and checks their expiration.

    Args:
        directory (str): The path to the directory to scan.
    """
    print(f"Scanning directory: {directory}\n")
    found_expired = False
    jakarta_tz = ZoneInfo("Asia/Jakarta")  # Define Jakarta timezone
    
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith((".crt", ".pem")):
                cert_path = os.path.join(root, filename)
                status, expiry_date = check_certificate_expiry(cert_path)
                
                if status == "EXPIRED":
                    found_expired = True
                    relative_path = os.path.relpath(cert_path, directory)
                    print(f"File: {relative_path}")
                    print(f"  - Status: {status}")
                    if expiry_date:
                        expiry_jakarta = expiry_date.astimezone(jakarta_tz)
                        print(f"  - Expired on: {expiry_jakarta.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                    print("-" * 30)

    if not found_expired:
        print("No expired .crt or .pem certificate files found in the specified directory.")

if __name__ == "__main__":
    # Using argparse to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Scan a directory for expired or soon-to-expire certificates."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.getcwd(),
        help="Path to the directory to be scanned. If not provided, the current directory will be used."
    )
    args = parser.parse_args()

    target_directory = args.directory

    if os.path.isdir(target_directory):
        check_certs_in_directory(target_directory)
    else:
        print(f"Error: The provided path '{target_directory}' is not a valid directory.")

