import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time


# タイトル
st.write("Suntory beacon data visualization")

####### Input部分（選択でファイルpath指定）#######
# csvを読み込む前提バージョン（事前に抽出が必要）
# TODO: データベース連携
Floor = st.selectbox("Floor", ["1F", "2F", "3F"])
Person_Num = st.radio("Number of User", ["1", "2", "3"])
User = st.selectbox("User", ["suzuki_7a", "nara_8a", "hamada_e4", "katou_79", "fujita_41"])
# multi_select = st.multiselect("好きな色",options=["赤","青","黄"])

# 可視化範囲
start_date = st.date_input(
    "Start date",
    value = datetime(2023, 11, 4)
)
end_date = st.date_input(
    "End date",
    value = datetime(2023, 11, 4)
)
start_time = st.time_input(
    "When do you start?",
    time(9, 30),
    step=timedelta(minutes=30)
)
end_time = st.time_input(
    "When do you end?",
    value=time(10, 30),
    step=timedelta(minutes=30)
)
# st.write("Start date:", start_date)
# st.write("Start time:", start_time)
# st.write("End date:", end_date)
# st.write("End time:", end_time)

######################
# TODO: multiselectではlist方に対応が必要
DataPath = f"./data/{Floor}_{User[-2:]}.csv"
#DataPath = "./data/test.csv"

# 可視化
# TODO: 複数人のデータを一括可視化
try:
    df = pd.read_csv(DataPath) # index: datatime
    # 時間の範囲指定
    start_time = pd.to_datetime(start_date.strftime("%Y-%m-%d") + " " + start_time.strftime("%H:%M:%S"))
    end_time = pd.to_datetime(end_date.strftime("%Y-%m-%d") + " " + end_time.strftime("%H:%M:%S"))
    
    x = pd.to_datetime(df["time"]) + timedelta(hours=9)
    y = df["prediction"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name=User))
    # 軸タイトル
    fig.update_xaxes(title="time")
    fig.update_yaxes(title="prediction")
    # 軸範囲
    fig.update_xaxes(range=[start_time, end_time])
    fig.update_xaxes(rangeslider={"visible":True})
    # タイトル
    fig.update_layout(title="Prediction of " + User + " in " + Floor)
    # 凡例
    fig.update_layout(showlegend=True)

    #if Person_Num == "2":
        # データの読み込み
        # 可視化
        

    #fig.show()
    st.plotly_chart(fig)

    # predictionごとの総時間
    st.write("Total time of visualization: ", end_time - start_time)
    st.write("Total time of room :", timedelta(seconds=int((df["prediction"]=="room").sum().sum())))
    st.write("Total time of Corridor Right :", timedelta(seconds=int((df["prediction"]=="Cor_R").sum().sum())))
    st.write("Total time of Corridor Left :", timedelta(seconds=int((df["prediction"]=="Cor_L").sum().sum())))


except:
    st.error("No data found. Please check the Floor or User Box.")