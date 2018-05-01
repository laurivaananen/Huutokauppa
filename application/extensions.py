from application import application

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance

import boto3

s3 = boto3.client(
   "s3",
   aws_access_key_id=application.config["S3_KEY"],
   aws_secret_access_key=application.config["S3_SECRET"]
)

def put_object_to_s3(image_bytes, filename, content_type='image/png'):
    print("\n\nTRYING TO PUT IMAGE TO S3")

    s3.put_object(
        Bucket=application.config["S3_BUCKET"],
        Key=filename,
        Body=image_bytes,
        ContentType=content_type
    )

def generate_presigned_url(filename):
    print("\n\nGENERATING URL")
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': application.config["S3_BUCKET"], 'Key': filename}
    )
    return url


def upload_file_to_s3(file, bucket_name, filename, acl="public-read"):

    print("\n\nHERE WE GO")

    print(s3.list_buckets())
    print(s3.list_objects(Bucket=application.config["S3_BUCKET"]))
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return "{}{}".format(application.config["S3_LOCATION"], filename)

