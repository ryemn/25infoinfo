import streamlit as st
import random
import time

# --- 게임 초기화 및 상태 관리 함수 ---
def init_game_state():
    """게임 초기 상태를 설정하거나 재설정합니다."""
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_char' not in st.session_state:
        st.session_state.current_char = ""
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False # 게임 시작 전
    if 'display_char' not in st.session_state:
        st.session_state.display_char = False # 글자 표시 여부
    if 'input_enabled' not in st.session_state:
        st.session_state.input_enabled = False # 사용자 입력 활성화 여부
    if 'message' not in st.session_state:
        st.session_state.message = "" # 사용자에게 보여줄 메시지
    if 'start_display_time' not in st.session_state:
        st.session_state.start_display_time = 0.0 # 글자가 표시되기 시작한 시간
    if 'last_char_generated_time' not in st.session_state:
        st.session_state.last_char_generated_time = 0.0 # 마지막 글자 생성 시간
    if 'user_guess_value' not in st.session_state: # 사용자의 마지막 입력 값 저장
        st.session_state.user_guess_value = ""


def generate_random_char():
    """랜덤 한글 자음/모음 또는 알파벳을 생성합니다."""
    char_type = random.choice(['korean', 'english'])
    if char_type == 'korean':
        korean_chars = [
            'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅍ', 'ㅌ', 'ㅃ', 'ㅉ', 'ㄸ', 'ㄲ', 'ㅆ',
            'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', 'ㅘ', 'ㅝ'
        ]
        return random.choice(korean_chars)
    else:
        return random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

def start_new_round():
    """새로운 게임 라운드를 시작합니다."""
    st.session_state.current_char = generate_random_char()
    st.session_state.display_char = True
    st.session_state.game_active = True
    st.session_state.input_enabled = False # 글자가 보일 때는 입력 비활성화
    st.session_state.message = ""
    st.session_state.start_display_time = time.time()
    st.session_state.last_char_generated_time = time.time() # 글자 생성 시간 기록
    st.session_state.user_guess_value = "" # 새 라운드 시작 시 입력값 초기화

# --- Streamlit 앱 시작 ---
init_game_state()

st.title("순간 포착! 글자 맞추기 게임 🚀")
st.markdown("눈 깜짝할 사이에 지나가는 글자를 맞춰보세요!")

# --- 사이드바 설정 ---
st.sidebar.header("게임 설정")
st.sidebar.markdown("---")
# 난이도 조절 슬라이더 (0.1초 ~ 1.0초)
display_duration = st.sidebar.slider(
    "**글자 노출 시간 (초)**",
    0.1, 1.0, 0.2, 0.05,
    help="글자가 화면에 나타나는 시간을 조절합니다. 숫자가 낮을수록 어려워집니다."
)
st.sidebar.markdown("---")
st.sidebar.write(f"현재 점수: **{st.session_state.score}점**")

# --- 게임 시작 버튼 ---
# 게임이 비활성 상태일 때만 '게임 시작' 버튼 표시
if not st.session_state.game_active and not st.session_state.display_char and not st.session_state.input_enabled:
    if st.button("게임 시작"):
        st.session_state.score = 0 # 새 게임 시작 시 점수 초기화
        start_new_round()
        st.rerun() # 라운드 시작 후 바로 렌더링

# --- 게임 진행 로직 ---
if st.session_state.game_active or st.session_state.display_char or st.session_state.input_enabled:
    placeholder = st.empty() # 동적 콘텐츠를 위한 플레이스홀더

    with placeholder.container():
        # 1. 글자 표시 단계
        if st.session_state.display_char:
            st.markdown(
                f"<h1 style='text-align: center; font-size: 150px; color: #ff4b4b;'>{st.session_state.current_char}</h1>",
                unsafe_allow_html=True
            )
            # 글자가 보인 후 설정된 시간 뒤에 사라지게 함
            if time.time() - st.session_state.start_display_time > display_duration:
                st.session_state.display_char = False
                st.session_state.input_enabled = True # 입력 활성화
                st.rerun() # 글자를 사라지게 하고 입력 필드를 보여주기 위해 다시 렌더링
            else:
                # 글자가 보이는 동안 계속 다시 렌더링하여 시간을 확인
                time.sleep(0.01) # CPU 부하를 줄이기 위한 짧은 대기
                st.rerun() # 계속해서 시간을 확인하고 다시 렌더링
        # 2. 글자 사라짐 및 입력 대기 단계
        else:
            st.markdown(f"<h1 style='text-align: center; font-size: 150px;'>❓</h1>", unsafe_allow_html=True)

        # 입력 필드는 항상 존재하도록 만듦 (visibility만 제어)
        user_input = st.text_input(
            "무엇이었을까요?",
            key="user_guess",
            max_chars=1, # 한 글자만 입력받음
            disabled=not st.session_state.input_enabled, # input_enabled 상태에 따라 활성화/비활성화
            placeholder="여기에 글자를 입력하세요...",
            value=st.session_state.user_guess_value # 세션 상태 값으로 제어
        )

        # 사용자 입력이 있고, 입력이 활성화된 상태에서만 정답 확인
        if st.session_state.input_enabled and user_input and user_input != st.session_state.user_guess_value:
            st.session_state.user_guess_value = user_input # 사용자의 현재 입력 저장

            if user_input.lower() == st.session_state.current_char.lower():
                st.session_state.message = f"🎉 **정답입니다!** 다음 글자로 넘어갑니다."
                st.session_state.score += 1
            else:
                st.session_state.message = f"❌ **틀렸습니다.** 정답은 **'{st.session_state.current_char}'** 이었습니다."

            st.session_state.game_active = False # 현재 라운드 종료
            st.session_state.input_enabled = False # 입력 비활성화 (새 라운드 시작 전까지)
            st.rerun() # 메시지를 표시하고 다음 라운드 버튼을 보여주기 위해 다시 렌더링

    # --- 라운드 결과 메시지 표시 ---
    if st.session_state.message:
        st.success(st.session_state.message)

    # --- 다음 라운드 또는 게임 재시작 버튼 ---
    # 글자가 표시되지 않고, 입력도 비활성화된 상태 (정답 확인 후)
    if not st.session_state.display_char and not st.session_state.input_enabled and not st.session_state.game_active:
        if st.button("다음 라운드 시작"):
            start_new_round()
            st.rerun() # 새 라운드 시작 후 바로 렌더링

    # 사용자가 아직 입력하지 않았고 글자가 사라진 상태에서 대기 중일 때
    elif not st.session_state.display_char and st.session_state.input_enabled:
        st.info("글자를 입력해주세요.")
