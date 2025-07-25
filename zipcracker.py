#    Zipfile password cracker using a brute-force dictionary attack

import argparse
import pyzipper
import itertools
import string
import os
import sys
from multiprocessing import Pool, cpu_count
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

# Fallback for interactive mode
if '__file__' in globals():
    script_dir = os.path.dirname(os.path.abspath(__file__))
else:
    script_dir = "/Users/vladstoyanov/scr/zipcracker" # os.getcwd()  # fallback: current working directory



def brute_force(length, charset=None):
    # Generate all possible combinations of passwords of given length from charset.
    if charset is None:
        charset = string.ascii_letters + string.digits
    return (''.join(candidate) for candidate in itertools.product(charset, repeat=length))



def _try_password(args):
    zipfilename, target_file, password = args
    try:
        with pyzipper.AESZipFile(zipfilename) as zip_file:
            zip_file.extract(target_file, pwd=password.encode('utf-8'))
        return password
    except Exception:
        return None

def crack_zip(zipfilename, password_length, charset=None):
    # Define root folder as the folder containing the script being executed
    root_folder = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(root_folder, 'attempted_passwords.log')
    found_file = os.path.join(root_folder, 'found_password.txt')
    if not os.path.isfile(zipfilename):
        print(f"File not found: {zipfilename}")
        return
    try:
        with pyzipper.AESZipFile(zipfilename) as zip_file:
            namelist = zip_file.namelist()
            if not namelist:
                print("No files in ZIP archive.")
                return
            target_file = namelist[0]
            charset_to_use = charset if charset is not None else (string.ascii_letters + string.digits)
            total = len(charset_to_use) ** password_length
            passwords = brute_force(password_length, charset_to_use)
            args_iter = ((zipfilename, target_file, password) for password in passwords)
            found = None
            attempted = 0
            last_logged = 0
            with Pool(processes=cpu_count()) as pool:
                if tqdm:
                    iterator = tqdm(pool.imap_unordered(_try_password, args_iter, chunksize=100), total=total, desc="Cracking", unit="pw")
                else:
                    iterator = pool.imap_unordered(_try_password, args_iter, chunksize=100)
                for result in iterator:
                    attempted += 1
                    # Log every 50,000 attempts
                    if attempted % 50000 == 0:
                        with open(log_file, 'a') as log:
                            log.write(f"Attempted {attempted} passwords\n")
                        last_logged = attempted
                    if result:
                        found = result
                        break
                pool.terminate()
            # Log at the end if not already logged
            if attempted != last_logged:
                with open(log_file, 'a') as log:
                    log.write(f"Attempted {attempted} passwords\n")
            with open(log_file, 'a') as log:
                log.write(f"Total attempted: {attempted}\n")
                if found:
                    log.write(f'Password found: {found}\n')
            if found:
                print("===================================")
                print(f'Password found: {found}')
                print("==================================")
                # Write found password to a file
                with open(found_file, 'w') as pwfile:
                    pwfile.write(f'{found}\n')
            else:
                print("Password not found.")
    except pyzipper.BadZipFile:
        print("Bad ZIP file.")
    except Exception as e:
        print(f"Error: {e}")
def main():
    parser = argparse.ArgumentParser(description="Zipfile password cracker using brute-force attack.")
    parser.add_argument('zipfilename', help='Path to the ZIP file')
    parser.add_argument('password_length', type=int, help='Length of the password to brute-force')
    parser.add_argument('--charset', default=string.ascii_letters + string.digits, help='Characters to use (default: all letters and digits)')
    args = parser.parse_args()
    crack_zip(args.zipfilename, args.password_length, args.charset)


if __name__ == '__main__':
    main()
