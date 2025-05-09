import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Analysis - CO2 Emission", layout="wide")

# 제목
st.title("Data Analysis - CO2 Emission")
st.write(
    '''
    Hello there, this web page is a simple data analysis web dashboard created using the Python Streamlit library.  
    on this page, you can visualize the distribution of some variables or the correlation between variables.

    안녕하세요! 이 웹 페이지는 Python의 Streamlit 라이브러리를 사용하여 만든 간단한 데이터 분석 대시보드입니다.  
    이 페이지에서는 일부 변수들의 분포 또는 변수 간의 상관관계를 시각화할 수 있습니다.
    ''')
st.divider()


# 함수 만들기
def load_dataset(path):
    return pd.read_csv(path)


# CSV 불러오기
path = 'data/CO2_Emissions.csv'
df = load_dataset(path)
df.head().T

# 필터 항목 준비
makers = df['Vehicle Class'].unique().tolist()

with st.sidebar:
    st.markdown('Filter the data you want to analyze: :tulip:')

    # 차량 종류 필터
    st.multiselect(
        'Select the vehicle class you want to analyze: ',
        makers, default=['TWO-SEATER'],
        key='maker_filter')

    # 엔진 크기 필터
    st.slider(
        'Select the engine size (Liter) you want to analyze: ',
        min_value=df['Engine Size(L)'].min(),
        max_value=df['Engine Size(L)'].max(),
        value=(df['Engine Size(L)'].quantile(0.1), df['Engine Size(L)'].quantile(0.95)),
        step=.3,
        key='engine_filter')

# 필터링 적용
df = df.loc[
    (df['Vehicle Class'].isin(st.session_state['maker_filter'])) &
    (df['Engine Size(L)'] < st.session_state['engine_filter'][1]) &
    (df['Engine Size(L)'] > st.session_state['engine_filter'][0])
    ]

# =========================================
# 자동차 제조사별 엔진 사이즈를 박스플롯으로 시각화하고,
# 두 개의 컬럼으로 텍스트 설명과 차트를 나란히 배치

# 소제목
st.subheader(
    'Analysis of Engine Sizes')

col1, col2 = st.columns(2)
with col1:
    st.write(
        '''
        The box plot of engine sizes by automotive manufacturer.  
        What types of engine sizes do manufacturers produce the most for each brand?

        제조사별 엔진 크기 박스플롯입니다.   
        각 브랜드에서 주로 생산하는 엔진 크기는 어떤 유형인가요?
        ''')
with col2:
    fig1 = px.box(
        data_frame=df.sort_values('Engine Size(L)', ascending=False),
        x='Make', y='Engine Size(L)', width=300, height=400, points='all')
    st.plotly_chart(fig1)

st.divider()

# ==========================================
# Engine Size에 따른 연비를 시각화하는 산점도

st.subheader(
    'Analysis of Fuel Consumption')

# 위젯, 시각화
col3, col4 = st.columns(2)
with col3:
    st.write(
        '''
        The scatter plot graph illustrating fuel efficiency based on engine sizes.  
        Which manufacturer might have lower fuel efficiency within the engine size?  
        Which manufacturer might have higher fuel efficiency within the same engine size? 

        이 산점도 그래프는 엔진 크기를 기준으로 연비 효율성을 보여줍니다.  
        동일한 엔진 크기 범위 내에서 어떤 제조사가 더 낮은 연비를 보일까요?  
        같은 엔진 크기라도 어떤 제조사는 더 높은 연비를 기록할까요?
        ''')

    st.selectbox(
        'Select Y-axis: ',
        ['Fuel Consumption City (L/100 km)',  # 도시
         'Fuel Consumption Hwy (L/100 km)',  # 고속도로
         'Fuel Consumption Comb (L/100 km)'],  # 복합
        key='fig2_yaxis')

with col4:
    fig2 = px.scatter(
        data_frame=df, x='Engine Size(L)', y=st.session_state['fig2_yaxis'],
        width=500, color='Make', trendline='ols', trendline_scope='overall')

    st.plotly_chart(fig2)

st.divider()

st.subheader('Analysis of Carbon Emissions')

col5, col6 = st.columns(2)
with col5:
    st.write(
        '''
        The scatter plot graph depicting the correlation between fuel efficiency and carbon emissions, with color differentiation for each manufacturer.  
        Which manufacturer might have higher carbon emissions within the same fuel efficiency range?

        이 산점도 그래프는 연비와 이산화탄소 배출량 간의 상관관계를 보여줍니다.  
        각 제조사는 색상으로 구분되어 있습니다.  
        동일한 연비 범위 내에서 어떤 제조사가 더 높은 탄소 배출량을 보일까요?
        ''')

    st.selectbox(
        'Select X-axis: ',
        ['Fuel Consumption City (L/100 km)',  # 도시
         'Fuel Consumption Hwy (L/100 km)',  # 고속도로
         'Fuel Consumption Comb (L/100 km)'],  # 복합
        key='fig3_xaxis')

with col6:
    fig3 = px.scatter(
        data_frame=df, x=st.session_state['fig3_xaxis'], y='CO2 Emissions(g/km)',
        width=500, color='Make', trendline='ols', trendline_scope='overall')

    st.plotly_chart(fig3)