import pytrec_eval
import os
import pandas as pd
from django.conf import settings

class Evaluation:
    def __init__(self):
        None

    def evaluate(self, system_results, dataset_name):
        
        qrels_path = os.path.join(settings.BASE_DIR, 'IR', 'static', 'datasets', f'{dataset_name}_qrels.csv')
        qrels_df = pd.read_csv(qrels_path, names=['query_id', 'doc_id', 'relevance_score'])

        qrels = {}

        for _, row in qrels_df.iterrows():
            query_id = str(row['query_id'])
            doc_id = str(row['doc_id'])
            relevance_score = int(row['relevance_score'])

            # If the query_id is not already in the dictionary, add it with an empty dict
            if query_id not in qrels:
                qrels[query_id] = {}

            # Add the doc_id and relevance_score to the dictionary
            qrels[query_id][doc_id] = relevance_score

        evaluator = pytrec_eval.RelevanceEvaluator(qrels, {'map', 'recall', 'P_10', 'recip_rank'})
        eval_metrics = evaluator.evaluate(system_results)
        overall_metrics = self.calculate_overall_metrics(eval_metrics)
        return overall_metrics

    def calculate_overall_metrics(self, eval_metrics):
        overall_metrics = {}
        query_metrics = []

        for query_id, query_result in eval_metrics.items():
            query_metrics.append(query_result)
            print(query_result)

        # Calculate Mean Average Precision (MAP)
        map_scores = [metrics.get('map', 0) for metrics in query_metrics]
        overall_metrics['map'] = sum(map_scores) / len(map_scores)

        # Calculate Reciprocal Rank (MRR)
        rr_scores = [metrics.get('recip_rank', 0) for metrics in query_metrics]
        overall_metrics['recip_rank'] = sum(rr_scores) / len(rr_scores)

        # Calculate Precision@10
        p10_scores = [metrics.get('P_10', 0) for metrics in query_metrics]
        overall_metrics['P_10'] = sum(p10_scores) / len(p10_scores)

        # Calculate Recall at different cut-offs
        for cutoff in [5, 10, 15, 20, 30, 100, 200, 500, 1000]:
            recall_key = f'recall_{cutoff}'
            recall_scores = [metrics.get(recall_key, 0) for metrics in query_metrics]
            overall_metrics[recall_key] = sum(recall_scores) / len(recall_scores)

        return overall_metrics
