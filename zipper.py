import pyzipper

input_file = "/Users/vladstoyanov/scr/zipcracker/README.md"
output_zip = "/Users/vladstoyanov/scr/zipcracker/README_protected.zip"
password = b"99999999"  # Use bytes, not string

len(password)

with pyzipper.AESZipFile(output_zip,
                         'w',
                         compression=pyzipper.ZIP_DEFLATED,
                         encryption=pyzipper.WZ_AES) as zf:
    zf.setpassword(password)
    zf.write(input_file, arcname="README.md")

print(f"✅ Zipped and password-protected: {output_zip}")
