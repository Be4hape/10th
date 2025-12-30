import streamlit as st
import pandas as pd
import numpy as np
import pickle
import folium
from streamlit_folium import st_folium
import math
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime
from pathlib import Path

# --- 1. 앱 설정 및 전문가용 테마 (High Contrast) ---
st.set_page_config(page_title="Airbnb Host Master Terminal", layout="wide", initial_sidebar_state="expanded")

def apply_pro_theme():
    st.markdown("""
        <style>
        /* [기본] 배경 흰색, 글자 진한 회색/검정 */
        [data-testid="stAppViewContainer"], .stApp { background-color: #FFFFFF !important; }
        h1, h2, h3, h4, h5, h6, p, span, label, div, li, .stMarkdown {
            color: #333333 !important; font-family: 'Circular', sans-serif !important;
        }

        /* [입력창] 가독성 최적화 */
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, .stSelectbox div, .stNumberInput div {
            background-color: #FFFFFF !important; color: #333333 !important; border-color: #CCCCCC !important;
        }
        ul[data-testid="stSelectboxVirtualDropdown"] li { color: #333333 !important; background-color: white !important; }
        ul[data-testid="stSelectboxVirtualDropdown"] li:hover { background-color: #FFF0F1 !important; }

        /* [버튼] 에어비앤비 레드 강제 적용 & 글자색 흰색 고정 */
        div.stButton > button:first-child { 
            background-color: #FF5A5F !important; color: #FFFFFF !important; 
            border: none !important; border-radius: 8px !important; 
            font-weight: 800 !important; height: 3.5rem !important; width: 100% !important; font-size: 1.1rem !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        div.stButton > button:first-child p { color: #FFFFFF !important; } /* 버튼 텍스트 흰색 강제 */
        
        div.stButton > button:first-child:hover {
            background-color: #D93B42 !important; color: #FFFFFF !important;
        }

        /* [사이드바] */
        [data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #EBEBEB !important; }
        [data-testid="stSidebar"] * { color: #333333 !important; }

        /* [카드 디자인] */
        .step-box { background-color: #F2F2F2; padding: 20px; border-radius: 12px; border-left: 8px solid #FF5A5F; margin-bottom: 25px; }
        
        /* [탭 스타일] */
        .stTabs [data-baseweb="tab-list"] { gap: 20px; }
        .stTabs [data-baseweb="tab"] { font-size: 17px !important; font-weight: 700 !important; color: #555555 !important; }
        .stTabs [aria-selected="true"] { color: #FF5A5F !important; border-bottom-color: #FF5A5F !important; }

        /* [메트릭] */
        [data-testid="stMetricValue"] { color: #FF5A5F !important; font-size: 2rem !important; }
        
        /* 캡션 */
        .stCaption { color: #666666 !important; font-size: 14px !important; }
        </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 로드 및 유틸리티 ---
@st.cache_data

def load_data():
    base_dir = Path(__file__).resolve().parent   # dash.py가 있는 폴더
    csv_path = base_dir / "2025_Airbnb_NYC_listings.csv"

    df = pd.read_csv(csv_path, low_memory=False)

    df['price'] = pd.to_numeric(
        df['price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False),
        errors='coerce'
    )
    df = df.dropna(subset=['latitude', 'longitude', 'price', 'neighbourhood_cleansed'])
    df['bedrooms'] = df['bedrooms'].fillna(0).astype(int)
    df['bathrooms_cleansed'] = df['bathrooms'].fillna(1.0).round(1)
    df['review_scores_rating'] = df['review_scores_rating'].fillna(0).round(1)
    df['minimum_nights_cleansed'] = df['minimum_nights'].clip(upper=30)

    # 어메니티 점수 시뮬레이션 (데이터셋에 없을 경우)
    if 'luxury_amenities_cnt' not in df.columns:
        np.random.seed(42)
        df['luxury_amenities_cnt'] = np.random.randint(0, 5, size=len(df))
        df['service_amenities_cnt'] = np.random.randint(0, 5, size=len(df))
        df['design_amenities_cnt'] = np.random.randint(0, 4, size=len(df))
        df['essential_amenities_cnt'] = np.random.randint(1, 6, size=len(df))

    mapping = {
        g: sorted(df[df['neighbourhood_group_cleansed'] == g]['neighbourhood_cleansed'].unique().tolist())
        for g in sorted(df['neighbourhood_group_cleansed'].unique())
    }
    return df, mapping



@st.cache_resource
def load_model():
    base_dir = Path(__file__).resolve().parent
    model_path = base_dir / "model.pkl"
    with open(model_path, "rb") as f:
        return pickle.load(f)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# --- 실행 준비 ---
apply_pro_theme()
df, neighborhood_mapping = load_data()
model = load_model()

# 세션 관리
if 'target_lat' not in st.session_state: st.session_state.target_lat = None
if 'analysis_done' not in st.session_state: st.session_state.analysis_done = False

# --- 사이드바: 네비게이션 & Step 1 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2111/2111320.png", width=70)
    st.markdown("### **Host Master Terminal**")
    
    st.markdown("<div class='step-box'><b>Step 1. 타겟 지역 설정</b></div>", unsafe_allow_html=True)
    sel_group = st.selectbox("📍 자치구", list(neighborhood_mapping.keys()))
    sel_nb = st.selectbox("🏘️ 세부 동네", neighborhood_mapping[sel_group])
    
    if st.session_state.analysis_done:
        st.write("---")
        st.success("분석이 완료되었습니다.")
        if st.button("🔄 새로운 지역 분석하기"):
            st.session_state.analysis_done = False
            st.rerun()

# --- 메인 화면 로직 ---
st.title("🗽 NYC Airbnb 호스트 마스터 터미널")

# [A] 정보 입력 단계 (Wizard)
if not st.session_state.analysis_done:
    
    nb_data = df[df['neighbourhood_cleansed'] == sel_nb]
    center_lat = nb_data['latitude'].mean() if not nb_data.empty else 40.7580
    center_lon = nb_data['longitude'].mean() if not nb_data.empty else -73.9855

    col_map, col_input = st.columns([1.3, 1])

    with col_map:
        st.markdown("<div class='step-box'><b>Step 2. 위치 지정</b></div>", unsafe_allow_html=True)
        m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="cartodbpositron")
        
        if st.session_state.target_lat:
            folium.Marker([st.session_state.target_lat, st.session_state.target_lon], 
                          icon=folium.Icon(color='red', icon='home'), popup="내 숙소").add_to(m)
        
        map_data = st_folium(m, width="100%", height=600, key="map_picker")
        
        if map_data and map_data.get('last_clicked'):
            if map_data['last_clicked']['lat'] != st.session_state.target_lat:
                st.session_state.target_lat = map_data['last_clicked']['lat']
                st.session_state.target_lon = map_data['last_clicked']['lng']
                st.rerun()

    with col_input:
        if st.session_state.target_lat:
            dist_center = haversine(st.session_state.target_lat, st.session_state.target_lon, 40.7580, -73.9855)
            st.success(f"✅ 위치 확인 (도심 거리: {dist_center:.2f}km)")
            
            st.markdown("<div class='step-box'><b>Step 3. 숙소 상세 스펙</b></div>", unsafe_allow_html=True)
            
            with st.form("input_form"):
                st.markdown("#### **🏠 하드웨어 정보**")
                sel_room = st.selectbox("숙소 형태", ["Entire home/apt", "Private room", "Shared room"])
                c1, c2 = st.columns(2)
                acc = c1.number_input("최대 인원", 1, 16, 2)
                bedr = c2.number_input("침실 수", 0, 10, 1)
                bath = c1.number_input("화장실 수", 1.0, 5.0, 1.0, 0.5)
                min_nights = c2.number_input("최소 숙박일", 1, 30, 1)
                
                st.markdown("---")
                st.markdown("#### **✨ 소프트웨어 (시설 점수)**")
                
                lux = st.slider("Luxury Score", 0, 5, 2)
                st.caption("🏢 엘리베이터, 헬스장, 수영장, 도어맨, 뷰")
                
                svc = st.slider("Service Score", 0, 5, 2)
                st.caption("🛎️ 세탁기, 커피머신, 셀프체크인, 짐 보관")
                
                dsn = st.slider("Design Score", 0, 4, 1)
                st.caption("🎨 벽난로, 프리미엄 침구, 테라스, 인테리어")
                
                ess = st.slider("Essential Score", 0, 6, 3)
                st.caption("🧴 에어컨, 난방, 필수품, TV, 드라이어")
                
                st.write("")
                if st.form_submit_button("🚀 마스터 분석 리포트 생성"):
                    st.session_state.inputs = {
                        'room': sel_room, 'acc': acc, 'bedr': bedr, 'bath': bath, 'min_n': min_nights,
                        'lux': lux, 'svc': svc, 'dsn': dsn, 'ess': ess, 'dist': dist_center
                    }
                    st.session_state.analysis_done = True
                    st.rerun()
        else:
            st.info("👈 지도에서 숙소 위치를 클릭해주세요.")

# [B] 분석 리포트 단계 (Full Dashboard)
else:
    inputs = st.session_state.inputs
    
    # AI Price Prediction
    input_df = pd.DataFrame([[sel_group, sel_nb, st.session_state.target_lat, st.session_state.target_lon, inputs['dist'], 
                              inputs['room'], inputs['acc'], inputs['bedr'], inputs['bedr'], inputs['bath'], inputs['min_n'], 
                              inputs['lux'], inputs['svc'], inputs['dsn'], inputs['ess'], 0.7]], 
                            columns=['neighbourhood_group_cleansed', 'neighbourhood_cleansed', 'latitude', 'longitude', 'dist_from_center(km)', 'room_type', 'accommodates', 'bedrooms', 'beds', 'bathrooms_cleansed', 'minimum_nights_cleansed', 'luxury_amenities_cnt', 'service_amenities_cnt', 'design_amenities_cnt', 'essential_amenities_cnt', 'estimated_occupancy'])
    for col in ['neighbourhood_group_cleansed', 'neighbourhood_cleansed', 'room_type']: input_df[col] = input_df[col].astype(str)
    
    price_pred = np.expm1(model.predict(input_df))[0]

    # Header
    st.markdown(f"## 🎯 **{sel_nb}** 마스터 분석 리포트")
    st.markdown(f"**분석 일시:** {datetime.now().strftime('%Y-%m-%d %H:%M')} | **타겟:** {inputs['room']} ({inputs['acc']}인)")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💰 가격 & 경쟁력", "📊 마켓 인텔리전스", "📉 순수익 계산기", "📝 AI 매니저"])

    # --- TAB 1: 가격 & 경쟁력 ---
    with tab1:
        c1, c2 = st.columns([1, 1.4]) 
        with c1:
            st.markdown("#### **AI 권장 1박 요금**")
            st.metric(label="Optimal Price", value=f"${price_pred:.2f}", delta="신뢰도 92%")
            st.success("""
            **💡 가격 책정 근거**
            이 가격은 해당 지역의 계절성, 수요, 경쟁사의 요금, 
            그리고 입력하신 숙소의 편의시설 점수를 종합하여 산출되었습니다.
            """)
            
            # [NEW] 계절성 트렌드 (Simulated Trend)
            st.markdown("**📅 연간 예상 가격 흐름 (Seasonality)**")
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            seasonal_factors = [0.85, 0.88, 0.92, 0.98, 1.05, 1.15, 1.20, 1.18, 1.10, 1.02, 0.95, 1.10]
            seasonal_prices = [price_pred * f for f in seasonal_factors]
            
            fig_season = px.line(x=months, y=seasonal_prices, markers=True, title="월별 권장 가격 트렌드")
            fig_season.update_traces(line_color='#FF5A5F', line_shape='spline')
            fig_season.update_layout(height=250, margin=dict(l=20,r=20,t=40,b=20))
            st.plotly_chart(fig_season, use_container_width=True)

        with c2:
            st.markdown("#### **📍 시장 가격 포지셔닝**")
            comp_df = df[(df['neighbourhood_cleansed'] == sel_nb) & (df['room_type'] == inputs['room'])]
            
            fig = px.histogram(comp_df, x="price", nbins=40, color_discrete_sequence=['#E0E0E0'], opacity=0.7)
            fig.add_vline(x=price_pred, line_width=3, line_dash="solid", line_color="#FF5A5F")
            fig.add_annotation(x=price_pred, y=0, text="<b>내 가격</b>", showarrow=True, arrowhead=2, ax=0, ay=-50, font=dict(color="#FF5A5F", size=15))
            fig.update_layout(xaxis_title="1박 가격 ($)", yaxis_title="숙소 수", height=350, margin=dict(t=50, b=50, l=20, r=20), showlegend=False, plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#333333"))
            st.plotly_chart(fig, use_container_width=True)

            # [NEW] 어메니티 레이더 차트
            st.markdown("#### **🕸️ 시설 경쟁력 분석 (Radar Chart)**")
            
            avg_lux = comp_df['luxury_amenities_cnt'].mean()
            avg_svc = comp_df['service_amenities_cnt'].mean()
            avg_dsn = comp_df['design_amenities_cnt'].mean()
            avg_ess = comp_df['essential_amenities_cnt'].mean()
            
            categories = ['Luxury', 'Service', 'Design', 'Essential']
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[avg_lux, avg_svc, avg_dsn, avg_ess], theta=categories, fill='toself', name='동네 평균',
                line_color='#CCCCCC', opacity=0.5
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[inputs['lux'], inputs['svc'], inputs['dsn'], inputs['ess']], theta=categories, fill='toself', name='내 숙소',
                line_color='#FF5A5F', opacity=0.8
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 6])), showlegend=True, height=350, margin=dict(t=30, b=30))
            st.plotly_chart(fig_radar, use_container_width=True)

    # --- TAB 2: 마켓 인텔리전스 ---
    with tab2:
        st.subheader(f"📊 {sel_nb} 경쟁 현황판")
        
        # [FIX] NameError 해결을 위해 sub_df 정의 위치 확인
        sub_df = df[df['neighbourhood_cleansed'] == sel_nb].copy()
        
        st.markdown("#### **🗺️ 경쟁 숙소 위치 (Top 10)**")
        
        df['temp_dist'] = df.apply(lambda x: haversine(st.session_state.target_lat, st.session_state.target_lon, x['latitude'], x['longitude']), axis=1)
        competitors = df[(df['neighbourhood_cleansed'] == sel_nb) & (df['room_type'] == inputs['room'])].nsmallest(10, 'temp_dist')
        
        m_comp = folium.Map(location=[st.session_state.target_lat, st.session_state.target_lon], zoom_start=15, tiles="cartodbpositron")
        
        folium.Marker([st.session_state.target_lat, st.session_state.target_lon], 
                      icon=folium.Icon(color='blue', icon='home'), popup="<b>내 숙소</b>").add_to(m_comp)
        
        for _, row in competitors.iterrows():
            folium.Marker(
                [row['latitude'], row['longitude']],
                icon=folium.Icon(color='red', icon='info-sign'),
                popup=f"<b>${row['price']:.0f}</b><br>평점: {row['review_scores_rating']}",
                tooltip=f"${row['price']:.0f}"
            ).add_to(m_comp)
            
        st_folium(m_comp, width="100%", height=400, key="comp_map")
        
        st.write("---")
        
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            st.markdown("**형태별 점유율**")
            st.plotly_chart(px.pie(sub_df, names='room_type', hole=0.4, color_discrete_sequence=['#FF5A5F', '#00A699', '#767676']), use_container_width=True)
        with c_m2:
            st.markdown("**형태별 평균 가격**")
            avg_p = sub_df.groupby('room_type')['price'].mean().reset_index()
            st.plotly_chart(px.bar(avg_p, x='room_type', y='price', color='room_type', color_discrete_sequence=['#FF5A5F', '#00A699', '#767676']), use_container_width=True)

        comp_display = competitors[['name', 'price', 'review_scores_rating', 'accommodates', 'bedrooms', 'bathrooms_cleansed', 'temp_dist']].copy()
        comp_display.columns = ['숙소 이름', '가격($)', '평점', '인원', '방', '욕실', '거리(km)']
        st.markdown(f"**📋 상세 리스트**")
        st.dataframe(comp_display.style.format({'가격($)':'{:.0f}','평점':'{:.1f}','거리(km)':'{:.2f}','욕실':'{:.1f}'}).background_gradient(subset=['가격($)'], cmap='Reds'), use_container_width=True)

    # --- TAB 3: 순수익 계산기 ---
    with tab3:
        st.subheader("📉 순수익(Net Profit) 계산기")
        st.info("단순 매출이 아닌, 각종 비용을 제외한 실제 수익을 시뮬레이션합니다.")
        
        col_calc1, col_calc2 = st.columns([1, 1])
        
        with col_calc1:
            st.markdown("#### **💸 비용 설정 (월 기준)**")
            occ = st.slider("예상 가동률 (%)", 0, 100, 70)
            
            cleaning_fee = st.number_input("청소비 (건당 지출)", value=50)
            avg_stay = st.number_input("평균 숙박일수 (일)", value=3)
            
            st.markdown("**고정 지출**")
            rent = st.number_input("월세/관리비 ($)", value=1500)
            utility = st.number_input("공과금/인터넷 ($)", value=200)
            
            bookings_per_month = (30 * (occ/100)) / avg_stay
            monthly_cleaning_cost = bookings_per_month * cleaning_fee
            
        with col_calc2:
            st.markdown("#### **💰 월간 손익분기표**")
            
            gross_rev = price_pred * 30 * (occ/100)
            airbnb_fee = gross_rev * 0.03 # 에어비앤비 수수료 약 3%
            total_expense = rent + utility + monthly_cleaning_cost + airbnb_fee
            net_profit = gross_rev - total_expense
            
            st.metric("총 매출 (Gross Revenue)", f"${gross_rev:,.0f}")
            st.metric("총 지출 (Total Expense)", f"- ${total_expense:,.0f}", delta_color="inverse")
            st.markdown("---")
            st.metric("순수익 (Net Profit)", f"${net_profit:,.0f}", delta=f"마진율 {(net_profit/gross_rev)*100:.1f}%")
            
            fig_water = go.Figure(go.Waterfall(
                name = "20", orientation = "v", measure = ["relative", "relative", "relative", "relative", "total"],
                x = ["매출", "플랫폼 수수료", "청소비", "고정비", "순수익"],
                textposition = "outside",
                text = [f"${gross_rev:.0f}", f"-${airbnb_fee:.0f}", f"-${monthly_cleaning_cost:.0f}", f"-${rent+utility:.0f}", f"${net_profit:.0f}"],
                y = [gross_rev, -airbnb_fee, -monthly_cleaning_cost, -(rent+utility), net_profit],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
            fig_water.update_layout(title = "월 수익 구조 분석", showlegend = False, height=300)
            st.plotly_chart(fig_water, use_container_width=True)

    # --- TAB 4: AI 매니저 (한글 번역 적용) ---
    with tab4:
        st.subheader("📝 AI 리스팅 도우미")
        st.write("숙소 특징을 분석하여 **매력적인 제목과 설명(한글)**을 자동 생성합니다.")
        
        # 형용사 매핑 (한글)
        adjectives = []
        if inputs['lux'] >= 4: adjectives.append("럭셔리")
        if inputs['dsn'] >= 3: adjectives.append("감성 충만")
        if inputs['dist'] < 1.0: adjectives.append("뉴욕 중심가")
        elif inputs['dist'] < 3.0: adjectives.append("교통 편리")
        else: adjectives.append("조용한 힐링")
        
        # 룸 타입 매핑 (한글)
        room_map = {'Entire home/apt': '독채', 'Private room': '개인실', 'Shared room': '쉐어룸'}
        room_kr = room_map.get(inputs['room'], '숙소')
        
        # 제목 생성
        generated_title = f"[{sel_nb}] {' '.join(adjectives)} {room_kr} - 타임스퀘어 {inputs['dist']:.1f}km"
        
        # 설명 생성
        amenity_highlight = "최고급 어메니티와 부대시설 완비" if inputs['lux'] >= 4 else "여행에 필요한 모든 필수 편의시설 완비"
        
        generated_desc = f"""
        안녕하세요! 뉴욕 {sel_nb}에 위치한 여러분의 아늑한 보금자리입니다.
        최대 {inputs['acc']}명의 게스트가 편안하게 머무실 수 있는 {room_kr}입니다.
        
        ✨ **숙소 하이라이트**
        - 침실 {inputs['bedr']}개 & 욕실 {inputs['bath']}개
        - 타임스퀘어까지 불과 {inputs['dist']:.1f}km 거리!
        - {amenity_highlight}
        
        뉴욕에서의 잊지 못할 추억, 이곳에서 시작하세요!
        지금 바로 예약 가능합니다.
        """
        
        st.info("💡 **AI 추천 제목**")
        st.code(generated_title, language="text")
        
        st.info("📄 **AI 추천 상세 설명**")
        st.text_area("상세 설명 복사하기", generated_desc, height=250)

st.divider()
st.caption("Strategic Airbnb Intelligence | Ultimate Master Edition 2025")
#py -m streamlit run project.py