import os
import time
import argparse
import concurrent.futures
import subprocess
import pathlib
import regex as re

max_retries = 30  # Número máximo de tentativas de download
retry_interval = 30  # 5 minutos em segundos
num_workers = 20  # Número de processos paralelos
user = 'arturo66cta@gmail.com'
password = 'Mazamorra2328'
output_Dir = 'D://Data//IMERG//raw//monthly'

def download_url(url):
    filename = re.search(r'LABEL=.\S+\b.S\d{6}', url).group(0)
    filename = filename[6:] + '.nc4'
    datetime = re.search(r'\d{8}', filename).group(0)
    datetime = datetime[0:4] + '/' + datetime[4:6] + '/' + datetime[6:8] + '/'
    outputDir = output_Dir + datetime
    pathlib.Path(outputDir).mkdir(parents=True, exist_ok=True)
    retries = 0
    while retries < max_retries:
        try:
            if not os.path.exists(os.path.basename(url)):
                subprocess.run(['wget --user='+user+' --password='+password+' --show-progress -c -q \"' +url + '\" -O '+outputDir + filename], shell=True, check=True)
                break
            else:
                print(f"File already exists: {url}")
                break
            print(f"Downloaded: {url}")
            with open("downloader_error.txt", "a") as log_file:
                log_file.write(f"{url}\n")
            break  # Sai do loop se o download for bem-sucedido ou se atingir o limite de tentativas
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            retries += 1
            print(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

def main(args):
    with open(args.url_file, "r") as file:
        url_list = [line.strip() for line in sorted(file.readlines())]
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        executor.map(download_url, url_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download URLs from a file in parallel using wget.")
    parser.add_argument("url_file", type=str, help="Path to the file containing URLs.")
    args = parser.parse_args()
    main(args)
