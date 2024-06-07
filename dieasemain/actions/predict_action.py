from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import os
from flask import Flask, Blueprint, url_for, render_template, current_app, session, g, request, jsonify

app = Flask(__name__)
bp = Blueprint('predictAct', __name__, url_prefix='/')

l1 = ['가려움', '피부발진', '결절성 피부 발진', '지속적인 재채기', '몸이 떨림', '오한', '관절 통증', '복통', '속쓰림', '혀 궤양', '근육 감소', '구토',
      '소변 배출시 화끈거림',
      '혈뇨', '피로', '체중증가', '불안감', '수족냉증', '심한감정기복', '체중감소', '안절부절못함', '무기력', '목에 반점', '불규칙한 혈당', '기침', '고열', '쑥 들어간 눈',
      '숨이 참', '발한', '탈수', '소화불량', '두통', '황갈색 피부', '어두운 소변', '메스꺼움', '식욕부진', '눈 뒤쪽 통증', '요통', '변비', '상복부 통증', '설사',
      '미열',
      '노란색 소변', '황달 눈', '급성간부전', '체액과다', '복부 부종', '림부절 비대', '불쾌감', '시야흐림', '가래', '인후통', '충혈', '부비동염', '콧물',
      '혈관 용종',
      '가슴통증', '팔다리 근력부족', '심박수 증가', '배변 통증', '항문 통증', '혈변', '목 통증', '어지럼증', '생리통', '상처', '비만', '혈관 붓기',
      "손톱 부러짐,갈라짐",
      '손발 붓기', '과도한 허기짐', '성관계', '입술건조', '어눌한 말투', '무릎 통증', '고관절 통증', '근력저하', '담 걸린 목', '관절 부종', '신체의 긴장', '회전운동',
      '균형상실', '불안정함', '한쪽 뇌의 이상', '후각 장애', '방광 불쾌감', '소변악취', '요실금', '방귀 악취', '내부 가려움', '창백한 피부', '우울감', '성급함',
      '근육통',
      '인지 기능 변화', '체내 붉은 반점', '하복부 통증', '생리 불규칙', '피부색 변화', '눈에서 물이 나옴', '식욕증가', '다뇨증', '가족력', '점액가래', '누런가래',
      '집중력 부족',
      '시각장애', '혈액 공급 여부', '위 출혈', '복부팽만', '음주력', '체액과다', '객혈', '다리혈관돌출', '심장박동감소', '보행 시 통증', '여드름', '피지과다', '흉터',
      '피부 벗겨짐', '은색 비듬', '손톱에 작은 움푹 들어간 자국', '염증성 손톱', '수포', '코 주위의 붉은 발진',
      '고름']  # 질병 리스트를 리스트에 담음

# disease=['진균증','알레르기','위-식도 역류질환','만성 담즙정체','약물반응','소화성 궤양','후천성 면역 결핍증','당뇨병','위장염'
# ,'기관지천식','고혈압','편두통','경부척추증','마비(뇌출혈)','고빌리루빈혈증','말라리아','수두','뎅기열'
# ,'장티푸스','A형간염','B형간염','C형간염','D형간염','E형간염','알코올성 간 질환','결핵','감기',
# '폐렴','치핵','심장마비','하지정맥류','갑상샘 저하증','갑상선 기능 항진증','저혈당증','골관절염','관절염','현기증','여드름','요로감염증','건선','농가진']
# l2 = []for i in range(0, len(l1)):    l2.append(0)

