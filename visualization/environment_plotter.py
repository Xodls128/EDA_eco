# visualization/environment_plotter.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

import matplotlib.ticker as mtick #비율화를 그래프에 적용하기위한 라이브러리


# 🔠 한글 폰트 설정 (Windows: 맑은 고딕 / macOS: AppleGothic)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'  # Windows
# matplotlib.rcParams['font.family'] = 'AppleGothic'  # macOS

# 깨진 한글 대체 문자 제거 (마이너스 깨짐 방지용)
matplotlib.rcParams['axes.unicode_minus'] = False


class EnvironmentPlotter:
    def __init__(self, df: pd.DataFrame, result_dir='./result'):
        self.df = df.copy()
        self.result_dir = result_dir
        os.makedirs(result_dir, exist_ok=True)



    def plot_individual_bar(self, column: str, title: str, ylabel: str, ylim_min: float = None, ascending=True, highlight: list = ['중구','영등포구','송파구','성동구','동대문구','구로구'], highlight_color="red", base_color="green"):
        """
        자치구별 값 기준으로 정렬하여 개별 지표 막대 그래프 출력
        """
        df_sorted = self.df.sort_values(by=column, ascending=ascending)

        plt.figure(figsize=(14, 6))
        palette = [base_color] * len(df_sorted)
        ax = sns.barplot(data=df_sorted, x='자치구', y=column, palette=palette)

        plt.title(title)
        plt.ylabel(ylabel)
        plt.xticks(rotation=90)

         # ✅ 퍼센트 단위 처리 (예: 녹지비율, 재활용률 등)
        if "비율" in column or "률" in column:
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))


        # ✅ x축 라벨 중 highlight에 해당하는 자치구만 빨간색
        for label in ax.get_xticklabels():
            if label.get_text() in highlight:
                label.set_color(highlight_color)
            else:
                label.set_color("black")  # 기본색

            if ylim_min is not None:
                ymax = df_sorted[column].max() * 1.05
                plt.ylim(ylim_min, ymax)

        plt.tight_layout()
        filename = f"{column}_자치구별.png"
        plt.savefig(os.path.join(self.result_dir, filename))
        plt.close()

    
    def plot_birth_correlation_heatmap(self):
        """
        출산율과 주요 환경지표 간 상관관계 히트맵
        """
        columns = [
            "PM10_avg",
            "PM25_avg",
            "녹지비율",
            "재활용률",
            "평균_출산율",
            "공원율"
        ]

        df_corr = self.df[columns].corr(method="pearson")

        plt.figure(figsize=(8, 6))
        sns.heatmap(df_corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("출산율과 환경지표 간 상관관계 (2020~2023)")
        plt.tight_layout()
        plt.savefig(os.path.join(self.result_dir, "출산율_환경지표_상관관계_히트맵.png"))
        plt.close()
