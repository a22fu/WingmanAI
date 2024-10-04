import boto3
import time
import pandas as pd
from awsconfig import S3_BUCKET_NAME, S3_OUTPUT_DIRECTORY, S3_CLIENT, ATHENA_CLIENT

def vlrgg_query(DATABASE = "vlrggdatabase", TABLE = "vct_data", QUERY_STRING = 'SELECT * FROM "vlrggdatabase"."vct_data"'):
    temp_file_location = "temp_results.csv"
    query_response = ATHENA_CLIENT.start_query_execution(
        QueryString = QUERY_STRING,
        QueryExecutionContext={"Database": "{DATABASE}"},
        ResultConfiguration={
            "OutputLocation": "s3://vct-results-bucket/output",
            "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
        },
    )
    while True:
        try:
            ATHENA_CLIENT.get_query_results(
                QueryExecutionId=query_response["QueryExecutionId"]
            )
            break
        except Exception as err:
            if "not yet finished" in str(err):
                time.sleep(0.001)
            else:
                raise err
    S3_CLIENT.download_file(
        S3_BUCKET_NAME,
        f"{S3_OUTPUT_DIRECTORY}/{query_response['QueryExecutionId']}.csv",
        temp_file_location,
    )
    df = pd.read_csv(temp_file_location)
    df.to_json (r'player_stats.json', indent=1, orient = 'records')
vlrgg_query()