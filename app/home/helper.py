from instance.config import S3_KEY, S3_SECRET, S3_BUCKET
import boto3

# S3 initialization
s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

def upload_file_to_s3(file, file_name):

    file_path = "ais/" + file_name + "." + file.filename.split('.')[-1]

    try:

        s3.upload_fileobj(
            file,
            S3_BUCKET,
            file_path,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return file.filename