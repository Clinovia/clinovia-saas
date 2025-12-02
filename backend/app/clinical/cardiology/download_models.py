import boto3
import os

# ----------------------------
# Configuration
# ----------------------------
S3_BUCKET = "clinovia.ai"
S3_KEY = "ef3dcnn_epoch17.pth"  # exact file in S3
LOCAL_DIR = os.path.join(os.path.dirname(__file__), "models")
LOCAL_PATH = os.path.join(LOCAL_DIR, os.path.basename(S3_KEY))

# Make sure local directory exists
os.makedirs(LOCAL_DIR, exist_ok=True)

# ----------------------------
# S3 Client
# ----------------------------
s3 = boto3.client("s3")

def download_s3_file(bucket: str, key: str, local_path: str):
    """
    Download a single file from S3 to a local path.
    """
    print(f"Downloading s3://{bucket}/{key} -> {local_path}")
    s3.download_file(bucket, key, local_path)
    print("Download completed!")

# ----------------------------
# Run download
# ----------------------------
if __name__ == "__main__":
    download_s3_file(S3_BUCKET, S3_KEY, LOCAL_PATH)
