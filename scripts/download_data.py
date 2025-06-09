import os
import yaml
import argparse
import yfinance as yf

from util import Logger

def ensure_directory(path: str, logger: Logger):
    """
    지정된 경로에 디렉토리가 없으면 생성합니다.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory: {path}")

def download_data(symbol: str, name: str, save_dir: str, logger: Logger):
    """
    주어진 티커(symbol)에 대해 yfinance 데이터를 다운로드하고
    CSV 파일로 저장한 뒤, 상태를 로그로 출력합니다.
    """
    logger.info(f"Downloading {name} ({symbol})")
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="max")  # 전체 기간 히스토리

    if df.empty:
        logger.warning(f"No data returned for {name} ({symbol})")
        return

    logger.info(f"Data points: {len(df)}")
    logger.info(f"Start date: {df.index[0]}")
    logger.info(f"End date: {df.index[-1]}")

    # 파일 저장
    file_path = os.path.join(save_dir, f"{name}.csv")
    df.to_csv(file_path)
    logger.info(f"Data saved to {file_path}")

def main(data_dir: str):
    """
    전체 자산에 대해 데이터를 다운로드하고 저장합니다.
    """
    logger = Logger("DownloadData")
    
    with open("config/data_config.yaml", "r") as file:
        config = yaml.safe_load(file)
        name_map = config.get("name_map", {})
    ensure_directory(data_dir, logger)

    logger.info("Starting data download...")
    logger.info(f"Downloading assets: {', '.join(name_map.keys())}")

    for name, symbol in name_map.items():
        download_data(symbol, name, data_dir, logger)

    logger.info("Data download completed.")

if __name__ == "__main__":
    # 커맨드라인 인자로 저장 디렉토리 지정
    parser = argparse.ArgumentParser(description="Download data for the project.")
    parser.add_argument("--data_dir", type=str, default="data", help="Directory to save downloaded data")
    args = parser.parse_args()

    main(args.data_dir)
