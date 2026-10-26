import streamlit as st
import language_tool_python
import nltk
from nltk.corpus import wordnet

# NLTK 데이터 다운로드 (최초 1회 실행)
@st.cache_resource
def download_nltk_data():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

download_nltk_data()

# LanguageTool 로더 (캐싱으로 속도 최적화)
@st.cache_resource
def load_tool(lang='en-US'):
    return language_tool_python.LanguageTool(lang)

st.set_page_config(page_title="문법 & 단어 분석기", page_icon="📝", layout="wide")

st.title("📝 문장 분석기 (문법 검사 & 단어 사전)")
st.write("영어 문장을 입력하면 **문법 오류 수정**과 **주요 단어의 뜻**을 알려드립니다.")

# 입력 폼
text_input = st.text_area("분석할 영어 문장을 입력하세요:", height=120, placeholder="예: She go to the school yesterday and buy a apple.")

if st.button("분석 시작", type="primary"):
    if not text_input.strip():
        st.warning("문장을 입력해주세요.")
    else:
        col1, col2 = st.columns(2)
        
        # 1. 문법 검사 기능
        with col1:
            st.subheader("🔍 문법 교정")
            tool = load_tool('en-US')
            matches = tool.check(text_input)
            
            corrected_text = language_tool_python.utils.correct(text_input, matches)
            
            if len(matches) == 0:
                st.success("🎉 문법 오류가 발견되지 않았습니다!")
            else:
                st.error(f"총 {len(matches)}개의 문법 개선점 발견:")
                st.write("**교정된 문장:**")
                st.info(corrected_text)
                
                st.write("**세부 수정사항:**")
                for match in matches:
                    with st.expander(f"❌ {match.message}"):
                        st.write(f"- **오류 부분:** `{text_input[match.offset:match.offset+match.errorLength]}`")
                        if match.replacements:
                            st.write(f"- **추천 수정:** `{', '.join(match.replacements[:3])}`")

        # 2. 단어 사전 기능
        with col2:
            st.subheader("📚 주요 단어 뜻 풀이")
            tokens = nltk.word_tokenize(text_input)
            # 알파벳 단어만 추출 (소문자화 및 중복 제거)
            words = sorted(list(set([word.lower() for word in tokens if word.isalpha()])))
            
            if not words:
                st.info("분석할 단어가 없습니다.")
            else:
                for word in words:
                    synsets = wordnet.synsets(word)
                    with st.expander(f"📌 **{word}**"):
                        if synsets:
                            # 첫 번째 대표 의미 추출
                            definition = synsets[0].definition()
                            pos = synsets[0].pos()
                            
                            # 품사 표기 전환
                            pos_dict = {'n': '명사', 'v': '동사', 'a': '형용사', 'r': '부사'}
                            pos_str = pos_dict.get(pos, pos)
                            
                            st.write(f"**품사:** {pos_str}")
                            st.write(f"**뜻 (영영):** {definition}")
                            
                            # 예문이 있는 경우 표시
                            examples = synsets[0].examples()
                            if examples:
                                st.write(f"**예문:** *\"{examples[0]}\"*")
                        else:
                            st.write("사전 정의를 찾을 수 없습니다.")
