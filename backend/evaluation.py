# backend/evaluation.py
import pandas as pd
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import streamlit as st

from ragas import evaluate, EvaluationDataset
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import (
    context_precision, 
    context_recall, 
    faithfulness,
    answer_relevancy
)

from config import llm, embedding

@dataclass
class ChatEvaluation:
    """チャット評価データクラス"""
    timestamp: datetime
    question: str
    answer: str
    contexts: List[str]
    source_files: List[str]
    context_precision: Optional[float] = None
    context_recall: Optional[float] = None
    faithfulness: Optional[float] = None
    answer_relevancy: Optional[float] = None
    overall_score: Optional[float] = None

class EvaluationService:
    def __init__(self):
        self.llm_wrapper = LangchainLLMWrapper(llm)
        self.embeddings_wrapper = LangchainEmbeddingsWrapper(embedding)
        
        # 使用可能なメトリクス
        self.available_metrics = {
            'context_precision': context_precision,
            'context_recall': context_recall,
            'faithfulness': faithfulness,
            'answer_relevancy': answer_relevancy
        }
    
    def add_chat_for_evaluation(self, question: str, answer: str, contexts: List[str], source_files: List[str]):
        """チャット結果を評価用に追加"""
        if "evaluation_data" not in st.session_state:
            st.session_state.evaluation_data = []
        
        evaluation_item = ChatEvaluation(
            timestamp=datetime.now(),
            question=question,
            answer=answer,
            contexts=contexts,
            source_files=source_files
        )
        
        st.session_state.evaluation_data.append(evaluation_item)
    
    def evaluate_single_chat(self, evaluation_item: ChatEvaluation, selected_metrics: List[str]) -> ChatEvaluation:
        """単一のチャット結果を評価"""
        try:
            # DataFrameを作成
            data = {
                'user_input': [evaluation_item.question],
                'answer': [evaluation_item.answer],
                'retrieved_contexts': [evaluation_item.contexts],
                'reference': [evaluation_item.answer]  # 自己参照として使用
            }
            
            df = pd.DataFrame(data)
            dataset = EvaluationDataset.from_pandas(df)
            
            # 選択されたメトリクスで評価
            metrics = [self.available_metrics[metric] for metric in selected_metrics if metric in self.available_metrics]
            
            if not metrics:
                return evaluation_item
            
            result = evaluate(
                dataset,
                llm=self.llm_wrapper,
                embeddings=self.embeddings_wrapper,
                metrics=metrics,
            )
            
            # 結果を評価アイテムに反映
            result_dict = result.to_pandas().iloc[0].to_dict()
            
            if 'context_precision' in selected_metrics:
                evaluation_item.context_precision = result_dict.get('context_precision')
            if 'context_recall' in selected_metrics:
                evaluation_item.context_recall = result_dict.get('context_recall')
            if 'faithfulness' in selected_metrics:
                evaluation_item.faithfulness = result_dict.get('faithfulness')
            if 'answer_relevancy' in selected_metrics:
                evaluation_item.answer_relevancy = result_dict.get('answer_relevancy')
            
            # 総合スコアを計算
            scores = []
            if evaluation_item.context_precision is not None:
                scores.append(evaluation_item.context_precision)
            if evaluation_item.context_recall is not None:
                scores.append(evaluation_item.context_recall)
            if evaluation_item.faithfulness is not None:
                scores.append(evaluation_item.faithfulness)
            if evaluation_item.answer_relevancy is not None:
                scores.append(evaluation_item.answer_relevancy)
            
            if scores:
                evaluation_item.overall_score = sum(scores) / len(scores)
            
            return evaluation_item
            
        except Exception as e:
            print(f"Evaluation error: {e}")
            return evaluation_item
    
    def evaluate_all_chats(self, selected_metrics: List[str], progress_callback=None) -> List[ChatEvaluation]:
        """全てのチャット結果を評価"""
        if "evaluation_data" not in st.session_state:
            return []
        
        evaluated_data = []
        total_items = len(st.session_state.evaluation_data)
        
        for i, item in enumerate(st.session_state.evaluation_data):
            if progress_callback:
                progress_callback(f"Evaluating {i+1}/{total_items}: {item.question[:50]}...")
            
            evaluated_item = self.evaluate_single_chat(item, selected_metrics)
            evaluated_data.append(evaluated_item)
        
        # セッション状態を更新
        st.session_state.evaluation_data = evaluated_data
        return evaluated_data
    
    def get_evaluation_summary(self) -> Dict[str, Any]:
        """評価結果のサマリーを取得"""
        if "evaluation_data" not in st.session_state:
            return {}
        
        data = st.session_state.evaluation_data
        evaluated_data = [item for item in data if item.overall_score is not None]
        
        if not evaluated_data:
            return {"total_chats": len(data), "evaluated_chats": 0}
        
        # 各メトリクスの平均を計算
        summary = {
            "total_chats": len(data),
            "evaluated_chats": len(evaluated_data),
            "avg_overall_score": sum(item.overall_score for item in evaluated_data) / len(evaluated_data)
        }
        
        # 各メトリクスの平均
        metrics = ['context_precision', 'context_recall', 'faithfulness', 'answer_relevancy']
        for metric in metrics:
            scores = [getattr(item, metric) for item in evaluated_data if getattr(item, metric) is not None]
            if scores:
                summary[f"avg_{metric}"] = sum(scores) / len(scores)
        
        return summary
    
    def export_evaluation_data(self) -> pd.DataFrame:
        """評価データをDataFrameとしてエクスポート"""
        if "evaluation_data" not in st.session_state:
            return pd.DataFrame()
        
        data = []
        for item in st.session_state.evaluation_data:
            data.append({
                'timestamp': item.timestamp,
                'question': item.question,
                'answer': item.answer,
                'contexts': '; '.join(item.contexts),
                'source_files': '; '.join(item.source_files),
                'context_precision': item.context_precision,
                'context_recall': item.context_recall,
                'faithfulness': item.faithfulness,
                'answer_relevancy': item.answer_relevancy,
                'overall_score': item.overall_score
            })
        
        return pd.DataFrame(data)
    
    def clear_evaluation_data(self):
        """評価データをクリア"""
        if "evaluation_data" in st.session_state:
            del st.session_state.evaluation_data

# グローバルインスタンス
evaluation_service = EvaluationService()