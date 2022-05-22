from boto3.session import Session
import boto3

ACCESS_KEY = input("Enter the ACCESS KEY :")
SECRET_KEY = input("Enter the SECRET KEY :")
PATH="C:\Users\mvhit\Downloads\Video" # Local path for the file
session = Session(aws_access_key_id=ACCESS_KEY,
              aws_secret_access_key=SECRET_KEY)
s3 = session.resource('s3')
your_bucket = s3.Bucket('bucket_name')

'''
for s3_file in your_bucket.objects.all():
    print(s3_file.key) # prints the contents of bucket
'''

s3 = boto3.client ('s3')
s3.download_file('your_bucket','Name of the file in s3 bucket',PATH+'Name to save the local file')