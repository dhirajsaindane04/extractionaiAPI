import io
from PIL import Image
from pdf2image import convert_from_bytes

def input_image_setup(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.read()

        if uploaded_file.mimetype == "application/pdf":
            images = convert_from_bytes(bytes_data)
            image_parts = []
            for image in images:
                with io.BytesIO() as output:
                    image.save(output, format="PNG")
                    image_parts.append({
                        "mime_type": "image/png",
                        "data": output.getvalue()
                    })
            return image_parts
        else:
            return [
                {
                    "mime_type": uploaded_file.mimetype,
                    "data": bytes_data
                }
            ]
    else:
        raise FileNotFoundError("No file uploaded")
