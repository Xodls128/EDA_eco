import pandas as pd
import numpy as np

class WasteProcessor:
    def __init__(self, df_waste: pd.DataFrame):
        self.df = df_waste.copy()

    def clean_columns(self):
        """자치구 컬럼명 통일 및 불필요 행 제거"""
        self.df.rename(columns={
            "자치구별(2)": "자치구",
            "수거율(D/C) (%)": "수거율",
            "처리방법 (톤/일).3": "재활용량",
            "처리량(D) (톤/일)": "총처리량"
        }, inplace=True)
        self.df = self.df[~self.df["자치구"].str.contains("합계|소계|서울", na=False)]
        return self

    def compute_metrics(self):
        """재활용률 계산 및 자치구별 평균 수거율, 재활용률 계산"""
        self.df["수거율"] = self.df["수거율"].replace("-", np.nan).astype(float)
        self.df["재활용량"] = self.df["재활용량"].replace("-", np.nan).astype(float)
        self.df["총처리량"] = self.df["총처리량"].replace("-", np.nan).astype(float)

        self.df["재활용률"] = self.df["재활용량"] / self.df["총처리량"]

        df_grouped = self.df.groupby("자치구").agg({
            "수거율": "mean",
            "재활용률": "mean"
        }).reset_index()

        return df_grouped
