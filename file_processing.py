import boto3
import json
import os
import re
import pandas as pd
import pandas_gbq
import zoneinfo
from google.oauth2 import service_account
from datetime import datetime

class FileProcess:

    def __init__(self,out_bucket:str,in_bucket:str) -> None:
        self.s3 = boto3.client('s3')
        self.lambda_dir = '/tmp'
        self.time_zone = zoneinfo.ZoneInfo("America/Los_Angeles")
        self.current_date = datetime.now(
                            tz=self.time_zone
                            ).date().strftime('%Y-%m-%d')
        self.in_bucket = in_bucket
        self.in_file_name = f'{self.current_date}_TechMeme_NLP.json'
        self.out_bucket = out_bucket
        self.out_recent_file_name = self.S3_recent_file()
    
    def S3_recent_file(self):
        response = self.s3.list_objects_v2(Bucket=self.out_bucket)
        sorted_objects = sorted(response['Contents'],
                                key=lambda obj: obj['LastModified'],
                                reverse=True)
        most_recent_file = sorted_objects[0]
        file_name = most_recent_file['Key']
        return file_name

    def s3_auth(self):
        file_name = 'yt-comments-dashboard-41b385655862.json'
        file_path = f'{self.lambda_dir}/{file_name}'
        self.s3.download_file('auth-ccdatapdx',file_name,file_path)
        return

    def open_S3_recent(self):
        file_path = f'{self.lambda_dir}/{self.out_recent_file_name}'
        self.s3.download_file(self.out_bucket,
                              self.out_recent_file_name,
                              file_path
                              )
        with open(file_path,'r') as f:
            s3_file = json.load(f)
        s3_file = pd.read_json(file_path)
        return s3_file

    def write_s3(self):
        self.s3.upload_file(f'{self.lambda_dir}/{self.in_file_name}',
                            self.in_bucket,f'{self.in_file_name}')
    
    def write_gbq(self,df:pd.DataFrame,destination_table:str):
        self.s3_auth()
        service_account_file = 'yt-comments-dashboard-41b385655862.json'
        credentials = service_account.Credentials.from_service_account_file(
            f'{self.lambda_dir}/{service_account_file}',
        )
        to_gbq = pandas_gbq.to_gbq(df,
                                   destination_table=f'yt_comments_nlp.{destination_table}',
                                   project_id='yt-comments-dashboard',
                                   if_exists='append',
                                   credentials=credentials
        )
        return to_gbq
