import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
from PIL import Image
import io
import uuid
import magic
import os

# Configuration S3 - Check for actual values, not placeholders
s3_client = None
def is_s3_configured():
    placeholders = ["", "votre_cle_secrete", "YOUR_ACCESS_KEY"]
    return (settings.S3_ACCESS_KEY and settings.S3_ACCESS_KEY not in placeholders and 
            settings.S3_SECRET_KEY and settings.S3_SECRET_KEY not in placeholders)

if is_s3_configured():
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION
    )

# Local Storage Configuration
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def optimize_image(content: bytes, max_width=1200, quality=80) -> bytes:
    """Optimise l'image pour le web/mobile: redimensionnement et compression."""
    img = Image.open(io.BytesIO(content))
    
    # Conversion en RGB pour JPEG
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Redimensionnement proportionnel si trop large
    if img.width > max_width:
        ratio = max_width / float(img.width)
        new_height = int(float(img.height) * float(ratio))
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    return output.getvalue()

async def upload_file_to_s3(file_content: bytes, folder: str, filename: str, content_type: str = None) -> str:
    """Upload un fichier sur S3 ou en local et retourne le chemin relatif."""
    if not content_type:
        content_type = magic.from_buffer(file_content, mime=True)

    # Optimisation si c'est une image
    if content_type.startswith("image/"):
        file_content = optimize_image(file_content)
        content_type = "image/jpeg"

    s3_key = f"{folder}/{uuid.uuid4().hex}-{filename}"
    
    # Fallback to local storage if S3 is not configured
    if not s3_client:
        local_path = os.path.join(UPLOAD_DIR, s3_key)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(file_content)
        return f"local://{s3_key}"

    try:
        s3_client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=s3_key,
            Body=file_content,
            ContentType=content_type
        )
        return s3_key
    except ClientError as e:
        print(f"S3 Upload Error: {e}")
        # Fallback even on error if misconfigured
        local_path = os.path.join(UPLOAD_DIR, s3_key)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(file_content)
        return f"local://{s3_key}"

def generate_signed_url(s3_key: str, expiration=3600) -> str:
    """Génère une URL pour accéder au fichier (signée pour S3, directe pour local)."""
    if not s3_key:
        return None
        
    if s3_key.startswith("local://"):
        relative_path = s3_key.replace("local://", "")
        # Assuming the API is on port 8000 and has a /uploads static mount
        return f"http://localhost:8000/uploads/{relative_path}"

    if not s3_client:
        # If it was stored locally without the local:// prefix (old logic)
        return f"http://localhost:8000/uploads/{s3_key}"

    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.S3_BUCKET, 'Key': s3_key},
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        print(f"S3 Signed URL Error: {e}")
        return f"http://localhost:8000/uploads/{s3_key}"
