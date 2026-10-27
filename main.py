import urllib.request
import urllib.parse
import json
import nltk
from nltk.corpus import wordnet

# NLTK 데이터 자동 다운로드 (최초 1회만 다운로드됨)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

def check_grammar_api(text):
    """자바 설치 없이 무료 오픈 API로 문법 검사하는 함수"""
    url = "https://api.languagetool.org/v2/check"
    data = urllib.parse.urlencode({'text': text, 'language': 'en-US'}).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('matches', [])
    except Exception as e:
        print(f"[경고] 문법 검사 API 호출 실패: {e}")
        return []

def analyze_sentence():
    print("=" * 60)
    print(" 📝 터미널 기반 문장 분석기 (문법 & 단어 뜻)")
    print("=" * 60)
    
    while True:
        text_input = input("\n분석할 영어 문장을 입력하세요 (종료하려면 'q' 입력): ").strip()
        
        if text_input.lower() == 'q':
            print("프로그램을 종료합니다.")
            break
            
        if not text_input:
            print("문장을 입력해주세요.")
            continue
            
        # 1. 문법 검사
        print("\n[🔍 문법 교정 결과]")
        matches = check_grammar_api(text_input)
        
        if not matches:
            print("✅ 발견된 문법 오류가 없습니다.")
        else:
            print(f"⚠️ 총 {len(matches)}개의 개선점이 발견되었습니다:")
            for idx, match in enumerate(matches, 1):
                offset = match['offset']
                length = match['length']
                error_word = text_input[offset:offset+length]
                message = match['message']
                replacements = [r['value'] for r in match.get('replacements', [])[:3]]
                
                print(f"  {idx}. 오류 단어: '{error_word}'")
                print(f"     설명: {message}")
                if replacements:
                    print(f"     추천 수정: {', '.join(replacements)}")

        # 2. 단어 뜻 풀이
        print("\n[📚 주요 단어 사전 (영영)]")
        tokens = nltk.word_tokenize(text_input)
        words = sorted(list(set([w.lower() for w in tokens if w.isalpha()])))
        
        pos_map = {'n': '명사', 'v': '동사', 'a': '형용사', 'r': '부사'}
        
        for word in words:
            synsets = wordnet.synsets(word)
            if synsets:
                syn = synsets[0]
                pos = pos_map.get(syn.pos(), syn.pos())
                definition = syn.definition()
                print(f"• {word} [{pos}]: {definition}")
                
                examples = syn.examples()
                if examples:
                    print(f"  └ 예문: \"{examples[0]}\"")
            else:
                print(f"• {word}: 사전 뜻을 찾을 수 없습니다.")

if __name__ == "__main__":
    analyze_sentence()
