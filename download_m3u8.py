import subprocess
import re
from tqdm import tqdm

def get_real_url(url):
    # 실제 HLS 스트림 URL 추출
    match = re.search(r"url=(http[s]?://.+)", url)
    if match:
        return match.group(1)
    return None

def download_video():
    # 사용자로부터 URL과 파일 이름을 입력받습니다.
    url = input("다운로드할 동영상의 URL을 입력하세요: ")
    file_name = input("저장할 파일의 이름을 입력하세요 (확장자 제외): ")

    # 원본 HLS 스트림 URL 추출
    real_url = get_real_url(url)
    if not real_url:
        print("올바른 HLS 스트림 URL을 입력하세요.")
        return

    # 다운로드 경로 설정
    download_path = f"/Users/imsang-yeob/Downloads/{file_name}.mp4"

    # FFmpeg 명령어 생성
    command = [
        "ffmpeg",
        "-i", real_url,
        "-c", "copy",
        download_path
    ]

    # FFmpeg 명령어 실행 및 진행 상황 표시
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    total_duration = None
    pbar = None

    for line in process.stderr:
        if "Duration" in line:
            match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", line)
            if match:
                hours, minutes, seconds = map(float, match.groups())
                total_duration = int(hours * 3600 + minutes * 60 + seconds)
                pbar = tqdm(total=total_duration, unit="s", unit_scale=True, desc="다운로드 진행 상황")
        
        if total_duration and "time=" in line:
            match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
            if match:
                hours, minutes, seconds = map(float, match.groups())
                elapsed_time = int(hours * 3600 + minutes * 60 + seconds)
                pbar.update(elapsed_time - pbar.n)

    if pbar:
        pbar.close()

    process.wait()
    if process.returncode == 0:
        print(f"동영상이 {download_path}에 저장되었습니다.")
    else:
        print("동영상을 다운로드하는 동안 오류가 발생했습니다.")
        print(process.stderr.read())

if __name__ == "__main__":
    download_video()
