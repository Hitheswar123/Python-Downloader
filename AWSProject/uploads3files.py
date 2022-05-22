import boto3
import os

ACCESS_KEY= input("Enter the Access key ID :")
SECRET_KEY= input("Enter the Secret Access Key :")

client= boto3.client('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

for file in os.listdir():
    if '.py' in file:
        upload_file_bucket='s3-bucket-files'
        upload_file_key='python/'+ str(file)
        client.upload_file(file,upload_file_bucket,upload_file_key)