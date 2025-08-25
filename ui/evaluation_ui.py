# ui/evaluation_ui.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

from backend.evaluation import evaluation_service

class EvaluationUI:
    def __init__(self):
        self.evaluation_service = evaluation_service

        # メトリクス名のマッピング（表示名 → バックエンド名）
        self.metrics_mapping = {
            "Context Precision": "context_precision",
            "Context Recall": "context_recall", 
            "Faithfulness": "faithfulness",
            "Answer Relevancy": "answer_relevancy"
        }
        
        # 逆マッピング（バックエンド名 → 表示名）
        self.metrics_display_mapping = {v: k for k, v in self.metrics_mapping.items()}
    
    def render_evaluation_summary(self):
        """評価サマリーを表示"""
        st.subheader("📊 評価の結果だよ〜")
        
        summary = self.evaluation_service.get_evaluation_summary()
        
        if not summary:
            st.info("まだ評価データがないよ〜。チャットで質問してから評価してみて💕")
            return
        
        # メトリクス表示
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("総チャット数", summary.get("total_chats", 0))
        
        with col2:
            st.metric("評価済み", summary.get("evaluated_chats", 0))
        
        with col3:
            if "avg_overall_score" in summary:
                st.metric("平均総合スコア", f"{summary['avg_overall_score']:.3f}", help="各メトリクスのスコアの平均である「総合スコア」の平均を表示してるよ〜")
            else:
                st.metric("平均総合スコア", "未評価", help="各メトリクスのスコアの平均である「総合スコア」の平均を表示してるよ〜")
        
        with col4:
            evaluation_rate = 0
            if summary.get("total_chats", 0) > 0:
                evaluation_rate = summary.get("evaluated_chats", 0) / summary["total_chats"] * 100
            st.metric("評価率", f"{evaluation_rate:.1f}%")
    
    def render_metrics_chart(self):
        """メトリクスのチャートを表示"""
        if "evaluation_data" not in st.session_state:
            return
        
        data = st.session_state.evaluation_data
        evaluated_data = [item for item in data if item.overall_score is not None]
        
        if not evaluated_data:
            return
        
        st.subheader("📈 グラフで見てみよ〜")
        
        # データを準備
        metrics_data = []
        for item in evaluated_data:
            if item.context_precision is not None:
                metrics_data.append({"metric": "Context Precision", "score": item.context_precision, "timestamp": item.timestamp})
            if item.context_recall is not None:
                metrics_data.append({"metric": "Context Recall", "score": item.context_recall, "timestamp": item.timestamp})
            if item.faithfulness is not None:
                metrics_data.append({"metric": "Faithfulness", "score": item.faithfulness, "timestamp": item.timestamp})
            if item.answer_relevancy is not None:
                metrics_data.append({"metric": "Answer Relevancy", "score": item.answer_relevancy, "timestamp": item.timestamp})
        
        if metrics_data:
            df = pd.DataFrame(metrics_data)
            
            # ボックスプロット
            fig = px.box(df, x="metric", y="score", title="メトリクスの分布💎")
            st.plotly_chart(fig, use_container_width=True)
            
            # 時系列チャート
            fig2 = px.line(df, x="timestamp", y="score", color="metric", title="時系列で見るメトリクスの変化✨")
            st.plotly_chart(fig2, use_container_width=True)
    
    def render_evaluation_controls(self):
        """評価制御UI"""
        st.subheader("🔧 評価の設定")
        
        # メトリクス選択
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # メトリクスの説明
            metrics_help = {
                "Context Precision": "検索で拾った文脈、質問とバチバチ合ってる率だよ💅 余計なのは即オフ〜",
                "Context Recall": "答えに必要なネタ、文脈にどれだけ盛れてるかチェックするやつ✨ 取りこぼしゼロ目指そ〜",
                "Faithfulness": "生成した答え、文脈にガチ忠実か見るやつ📚 妄想混ぜたら一発アウトだよ👀",
                "Answer Relevancy": "答えの内容、質問と神一致してるかの温度感だよ🔥 ずれてたら『それはそれ』じゃなくてNG〜"
            }

            # 表示名でメトリクスを選択
            selected_display_metrics = st.multiselect(
                "評価したいメトリクスを選んでね〜",
                options=list(self.metrics_mapping.keys()),
                default=["Context Precision", "Context Recall"],
                help="どの項目で評価するか選んでね💕"
            )

            # 選択されたメトリクスの説明を表示
            if selected_display_metrics:
                st.write("**選んだメトリクスの説明:**")
                for metric in selected_display_metrics:
                    st.write(f"• **{metric}**: {metrics_help[metric]}")

            # バックエンド用に変換
            selected_metrics = [self.metrics_mapping[metric] for metric in selected_display_metrics]
        
        with col2:
            st.write("") # スペース
            st.write("") # スペース
            if st.button("🚀 評価スタート！", type="primary", disabled=not selected_metrics):
                self.run_evaluation(selected_metrics)
    
    def run_evaluation(self, selected_metrics):
        """評価を実行"""
        if "evaluation_data" not in st.session_state or not st.session_state.evaluation_data:
            st.warning("評価するデータがないよ〜")
            return
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def progress_callback(message):
            status_text.text(message)
        
        try:
            # 評価実行
            evaluated_data = self.evaluation_service.evaluate_all_chats(
                selected_metrics, 
                progress_callback
            )
            
            progress_bar.progress(1.0)
            status_text.text("✅ 評価完了〜！")
            
            st.success(f"🎉 {len(evaluated_data)}件のチャットを評価したよ〜！")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ 評価中にエラーが起きちゃった💦: {str(e)}")
            status_text.text("エラーが発生しました")
    
    def render_evaluation_details(self):
        """評価詳細を表示"""
        if "evaluation_data" not in st.session_state:
            return
        
        st.subheader("📋 詳しい評価結果")
        
        data = st.session_state.evaluation_data
        
        if not data:
            st.info("評価データがないよ〜")
            return
        
        # フィルタリング
        col1, col2 = st.columns([1, 1])
        
        with col1:
            show_evaluated_only = st.checkbox("評価済みだけ見る", value=False)
        
        with col2:
            sort_by = st.selectbox("並び順", ["時間順", "スコア順"], index=0)
        
        # データをフィルタリング・ソート
        filtered_data = data
        if show_evaluated_only:
            filtered_data = [item for item in data if item.overall_score is not None]
        
        if sort_by == "スコア順" and filtered_data:
            filtered_data = sorted(filtered_data, key=lambda x: x.overall_score or 0, reverse=True)
        
        # データ表示
        for i, item in enumerate(filtered_data):
            with st.expander(f"💬 {item.question[:50]}... ({item.timestamp.strftime('%Y-%m-%d %H:%M')})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**質問:**")
                    st.write(item.question)
                    st.write("**回答:**")
                    st.write(item.answer)
                    st.write("**参照ファイル:**")
                    st.write(", ".join(item.source_files))
                
                with col2:
                    if item.overall_score is not None:
                        st.metric("総合スコア", f"{item.overall_score:.3f}", help="各メトリクスのスコアの平均だよ〜")
                        
                        if item.context_precision is not None:
                            st.metric("Context Precision", f"{item.context_precision:.3f}")
                        if item.context_recall is not None:
                            st.metric("Context Recall", f"{item.context_recall:.3f}")
                        if item.faithfulness is not None:
                            st.metric("Faithfulness", f"{item.faithfulness:.3f}")
                        if item.answer_relevancy is not None:
                            st.metric("Answer Relevancy", f"{item.answer_relevancy:.3f}")
                    else:
                        st.info("まだ評価してないよ〜")
    
    def render_data_management(self):
        """データ管理UI"""
        st.subheader("🗂️ データの管理")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 CSVでダウンロード"):
                df = self.evaluation_service.export_evaluation_data()
                if not df.empty:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 ダウンロード開始",
                        data=csv,
                        file_name=f"evaluation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("ダウンロードするデータがないよ〜")
        
        with col2:
            if st.button("🗑️ データ全削除", type="secondary"):
                if st.checkbox("本当に全部消しちゃう？"):
                    self.evaluation_service.clear_evaluation_data()
                    st.success("データを全部消したよ〜")
                    st.rerun()
    
    def render_evaluation_page(self):
        """評価ページ全体をレンダリング"""
        st.header("RAGの性能チェック✨")
        
        # サマリー表示
        self.render_evaluation_summary()
        
        st.divider()
        
        # 評価制御
        self.render_evaluation_controls()
        
        st.divider()
        
        # チャート表示
        self.render_metrics_chart()
        
        st.divider()
        
        # 詳細表示
        self.render_evaluation_details()
        
        st.divider()
        
        # データ管理
        self.render_data_management()

def render_evaluation_page():
    """評価ページをレンダリング"""
    evaluation_ui = EvaluationUI()
    evaluation_ui.render_evaluation_page()