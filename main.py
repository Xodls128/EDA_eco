from preprocess.data_load import DataLoader
from preprocess.air_process import AirQualityProcessor
from preprocess.green_process import GreenAreaProcessor
from preprocess.waste_process import WasteProcessor
from preprocess.merge import EnvironmentDataMerger
from visualization.environment_plotter import EnvironmentPlotter
from tabulate import tabulate

def main():
    print("📥 데이터 로딩 중...")
    loader = DataLoader()
    df_air = loader.load_air_quality()
    df_green = loader.load_green_area()
    df_waste = loader.load_waste_data()

    print("🧹 전처리 수행 중...")
    df_air_p = AirQualityProcessor(df_air).clean().compute_pm_avg()
    df_green_p = GreenAreaProcessor(df_green).filter_district_rows().compute_avg_green_area()
    df_waste_p = WasteProcessor(df_waste).clean_columns().compute_metrics()

    print("🔗 데이터 병합 및 순위화 중...")
    merger = EnvironmentDataMerger(df_air_p, df_green_p, df_waste_p)
    df_env_final = merger.merge().add_ranking().get()

    print("📈 시각화 이미지 생성 중...")
    plotter = EnvironmentPlotter(df_env_final)
    plotter.plot_comparative_bars()
    plotter.plot_rank_bar("녹지_rank", "녹지면적 높은 자치구 Top 10", ascending=True)
    plotter.plot_rank_bar("PM10_rank", "미세먼지 낮은 자치구 Top 10", ascending=True)
    plotter.plot_rank_bar("재활용률_rank", "재활용률 높은 자치구 Top 10", ascending=True)
    plotter.plot_heatmap()

    print("💾 결과 저장 중...")
    df_env_final.to_csv('./result/자치구_환경지표_종합순위.csv', index=False)

    print("✅ 완료! 결과는 result/ 폴더에 저장되었습니다.")
    print(tabulate(df_env_final.head(10), headers='keys', tablefmt='fancy_grid'))

if __name__ == '__main__':
    main()
