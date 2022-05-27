from numpy.core.numeric import NaN
from pandas._libs.missing import NA
from pyproj import Proj, transform
import numpy as np
import pandas  as pd

proj_origin = Proj(init='epsg:2097') # 중부원점TM 지도 사용 중
proj_WGS84 = Proj(init='epsg:4166') # Wgs84 경도/위도, GPS사용 전지구 좌표

origin = pd.read_csv('./Cafe_Data_Jeju_by_Sophia.csv', encoding='cp949')
converted = origin.copy()
origin['x'] = NaN
origin['y'] = NaN

for i, row in origin.iterrows():
    x1, y1 = row['좌표정보(x)'], row['좌표정보(y)']
    x2, y2 = transform(proj_origin,proj_WGS84,x1,y1)
    origin.at[i, 'x'] = x2
    origin.at[i, 'y'] = y2

origin.to_csv('./Cafe_Data_Jeju_by_Sophia.csv')
