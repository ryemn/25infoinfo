import streamlit as st
import random
import time

def generate_random_char():
    """랜덤 한글 자음/모음 또는 알파벳을 생성합니다."""
    char_type = random.choice(['korean', 'english'])
    if char_type == 'korean':
        # 자주 사용되는 한글 자음 (ㄱ~ㅎ)과 모음 (ㅏ~ㅣ) 범위
        # 모든 한글 문자를 커버하기에는 복잡하므로, 대표적인 자모음 위주로 선택
        korean_chars = [
            'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅍ', 'ㅌ', 'ㅃ', 'ㅉ', 'ㄸ', 'ㄲ', 'ㅆ',
            'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', 'ㅘ', 'ㅝ'
        ]
        return random.choice(korean_chars)
    else:
        return random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

def game_start():
    st.session_state.current_char = generate_random_char()
    st.session_state.display_char = True
    st.session_state.game_active = True
    st.session_state.input_enabled = False # 글자가 보일 때는 입력 비활성화
    st.session_state.message = ""
    st.session_state.start_display_time = time.time()

def init_game_state():
    """게임 초기 상태를 설정합니다."""
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_char' not in st.session_state:
        st.session_state.current_char = ""
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'display_char' not in st.session_state:
        st.session_state.display_char = False
    if 'input_enabled' not in st.session_state:
        st.session_state.input_enabled = False
    if 'message' not in st.session_state:
        st.session_state.message = ""
    if 'start_display_time' not in st.session_state:
        st.session_state.start_display_time = 0.0

init_game_state()

st.title("순간 포착! 글자 맞추기 게임 🚀")
st.markdown("눈 깜짝할 사이에 지나가는 글자를 맞춰보세요!")

st.sidebar.header("게임 설정")
display_duration = st.sidebar.slider("글자 노출 시간 (초)", 0.1, 1.0, 0.2, 0.05)

if st.session_state.game_active:
    st.write(f"현재 점수: {st.session_state.score}점")

    placeholder = st.empty()

    if st.session_state.display_char:
        with placeholder.container():
            st.markdown(f"<h1 style='text-align: center; font-size: 150px; color: #ff4b4b;'>{st.session_state.current_char}</h1>", unsafe_allow_html=True)
            # 글자가 보인 후 일정 시간 뒤에 사라지게 함
            if time.time() - st.session_state.start_display_time > display_duration:
                st.session_state.display_char = False
                st.session_state.input_enabled = True
                st.experimental_rerun() # 글자를 사라지게 하기 위해 다시 렌더링
            else:
                # 글자가 보이는 동안에는 잠시 대기
                time.sleep(0.01) # 짧게 대기하여 CPU 부하를 줄임
                st.experimental_rerun() # 계속해서 시간을 확인하고 다시 렌더링
    else:
        with placeholder.container():
            st.markdown(f"<h1 style='text-align: center; font-size: 150px;'>❓</h1>", unsafe_allow_html=True)
            if st.session_state.input_enabled:
                user_input = st.text_input("무엇이었을까요?", key="user_guess", max_chars=1, disabled=not st.session_state.input_enabled)
                if user_input:
                    if user_input.lower() == st.session_state.current_char.lower():
                        st.session_state.message = f"🎉 정답입니다! 다음 글자로 넘어갑니다."
                        st.session_state.score += 1
                    else:
                        st.session_state.message = f"❌ 틀렸습니다. 정답은 '{st.session_state.current_char}' 이었습니다."
                    st.session_state.game_active = False # 정답 확인 후 게임 비활성화
                    st.session_state.input_enabled = False # 입력 비활성화
                    st.experimental_rerun() # 메시지를 표시하고 게임 재시작 버튼을 보여주기 위해 다시 렌더링

    if st.session_state.message:
        st.success(st.session_state.message)

    if not st.session_state.display_char and not st.session_state.input_enabled and st.session_state.game_active:
        st.info("글자가 나타날 때까지 기다려주세요...")

    if not st.session_state.game_active and not st.session_state.input_enabled:
        if st.button("다음 라운드 시작 / 다시 시작"):
            game_start()
            st.session_state.message = "" # 메시지 초기화
            st.experimental_rerun() # 새 라운드 시작

else:
    if st.button("게임 시작"):
        st.session_state.score = 0 # 새 게임 시작 시 점수 초기화
        game_start()
        st.experimental_rerun()
