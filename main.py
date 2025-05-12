# main.py

from preprocess.data_load import DataLoader
from preprocess.air_process import AirQualityProcessor
from preprocess.green_process import GreenAreaProcessor
from preprocess.waste_process import WasteProcessor
from preprocess.merge import EnvironmentDataMerger
from visualization.environment_plotter import EnvironmentPlotter
from tabulate import tabulate
from preprocess.birth_rate import BirthRateProcessor

def main():
    print("📥 데이터 로딩 중...")
    loader = DataLoader()
    df_air = loader.load_air_quality()
    df_green = loader.load_green_area()
    df_waste = loader.load_waste_data()
    df_birth_raw = loader.load_birth_rate()  # ✅ 출산율 데이터 로딩
    df_birth = BirthRateProcessor(df_birth_raw).clean_and_aggregate()  # ✅ 전처리 수행



    print("🧹 전처리 수행 중...")
    df_air_p = AirQualityProcessor(df_air).clean().compute_pm_avg()
    df_green_p = GreenAreaProcessor(df_green).filter_district_rows().compute_avg_green_area()
    df_waste_p = WasteProcessor(df_waste).clean_columns().compute_metrics()

    print("🔗 데이터 병합 및 순위화 중...")
    df_env_final = (
        EnvironmentDataMerger(df_air_p, df_green_p, df_waste_p)
        .merge()
        .add_ranking()
        .add_birth_rate(df_birth)  # ✅ 반드시 이 시점에 포함되어야 함
        .get()
    )

    print("📈 시각화 이미지 생성 중...")
    plotter = EnvironmentPlotter(df_env_final)
    plotter.plot_heatmap()

    # ✅ [변경] 각 지표별 개별 그래프 생성 (순위 막대그래프 제거됨)
    plotter.plot_individual_bar(
        column="PM10_avg",  # 🔍 PM10 지표
        title="서울시 자치구별 PM10 농도",
        ylabel="PM10 (㎍/m³)",
        palette="Blues_d",
        ylim_min= 6  # 🔽 y축 최소값 조정으로 시각 강조
    )

    plotter.plot_individual_bar(
        column="PM25_avg",  # 🔍 PM2.5 지표
        title="서울시 자치구별 PM2.5 농도",
        ylabel="PM2.5 (㎍/m³)",
        palette="Blues",
        ylim_min= 11
    )

    plotter.plot_individual_bar(
        column="평균_녹지면적",  # 🌳 녹지면적 지표
        title="서울시 자치구별 평균 녹지면적",
        ylabel="녹지면적 (㎡)",
        palette="Greens_d",
        ylim_min= 5000,
        ascending=False  # 🔽 내림차순 정렬(큰값이 앞에오도록)
    )
        # ✅ 자치구 전체 면적 대비 녹지 비율 시각화
    plotter.plot_individual_bar(
        column="녹지비율",  # 🌳 녹지면적 비율
        title="서울시 자치구별 녹지면적 비율",
        ylabel="녹지비율 (%)",
        palette="Greens",
        ylim_min=0, 
        ascending=False  # 🔽 내림차순 정렬(큰값이 앞에오도록)
    )

    plotter.plot_individual_bar(
        column="재활용률",  # ♻️ 재활용률 지표
        title="서울시 자치구별 재활용률",
        ylabel="재활용률 (비율)",
        palette="Purples_d",
        ylim_min= 65,
        ascending=False  # 🔽 내림차순 정렬(큰값이 앞에오도록)
    )

    plotter.plot_birth_correlation_heatmap()

    print("💾 결과 저장 중...")
    df_env_final.to_csv('./result/자치구_환경지표_종합순위.csv', index=False)

    print("✅ 완료! 결과는 result/ 폴더에 저장되었습니다.")
    print(tabulate(df_env_final.head(10), headers='keys', tablefmt='fancy_grid'))

if __name__ == '__main__':
    main()
