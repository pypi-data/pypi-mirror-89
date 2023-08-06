import argparse
import datetime
import math
import time
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from ectcm.download import (extract_data_list, extract_total_count,
                            get_clinics, get_doctors, get_doctors_by_clinic)


def get_args():
    parser = argparse.ArgumentParser(description='download data from https://www.ectcm.com/ and export as csv')
    parser.add_argument("--output-folder", dest='output_folder', type=str, default='C:/ProgramData/ectcm/output',
                        help="output folder")
    parser.add_argument("--pagesize", dest='pagesize', type=int, default=500,
                        help="pagesize, cant be too large")
    parser.add_argument("--delay", dest='delay', type=int, default=2,
                        help="number of seconds between each request")
    parser.add_argument("--by-clinic-pagesize", dest='by_clinic_pagesize', type=int, default=100,
                        help="by clinic doctors page size")
    parser.add_argument('--skip-by-clinic', dest='skip_by_clinic', action='store_true', default=False, help='skip downloading ectcm_doctors_by_clinic_{today_str}.csv, which is slow')
    
    args = parser.parse_args()
    return args

def run():
    args = get_args()
    today_dt = datetime.datetime.now()
    today_str = today_dt.strftime('%Y%m%d')
    pagesize = args.pagesize
    delay = args.delay
    by_clinic_pagesize = args.by_clinic_pagesize
    
    print(f"start ectcm download at {today_dt}, pagesize = {pagesize}")
    
    output_folder = Path(args.output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    
    print("start download ectcm_clinics")
    res_clinics = get_clinics(pageno=1, pagesize=pagesize)
    all_res_clinics = [res_clinics]
    total_clinics_count = extract_total_count(res_clinics)
    for page in tqdm(list(range(2, math.ceil(total_clinics_count / pagesize) + 1))):
        res_clinics = get_clinics(pageno=page, pagesize=pagesize)
        all_res_clinics.append(res_clinics)
    print("finish download ectcm_clinics")
    
    print("start download ectcm_doctors")
    res_doctors = get_doctors(pageno=1, pagesize=pagesize)
    all_res_doctors = [res_doctors]
    total_doctors_count = extract_total_count(res_doctors)
    for page in tqdm(list(range(2, math.ceil(total_doctors_count / pagesize) + 1))):
        res_doctors = get_doctors(pageno=page, pagesize=pagesize)
        all_res_doctors.append(res_doctors)
    print("finish download ectcm_doctors")
    
    df_clinics = pd.DataFrame([data for data_list in map(extract_data_list, all_res_clinics) for data in data_list])
    df_clinics = df_clinics.drop(columns=['introduce'])
    df_clinics['donwload_datetime'] = today_dt
    
    df_doctors = pd.DataFrame([data for data_list in map(extract_data_list, all_res_doctors) for data in data_list])
    df_doctors = df_doctors.drop(columns=['workexperience'])
    df_doctors['donwload_datetime'] = today_dt
    
    # get doctors by clinic id
    if not args.skip_by_clinic:
        print("start download ectcm_doctors_by_clinic...")
        all_res_doctors_by_clinic = []
        clinicid_list = df_clinics['clinicid'].to_list()
        for clinicid in tqdm(clinicid_list):
            res_doctors_by_clinic = get_doctors_by_clinic(clinicid, pagesize=by_clinic_pagesize)
            all_res_doctors_by_clinic.append(res_doctors_by_clinic)
            if delay > 0:
                time.sleep(delay)
        print("finish download ectcm_doctors_by_clinic...")
        df_doctors_by_clinic = pd.DataFrame([data for data_list in map(extract_data_list, all_res_doctors_by_clinic) for data in data_list])
        df_doctors_by_clinic['donwload_datetime'] = today_dt
        df_doctors_by_clinic_path = output_folder / f'ectcm_doctors_by_clinic_{today_str}.csv'
        df_doctors_by_clinic.to_csv(df_doctors_by_clinic_path, encoding='utf-8-sig', index=False)
        print(f"ectcm doctor by clinic data saved to {df_doctors_by_clinic_path}, df_doctors_by_clinic.shape = {df_doctors_by_clinic.shape}")
    else:
        print('skip download ectcm_doctors_by_clinic')
    
    df_clinics_path = output_folder / f'ectcm_clinics_{today_str}.csv'
    df_clinics.to_csv(df_clinics_path, encoding='utf-8-sig', index=False)
    print(f"ectcm clinic data saved to {df_clinics_path}, df_clinics.shape = {df_clinics.shape}")
    
    df_doctors_path = output_folder / f'ectcm_doctors_{today_str}.csv'
    df_doctors.to_csv(df_doctors_path, encoding='utf-8-sig', index=False)
    print(f"ectcm doctor data saved to {df_doctors_path}, df_doctors.shape = {df_doctors.shape}")
    
    end_dt = datetime.datetime.now()
    print(f"finish ectcm download at {end_dt}")

if __name__ == "__main__":
    run()
