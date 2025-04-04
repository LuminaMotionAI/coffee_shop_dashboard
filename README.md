# 커피숍 매출 분석 대시보드

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://커피숍-매출-분석-대시보드.streamlit.app)

## 프로젝트 개요

이 프로젝트는 커피숍의 매출 데이터를 분석하여 인사이트를 도출하는 대시보드 애플리케이션입니다. 다양한 요인들이 매출에 미치는 영향을 시각화하고 분석하여 효과적인 사업 전략을 수립하는 데 도움을 줍니다. Plotly를 활용한 인터랙티브 시각화를 통해 보다 직관적인 분석 경험을 제공합니다.

## 주요 기능

- **기본 통계 분석**: 매출의 기본 통계량과 분포를 시각화합니다.
- **상관관계 분석**: 다양한 변수와 매출 간의 상관관계를 분석합니다.
- **시계열 분석**: 시간에 따른 매출 추이와 이동평균을 분석합니다.
- **특성 분석**: 고객 수, 평균 주문 금액 등의 주요 특성을 분석합니다.

## 인터랙티브 시각화

- **Plotly 기반 차트**: 마우스 호버 시 세부 데이터 확인 가능
- **확대/축소 기능**: 특정 구간을 확대하여 세부 분석 가능
- **동적 필터링**: 사용자 선택에 따라 데이터 필터링 가능
- **상관관계 히트맵**: 변수 간 관계를 직관적으로 시각화
- **추세선 분석**: 주요 변수와 매출의 관계에 추세선 표시

## 데이터셋

분석에 사용된 데이터셋에는 다음과 같은 변수들이 포함되어 있습니다:

- `Number_of_Customers_Per_Day`: 일일 고객 수
- `Average_Order_Value`: 평균 주문 금액
- `Operating_Hours_Per_Day`: 일일 영업 시간
- `Number_of_Employees`: 직원 수
- `Marketing_Spend_Per_Day`: 일일 마케팅 지출
- `Location_Foot_Traffic`: 위치 유동인구
- `Daily_Revenue`: 일일 매출

## 인사이트 요약

1. **고객 수**와 **평균 주문 금액**이 매출에 가장 큰 영향을 미칩니다.
2. 마케팅 지출은 매출과 약한 상관관계를 보입니다.
3. 영업 시간, 직원 수, 위치 유동인구는 매출과 거의 상관관계가 없습니다.

## 앱 실행 방법

1. 저장소 클론:
```
git clone https://github.com/LuminaMotionAI/coffee_shop_dashboard.git
```

2. 필요한 패키지 설치:
```
pip install -r requirements.txt
```

3. Streamlit 앱 실행:
```
streamlit run app.py
```

## 기술 스택

- **Streamlit**: 웹 애플리케이션 프레임워크
- **Plotly**: 인터랙티브 시각화 라이브러리
- **Pandas**: 데이터 조작 및 분석
- **NumPy**: 수치 계산
- **Statsmodels**: 통계 모델링 및 분석

## 온라인 데모

Streamlit Cloud에서 실행 중인 라이브 데모를 확인하세요:
[커피숍 매출 분석 대시보드](https://coffeeshopdashboard.streamlit.app/)

## 개선 제안

데이터 분석 결과를 바탕으로 다음과 같은 개선 전략을 제안합니다:

1. **고객 수 증가 전략**:
   - 고객 유치 프로그램 강화
   - 충성도 프로그램 도입
   - 재방문율 향상 전략

2. **평균 주문 금액 증가 전략**:
   - 메뉴 구성 최적화
   - 세트 메뉴 또는 업셀링 전략 도입
   - 프리미엄 메뉴 라인업 확대

## 라이센스

MIT License 
