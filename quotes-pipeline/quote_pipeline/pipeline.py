
import argparse
import typing

import apache_beam as beam
from apache_beam.io.gcp.internal.clients import bigquery
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions, SetupOptions
from apache_beam.runners import DataflowRunner

import google.auth
from google.cloud import language

import time

import json


class Quote(typing.NamedTuple):
    text : str
    author : str
    tags : typing.Sequence[str]
    sentiment : float
    magnitude : float

beam.coders.registry.register_coder(Quote, beam.coders.RowCoder)


def analyze_quote(element):
    row = json.loads(element.decode('utf-8'))
    
    client = language.LanguageServiceClient()
    
    doc = language.Document(content=row['text'],
                            type_=language.Document.Type.PLAIN_TEXT)
    
    response = client.analyze_sentiment(document=doc)

    row.update(
      sentiment=response.document_sentiment.score,
      magnitude=response.document_sentiment.magnitude
    )
    
    return row


def main(args, beam_args):
    options = PipelineOptions(beam_args,
                              runner=args.runner,
                              streaming=True,
                              project=args.project,
                              region=args.region,
                              job_name='{}{}'.format('quotes-pipeline-', time.time_ns()),
                              staging_location=args.staginglocation,
                              temp_location=args.templocation,
                              save_main_session=True)
    
    table_spec = bigquery.TableReference(projectId=args.project,
                                         datasetId=args.bqdataset,
                                         tableId=args.bqtable)
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
        (p  | "ReadPubSub" >> beam.io.ReadFromPubSub(args.pubsubtopic)
            | "AnalyzeQuote" >> beam.Map(analyze_quote)
            | "SaveToBigQuery" >> beam.io.WriteToBigQuery(
                                          table_spec,
                                          schema=QUOTES_TABLE_SCHEMA,
                                          create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                                          write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', default='DataflowRunner')
    parser.add_argument('--project')
    parser.add_argument('--region')
    parser.add_argument('--bqdataset')
    parser.add_argument('--bqtable')
    parser.add_argument('--staginglocation')
    parser.add_argument('--templocation')
    parser.add_argument('--pubsubtopic')
    parser.add_argument('--requirements_file')
    
    args, beam_args = parser.parse_known_args()
    
    main(args, beam_args)
