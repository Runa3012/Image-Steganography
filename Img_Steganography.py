from PIL import Image

# Converting types to binary
def msg_to_bin(msg):
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == bytearray:
        return [format(i, "08b") for i in msg]
    elif type(msg) == int:
        return format(msg, "08b")
    else:
        raise TypeError("Input type not supported")

# Defining function to hide the secret message into the image
def hide_data(image, secret_msg):
    # Converting the input image to RGB mode
    image = image.convert("RGB")

    # Calculating the maximum bytes for encoding
    n_bytes = image.width * image.height * 3 // 8
    print("Maximum Bytes for encoding:", n_bytes)

    # Checking whether the number of bytes for encoding is sufficient
    if len(secret_msg) > n_bytes:
        raise ValueError("Error encountered: insufficient bytes, need a bigger image or less data!")

    secret_msg += '#####'  # We can utilize any string as the delimiter
    data_index = 0

    # Converting the input data to binary format using the msg_to_bin() function
    bin_secret_msg = msg_to_bin(secret_msg)

    # Finding the length of data that requires to be hidden
    data_len = len(bin_secret_msg)

    # Creating a new image to store the encoded data
    encoded_image = Image.new("RGB", (image.width, image.height))

    for i in range(image.width):
        for j in range(image.height):
            # Getting the RGB values of the current pixel
            r, g, b = image.getpixel((i, j))

            # Modifying the least significant bit (LSB) of each color channel
            if data_index < data_len:
                # Hiding the data into LSB of Red pixel
                r = r & 0xFE | int(bin_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # Hiding the data into LSB of Green pixel
                g = g & 0xFE | int(bin_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # Hiding the data into LSB of Blue pixel
                b = b & 0xFE | int(bin_secret_msg[data_index], 2)
                data_index += 1

            # Setting the modified pixel values in the new image
            encoded_image.putpixel((i, j), (r, g, b))

            # If data is encoded, break out of the loop
            if data_index >= data_len:
                break

    return encoded_image

# Defining function to decode the data from the image
def decode_data(image):
    # Converting the input image to RGB mode
    image = image.convert("RGB")

    bin_data = ""
    width, height = image.size

    for i in range(width):
        for j in range(height):
            # Getting the RGB values of the current pixel
            r, g, b = image.getpixel((i, j))

            # Extracting the least significant bit (LSB) of each color channel
            bin_data += bin(r)[-1]
            bin_data += bin(g)[-1]
            bin_data += bin(b)[-1]

    # Splitting by 8-Bits
    all_bytes = [bin_data[i:i + 8] for i in range(0, len(bin_data), 8)]

    # Converting from bits to characters
    decoded_msg = ""
    for byte in all_bytes:
        decoded_msg += chr(int(byte, 2))
        # Checking if we have reached the delimiter which is "#####"
        if decoded_msg[-5:] == "#####":
            break

    return decoded_msg

# Load the image
image = Image.open("bullet.png")

# Hide the secret message
secret_msg = "This is a secret message!"
encoded_image = hide_data(image, secret_msg)

# Save the encoded image
encoded_image.save("encoded_image.png")

# Load the encoded image
encoded_image = Image.open("encoded_image.png")

# Decode the hidden message
decoded_msg = decode_data(encoded_image)
print("Decoded message:", decoded_msg)
