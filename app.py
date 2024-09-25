import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time


# タイトル
st.write("Suntory beacon data visualization")

####### Data Input部分（選択でファイルpath指定）#######
# csvを読み込む前提バージョン（事前に抽出が必要）
# TODO: データベース連携
Floor = st.selectbox("Floor", ["F1", "F2", "F3"])
#Person_Num = st.radio("Number of User", ["1", "2", "3"])
User = st.selectbox("User", ["suzuki_7a", "nara_8a", "hamada_e4", "katou_79", "fujita_41"])
User_and_DAY = st.selectbox("Day", ["8a_0923", "8a_1015", "8a_1125", "e4_1020", "8a_0923_smoothing_5", "8a_0923_smoothing_11", "8a_1015_smoothing", "e4_1020_smoothing"])
# multi_select = st.multiselect("好きな色",options=["赤","青","黄"])

# 可視化範囲
st.write("experimental period: 2023/9/10/18:00 - 2024/1/26/00:00")
start_date = st.date_input(
    "Start date",
    value = datetime(2023, 9, 10)
)
end_date = st.date_input(
    "End date",
    value = datetime(2023, 9, 11)
)
start_time = st.time_input(
    "When do you start?",
    time(18, 30),
    step=timedelta(minutes=30)
)
end_time = st.time_input(
    "When do you end?",
    value=time(18, 30),
    step=timedelta(minutes=30)
)
# st.write("Start date:", start_date)
# st.write("Start time:", start_time)
# st.write("End date:", end_date)
# st.write("End time:", end_time)
######################

# TODO: multiselectではlist方に対応が必要
DataPath = f"./data/{Floor}_{User[-2:]}.csv"
DataPath = f"./data/{Floor}_{User_and_DAY}.csv"
#DataPath = "./data/test.csv"
try:
    df = pd.read_csv(DataPath) # index: datatime
    df["time"] = pd.to_datetime(df["time"]).dt.tz_localize(None) + timedelta(hours=9)
except:
    st.error("No data found. Please check the Floor or User Box.")

# 可視化
# TODO: 複数人のデータを一括可視化
try:
    # 時間の範囲指定
    start_time = pd.to_datetime(start_date.strftime("%Y-%m-%d") + " " + start_time.strftime("%H:%M:%S"))
    end_time = pd.to_datetime(end_date.strftime("%Y-%m-%d") + " " + end_time.strftime("%H:%M:%S"))
    
    x = df["time"]
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
        
    st.plotly_chart(fig)

    # predictionごとの総時間
    st.write("Total time of visualization: ", end_time - start_time)
    df = df[(df["time"] >= start_time) & (df["time"] <= end_time)]
    st.write("Total time of room :", timedelta(seconds=int((df["prediction"]=="room").sum().sum())))
    st.write("Total time of Corridor Right :", timedelta(seconds=int((df["prediction"]=="Cor_R").sum().sum())))
    st.write("Total time of Corridor Left :", timedelta(seconds=int((df["prediction"]=="Cor_L").sum().sum())))

    ### RRSIとpredictionの可視化 ###
    # TODO: 処理が重すぎる→表示区間を1時間で固定などで対応したい
    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    # fig.add_trace(go.Scatter(x=df["time"], y=df["prediction"], name=User), secondary_y=False)
    # fig.add_trace(go.Scatter(x=df["time"], y=df["B_rssi"], mode='markers', name="B_rssi"), secondary_y=True)
    # fig.add_trace(go.Scatter(x=df["time"], y=df["L_rssi"], mode='markers', name="L_rssi"), secondary_y=True)
    # if Floor == "F1":
    #     fig.add_trace(go.Scatter(x=x, y=df["R_rssi"], mode='markers', name="R_rssi"), secondary_y=True)
    # else:
    #     fig.add_trace(go.Scatter(x=x, y=df["F_rssi"], mode='markers', name="F_rssi"), secondary_y=True)
    # fig.update_traces(marker_size=6)
    # # タイトル
    # fig.update_layout(title="Prediction with RSSI")
    # fig.update_xaxes(rangeslider={"visible":True})
    # st.plotly_chart(fig)

except:
    st.error("No data found. Please check the date and time.")

