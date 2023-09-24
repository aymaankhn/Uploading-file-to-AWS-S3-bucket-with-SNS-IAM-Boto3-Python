import pandas as pd 
import boto3
from io import StringIO

data = [["AA",1],["BB",2],['CC',3]]
df = pd.DataFrame(data, columns=['Name','Roll.No'])

Access_key1= "AKIA5I7FIHYRODVTIF7N"
Secret_key1 = "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"

def upload_to_s3(df):
    f = "file.csv"
    s3 = boto3.client('s3',aws_access_key_id = Access_key1, aws_secret_access_key = Secret_key1) # Creating S3 Client
    
    csv_buf = StringIO() # Convert dataframe to csv file                                          
    df.to_csv(csv_buf, header=True, index=False)
    csv_buf.seek(0)

    # Uploading file to s3
    s3.put_object(Bucket = 'aymaan-bucket', Body = csv_buf.getvalue(), Key = 'MyFolder/' + f)

# Creating SNS 
ses = boto3.client('sns', aws_access_key_id = Access_key1, aws_secret_access_key = Secret_key1, region_name='ap-south-1')
sns_topicname_arn = "arn:aws:sns:ap-south-1:912624467490:upload_notification"

def Message(snsArn, msg):
    client = boto3.client('sns', aws_access_key_id = Access_key1, aws_secret_access_key =Secret_key1,region_name='ap-south-1')
    client.publish(TargetArn=snsArn, Message=msg)


upload_to_s3(df)

msg = "Hey! File has been uploaded into your bucket\n Regards Aymaan"

Message(sns_topicname_arn, msg)