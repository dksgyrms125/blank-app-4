import streamlit as st
from statistics import mean, median, multimode

st.title("xx중학교 급식 만족도 조사")

# 고정 데이터: 1~10 사이 일반값 18개(중복 포함) + 100 이상 이상치 2개
# 7이 단일 최빈값이 되도록 빈도 조정
survey_scores = [3, 5, 7, 8, 7, 4, 9, 7, 5, 8, 6, 2, 10, 7, 5, 9, 4, 6, 112, 137]

st.subheader("원본 데이터")
student_labels = [
	"민준", "서준", "지후", "도윤", "하준",
	"예은", "서연", "지민", "수아", "채원",
	"지호", "유찬", "서진", "현우", "건우",
	"민서", "다은", "하린", "지아", "서율",
]

if "is_sorted_answer_correct" not in st.session_state:
	st.session_state.is_sorted_answer_correct = False

if "has_viewed_stats" not in st.session_state:
	st.session_state.has_viewed_stats = False

if "removed_outlier_indices" not in st.session_state:
	st.session_state.removed_outlier_indices = set()

if "outlier_feedback" not in st.session_state:
	st.session_state.outlier_feedback = ""

can_play_outlier = st.session_state.is_sorted_answer_correct and st.session_state.has_viewed_stats

if not can_play_outlier:
	st.warning("오름차순 정답 확인 후 통계값까지 확인해야 자료값 버튼을 누를 수 있습니다.")

items_per_row = 5
visible_indices = [
	i for i in range(len(survey_scores))
	if i not in st.session_state.removed_outlier_indices
]
remaining_scores = [survey_scores[i] for i in visible_indices]

for row_start in range(0, len(visible_indices), items_per_row):
	cols = st.columns(items_per_row)
	for col_idx, data_idx in enumerate(visible_indices[row_start:row_start + items_per_row]):
		name = student_labels[data_idx]
		score = survey_scores[data_idx]
		if cols[col_idx].button(
			f"{name}: {score}",
			key=f"score_btn_{data_idx}",
			disabled=not can_play_outlier,
		):
			if score >= 100:
				st.session_state.removed_outlier_indices.add(data_idx)
				removed_count = len(st.session_state.removed_outlier_indices)
				if removed_count == 2:
					st.session_state.outlier_feedback = "정답입니다! 이상치 2개를 모두 찾았습니다."
				else:
					st.session_state.outlier_feedback = "이상치 1개를 찾았습니다. 나머지 1개를 찾아보세요."
			else:
				st.session_state.outlier_feedback = "선택한 값은 이상치가 아닙니다. 다시 시도해 보세요."

if st.session_state.outlier_feedback:
	if len(st.session_state.removed_outlier_indices) == 2:
		st.success(st.session_state.outlier_feedback)
	else:
		st.info(st.session_state.outlier_feedback)

if len(st.session_state.removed_outlier_indices) == 2:
	st.caption("이상치 2개(112, 137)가 제거되었습니다.")

st.subheader("오름차순 정렬 연습")
sorted_scores = sorted(survey_scores)

user_input = st.text_area(
	"작은 수부터 큰 수까지 순서대로 입력하세요 (쉼표 또는 공백으로 구분)",
	placeholder="예: 2, 3, 4, 4, 5, ...",
)

if st.button("정답 확인"):
	try:
		tokens = user_input.replace(",", " ").split()
		user_values = [int(token) for token in tokens]

		if len(user_values) != len(sorted_scores):
			st.session_state.is_sorted_answer_correct = False
			st.session_state.has_viewed_stats = False
			st.error(f"총 {len(sorted_scores)}개 값을 입력해야 합니다. 현재 {len(user_values)}개를 입력했습니다.")
		elif user_values == sorted_scores:
			st.session_state.is_sorted_answer_correct = True
			st.success("정답입니다! 자료값을 오름차순으로 정확하게 입력했습니다.")
		else:
			st.session_state.is_sorted_answer_correct = False
			st.session_state.has_viewed_stats = False
			st.error("아직 정답이 아닙니다. 값 또는 순서를 다시 확인해 보세요.")
	except ValueError:
		st.session_state.is_sorted_answer_correct = False
		st.session_state.has_viewed_stats = False
		st.error("숫자만 입력해 주세요. 구분자는 쉼표(,) 또는 공백만 사용할 수 있습니다.")

if st.button("평균, 중앙값, 최빈값 보기", disabled=not st.session_state.is_sorted_answer_correct):
	st.session_state.has_viewed_stats = True
	if remaining_scores:
		avg_score = mean(remaining_scores)
		median_score = median(remaining_scores)
		mode_scores = multimode(remaining_scores)
		col1, col2, col3 = st.columns(3)
		col1.metric("평균", f"{avg_score:.2f}")
		col2.metric("중앙값", f"{median_score:.2f}")
		col3.metric("최빈값", ", ".join(str(v) for v in mode_scores))
		st.caption("최빈값은 동률일 경우 여러 개가 표시됩니다.")
	else:
		st.error("남아있는 자료값이 없어 통계를 계산할 수 없습니다.")
else:
	if st.session_state.is_sorted_answer_correct:
		st.info("버튼을 눌러 통계값을 확인하세요.")
	else:
		st.warning("오름차순 정렬을 정답으로 맞춰야 통계 버튼이 활성화됩니다.")
