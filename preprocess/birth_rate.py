# preprocess/birth_rate.py
import pandas as pd

class BirthRateProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def clean_and_aggregate(self):
        """
        자치구별 합계출산율 (2020~2023) 평균 계산
        """
        # 실제 데이터는 3번째 행부터 시작
        df = self.df.iloc[2:].copy()
        df.rename(columns={"자치구별(1)": "자치구"}, inplace=True)

        # 2020~2023 열만 선택
        years = ["2020", "2021", "2022", "2023"]
        df_birth = df[["자치구"] + years]

        # 문자열을 숫자로 변환
        for year in years:
            df_birth[year] = pd.to_numeric(df_birth[year], errors="coerce")

        # Long format으로 변환
        df_long = df_birth.melt(id_vars=["자치구"], value_vars=years,
                                var_name="연도", value_name="출산율")
        df_long["연도"] = df_long["연도"].astype(int)

        # 자치구별 평균 출산율
        df_avg = df_long.groupby("자치구")["출산율"].mean().reset_index()
        df_avg.rename(columns={"출산율": "평균_출산율"}, inplace=True)

        return df_avg
