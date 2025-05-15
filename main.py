# main.py

from preprocess.data_load import DataLoader
from preprocess.air_process import AirQualityProcessor
from preprocess.green_process import GreenAreaProcessor
from preprocess.waste_process import WasteProcessor
from preprocess.merge import EnvironmentDataMerger
from visualization.environment_plotter import EnvironmentPlotter
from tabulate import tabulate
from preprocess.birth_rate import BirthRateProcessor
from preprocess.park_process import ParkAreaProcessor


def main():
    print("📥 데이터 로딩 중...")
    loader = DataLoader()
    df_air = loader.load_air_quality()
    df_green = loader.load_green_area()
    df_waste = loader.load_waste_data()
    df_birth_raw = loader.load_birth_rate()  
    df_birth = BirthRateProcessor(df_birth_raw).clean_and_aggregate()  



    print("🧹 전처리 수행 중...")
    df_air_p = AirQualityProcessor(df_air).clean().compute_pm_avg()
    df_green_p = GreenAreaProcessor(df_green).filter_district_rows().compute_avg_green_area()
    df_waste_p = WasteProcessor(df_waste).clean_columns().compute_metrics()
    df_park = ParkAreaProcessor(loader.load_park_area()).clean_and_aggregate()

    print("🔗 데이터 병합 및 순위화 중...")
    df_env_final = (
        EnvironmentDataMerger(df_air_p, df_green_p, df_waste_p)
        .merge()
        .add_green_ratio()
        .add_birth_rate(df_birth)
        .add_park_area(df_park)
        .get()
    )

    print("📈 시각화 이미지 생성 중...")
    plotter = EnvironmentPlotter(df_env_final)

    # ✅ [변경] 각 지표별 개별 그래프 생성 (순위 막대그래프 제거됨)
    plotter.plot_individual_bar(
        column="PM10_avg",  # 🔍 PM10 지표
        title="서울시 자치구별 PM10 농도",
        ylabel="PM10 (㎍/m³)",
        ylim_min= 6, # 🔽 y축 최소값 조정으로 시각 강조
        highlight=["강남구", "서초구"],
    )

    plotter.plot_individual_bar(
        column="PM25_avg",  # 🔍 PM2.5 지표
        title="서울시 자치구별 PM2.5 농도",
        ylabel="PM2.5 (㎍/m³)",
        ylim_min= 11,
    )


    plotter.plot_individual_bar(
        column="재활용률",  # ♻️ 재활용률 지표
        title="서울시 자치구별 재활용률",
        ylabel="재활용률(%)",
        ylim_min= 65,
        ascending=False,  # 🔽 내림차순 정렬(큰값이 앞에오도록)
    )
    
    plotter.plot_individual_bar(
        column="공원율",
        title="서울시 자치구별 공원율",
        ylabel="공원율(%)",
        ylim_min=10,
        ascending=False,  # 높은 순부터
    )


    plotter.plot_birth_correlation_heatmap()

    print("💾 결과 저장 중...")
    df_env_final.to_csv('./result/자치구_환경지표_종합순위.csv', index=False)

    print("✅ 완료! 결과는 result/ 폴더에 저장되었습니다.")
    print(tabulate(df_env_final.head(10), headers='keys', tablefmt='fancy_grid'))

if __name__ == '__main__':
    main()
