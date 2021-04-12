import plotly.express as px
import geopandas as gpd
import pandas as pd 
import os 
import json 



# 경로 설정
root_path = os.getcwd() # 실행 코드가 있는 곳 
data_path = os.path.join(root_path, 'data') # 실험에 쓰일 데이터가 있는 곳 
os.chdir(data_path)



# 데이터 로드 
geometry_gj = json.load(open('용인시_법정경계(읍면동).geojson', encoding='utf-8'))
car_df = pd.read_csv('경기도_용인시_자동차 등록 현황_읍면동_20190331.csv', encoding='cp949')



# 데이터 전처리 
int_car = [] 
for i in range(len(car_df)): 
    cur_price = car_df.iloc[i]['자가용']
    int_price = int(cur_price.replace(',', ''))
    int_car.append(int_price)
car_df['자가용_int'] = int_car
car_df = car_df.rename(columns={'구  분':'EMD_KOR_NM'})




# Choropleth 시각화
fig = px.choropleth(car_df, geojson=geometry_gj, locations='EMD_KOR_NM', color='자가용_int',
                                color_continuous_scale='Blues',
                                featureidkey='properties.EMD_KOR_NM')
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title_text='용인시 법정동 별 자가용 등록 대수', title_font_size=20)




# 시각화 파일 저장 
os.chdir('../')
fig.write_image('choropleth.png')