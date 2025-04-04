import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="커피숍 매출 분석 대시보드",
    page_icon="☕",
    layout="wide"
)

# 데이터 로드
@st.cache_data
def load_data():
    """데이터 로드 함수"""
    try:
        # 직접 데이터 파일 경로 지정 (Streamlit Cloud에 최적화)
        df = pd.read_csv("coffee_shop_revenue.csv")
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {str(e)}")
        return None

# 색상 스케일 생성 함수
def get_color_scale(values, cmap='coolwarm'):
    """값에 따른 색상 스케일 반환"""
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val
    
    # 값 정규화 및 색상 할당
    colors = []
    for val in values:
        if range_val == 0:  # 모든 값이 같을 경우
            normalized = 0.5
        else:
            normalized = (val - min_val) / range_val
        
        # coolwarm 색상 맵 사용
        if cmap == 'coolwarm':
            if normalized < 0.5:
                # 파란색 계열 (낮은 값)
                r = 0
                g = 0
                b = int(255 * (1 - 2 * normalized))
            else:
                # 빨간색 계열 (높은 값)
                r = int(255 * (2 * normalized - 1))
                g = 0
                b = 0
            colors.append(f'rgb({r},{g},{b})')
    
    return colors

# 기본 통계 분석 탭
def show_basic_stats(df):
    st.header("기본 통계 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("매출 통계")
        st.dataframe(df['Daily_Revenue'].describe())
        
        # 매출 분포 - 히스토그램으로 표시
        st.subheader("일일 매출 분포")
        
        # 데이터 준비
        hist_data = pd.DataFrame({
            'values': df['Daily_Revenue'],
            'count': 1
        })
        hist_data = hist_data.groupby(pd.cut(hist_data['values'], bins=20)).count().reset_index()
        hist_data['values'] = hist_data['values'].astype(str)
        
        # 차트 표시
        st.bar_chart(hist_data.set_index('values')['count'])
    
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
        
        # 시간별 추세 (간소화된 버전)
        st.subheader("매출 추세")
        df_sample = df.iloc[::max(1, len(df)//100)].copy()  # 데이터 샘플링
        st.line_chart(df_sample['Daily_Revenue'])
    
    st.markdown("---")
    st.subheader("📊 기본 통계 분석 인사이트")
    
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

# 상관관계 분석 탭
def show_correlation_analysis(df):
    st.header("상관관계 분석")
    
    # 상관관계 히트맵
    st.subheader("변수 간 상관관계 히트맵")
    
    # 상관관계 계산
    corr_matrix = df.corr().round(2)
    
    # 히트맵 표시
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # CSS를 이용한 히트맵 구현
        corr_html = """
        <style>
        .dataframe-heatmap {
            font-family: Arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        .dataframe-heatmap th, .dataframe-heatmap td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        .dataframe-heatmap th {
            background-color: #f2f2f2;
            font-weight: bold;
            color: #333;
        }
        </style>
        <table class='dataframe-heatmap'>
        """
        
        # 헤더 추가
        corr_html += "<tr><th></th>"
        for col in corr_matrix.columns:
            corr_html += f"<th>{col}</th>"
        corr_html += "</tr>"
        
        # 데이터 행 추가
        for idx, row in corr_matrix.iterrows():
            corr_html += f"<tr><th>{idx}</th>"
            for val in row:
                # 색상 설정
                if val > 0:
                    r = min(255, int(val * 255))
                    g = min(255, int((1 - val) * 255))
                    b = min(255, int((1 - val) * 255))
                else:
                    r = min(255, int((1 + val) * 255))
                    g = min(255, int((1 + val) * 255))
                    b = min(255, int(abs(val) * 255))
                    
                text_color = "white" if abs(val) > 0.5 else "black"
                corr_html += f"<td style='background-color: rgb({r}, {g}, {b}); color: {text_color}'>{val}</td>"
            corr_html += "</tr>"
        
        corr_html += "</table>"
        st.write(corr_html, unsafe_allow_html=True)
    
    with col2:
        # 상관관계 설명
        st.write("상관관계 강도:")
        st.markdown("""
        - **1.0**: 완전한 양의 상관관계
        - **0.7-0.9**: 강한 양의 상관관계
        - **0.4-0.6**: 중간 정도의 양의 상관관계
        - **0.1-0.3**: 약한 양의 상관관계
        - **0**: 상관관계 없음
        - **-0.1--0.3**: 약한 음의 상관관계
        - **-0.4--0.6**: 중간 정도의 음의 상관관계
        - **-0.7--0.9**: 강한 음의 상관관계
        - **-1.0**: 완전한 음의 상관관계
        """)
    
    # 매출과의 상관관계
    st.subheader("매출과의 상관관계")
    revenue_corr = df.corr()['Daily_Revenue'].sort_values(ascending=False)
    
    # 상관관계 데이터 시각화
    corr_df = pd.DataFrame({
        '변수': revenue_corr.index,
        '상관계수': revenue_corr.values
    })
    
    # 차트 색상 설정
    colors = []
    for val in corr_df['상관계수']:
        if val > 0:
            opacity = min(1.0, abs(val) + 0.3)
            colors.append(f'rgba(255, 99, 71, {opacity})')  # 양의 상관관계: 빨간색 계열
        else:
            opacity = min(1.0, abs(val) + 0.3)
            colors.append(f'rgba(70, 130, 180, {opacity})')  # 음의 상관관계: 파란색 계열
    
    # 상관관계 차트 (가로 막대 그래프)
    chart_data = pd.DataFrame({
        '상관계수': revenue_corr.values
    }, index=revenue_corr.index)
    st.bar_chart(chart_data)
    
    # 주요 변수와 매출의 관계
    st.subheader("주요 변수와 매출의 관계")
    selected_feature = st.selectbox(
        "변수 선택",
        ['Number_of_Customers_Per_Day', 'Average_Order_Value', 
         'Marketing_Spend_Per_Day', 'Operating_Hours_Per_Day']
    )
    
    # 산점도 차트
    chart_data = df[[selected_feature, 'Daily_Revenue']]
    st.scatter_chart(chart_data, x=selected_feature, y='Daily_Revenue')
    
    st.markdown("---")
    st.subheader("📊 상관관계 분석 인사이트")
    
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

# 시계열 분석 탭
def show_time_series_analysis(df):
    st.header("시계열 분석")
    
    # 인덱스 생성 (더 명확한 시각화를 위해)
    df_time = df.copy()
    df_time = df_time.reset_index()
    df_time.rename(columns={'index': 'Day'}, inplace=True)
    
    # 구간 선택
    window_size = len(df_time)
    start, end = st.select_slider(
        '분석할 데이터 구간 선택',
        options=list(range(window_size)),
        value=(0, min(100, window_size-1))
    )
    
    # 선택된 구간의 데이터
    df_selected = df_time.iloc[start:end+1].copy()
    
    # 매출 추이
    st.subheader("일별 매출 추이")
    
    # 차트 데이터 준비
    chart_data = pd.DataFrame({
        'Day': df_selected['Day'],
        'Daily_Revenue': df_selected['Daily_Revenue']
    }).set_index('Day')
    
    st.line_chart(chart_data)
    
    # 이동평균
    window = st.slider('이동평균 기간', 3, min(30, len(df_selected)), 7)
    
    # 이동평균 계산
    df_selected['MA'] = df_selected['Daily_Revenue'].rolling(window=window).mean()
    
    st.subheader(f"매출 추이와 {window}일 이동평균")
    
    # 차트 데이터 준비
    ma_chart_data = pd.DataFrame({
        'Day': df_selected['Day'],
        'Daily_Revenue': df_selected['Daily_Revenue'],
        f'{window}일 이동평균': df_selected['MA']
    }).set_index('Day')
    
    st.line_chart(ma_chart_data)
    
    # 매출 변동성 분석
    st.subheader("매출 변동성 분석")
    
    # 표준편차를 이용한 변동성 시각화
    rolling_std = df_time['Daily_Revenue'].rolling(window=max(7, window//2)).std()
    
    # 변동성 차트 데이터
    volatility_data = pd.DataFrame({
        'Day': df_time['Day'],
        '7일 변동성 (표준편차)': rolling_std
    }).set_index('Day')
    
    st.line_chart(volatility_data.iloc[start:end+1])
    
    st.markdown("---")
    st.subheader("📊 시계열 분석 인사이트")
    
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

# 특성 분석 탭
def show_feature_analysis(df):
    st.header("특성 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("고객 수 분석")
        
        # 히스토그램 데이터 준비
        hist_data = pd.DataFrame({
            'values': df['Number_of_Customers_Per_Day'],
            'count': 1
        })
        hist_data = hist_data.groupby(pd.cut(hist_data['values'], bins=15)).count().reset_index()
        hist_data['values'] = hist_data['values'].astype(str)
        
        # 차트 표시
        st.bar_chart(hist_data.set_index('values')['count'])
        
        st.write("고객 수 통계:")
        st.dataframe(df['Number_of_Customers_Per_Day'].describe())
        
        # 고객 수와 매출의 관계
        st.subheader("고객 수와 매출의 관계")
        customer_data = df[['Number_of_Customers_Per_Day', 'Daily_Revenue']].copy()
        
        # 그룹화 및 평균 계산
        customer_groups = pd.cut(customer_data['Number_of_Customers_Per_Day'], bins=5)
        customer_revenue = customer_data.groupby(customer_groups)['Daily_Revenue'].mean().reset_index()
        customer_revenue['Number_of_Customers_Per_Day'] = customer_revenue['Number_of_Customers_Per_Day'].astype(str)
        
        st.bar_chart(customer_revenue.set_index('Number_of_Customers_Per_Day'))
    
    with col2:
        st.subheader("평균 주문 금액 분석")
        
        # 히스토그램 데이터 준비
        hist_data = pd.DataFrame({
            'values': df['Average_Order_Value'],
            'count': 1
        })
        hist_data = hist_data.groupby(pd.cut(hist_data['values'], bins=15)).count().reset_index()
        hist_data['values'] = hist_data['values'].astype(str)
        
        # 차트 표시
        st.bar_chart(hist_data.set_index('values')['count'])
        
        st.write("평균 주문 금액 통계:")
        st.dataframe(df['Average_Order_Value'].describe())
        
        # 주문 금액과 매출의 관계
        st.subheader("주문 금액과 매출의 관계")
        order_data = df[['Average_Order_Value', 'Daily_Revenue']].copy()
        
        # 그룹화 및 평균 계산
        order_groups = pd.cut(order_data['Average_Order_Value'], bins=5)
        order_revenue = order_data.groupby(order_groups)['Daily_Revenue'].mean().reset_index()
        order_revenue['Average_Order_Value'] = order_revenue['Average_Order_Value'].astype(str)
        
        st.bar_chart(order_revenue.set_index('Average_Order_Value'))
    
    # 주요 변수 비교 분석
    st.subheader("주요 변수 비교 분석")
    
    # 특성 선택
    features = st.multiselect(
        "비교할 변수 선택",
        options=['Number_of_Customers_Per_Day', 'Average_Order_Value', 
                'Marketing_Spend_Per_Day', 'Operating_Hours_Per_Day', 
                'Number_of_Employees', 'Location_Foot_Traffic'],
        default=['Number_of_Customers_Per_Day', 'Average_Order_Value']
    )
    
    if features:
        # 데이터 정규화 - 시각화를 위해
        df_norm = df[features].copy()
        for feature in features:
            df_norm[feature] = (df_norm[feature] - df_norm[feature].min()) / (df_norm[feature].max() - df_norm[feature].min())
        
        # 그래프 표시
        st.line_chart(df_norm.iloc[::max(1, len(df_norm)//100)])
    
    st.markdown("---")
    st.subheader("📊 특성 분석 인사이트")
    
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

# 메인 함수
def main():
    st.title("☕ 커피숍 매출 분석 대시보드")
    
    # 데이터 로드
    df = load_data()
    if df is None:
        st.error("데이터를 로드할 수 없습니다. coffee_shop_revenue.csv 파일이 올바른 위치에 있는지 확인하세요.")
        return
    
    # 사이드바
    st.sidebar.header("분석 옵션")
    analysis_type = st.sidebar.selectbox(
        "분석 유형 선택",
        ["기본 통계", "상관관계 분석", "시계열 분석", "특성 분석"]
    )
    
    # 데이터 미리보기
    with st.sidebar.expander("데이터 미리보기"):
        st.dataframe(df.head())
    
    # 각 분석 유형에 따른 화면 표시
    if analysis_type == "기본 통계":
        show_basic_stats(df)
    elif analysis_type == "상관관계 분석":
        show_correlation_analysis(df)
    elif analysis_type == "시계열 분석":
        show_time_series_analysis(df)
    elif analysis_type == "특성 분석":
        show_feature_analysis(df)

# 앱 실행
if __name__ == "__main__":
    main() 