# 질병 리스트 생성
l1 = ['가려움', '피부발진', '결절성 피부 발진', '지속적인 재채기', '몸이 떨림', '오한', '관절 통증', '복통', '속쓰림'
    , '혀 궤양', '근육 감소', '구토', '소변 배출시 화끈거림', '혈뇨', '피로', '체중증가', '불안감', '수족냉증', '심한감정기복'
    , '체중감소', '안절부절못함', '무기력', '목에 반점', '불규칙한 혈당', '기침', '고열', '쑥 들어간 눈', '숨이 참', '발한', '탈수'
    , '소화불량', '두통', '황갈색 피부', '어두운 소변', '메스꺼움', '식욕부진', '눈 뒤쪽 통증', '요통', '변비', '상복부 통증', '설사'
    , '미열', '노란색 소변', '황달 눈', '급성간부전', '체액과다', '복부 부종', '림부절 비대', '불쾌감', '시야흐림', '가래', '인후통'
    , '충혈', '부비동염', '콧물', '혈관 용종', '가슴통증', '팔다리 근력부족', '심박수 증가', '배변 통증', '항문 통증', '혈변', '목 통증'
    , '어지럼증', '생리통', '상처', '비만', '혈관 붓기', "손톱 부러짐,갈라짐", '손발 붓기', '과도한 허기짐', '성관계', '입술건조'
    , '어눌한 말투', '무릎 통증', '고관절 통증', '근력저하', '담 걸린 목', '관절 부종', '신체의 긴장', '회전운동', '균형상실', '불안정함'
    , '한쪽 뇌의 이상', '후각 장애', '방광 불쾌감', '소변악취', '요실금', '방귀 악취', '내부 가려움', '창백한 피부', '우울감', '성급함'
    , '근육통', '인지 기능 변화', '체내 붉은 반점', '하복부 통증', '생리 불규칙', '피부색 변화', '눈에서 물이 나옴', '식욕증가', '다뇨증'
    , '가족력', '점액가래', '누런가래', '집중력 부족', '시각장애', '혈액 공급 여부', '위 출혈', '복부팽만', '음주력', '체액과다', '객혈'
    , '다리혈관돌출', '심장박동감소', '보행 시 통증', '여드름', '피지과다', '흉터', '피부 벗겨짐', '은색 비듬', '손톱에 작은 움푹 들어간 자국'
    , '염증성 손톱', '수포', '코 주위의 붉은 발진', '고름']

l1.sort()
disease = ['진균증', '알레르기', '위식도 역류 질환', '담즙정체', '약물반응', '소화성 궤양', '후천성 면역 결핍 증후군', '당뇨병', '위장염'
    , '기관지천식', '고혈압', '편두통', '경추증', '마비(뇌출혈)', '고빌리루빈혈증', '말라리아', '수두', '뎅기열', '장티푸스', 'A형간염'
    , 'B형간염', 'C형간염', 'D형간염', 'E형간염', '알코올성 간 질환', '결핵', '감기', '폐렴', '치핵', '심장마비', '하지정맥류', '갑상샘 저하증'
    , '갑상선 기능 항진증', '저혈당증', '골관절염', '관절염', '현기증', '여드름', '요로감염증', '건선', '농가진']

# 프로젝트 루트 디렉토리 경로 가져오기
#    pd.set_option("future.no_silent_downcasting", True)

dir_path = os.path.dirname(os.path.abspath(__file__))  # 프로젝트 루트 디렉토리 경로 가져오기
csv_path = os.path.join(dir_path, 'trainingLast.csv')
df = pd.read_csv(csv_path, encoding='cp949')
DF = pd.read_csv(csv_path, index_col='예후', encoding='cp949')

testCsv_path = os.path.join(dir_path, 'testingLast.csv')
tr = pd.read_csv(testCsv_path, encoding='cp949')

# 증상의 길이만큼 리스트 준비
l2 = []
for i in range(0, len(l1)):
    l2.append(0)

# 질병들을 int값으로 대체함
df.replace({'예후': {'진균증': 0, '알레르기': 1, '위식도 역류 질환': 2, '담즙정체': 3, '약물반응': 4, '소화성 궤양': 5, '후천성 면역 결핍 증후군': 6
    , '당뇨병': 7, '위장염': 8, '기관지천식': 9, '고혈압': 10, '편두통': 11, '경추증': 12, '마비(뇌출혈)': 13, '고빌리루빈혈증': 14, '말라리아': 15
    , '수두': 16, '뎅기열': 17, '장티푸스': 18, 'A형간염': 19, 'B형간염': 20, 'C형간염': 21, 'D형간염': 22, 'E형간염': 23, '알코올성 간 질환': 24
    , '결핵': 25, '감기': 26, '폐렴': 27, '치핵': 28, '심장마비': 29, '하지정맥류': 30, '갑상샘 저하증': 31, '갑상선 기능 항진증': 32, '저혈당증': 33
    , '골관절염': 34, '관절염': 35, '현기증': 36, '여드름': 37, '요로감염증': 38, '건선': 39, '농가진': 40}}, inplace=True)

X = df[l1]  # int값의 2차원 데이터로 만들기
y = df[['예후']]

np.ravel(y)

# 위와 동일하게 테스트값의 질병들을 대체하기 위해 판다스의 내장함수 이용

