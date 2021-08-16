
from google.cloud import language_v1

def main():
    client = language_v1.LanguageServiceClient()

    doc = {
      'content': 'I hate that this is such a stupic message',
      'type_': language_v1.Document.Type.PLAIN_TEXT,
      'language': 'en' 
    }

    response = client.analyze_sentiment(request={'document': doc, 'encoding_type': language_v1.EncodingType.UTF8})

    print("Document sentiment score: {}".format(response.document_sentiment.score))
    print("Document sentiment magnitude: {}".format(response.document_sentiment.magnitude))


if __name__ == '__main__':
    main()

