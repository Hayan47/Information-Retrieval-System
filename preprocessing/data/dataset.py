import os
import pandas as pd
from django.conf import settings
from admin_tools.models import Document

def load_dataset(dataset_name):
    dataset_path = os.path.join(settings.BASE_DIR, 'IR', 'static', 'datasets', f'{dataset_name}.tsv')
    df = pd.read_csv(dataset_path, sep='\t', header=None, names=['doc_id', 'text'])
    df['text'] = df['text'].fillna('')
    # df = df.head()
    # store_dataset(df)
    return df

def store_dataset(df):
    for _, row in df.iterrows():
        doc_id = row['doc_id']
        text = row['text']
        Document.objects.create(doc_id=doc_id ,text=text)

