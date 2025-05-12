import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class EnvironmentPlotter:
    def __init__(self, df: pd.DataFrame, result_dir='./result'):
        self.df = df.copy()
        self.result_dir = result_dir
        os.makedirs(result_dir, exist_ok=True)

    def plot_rank_bar(self, column: str, title: str, top_n=10, ascending=True):
        """
        특정 순위 컬럼 기준으로 상위/하위 자치구 막대 그래프
        """
        df_plot = self.df.sort_values(by=column, ascending=ascending).head(top_n)

        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_plot, x=column, y='자치구', palette='viridis')
        plt.title(title)
        plt.xlabel('순위값')
        plt.ylabel('자치구')
        plt.tight_layout()

        path = os.path.join(self.result_dir, f'{column}_top{top_n}.png')
        plt.savefig(path)
        plt.close()

    def plot_heatmap(self):
        """
        순위 컬럼 간의 스피어만 상관관계 히트맵
        """
        rank_cols = [col for col in self.df.columns if col.endswith('_rank')]
        corr = self.df[rank_cols].corr(method='spearman')

        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("환경 순위 지표 간 상관관계")
        plt.tight_layout()

        path = os.path.join(self.result_dir, 'rank_heatmap.png')
        plt.savefig(path)
        plt.close()

    def plot_comparative_bars(self):
        """
        대기오염 낮은 순서로 정렬 후, 녹지·재활용률을 나란히 보여주는 비교 시각화
        """
        df_sorted = self.df.sort_values(by="PM10_avg", ascending=True)

        fig, axes = plt.subplots(3, 1, figsize=(12, 15), sharex=True)

        sns.barplot(data=df_sorted, x="자치구", y="PM10_avg", ax=axes[0], palette="Blues_d")
        axes[0].set_title("PM10 평균 (낮을수록 좋음)")
        axes[0].set_ylabel("PM10")

        sns.barplot(data=df_sorted, x="자치구", y="평균_녹지면적", ax=axes[1], palette="Greens_d")
        axes[1].set_title("평균 녹지면적 (㎡)")
        axes[1].set_ylabel("녹지면적")

        sns.barplot(data=df_sorted, x="자치구", y="재활용률", ax=axes[2], palette="Purples_d")
        axes[2].set_title("재활용률 (비율)")
        axes[2].set_ylabel("재활용률")

        for ax in axes:
            ax.tick_params(axis='x', rotation=90)

        plt.tight_layout()
        save_path = os.path.join(self.result_dir, '환경3지표_자치구비교.png')
        plt.savefig(save_path)
        plt.close()
