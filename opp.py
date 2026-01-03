import streamlit as st
from PIL import Image
import os
import datetime

# 1. 페이지 설정 (브라우저 탭 이름과 아이콘)
st.set_page_config(page_title="Jiy00n word", page_icon="", layout="centered")

# 2. CSS를 이용한 스타일 꾸미기 (글자 크기, 배경 등)
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTitle {
        color: #4a3728;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
    }
    .stSubheader {
        color: #6b4f3a;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Jiy00n word transfer site")
st.subheader("words")

# 이미지 폴더 경로
IMAGE_DIR = "alphabet_images"

# 3. 입력창 디자인
user_input = st.text_input("Type words", placeholder="what?")

if user_input:
    word = user_input.lower()
    images = []
    
    # 이미지 불러오기 루프
    for char in word:
        if char.isalpha():
            img_path = os.path.join(IMAGE_DIR, f"{char}.jpg")
            if os.path.exists(img_path):
                images.append(Image.open(img_path))
    
    if images:
        # 4. 이미지 합성
        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)
        combined_img = Image.new('RGB', (total_width, max_height), color='white')
        
        x_offset = 0
        for img in images:
            combined_img.paste(img, (x_offset, 0))
            x_offset += img.width
        
        # 5. 결과 출력 섹션
        st.write("---")
        st.success(f"'{user_input}' success")
        
        # 이미지를 화면 중앙에 배치
        st.image(combined_img, use_container_width=True)
        
        # 6. 저장 안내 및 버튼
        col1, col2 = st.columns(2)
        with col1:
            st.info("Save to click.")
        with col2:
            # 임시 저장 후 다운로드 버튼 생성
            combined_img.save("result.png")
            with open("result.png", "rb") as file:
                st.download_button(
                    label="download",
                    data=file,
                    file_name=f"{user_input}_Jword.png",
                    mime="image/png"
                )
    else:
        st.warning("Cannot find image")

# 7. 푸터(하단 설명)
st.write("---")
st.caption("© 2026 Cave of Jiy00n word site | Jiyoon Park")
