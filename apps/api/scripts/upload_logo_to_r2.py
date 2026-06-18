#!/usr/bin/env python3
"""
Extract base64 PNG logo from outreach email template and upload to Cloudflare R2.
"""

import base64
import os
import re
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def extract_base64_logo(template_path: str) -> bytes:
    """Extract base64 PNG data from the email template."""
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Match src="data:image/png;base64,{DATA}"
    pattern = r'src="data:image/png;base64,([^"]+)"'
    match = re.search(pattern, html_content)

    if not match:
        raise ValueError("No base64 PNG data found in template")

    base64_data = match.group(1)
    return base64.b64decode(base64_data)


def upload_to_r2(image_data: bytes) -> str:
    """Upload image data to Cloudflare R2 and return the public URL."""
    endpoint_url = os.environ.get("R2_ENDPOINT_URL")
    access_key_id = os.environ.get("R2_ACCESS_KEY_ID")
    secret_access_key = os.environ.get("R2_SECRET_ACCESS_KEY")
    bucket_name = os.environ.get("R2_BUCKET_NAME")
    public_base_url = os.environ.get("R2_PUBLIC_BASE_URL", "https://images.nevumo.com")

    if not all([endpoint_url, access_key_id, secret_access_key, bucket_name]):
        raise ValueError("Missing required R2 environment variables")

    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key="nevumo-logo.png",
            Body=image_data,
            ContentType="image/png",
            CacheControl="public, max-age=31536000",
        )
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to upload to R2: {e}") from e

    return f"{public_base_url}/nevumo-logo.png"


def main() -> None:
    template_path = "apps/api/scripts/templates/outreach_email_pl.html"

    try:
        image_data = extract_base64_logo(template_path)
        public_url = upload_to_r2(image_data)
        print(f"✅ Logo uploaded: {public_url}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
