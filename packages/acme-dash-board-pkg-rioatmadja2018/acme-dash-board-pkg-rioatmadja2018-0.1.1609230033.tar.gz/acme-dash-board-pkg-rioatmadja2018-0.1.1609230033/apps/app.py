import dash 
import pandas as pd 
import numpy as np 
from base64 import urlsafe_b64decode 
import seaborn as sns 
import os 

# ACME Libraries 

# Dash libraries 
import dash_core_components as doc 
import dash_html_components as html 
import plotly.express as px 
import plotly as plt 
import plotly.graph_objects as go
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output
import sqlite3 

# alias 
from typing import Dict, List 
from pandas.core.frame import DataFrame 
from pandas.core.series import Series 

APP_PATH: str = '/var/www/html/apps'
csv_files: List[str]  = ['main_posts.csv' , 'embedded_messages.csv' ] 
file_unions: set = set(csv_files) & set(os.listdir(APP_PATH))

if not file_unions:
    raise FileNotFoundError(f"Error: Please provide the following files {' , '.join(csv_files)}")
    
# Load the main posts from the local sqlite 
posts_df: DataFrame = pd.read_csv(os.path.join(APP_PATH,"main_posts.csv"))
posts_df['date_created'] = pd.to_datetime( posts_df['date_created'] ) 
post_sentiment_trends = posts_df.set_index('date_created')['sentiment_polarity'].resample('M').mean().dropna() 
post_numberviews_trends = posts_df.set_index('date_created')['number_views'].resample('M').mean().dropna() 

# Load the embedde posts from the local sqlite 
embedded_messages_df: DataFrame = pd.read_csv(os.path.join( APP_PATH,"embedded_messages.csv"))
embedded_messages_df.index = pd.to_datetime( embedded_messages_df['date_created'] )
embedded_messages_df.drop('date_created', axis=1, inplace=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# make subplots of posts sentiment and number of views 
fig = plt.subplots.make_subplots(rows=3, cols=2, subplot_titles=("Trends in Sentiment Polarity", "Trends in Number of Views", "Frequency of the Tones", "Frequency of the Topics and the Tones", "Monthly trends of the language used in the post. ".title(), "Number of Languages embedded inside the images".title()))
fig.add_trace(go.Scatter(x=post_sentiment_trends.index.tolist(), y=post_sentiment_trends.tolist(), name='Sentiment Polarity'), row=1, col=1)
fig.add_trace(go.Scatter(x=post_numberviews_trends.index.tolist(), y=post_numberviews_trends.tolist(), name='Number of Views'), row=1, col=2)

colors: List = sns.color_palette(palette='ocean_r', n_colors=100)
tones, freq_tones = zip(*posts_df.groupby(['tone_name']).size().sort_values(ascending=False).to_dict().items())
fig.add_trace(go.Bar(x=list(tones), y=list(freq_tones), name='By Tone and Languages', marker=dict(color=colors, coloraxis='coloraxis'), marker_color='crimson' ), row=2, col=1)

# topics by the tones
by_topics: DataFrame = posts_df.groupby(['search_keyword','tone_name']).size().unstack('search_keyword')
by_topics.columns = pd.Series( by_topics.columns).astype(str).apply(lambda topic: topic.replace('_', ' ').title())

for index,topic in enumerate(by_topics.columns.tolist()): 
    fig.add_trace(go.Bar(x=by_topics[topic].sort_values(ascending=False).index.tolist(), y=by_topics[topic].sort_values(ascending=False).tolist(), text=topic, name=topic, showlegend=True), row=2, col=2 )

# monthly frequency of the language used in the post. 
line_colors: List[tuple] = [sns.dark_palette('blue')[0], sns.dark_palette('red')[-1]]
monthly_lang_freq: DataFrame = posts_df.pivot_table(values='tone_name', index='date_created', columns='Post Language', aggfunc='count').interpolate().resample('M').mean().rename({'ar':'Arabic', 'en':'English'}, axis=1).interpolate()
for index,lang in enumerate(monthly_lang_freq.columns.tolist()):
    fig.add_trace(go.Scatter(x=monthly_lang_freq.index.tolist() , y=monthly_lang_freq[lang].tolist(), name=lang, mode='lines+markers', marker_color=line_colors[index]), row=3, col=1)

# Language in embedded messages    
for column in embedded_messages_df.columns.tolist():
    current_df: DataFrame = embedded_messages_df[column].resample('M').mean().interpolate() 
    fig.add_trace(go.Scatter(x=current_df.index.tolist(), y=current_df.tolist(), name=column, mode='lines+markers'), row=3, col=2)

# y-axis labels
fig.update_yaxes(title_text="Sentiment Polarity Scores", row=1, col=1)
fig.update_yaxes(title_text="Number of Views", row=1, col=2)
fig.update_yaxes(title="Number of Posts", row=3, col=1)
fig.update_yaxes(title="Number of Posts", row=3, col=2)

fig.update_layout(width=1500, height=1000)
app.layout = html.Div(children=[html.H1(children='Text Mining and Analysis: Islamic State Recruitment' , style={'textAlign':'center', 'color': 'black'}), doc.Graph(id='page-content',figure=fig)], style={'background-image':'url(https://www.teahub.io/photos/full/165-1650027_mountain-backgrounds-download-desktop-desktop-wallpapers-mountain-wallpaper.jpg)', 'height': '100%'})

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8000")