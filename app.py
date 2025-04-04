import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import matplotlib
import platform

# 한글 폰트 설정
if platform.system() == 'Darwin':  # macOS
    matplotlib.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':  # Windows
    matplotlib.rcParams['font.family'] = 'Malgun Gothic'
else:
    matplotlib.rcParams['font.family'] = 'NanumGothic'
    
matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

# 페이지 설정
st.set_page_config(
    page_title="커피숍 매출 분석 대시보드",
    page_icon="☕",
    layout="wide"
)

# 데이터 로드
@st.cache_data
def load_data():
    data_path = Path("data/raw/coffee_shop_revenue.csv")
    if data_path.exists():
        df = pd.read_csv(data_path)
        return df
    else:
        st.error("데이터 파일을 찾을 수 없습니다. data/raw/coffee_shop_revenue.csv 파일을 확인해주세요.")
        return None

# 메인 함수
def main():
    st.title("☕ 커피숍 매출 분석 대시보드")
    
    # 데이터 로드
    df = load_data()
    if df is None:
        return
    
    # 사이드바
    st.sidebar.header("분석 옵션")
    analysis_type = st.sidebar.selectbox(
        "분석 유형 선택",
        ["기본 통계", "상관관계 분석", "시계열 분석", "특성 분석"]
    )
    
    # 기본 통계
    if analysis_type == "기본 통계":
        st.header("기본 통계 분석")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("매출 통계")
            st.write(df['Daily_Revenue'].describe())
            
            # 매출 분포
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=df, x='Daily_Revenue', bins=30)
            plt.title('일일 매출 분포')
            st.pyplot(fig)
        
        with col2:
            st.subheader("주요 지표")
            metrics = {
                '평균 매출': df['Daily_Revenue'].mean(),
                '최대 매출': df['Daily_Revenue'].max(),
                '최소 매출': df['Daily_Revenue'].min(),
                '매출 표준편차': df['Daily_Revenue'].std()
            }
            for metric, value in metrics.items():
                st.metric(metric, f"${value:,.2f}")
        
        # 인사이트 추가
        st.markdown("---")
        st.subheader("📊 기본 통계 분석 인사이트")
        
        # 인사이트 내용
        st.markdown("""
        ### 주요 인사이트:
        1. **평균 매출**은 $1,917.33로, 일반적인 커피숍 평균 매출과 비교하여 양호한 수준입니다.
        2. **매출 변동성**이 크게 나타납니다 (표준편차: $976.20). 이는 요일별, 계절별 변동이 크다는 것을 의미합니다.
        3. **최소 매출**이 음수(-$58.95)인 경우가 있어, 일부 환불이나 조정 사항이 있었던 것으로 추정됩니다.
        4. **최대 매출**($5,114.60)과 최소 매출 간의 차이가 크게 나타나 특별 이벤트나 성수기 효과가 있을 수 있습니다.
        
        ### 개선 제안:
        - 매출 변동성을 줄이기 위한 전략 수립이 필요합니다.
        - 매출이 낮은 날의 패턴을 분석하여 프로모션 전략을 구상해볼 수 있습니다.
        - 최대 매출을 기록한 날의 요인을 분석하여 유사 전략을 수립할 필요가 있습니다.
        """)
    
    # 상관관계 분석
    elif analysis_type == "상관관계 분석":
        st.header("상관관계 분석")
        
        # 상관관계 히트맵
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
        plt.title('변수 간 상관관계')
        st.pyplot(fig)
        
        # 매출과의 상관관계
        st.subheader("매출과의 상관관계")
        revenue_corr = df.corr()['Daily_Revenue'].sort_values(ascending=False)
        st.write(revenue_corr)
        
        # 주요 변수와 매출의 관계
        st.subheader("주요 변수와 매출의 관계")
        selected_feature = st.selectbox(
            "변수 선택",
            ['Number_of_Customers_Per_Day', 'Average_Order_Value', 
             'Marketing_Spend_Per_Day', 'Operating_Hours_Per_Day']
        )
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x=selected_feature, y='Daily_Revenue')
        plt.title(f'{selected_feature}와 매출의 관계')
        st.pyplot(fig)
        
        # 인사이트 추가
        st.markdown("---")
        st.subheader("📊 상관관계 분석 인사이트")
        
        # 인사이트 내용
        st.markdown("""
        ### 주요 인사이트:
        1. **고객 수**(0.736)와 **평균 주문 금액**(0.536)이 매출과 가장 강한 양의 상관관계를 보입니다.
        2. **마케팅 지출**(0.255)은 매출과 약한 양의 상관관계를 보입니다.
        3. **영업시간**(-0.005), **직원 수**(0.003), **위치 유동인구**(0.013)는 매출과 거의 상관관계가 없습니다.
        
        ### 개선 제안:
        - **고객 수 증가 전략**에 집중하는 것이 가장 효과적입니다:
          * 고객 유치 프로그램 강화
          * 충성도 프로그램 도입
          * 재방문율 향상 전략 수립
        - **평균 주문 금액 증가 전략**도 효과적입니다:
          * 메뉴 구성 최적화
          * 세트 메뉴 또는 업셀링 전략 도입
          * 고가 메뉴 아이템 추가 검토
        - **마케팅 효율성 개선**이 필요합니다:
          * 현재 마케팅 지출이 매출에 미치는 영향이 제한적임
          * 타겟 마케팅 및 ROI 분석 강화 필요
        """)
    
    # 시계열 분석
    elif analysis_type == "시계열 분석":
        st.header("시계열 분석")
        
        # 매출 추이
        fig, ax = plt.subplots(figsize=(15, 6))
        plt.plot(df.index, df['Daily_Revenue'])
        plt.title('일별 매출 추이')
        plt.xlabel('일자')
        plt.ylabel('매출')
        st.pyplot(fig)
        
        # 이동평균
        window = st.slider('이동평균 기간', 7, 30, 7)
        df['MA'] = df['Daily_Revenue'].rolling(window=window).mean()
        
        fig, ax = plt.subplots(figsize=(15, 6))
        plt.plot(df.index, df['Daily_Revenue'], label='일별 매출')
        plt.plot(df.index, df['MA'], label=f'{window}일 이동평균')
        plt.title('매출 추이와 이동평균')
        plt.legend()
        st.pyplot(fig)
        
        # 인사이트 추가
        st.markdown("---")
        st.subheader("📊 시계열 분석 인사이트")
        
        # 인사이트 내용
        st.markdown("""
        ### 주요 인사이트:
        1. 매출 데이터는 **주기적인 패턴**을 보이며, 이는 요일별 패턴이 있음을 시사합니다.
        2. 이동평균선을 통해 전반적인 **추세**를 파악할 수 있으며, 특정 기간에 매출이 증가 또는 감소하는 패턴이 있습니다.
        3. 단기적인 **이상치**(특별히 높거나 낮은 매출)가 관찰되며, 특별 이벤트나 외부 요인의 영향일 수 있습니다.
        
        ### 개선 제안:
        - **요일별 패턴**을 분석하여 요일별 맞춤형 프로모션 전략을 구상할 수 있습니다.
        - 매출이 낮은 기간에 **특별 프로모션**을 계획하여 매출 안정화를 도모할 수 있습니다.
        - 장기적인 **계절성**을 파악하여 계절에 맞는 메뉴 구성 및 마케팅 전략을 수립할 수 있습니다.
        - 높은 매출을 기록한 날의 **성공 요인**을 분석하여 향후 전략에 반영할 수 있습니다.
        """)
    
    # 특성 분석
    elif analysis_type == "특성 분석":
        st.header("특성 분석")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("고객 수 분석")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=df, x='Number_of_Customers_Per_Day', bins=30)
            plt.title('일일 고객 수 분포')
            st.pyplot(fig)
            
            st.write("고객 수 통계:")
            st.write(df['Number_of_Customers_Per_Day'].describe())
        
        with col2:
            st.subheader("평균 주문 금액 분석")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=df, x='Average_Order_Value', bins=30)
            plt.title('평균 주문 금액 분포')
            st.pyplot(fig)
            
            st.write("평균 주문 금액 통계:")
            st.write(df['Average_Order_Value'].describe())
        
        # 인사이트 추가
        st.markdown("---")
        st.subheader("📊 특성 분석 인사이트")
        
        # 인사이트 내용
        st.markdown("""
        ### 주요 인사이트:
        1. **고객 수 분포**는 정규 분포에 가까우며, 평균적으로 하루에 약 400명의 고객이 방문합니다.
        2. **평균 주문 금액**은 약 $8.5 정도로, 일반 커피 가격대보다 높은 편으로 프리미엄 커피 및 푸드 아이템이 매출에 기여하는 것으로 보입니다.
        3. 고객 수와 평균 주문 금액 모두 **변동성**이 있어, 이를 안정화하는 전략이 필요합니다.
        
        ### 개선 제안:
        - **고객 수 증가 및 안정화 전략**:
          * 피크 타임과 비피크 타임의 고객 수 차이를 줄이기 위한 시간대별 프로모션
          * 멤버십 프로그램을 통한 충성 고객 확보
          * 그룹 방문객을 위한 특별 혜택 제공
        
        - **평균 주문 금액 증가 전략**:
          * 번들 상품 또는 세트 메뉴 구성
          * 고가 프리미엄 메뉴 라인업 확대
          * 시즌별 특별 메뉴 도입
          * 직원 교육을 통한 업셀링 능력 향상
        
        - **통합 전략**:
          * 고객 세그먼트별 맞춤형 마케팅 전략 수립
          * 데이터 기반 의사결정을 위한 정기적인 분석 시스템 구축
        """)

if __name__ == "__main__":
    main() 