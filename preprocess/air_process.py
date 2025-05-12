import pandas as pd

class AirQualityProcessor:
    def __init__(self, df_air: pd.DataFrame):
        self.df = df_air.copy()

    def clean(self):
        """자치구 컬럼 이름 정리 및 합계 행 제거"""
        self.df.rename(columns={"구분별(1)": "자치구"}, inplace=True)
        self.df = self.df[~self.df["자치구"].str.contains("합계|서울", na=False)]
        return self

    def compute_pm_avg(self):
        """PM10과 PM2.5의 연도별 평균을 자치구별로 계산"""
        pm10_cols = [col for idx, col in enumerate(self.df.columns[1:]) if idx % 2 == 0]
        pm25_cols = [col for idx, col in enumerate(self.df.columns[1:]) if idx % 2 == 1]

        # 문자열 값이 있을 수 있으므로 float 변환 시 에러 무시하고 NaN 처리
        self.df["PM10_avg"] = self.df[pm10_cols].apply(pd.to_numeric, errors='coerce').mean(axis=1)
        self.df["PM25_avg"] = self.df[pm25_cols].apply(pd.to_numeric, errors='coerce').mean(axis=1)

        return self.df[["자치구", "PM10_avg", "PM25_avg"]]
