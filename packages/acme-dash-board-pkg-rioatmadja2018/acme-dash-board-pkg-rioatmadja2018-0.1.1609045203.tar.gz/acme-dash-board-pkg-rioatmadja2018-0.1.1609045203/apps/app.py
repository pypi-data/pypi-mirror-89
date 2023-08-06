import dash 
import pandas as pd 
import numpy as np 
from base64 import urlsafe_b64decode 
import seaborn as sns 

# ACME Libraries 
from acme_collectors.engines.mysql_engine import MySQLEngine 

# Dash libraries 
import dash_core_components as doc 
import dash_html_components as html 
import plotly.express as px 
import plotly as plt 
import plotly.graph_objects as go
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output

# alias 
from typing import Dict, List 
from pandas.core.frame import DataFrame 
from pandas.core.series import Series 

# constants 
MONTHS: Dict = dict(zip(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 
                        [ f"0{month}" if month < 10 else month for month in  range(1,13)] 
                       ) 
                   )

def format_date(current_date:str) -> str: 
    """
    Description
    -----------
    Helper function to format the given string of date, so it can be parsed by the Pandas utilities. 
    
    Paramters
    ---------
    :param current_date: given a valid current_date 
    
    Returns
    -------
    :return: return date of string in "%m/%d/%Y"
    
    Examples
    ---------
    >>> pd.to_datetime(justpasteit_df['date_created'].astype(str).apply(format_date), format="%m/%d/%Y" ) # format the strings, so they can be converted to pandas datetime object. 
    >>> 0      2015-05-27
        1      2014-11-27
        2      2015-03-15
        3      2014-08-29
    """
    
    if not current_date:
        raise ValueError("Error: current_date can't be empty.")
    
    try:

        current_dates: List[str] = current_date.replace(',','').split(' ')
        if len(current_dates) == 1:
            return datetime.utcnow().strftime('%m/%d/%Y') 
        
        else:
            month, day, year = current_dates if len(current_dates) == 3 else (*current_dates, '2020')
            return f"{MONTHS.get(month)}/{day}/{year}"
    
    except AttributeError as e:
        raise AttributeError("The string must be in Month date, Year fromat.") from e 

# conncet to local MySQL database on Ubuntu 20.04 LTS 
mysql_engine = MySQLEngine(host='127.0.0.1', user='cloud_user')
SQL_QUERY: str = """
    SELECT  jp.date_created, 
            jp.number_views,
            jp.search_keyword, 
            jp.language AS `Post Language`,

            mpt.tone_name,
            mpt.score AS `Tone Scores`, 
            mpt.sentiment_polarity ,
            mpt.post_url

    FROM justpasteit_posts jp 
    LEFT JOIN main_post_tone mpt ON mpt.post_url = jp.url
""" 
posts_df: DataFrame = pd.read_sql_query(SQL_QUERY, con=mysql_engine.conn)
posts_df['date_created'] = pd.to_datetime( posts_df['date_created'].apply(format_date) ) 
posts_df['number_views'] = posts_df['number_views'].apply(lambda post: eval(urlsafe_b64decode(post.encode('utf-8')).decode('utf-8').replace(',','')))

post_sentiment_trends = posts_df.set_index('date_created')['sentiment_polarity'].resample('M').mean().dropna() 
post_numberviews_trends = posts_df.set_index('date_created')['number_views'].resample('M').mean().dropna() 

# Load embedded messages from MySQL database 
SQL_QUERY_EMBEDDED_MSG: str = """
    SELECT jp.date_created,
        iuj.language,
        eit.tone_name,
        eit.score 
        
    FROM image_urls_justpasteit iuj 
    LEFT JOIN embedded_image_tones eit ON eit.url = iuj.image_url
    LEFT JOIN justpasteit_posts jp ON jp.url = iuj.post_url 
"""

embedded_messages_df: DataFrame = pd.read_sql_query(SQL_QUERY_EMBEDDED_MSG, con=MySQLEngine(host='127.0.0.1', user='cloud_user').conn)
embedded_messages_df = embedded_messages_df.dropna(subset=['tone_name','score'])
embedded_messages_df['date_created'] = pd.to_datetime( embedded_messages_df['date_created']) 
embedded_messages_df = embedded_messages_df.pivot_table(values='tone_name', index='date_created', columns='language', aggfunc='count').rename({'ar': 'Arabic', 
                                                                                                                        'en': 'English', 
                                                                                                                        'it': 'Italian', 
                                                                                                                        'ja':'japanese', 
                                                                                                                        'tr':'Turkish'
                                                                                                                       },axis=1)


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
    app.run_server(debug=True, host="0.0.0.0", port="8000")