tr.replace({'예후': {'진균증': 0, '알레르기': 1, '위식도 역류 질환': 2, '담즙정체': 3, '약물반응': 4, '소화성 궤양': 5, '후천성 면역 결핍 증후군': 6
    , '당뇨병': 7, '위장염': 8, '기관지천식': 9, '고혈압': 10, '편두통': 11, '경추증': 12, '마비(뇌출혈)': 13, '고빌리루빈혈증': 14, '말라리아': 15
    , '수두': 16, '뎅기열': 17, '장티푸스': 18, 'A형간염': 19, 'B형간염': 20, 'C형간염': 21, 'D형간염': 22, 'E형간염': 23, '알코올성 간 질환': 24
    , '결핵': 25, '감기': 26, '폐렴': 27, '치핵': 28, '심장마비': 29, '하지정맥류': 30, '갑상샘 저하증': 31, '갑상선 기능 항진증': 32, '저혈당증': 33
    , '골관절염': 34, '관절염': 35, '현기증': 36, '여드름': 37, '요로감염증': 38, '건선': 39, '농가진': 40}}, inplace=True)

tr.head()

X_test = tr[l1]
y_test = tr[["예후"]]
np.ravel(y_test)


# 결정트리 예측
@bp.route('/predictAct', methods=['POST'])
def predictA():
    # 질병 컬럼들 받아오기
    selected_symptoms = [request.form.get(f'symptom{i}') for i in range(1, 6)]

    filtered_symptoms = [symptom for symptom in selected_symptoms if symptom is not None]
    print(filtered_symptoms)
    print(len(filtered_symptoms), '=======================================')
    prediction = []

    if (len(filtered_symptoms) < 2):
        prediction.set('')
    else:
        Symptom1 = filtered_symptoms[0]
        Symptom2 = filtered_symptoms[1]
        Symptom3 = filtered_symptoms[2] if len(filtered_symptoms) > 2 else None
        Symptom4 = filtered_symptoms[3] if len(filtered_symptoms) > 3 else None
        Symptom5 = filtered_symptoms[4] if len(filtered_symptoms) > 4 else None
        from sklearn import tree
        clf3 = tree.DecisionTreeClassifier()
        clf3 = clf3.fit(X, y)
        from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
        y_pred = clf3.predict(X_test)
        print(y_pred)
        print("Decision Tree")
        print("Accuracy")
        print(accuracy_score(y_test, y_pred))
        print(accuracy_score(y_test, y_pred, normalize=False))
        print("Confusion matrix")
        conf_matrix = confusion_matrix(y_test, y_pred)
        print(conf_matrix)

        psymptoms = [Symptom1, Symptom2, Symptom3, Symptom4, Symptom5]

        for k in range(0, len(l1)):
            for z in psymptoms:
                if (z == l1[k]):
                    l2[k] = 1

        inputtest = [l2]
        predict = clf3.predict(inputtest)
        predicted = predict[0]

        h = 'no'
        for a in range(0, len(disease)):
            if (predicted == a):
                h = 'yes'
                break

        if (h == 'yes'):
            prediction = (" ")
            prediction = (disease[a])
        else:
            prediction = " "
            prediction = "Not Found"

    return jsonify({'prediction': prediction})


# 랜덤포레스트 예측
@bp.route('/predictAct', methods=['POST'])
def predictB():
    # 질병 컬럼들 받아오기
    selected_symptoms = [request.form.get(f'symptom{i}') for i in range(1, 6)]

    filtered_symptoms = [symptom for symptom in selected_symptoms if symptom is not None]
    print(filtered_symptoms)
    print(len(filtered_symptoms), '=======================================')

    prediction = []

    if (len(filtered_symptoms) < 2):
        prediction.set(None)
    else:
        Symptom1 = filtered_symptoms[0]
        Symptom2 = filtered_symptoms[1]
        Symptom3 = filtered_symptoms[2] if len(filtered_symptoms) > 2 else None
        Symptom4 = filtered_symptoms[3] if len(filtered_symptoms) > 3 else None
        Symptom5 = filtered_symptoms[4] if len(filtered_symptoms) > 4 else None
        from sklearn.ensemble import RandomForestClassifier
        clf4 = RandomForestClassifier(n_estimators=100)
        clf4 = clf4.fit(X, np.ravel(y))

        # calculating accuracy
        from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
        y_pred = clf4.predict(X_test)
        print(y_pred)

        print("Random Forest")
        print("Accuracy")
        print(accuracy_score(y_test, y_pred))
        print(accuracy_score(y_test, y_pred, normalize=False))
        print("Confusion matrix")
        conf_matrix = confusion_matrix(y_test, y_pred)
        print(conf_matrix)

        psymptoms = [Symptom1, Symptom2, Symptom3, Symptom4, Symptom5]

        for k in range(0, len(l1)):
            for z in psymptoms:
                if (z == l1[k]):
                    l2[k] = 1

        inputtest = [l2]
        predict = clf4.predict(inputtest)
        predicted = predict[0]

        h = 'no'
        for a in range(0, len(disease)):
            if (predicted == a):
                h = 'yes'
                break
        if (h == 'yes'):
            prediction.set(" ")
            prediction.set(disease[a])
        else:
            prediction = []
            prediction.set = ("Not Found")
    return jsonify({'prediction': prediction})


