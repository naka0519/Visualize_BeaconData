import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# タイトル
st.write("Suntory beacon data visualization")

# データを選択（選択でファイルpath指定）
# csvを読み込む前提バージョン（事前に抽出が必要）
# TODO: データベース連携
Floor = st.selectbox("Floor", ["1F", "2F", "3F"])
Person_Num = st.radio("可視化する人数", ["1", "2", "3"])
User = st.selectbox("User", ["User1", "User2", "User3"])
# multi_select = st.multiselect("好きな色",options=["赤","青","黄"])
age = st.slider("How old are you?", 0, 130, 25)
# 可視化範囲
start_time = st.slider(
    "When do you start?",
    value=datetime(2023, 11, 4, 9, 30),
    format="MM/DD/YY - hh:mm"
)
end_time = st.slider(
    "When do you end?",
    value=datetime(2023, 11, 4, 10, 30),
    format="MM/DD/YY - hh:mm"
)
st.write("Start time:", start_time)
st.write("End time:", end_time)


DataPath = f"./data/{Floor}_{User}.csv"
DataPath = "./data/test.csv"

# 可視化
# TODO: 複数人のデータを一括可視化
try:
    df = pd.read_csv(DataPath) # index: datatime

    #x = df.index
    x = pd.to_datetime(df["time"]) + timedelta(hours=9)
    y = df["prediction"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name=User))
    #fig.show()
    st.plotly_chart(fig)

except:
    st.error("No data found. Please check the Floor or User Box.")