import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="연기 연습 프로그램", page_icon="🎭")

# 25가지 감정
emotions = [
    "기쁨", "슬픔", "화남", "경악", "공포", "혐오", "놀람", "기대", 
    "질투", "부끄러움", "당당함", "우울", "짜증", "설렘", "지루함", 
    "불안", "환희", "허탈", "안도", "죄책감", "동정", "경멸", 
    "억울함", "비장함", "혼란"
]

# 25가지 대사
dialogues = [
    "정말 이게 최선이라고 생각해?", "난 이제 더 이상 못 참겠어!", "잠깐, 내 말 좀 끝까지 들어봐.",
    "어떻게 나한테 이럴 수가 있어?", "내일은 다를 거라고 믿을게.", "왜 자꾸 나를 피하는 거야?",
    "네가 알아서 할 일이라고 했잖아.", "이런 결과가 나올 줄은 꿈에도 몰랐어.", "지금 장난하는 거 아니지?",
    "다시는 내 앞에 나타나지 마.", "내가 미안해, 다 내 잘못이야.", "정말 고마워, 평생 잊지 않을게.",
    "우리 예전으로 다시 돌아갈 순 없을까?", "도대체 무슨 생각을 하고 있는 거야?", "그만해! 더는 듣고 싶지 않아.",
    "이번엔 무슨 일이 있어도 포기하지 않을 거야.", "나한테 왜 그렇게 차갑게 구는 건데?", "이게 다 널 위해서 그러는 거야.",
    "솔직히 말해서 네가 좀 실망스러워.", "우리가 함께라면 뭐든 이겨낼 수 있어.", "아무것도 묻지 말고 그냥 안아줘.",
    "너 없이 난 아무것도 아니야.", "결국엔 이렇게 끝나는구나.", "제발 나에게 한 번만 더 기회를 줘.",
    "이제 와서 후회해도 아무 소용없어."
]

# 5가지 체크리스트 (스스로 평가)
evaluations = [
    "1. 감정에 맞는 표정을 자연스럽게 지었는가?",
    "2. 대사의 전달력이 좋았는가? (발음, 성량, 억양)",
    "3. 감정에 맞는 몸짓과 제스처를 사용했는가?",
    "4. 감정의 디테일과 깊이가 잘 표현되었는가?",
    "5. 내 연기에 스스로 100% 몰입했는가?"
]

# 세션 상태 초기화 (게임 데이터 유지용)
if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.lacking_counts = {item: 0 for item in evaluations}
    st.session_state.current_emotion = random.choice(emotions)
    st.session_state.current_dialogue = random.choice(dialogues)
    st.session_state.game_over = False
    st.session_state.history = [] # 이전 상태 저장을 위한 리스트

# 다음 라운드로 넘어가는 함수
def next_round():
    # 1. 점수 계산 전, 현재 상태를 history에 저장 (되돌리기용)
    current_state = {
        "emotion": st.session_state.current_emotion,
        "dialogue": st.session_state.current_dialogue,
        "score": st.session_state.score,
        "lacking_counts": st.session_state.lacking_counts.copy()
    }
    st.session_state.history.append(current_state)

    # 2. 현재 라운드의 점수 및 부족한 점 계산
    for i, item in enumerate(evaluations):
        checked = st.session_state.get(f"check_{i}_{st.session_state.round}", False)
        if checked:
            st.session_state.score += 1
        else:
            st.session_state.lacking_counts[item] += 1
    
    # 3. 라운드 증가
    st.session_state.round += 1
    
    # 4. 10라운드 종료 여부 체크
    if st.session_state.round > 10:
        st.session_state.game_over = True
    else:
        st.session_state.current_emotion = random.choice(emotions)
        st.session_state.current_dialogue = random.choice(dialogues)

