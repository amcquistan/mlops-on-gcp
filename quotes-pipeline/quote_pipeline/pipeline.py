
import argparse
import typing

import apache_beam as beam
from apache_beam.io.gcp.internal.clients import bigquery
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions, SetupOptions
from apache_beam.runners import DataflowRunner

import google.auth
from google.cloud import language_v1, language

import time

import json


def analyze_quote(element):
    row = json.loads(element.decode('utf-8'))
    
    client = language_v1.LanguageServiceClient()
    
    doc = language.types.Document(
      content=row['text'],
      language='en',
      type='PLAIN_TEXT'
    )
    response = client.analyze_sentiment(document=doc)

    row.update(
      sentiment=response.document_sentiment.score,
      magnitude=response.document_sentiment.magnitude
    )
    
    return row


def main(args):
    options = PipelineOptions(save_main_session=True, streaming=True)
    options.view_as(StandardOptions).runner = args.runner
    options.view_as(GoogleCloudOptions).project = args.project
    options.view_as(GoogleCloudOptions).region = args.region
    options.view_as(GoogleCloudOptions).staging_location = args.staging_location
    options.view_as(GoogleCloudOptions).temp_location = args.temp_location
    options.view_as(GoogleCloudOptions).job_name = '{}{}'.format('quotes-pipeline-', time.time_ns())
    
    
    table_spec = bigquery.TableReference(projectId=args.project,
                                         datasetId=args.bq_dataset,
                                         tableId=args.bq_table)
    QUOTES_TABLE_SCHEMA = {
        "fields": [
            {
                "name": "text",
                "type": "STRING"
            },
            {
                "name": "author",
                "type": "STRING"
            },
            {
                "name": "tags",
                "type": "STRING",
                "mode": "REPEATED"
            },
            {
                "name": "sentiment",
                "type": "FLOAT"
            },
            {
                "name": "sentiment",
                "type": "FLOAT"
            }
        ]
    }
    
    with beam.Pipeline(options=options) as p:
        (p  | "ReadPubSub" >> beam.io.ReadFromPubSub(args.pubsub_topic)
            | "AnalyzeQuote" >> beam.Map(analyze_quote)
            | "SaveToBigQuery" >> beam.io.WriteToBigQuery(
                                          table_spec,
                                          schema=QUOTES_TABLE_SCHEMA,
                                          create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                                          write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', default='DataflowRunner')
    parser.add_argument('--project', required=True)
    parser.add_argument('--region', required=True)
    parser.add_argument('--bq_dataset', required=True)
    parser.add_argument('--bq_table', required=True)
    parser.add_argument('--staging_location', required=True)
    parser.add_argument('--temp_location', required=True)
    parser.add_argument('--pubsub_topic', required=True)
    parser.add_argument('--requirements_file')
    
    args = parser.parse_args()
    
    main(args)
