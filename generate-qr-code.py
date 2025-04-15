import qrcode
import io
from PIL import Image

def generate_qr_code(link, output_filename="qrcode"):
    """
    Generates a QR code from a given link and saves it as an image and a binary data file.

    Args:
        link (str): The link to encode in the QR code.
        output_filename (str): The base filename for the output image and data file.
    """
    try:
        qr = qrcode.QRCode(
            version=None,  # Auto-determine the best version
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image
        image_filename = f"{output_filename}.png"
        img.save(image_filename)
        print(f"QR code image saved as: {image_filename}")

        # Save the QR code data as a binary string with other data.
        data = qr.get_matrix()
        binary_data = ""
        for row in data:
            for cell in row:
                binary_data += "1" if cell else "0"

        #Include the link and version information in the data file.
        additional_info = f"Link: {link}\nVersion: {qr.version}\n"
        data_file_content = additional_info.encode('utf-8') + binary_data.encode('utf-8')

        data_filename = f"{output_filename}.bin"
        with open(data_filename, "wb") as f:
            f.write(data_file_content)

        print(f"QR code data saved as: {data_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    link = input("Enter the link to generate a QR code for: ")
    generate_qr_code(link)