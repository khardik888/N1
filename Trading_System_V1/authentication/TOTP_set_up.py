from pyzbar.pyzbar import decode
from PIL import Image
import pyotp

# Assuming 'your_qr_code.png' is in the same directory as this script
qr_image = Image.open('qr.png')

decoded_data = decode(qr_image)
# The secret is typically encoded in a URI format in the 0QR, so you'll need to parse it
uri = decoded_data[0].data.decode()
secret_key = uri.split('secret=')[1].split('&')[0]

# Now, you can use the secret key to generate a TOTP code
totp = pyotp.TOTP(secret_key)
first_totp = totp.now()  # This is the first TOTP code generated from the secret key

# You can print it out, or use it wherever you need to
print(f"The first TOTP code is: {first_totp}")

# The rest of your script would continue from here
