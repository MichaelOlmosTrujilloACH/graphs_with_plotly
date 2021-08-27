import pandas as pd
import plotly.express as px
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from vega_datasets import data
barley_data_set = data.barley()


app = dash.Dash(__name__)
server = app.server
# Verifying if there are na values in the dataframe
print(barley_data_set.isnull().values.any())

print(barley_data_set[:5])

# Times series
# barley_data_set_groups = barley_data_set.groupby(['year', 'site'])['yield'].groups.keys()
# print(barley_data_set_groups)
barley_data_set_median_series = barley_data_set.groupby(['year', 'site'])[
    'yield'].apply(np.median)
print(barley_data_set_median_series)
barley_data_set_median_df = pd.DataFrame(
    {'Median of yield': barley_data_set_median_series}).reset_index()
print(barley_data_set_median_df)

# bar chart
barley_variety_site_series = barley_data_set.groupby(['variety', 'site'])[
    'yield'].apply(np.sum)
barley_variety_site_df = pd.DataFrame(
    {'sum_of_yield_by_site': barley_variety_site_series}).reset_index()
print(barley_variety_site_df)
barley_variety_site_sum_yield_series = barley_data_set.groupby(['variety'])[
    'yield'].apply(np.sum)
barley_variety_site_sum_yield_df = pd.DataFrame(
    {'Sum of yield': barley_variety_site_sum_yield_series}).reset_index()
print(barley_variety_site_sum_yield_df)
merge_sum_yield_df_variety_site_df = pd.merge(left=barley_variety_site_df,
                                              right=barley_variety_site_sum_yield_df,
                                              left_on='variety', right_on='variety')
print(merge_sum_yield_df_variety_site_df)

fig1 = px.line(barley_data_set_median_df, x='year',
               y=barley_data_set_median_df['Median of yield'],
               title='Median of yield by year and site',
               line_group=barley_data_set_median_df['site'],
               color=barley_data_set_median_df['site'])

fig2 = px.bar(merge_sum_yield_df_variety_site_df, x='variety',
              y='sum_of_yield_by_site', color='site', title='Sum of yield by variety and site')

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children='Dashboard of Barley data set',
                        style={'text-align': 'center'}),
                html.Div(
                    children='''
            A dashboard test with plotly/dash
            ''',
                    style={'text-align': 'center'}
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='time_series',
                            figure=fig2,
                            style={'display': 'inline-block', 'width': '50%',
                                    'background-color':'rgba(135, 144, 11)'
                                    }
                        ),
                        dcc.Graph(
                            id='bar_chart',
                            figure=fig1,
                            style={'display': 'inline-block', 'width': '50%',
                                    'background-color':'rgba(135, 144, 11)'
                            }
                        )
                    ],
                    
                )
            ],
        )


    ],
    style={'background-color': 'black', 'color': 'white'}
)

# fig.show()

if __name__ == '__main__':
    app.run_server(debug=True)
