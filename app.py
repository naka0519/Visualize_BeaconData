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
# TODO: データベースから取得するように変更
Floor = st.selectbox("Floor", ["1F", "2F", "3F"])
User = st.selectbox("User", ["User1", "User2", "User3"])

DataPath = f"./data/{Floor}_{User}.csv"
DataPath = "./data/test.csv"
# 可視化
df = pd.read_csv(DataPath) # index: datatime

#x = df.index
x = pd.to_datetime(df["time"]) + timedelta(hours=9)
y = df["prediction"]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, name=User))
#fig.show()
st.plotly_chart(fig)