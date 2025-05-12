# preprocess/merge.py

import pandas as pd
from data.area_data import district_area_dict

class EnvironmentDataMerger:
    def __init__(self, df_air: pd.DataFrame, df_green: pd.DataFrame, df_waste: pd.DataFrame):
        self.df_air = df_air
        self.df_green = df_green
        self.df_waste = df_waste

    def merge(self):
        """자치구 기준 병합"""
        df = self.df_air.merge(self.df_green, on='자치구', how='inner')
        df = df.merge(self.df_waste, on='자치구', how='inner')
        self.df_merged = df
        return self

    def add_ranking(self):
        """각 항목별 순위 컬럼 추가"""
        df = self.df_merged.copy()

        df["PM10_rank"] = df["PM10_avg"].rank(ascending=True)
        df["PM25_rank"] = df["PM25_avg"].rank(ascending=True)
        df["녹지_rank"] = df["평균_녹지면적"].rank(ascending=False)
        df["수거율_rank"] = df["수거율"].rank(ascending=False)
        df["재활용률_rank"] = df["재활용률"].rank(ascending=False)

        df["종합순위"] = df[[
            "PM10_rank", "PM25_rank", "녹지_rank", "수거율_rank", "재활용률_rank"
        ]].mean(axis=1)

        
        # ✅ 면적 기반 비율 추가
        df["자치구_전체면적"] = df["자치구"].map(district_area_dict)
        df["녹지비율"] = (df["평균_녹지면적"] / df["자치구_전체면적"]) * 100

        self.df_merged = df
        return self
    def add_birth_rate(self, df_birth: pd.DataFrame):
        self.df_merged = self.df_merged.merge(df_birth, on="자치구", how="left")
        return self

    def get(self) -> pd.DataFrame:
        return self.df_merged
