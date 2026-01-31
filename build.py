import os
import subprocess
import re

def update_and_push():
    script_dir = './script'
    if not os.path.exists(script_dir):
        os.makedirs(script_dir)
        print("'script' 폴더를 생성했습니다. 파일을 넣고 다시 실행하세요.")
        return

    # 1. 파일 목록 분석
    files = [f for f in os.listdir(script_dir) if f.startswith('day') and f.endswith('.txt')]
    files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    # 2. Select Option 생성
    options_html = ""
    for f in files:
        day_num = re.findall(r'\d+', f)[0]
        with open(os.path.join(script_dir, f), 'r', encoding='utf-8') as file:
            first_line = file.readline().strip().replace('🌳', '').split(':')[-1].strip()
        options_html += f'                <option value="{day_num}">Day {day_num}: {first_line}</option>\n'

    # 3. index.html 업데이트
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(
        r'<select id="day-select".*?>.*?</select>',
        f'<select id="day-select" onchange="loadScript(this.value)">\n{options_html}            </select>',
        content, flags=re.DOTALL
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ index.html 메뉴 업데이트 완료!")

    # 4. Git 자동화 (선택 사항: Git 설정이 되어 있을 경우)
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Update: {len(files)} days recorded"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 GitHub Push 성공! Netlify 배포가 시작됩니다.")
    except Exception as e:
        print(f"ℹ️ Git Push는 건너뛰었습니다 (설정 확인 필요): {e}")

if __name__ == "__main__":
    update_and_push()