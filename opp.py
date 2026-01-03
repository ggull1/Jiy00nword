import streamlit as st
from PIL import Image
import os
import datetime

# 페이지 설정
st.set_page_config(page_title="나만의 상형문자 변환기")
st.title("𓀀 상형문자 변환기")

# 이미지 폴더 경로 (GitHub에 올린 폴더명)
IMAGE_DIR = "alphabet_images"

# 1. 입력 받기
user_input = st.text_input("변환할 단어를 영문으로 입력하세요:", "apple")

if user_input:
    word = user_input.lower()
    images = []
    
    # 2. 이미지 불러오기
    for char in word:
        if char.isalpha():
            img_path = os.path.join(IMAGE_DIR, f"{char}.png")
            if os.path.exists(img_path):
                images.append(Image.open(img_path))
    
    if images:
        # 3. 이미지 합성
        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)
        combined_img = Image.new('RGB', (total_width, max_height), color='white')
        
        x_offset = 0
        for img in images:
            combined_img.paste(img, (x_offset, 0))
            x_offset += img.width
        
        # 4. 화면에 출력
        st.image(combined_img, caption=f"'{user_input}'의 변환 결과")
        
        # 5. 저장하기 (서버 내 'outputs' 폴더에 시간별로 저장)
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"outputs/{user_input}_{timestamp}.png"
        combined_img.save(save_path)
        
        # 다운로드 버튼 제공
        with open(save_path, "rb") as file:
            st.download_button("이미지 다운로드", file, file_name=f"{user_input}.png")