# K-이웃 예측
@bp.route('/predictAct', methods=['POST'])
def predictC():
    prediction = []
    # 질병 컬럼들 받아오기
    selected_symptoms = [request.form.get(f'symptom{i}') for i in range(1, 6)]
    filtered_symptoms = [symptom for symptom in selected_symptoms if symptom is not None]

    if (len(filtered_symptoms) < 2):
        prediction.set('')

    else:
        Symptom1 = filtered_symptoms[0]
        Symptom2 = filtered_symptoms[1]
        Symptom3 = filtered_symptoms[2] if len(filtered_symptoms) > 2 else None
        Symptom4 = filtered_symptoms[3] if len(filtered_symptoms) > 3 else None
        Symptom5 = filtered_symptoms[4] if len(filtered_symptoms) > 4 else None

        from sklearn.neighbors import KNeighborsClassifier
        knn = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
        knn = knn.fit(X, np.ravel(y))

        from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
        y_pred = knn.predict(X_test)
        print("KNN")
        print(y_pred)
        print("Accuracy")
        print(accuracy_score(y_test, y_pred))
        print(accuracy_score(y_test, y_pred, normalize=False))
        print("Confusion matrix")
        conf_matrix = confusion_matrix(y_test, y_pred)
        print(conf_matrix)

        psymptoms = [Symptom1, Symptom2, Symptom3, Symptom4, Symptom5]

        for k in range(0, len(l1)):
            for z in psymptoms:
                if (z == l1[k]):
                    l2[k] = 1

        inputtest = [l2]
        predict = knn.predict(inputtest)
        predicted = predict[0]

        h = 'no'
        for a in range(0, len(disease)):
            if (predicted == a):
                h = 'yes'
                break

        if (h == 'yes'):
            prediction.set(" ")
            prediction.set(disease[a])
        else:
            prediction.set(" ")
            prediction.set("Not Found")

    return jsonify({'prediction': prediction})

#나이브 베이즈 예측
@bp.route('/predictAct', methods=['POST'])
def predictD():

    # 질병 컬럼들 받아오기
    selected_symptoms = [request.form.get(f'symptom{i}') for i in range(1, 6)]
    filtered_symptoms = [symptom for symptom in selected_symptoms if symptom is not None]

    prediction = []

    if (len(filtered_symptoms) < 2):
        prediction = ''

    else:
        Symptom1 = filtered_symptoms[0]
        Symptom2 = filtered_symptoms[1]
        Symptom3 = filtered_symptoms[2] if len(filtered_symptoms) > 2 else None
        Symptom4 = filtered_symptoms[3] if len(filtered_symptoms) > 3 else None
        Symptom5 = filtered_symptoms[4] if len(filtered_symptoms) > 4 else None
        from sklearn.naive_bayes import GaussianNB
        gnb = GaussianNB()
        gnb = gnb.fit(X, np.ravel(y))

        from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
        y_pred = gnb.predict(X_test)
        print("Naive Bayes")
        print("Accuracy")
        print(accuracy_score(y_test, y_pred))
        print(accuracy_score(y_test, y_pred, normalize=False))
        print("Confusion matrix")
        conf_matrix = confusion_matrix(y_test, y_pred)
        print(conf_matrix)

        psymptoms = [Symptom1, Symptom2, Symptom3, Symptom4, Symptom5]
        for k in range(0, len(l1)):
            for z in psymptoms:
                if (z == l1[k]):
                    l2[k] = 1

        inputtest = [l2]
        predict = gnb.predict(inputtest)
        predicted = predict[0]

        h = 'no'
        for a in range(0, len(disease)):
            if (predicted == a):
                h = 'yes'
                break
        if (h == 'yes'):
            prediction.set(" ")
            prediction.set(disease[a])
        else:
            prediction.set(" ")
            prediction.set("Not Found")

    return jsonify({'prediction': prediction})
