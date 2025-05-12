# preprocess/park_process.py
import pandas as pd

class ParkAreaProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def clean_and_aggregate(self) -> pd.DataFrame:
        df = self.df.copy()

        # 3번째 행부터 실제 데이터
        df = df.iloc[2:].copy()

        # 주요 컬럼명 통일
        df = df.rename(columns={"자치구별(2)": "자치구", "2023.2": "공원율"})

        df["공원율"] = pd.to_numeric(df["공원율"], errors="coerce")
        df = df[["자치구", "공원율"]].dropna()
        df["공원율"] = df["공원율"].astype(float)

        return df
