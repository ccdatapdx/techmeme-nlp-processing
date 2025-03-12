from techmeme_process_nlp import SpacyProcessing
from file_processing import FileProcess

def lambda_handler(event,context):
     file_process = FileProcess('techmeme-headlines','techmeme-headlines-nlp-processing')
     original_df = file_process.open_S3_recent()
     nlp_process = SpacyProcessing()
     df_row = nlp_process.df_by_row(original_df)
     nlp_df = nlp_process.process_headlines_nlp(df_row)
     event = nlp_df.to_json(f'{file_process.lambda_dir}/{file_process.in_file_name}')
     event = file_process.write_s3()
     event = file_process.write_gbq(nlp_df,'techmeme_ner')

     return event