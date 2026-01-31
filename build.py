import os
import subprocess

def update_and_push():
    # 1. script 폴더 내의 dayX.txt 파일들 찾기
    script_dir = './script'
    if not os.path.exists(script_dir):
        print("Error: 'script' 폴더가 없습니다.")
        return

    files = [f for f in os.listdir(script_dir) if f.startswith('day') and f.endswith('.txt')]
    # 숫자 순서대로 정렬 (day1, day2, day10...)
    files.sort(key=lambda x: int(x.replace('day', '').replace('.txt', '')))

    # 2. index.html의 select 옵션 부분 생성
    options_html = ""
    for f in files:
        day_num = f.replace('day', '').replace('.txt', '')
        # 파일 첫 줄에서 테마 이름 가져오기 (예: "Parks")
        with open(os.path.join(script_dir, f), 'r', encoding='utf-8') as file:
            first_line = file.readline().strip().replace('🌳', '').split(':')[-1].strip()
        
        options_html += f'            <option value="{day_num}">Day {day_num}: {first_line}</option>\n'

    # 3. index.html 읽어서 내용 교체
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # <select> 태그 사이의 내용을 교체 (간단한 문자열 치환 방식)
    import re
    new_content = re.sub(
        r'<select id="day-select".*?>.*?</select>',
        f'<select id="day-select" onchange="loadScript(this.value)">\n{options_html}        </select>',
        content,
        flags=re.DOTALL
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ index.html 업데이트 완료!")

    # 4. Git Push 자동화
    try:
        subprocess.run(["git", "add", "."], check=True)
        # 커밋 메시지에 추가된 날짜 정보 포함
        commit_msg = f"Add/Update scripts: Total {len(files)} days"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 Git Push 성공! 잠시 후 Netlify에 반영됩니다.")
    except Exception as e:
        print(f"❌ Git 작업 중 오류 발생: {e}")

if __name__ == "__main__":
    update_and_push()