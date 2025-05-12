import pandas as pd
import numpy as np

class GreenAreaProcessor:
    def __init__(self, df_green: pd.DataFrame):
        self.df = df_green.copy()

        # 서울시 자치구 목록 (정규화 필요 시 외부에서 받을 수도 있음)
        self.districts = [
            '강남구','강동구','강북구','강서구','관악구','광진구','구로구','금천구','노원구','도봉구','동대문구','동작구',
            '마포구','서대문구','서초구','성동구','성북구','송파구','양천구','영등포구','용산구','은평구','종로구','중구','중랑구'
        ]

    def filter_district_rows(self):
        """자치구만 필터링"""
        self.df = self.df[self.df['구분별(2)'].isin(self.districts)]
        return self

    def compute_avg_green_area(self):
        """시설녹지(.2) + 일반녹지(.3)를 연도별로 더하고 평균"""
        years = ['2020', '2021', '2022', '2023']
        green_cols = []

        for y in years:
            col_2 = f'{y}.2'
            col_3 = f'{y}.3'
            if col_2 in self.df.columns and col_3 in self.df.columns:
                self.df[f'{y}_녹지합'] = self.df[[col_2, col_3]].replace("-", np.nan).astype(float).sum(axis=1)
                green_cols.append(f'{y}_녹지합')

        self.df['평균_녹지면적'] = self.df[green_cols].mean(axis=1)
        return self.df[['구분별(2)', '평균_녹지면적']].rename(columns={'구분별(2)': '자치구'})
