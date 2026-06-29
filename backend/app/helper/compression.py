from io import BytesIO
from PIL import Image
from fastapi import HTTPException

MAX_FILE_SIZE = 4 * 1024 * 1024  # 4 MB


def prepare_file_for_ocr(
    file_bytes: bytes,
    content_type: str
) -> bytes:
    """
    Ensures file is compatible with Azure Document Intelligence free tier.

    - Images are compressed if needed.
    - PDFs are accepted only if under 4 MB. for now
    - Other file types are accepted only if under 4 MB.
    """

    if len(file_bytes) <= MAX_FILE_SIZE:
        return file_bytes

    image_types = {
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp",
    }

    if content_type in image_types:
        return compress_image(file_bytes)

    raise HTTPException(
        status_code=400,
        detail="File exceeds Azure Document Intelligence free-tier limit (4 MB)."
    )


def compress_image(file_bytes: bytes) -> bytes:
    img = Image.open(BytesIO(file_bytes))

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize large images
    max_width = 2000

    if img.width > max_width:
        ratio = max_width / img.width

        img = img.resize(
            (
                int(img.width * ratio),
                int(img.height * ratio)
            ),
            Image.LANCZOS
        )

    quality = 85

    while quality >= 20:
        output = BytesIO()

        img.save(
            output,
            format="JPEG",
            optimize=True,
            quality=quality
        )

        compressed = output.getvalue()

        if len(compressed) <= MAX_FILE_SIZE:
            return compressed

        quality -= 10

    raise HTTPException(
        status_code=400,
        detail="Unable to compress image below 4 MB."
    )