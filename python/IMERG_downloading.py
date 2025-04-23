import os
import subprocess
import concurrent.futures

num_workers = 5

USER=os.environ['EARTH_DATA_USER']
PASS=os.environ['EARTH_DATA_PASS']

list_txt = '/home/arturo/Downloads/SA_IMERG_1dy_1999_01_01_31_12_2024.txt'

with open(list_txt) as f:
    file_download = f.readlines()

len_files = len(file_download)
print(f'Number of files to download: {len_files}')

file_list = []
for t in range(2,len(file_download)):#len(file_download)
    file_list.append(file_download[t])
print(f'Number of files to download: {len(file_list)}')

def download_litte_r_for_date(link):
    filename = link.split('/')[-1].split('?')[0].replace('.nc4.nc4','.nc4')
    file_complete = os.path.join('/','home','arturo','Downloads','IMERG','raw',filename)
    if os.path.isfile(file_complete) and os.path.getsize(file_complete) > 0:
        print(f"File {filename} already exists and is not empty. Skipping download.")
    else:
        subprocess.run([
            "wget", 
            "--user", USER, 
            "--password", PASS, 
            link, 
            "-O", file_complete
            ])

with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    executor.map(download_litte_r_for_date, file_list)