## 중간중간 저장 + 여러개 api 키를 이용해서 매치 포인트 수집코드
##

import requests
import pandas as pd
import time
import os
from pathlib import Path
from multiprocessing import Pool

# 1. 갖고 있는 수에 맞게api키 적으시면 됩니다
API_KEYS = [
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwYzM2NzQ0MC1kZGE0LTAxM2UtNDhkZC03ZTkxMmRlNThlZGEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzY5NTE0NTIwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6IjI2MDEyNyJ9.wvms9cTOB-d8FjwC4FF7ml21Av-nTmgyftEqARoJh8Y", 
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiYWIyNDM0MC1lODhjLTAxM2UtMmU1OS0zNjkwYjYzZDM1NGYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzcwNzEzOTY4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Indvcms0In0.RLx2wD64znm8JwOa2RtG3JqUfKLi32P4r5W4dgFzr6A", 
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJkZTU0YTUxMC1lOTFlLTAxM2UtZDA5ZS0xMjY0NTY0M2Y0YzQiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzcwNzc2NzM0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Indvcms5In0.1QVUqTq7gMr_nv2afba5QQXQp4GUe0u2CeP5fA-zpfA",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNjJkM2FhMC1lOTFlLTAxM2UtZDBhMC0xMjY0NTY0M2Y0YzQiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzcwNzc2NzQ3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6IndvcmsxMCJ9.czz73Dpjhp_vVQ7uS87AKSG8nHTDE0eRPi3L904_Fh4",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNzcyZDllMC1lODg4LTAxM2UtNWViMC02NjA2MjJjNmQwYmIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzcwNzEyMzI1LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6IndvcmsxIn0.Nx2IFYySqc83Aj2SyyNLuECRMd-_kcYghUN_NlTlvLI", 
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyODEyMzU2MC1lODhkLTAxM2UtMmU1Yy0zNjkwYjYzZDM1NGYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzcwNzE0MTUxLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Indvcms1In0.i3bw5ylY36vqgp5U8SIGscdZXv_5x_38iQz8Fdk8QZM",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2NzNlNDgxMC1lODg5LTAxM2UtNWViMi02NjA2MjJjNmQwYmIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzcwNzEyNTM5LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6IndvcmsyIn0.GxKZXVVcTUSNIn5bjj4iWnGzGSSOwB7Q9OBnx0XhdSg",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0NTIxNDY3MC1lODhkLTAxM2UtMmU1ZS0zNjkwYjYzZDM1NGYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzcwNzE0MjAwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Indvcms2In0.vqerBiiBw22bRVb511Z1wb6_wEPVOj1OMPilurtXr0c",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlYjgxODRiMC1lODg5LTAxM2UtMmU1NC0zNjkwYjYzZDM1NGYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzcwNzEyNzYxLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6IndvcmszIn0.2EDH8zNzoJ_r2gdZ1X4HRkWzUzdhx8UklczyyQQZ6Po",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2NmVhY2I4MC1lODhkLTAxM2UtNWViOS02NjA2MjJjNmQwYmIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzcwNzE0MjU3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Indvcms3In0._tSdHeyrFQsm8gWWCXEx1SM4kLnwzz3EXfbtjLwEIO0"
]

### customizing - change the value
SHARD = "kakao" # 카카오/스팀 설정
SEASON_ID = "division.bro.official.pc-2018-40"
INPUT_FILE =  Path(r"C:\msys64\home\for\10th\00_Project\04_final\day_account\0211_kakao_시형.csv") # 내 파일 이름
OUTPUT_FILE = "0211_kakao_시형_결과.csv"
###


def fetch_data_worker(chunk_info):
    df_subset, api_key, worker_id = chunk_info
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.api+json"
    }
    temp_file = f"temp_worker_{worker_id}.csv"
    
    if os.path.exists(temp_file):
        df_subset = pd.read_csv(temp_file)
        print(f"worker {worker_id}: 기존 파일 로드 완료")
    else:
        df_subset['currentRankPoint'] = None

    print(f"worker {worker_id} 시작 (대상: {len(df_subset)}명)")

    for idx, row in df_subset.iterrows():
        if pd.notna(row['currentRankPoint']):
            continue
            
        p_id = row['playerId']
        p_name = row['name']
        url = f"https://api.pubg.com/shards/{SHARD}/players/{p_id}/seasons/{SEASON_ID}/ranked"
        
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                stats = data['data']['attributes']['rankedGameModeStats']
                rp = stats.get('squad', {}).get('currentRankPoint', 0)
                df_subset.at[idx, 'currentRankPoint'] = rp
                print(f"[worker {worker_id}] {idx+1}/{len(df_subset)} | {p_name}: {rp} RP")
            elif res.status_code == 429:
                print(f"worker {worker_id}: RPM 초과 10초 대기")
                time.sleep(10)
                continue
            else:
                df_subset.at[idx, 'currentRankPoint'] = 0
                print(f"[worker {worker_id}] {p_name}: 데이터 없음(0)")
        except:
            df_subset.at[idx, 'currentRankPoint'] = 0
            
        if (idx + 1) % 10 == 0:
            df_subset.to_csv(temp_file, index=False, encoding='utf-8-sig')
        
        time.sleep(6.1)

    df_subset.to_csv(temp_file, index=False, encoding='utf-8-sig')
    return df_subset

if __name__ == "__main__":
    full_df = pd.read_csv(INPUT_FILE)
    num_keys = len(API_KEYS)
    
    chunks = []
    chunk_size = len(full_df) // num_keys
    for i in range(num_keys):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_keys - 1 else len(full_df)
        chunks.append((full_df.iloc[start:end].copy(), API_KEYS[i], i))

    print(f"총 {num_keys}개의 키로 병렬 수집 시작")

    with Pool(num_keys) as p:
        final_dfs = p.map(fetch_data_worker, chunks)
    
    final_result = pd.concat(final_dfs)
    final_result.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"최종 수집 완료: {OUTPUT_FILE}")