import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt


st.write("hello streamlit")

xs = np.linspace(0, 10, 100)
sins = np.sin(xs)
randoms = np.random.rand(100)

fig = go.Figure()
fig.add_trace(go.Scatter(x=xs, y=sins, name="sin"))
fig.add_trace(go.Scatter(x=xs, y=randoms, name="random"))
fig.show() # 上と同じ結果