import boto3
import streamlit as st

session = boto3.session.Session()
s3 = session.client(
    aws_access_key_id = st.secrets["KEY_ID_FOR_BOTO"],
    aws_secret_access_key = st.secrets["SECRET_KEY_FOR_BOTO"],
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

def uploadToBucketAndGetPath(bucket_name,object_name):
    s3.upload_file(object_name, bucket_name, object_name)
    presigned_url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": bucket_name, "Key": object_name},
    ExpiresIn=100)
    return presigned_url