# 이전 라운드로 돌아가는 함수
def go_back():
    if st.session_state.history:
        # 가장 최근의 이전 기록을 꺼내서 상태 복구
        last_state = st.session_state.history.pop()
        st.session_state.current_emotion = last_state["emotion"]
        st.session_state.current_dialogue = last_state["dialogue"]
        st.session_state.score = last_state["score"]
        st.session_state.lacking_counts = last_state["lacking_counts"]
        st.session_state.round -= 1
        st.session_state.game_over = False

# --- UI 시작 ---
st.title("🎬 10라운드 실전 연기 트레이닝")

if not st.session_state.game_over:
    st.subheader(f"현재 라운드: {st.session_state.round} / 10")
    st.progress(st.session_state.round / 10)
    st.markdown("---")
    
    # 감정과 대사 출력
    st.markdown("### 🎭 표현해야 할 감정")
    st.info(f"**{st.session_state.current_emotion}**")
    
    st.markdown("### 💬 연기할 대사")
    st.success(f"**\"{st.session_state.current_dialogue}\"**")
    
    st.markdown("---")
    st.markdown("### ✅ 스스로 평가하기 (체크 하나당 1점)")
    
    # 5가지 체크박스 생성
    for i, item in enumerate(evaluations):
        st.checkbox(item, key=f"check_{i}_{st.session_state.round}")
        
    st.write("") # 여백
    
    # 버튼 배치 (가로로 2개 배치)
    col1, col2 = st.columns(2)
    
    with col1:
        # 1라운드에서는 이전 버튼을 숨기거나 비활성화
        if st.session_state.round > 1:
            st.button("⬅️ 이전 대사로", on_click=go_back, use_container_width=True)
            
    with col2:
        st.button("다음으로 넘어가기 ➡️", on_click=next_round, use_container_width=True)

else:
    # --- 게임 종료 화면 ---
    st.balloons()
    
    # 화면 흔들림 애니메이션 CSS 적용
    shake_css = """
    <style>
    @keyframes shake {
      0% { transform: translate(1px, 1px) rotate(0deg); }
      10% { transform: translate(-2px, -3px) rotate(-1deg); }
      20% { transform: translate(-4px, 0px) rotate(2deg); }
      30% { transform: translate(4px, 3px) rotate(0deg); }
      40% { transform: translate(2px, -2px) rotate(2deg); }
      50% { transform: translate(-2px, 3px) rotate(-1deg); }
      60% { transform: translate(-4px, 2px) rotate(0deg); }
      70% { transform: translate(4px, 2px) rotate(-2deg); }
      80% { transform: translate(-2px, -2px) rotate(2deg); }
      90% { transform: translate(2px, 3px) rotate(0deg); }
      100% { transform: translate(2px, -3px) rotate(-1deg); }
    }
    .stApp {
      animation: shake 0.6s cubic-bezier(.36,.07,.19,.97) both;
      animation-iteration-count: 3;
    }
    </style>
    """
    st.markdown(shake_css, unsafe_allow_html=True)
    
    # 결과 출력
    st.markdown("## 🎉 연기 훈련 완료! 🎉")
    st.markdown(f"### 🏆 당신의 최종 점수: **{st.session_state.score} / 50 점**")
    st.markdown("---")
    
    st.markdown("### 💡 나의 연기 피드백 (많이 놓친 항목)")
    st.write("체크를 적게 한 항목일수록 다음 연습 때 더 신경 써야 합니다.")
    
    # 놓친 횟수가 많은 순서대로 정렬
    sorted_lacking = sorted(st.session_state.lacking_counts.items(), key=lambda x: x[1], reverse=True)
    
    max_misses = sorted_lacking[0][1]
    if max_misses == 0:
        st.success("완벽합니다! 모든 라운드에서 모든 평가 항목을 만족하셨습니다. 👏")
    else:
        for item, count in sorted_lacking:
            if count > 0:
                st.warning(f"**{item}** (총 {count}번 부족함)")
    
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>🎆🎇🎉🎈🎊</h1>", unsafe_allow_html=True)
    
    st.write("")
    if st.button("처음부터 다시 연습하기 🔄", use_container_width=True):
        st.session_state.clear()
        st.rerun()