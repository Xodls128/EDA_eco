#preprocess/waste_process.py

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
        
        # '소계', '합계', '서울', NaN 등의 행 제거
        self.df = self.df[~self.df["자치구"].astype(str).str.contains("소계|합계|서울", na=False)]
        self.df = self.df[self.df["자치구"].notna()]

        return self

    def compute_metrics(self):
        """재활용률 계산 및 자치구별 평균 수거율, 재활용률 계산"""
        # 수치 변환 (문자 -> 숫자)
        self.df["수거율"] = pd.to_numeric(self.df["수거율"], errors='coerce')
        self.df["재활용량"] = pd.to_numeric(self.df["재활용량"], errors='coerce')
        self.df["총처리량"] = pd.to_numeric(self.df["총처리량"], errors='coerce')

        # 재활용률 계산
        self.df["재활용률"] = self.df["재활용량"] / self.df["총처리량"] * 100

        # 자치구별 평균 계산
        df_grouped = self.df.groupby("자치구").agg({
            "수거율": "mean",
            "재활용률": "mean"
        }).reset_index()

        return df_grouped
