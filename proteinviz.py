import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('/Users/Tytyty/Desktop/test_result.csv')

PAGE_SIZE = 6

app.layout = html.Div(
    className="row",
    children=[
        html.Div(
            dash_table.DataTable(
                id='table-paging-with-graph',
                columns=[
                    {"name": i, "id": i} for i in sorted(df.columns)
                ],
                page_current=0,
                page_size=20,
                page_action='custom',

                filter_action='custom',
                filter_query='',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[]
            ),
            style={'height': 350, 'overflowY': 'scroll'},
            className='six columns'
        ),
        html.Div(
            id='table-paging-with-graph-container',
            className="five columns"
        )
    ]
)

operators = [['eq ', '=='],
             ['contains ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if v0 == value_part[-1] and v0 in ("'", '"', '`'):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('table-paging-with-graph', "filter_query")])
def update_table(page_current, page_size, filters):
    filtering_expressions = filters.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator == 'eq':
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]

    return dff.iloc[
        page_current*page_size: (page_current + 1)*page_size
           ].to_dict('records')


@app.callback(
    Output('table-paging-with-graph-container', "children"),
    [Input('table-paging-with-graph', "data")])
def update_graph(rows):
    dff = pd.DataFrame(rows)
    return html.Div(
        [
            dcc.Graph(
                id='column',
                figure={
                    "data": [
                        {
                            "x": dff["ProteinName"],
                            "y": dff["ProteinName"], #change to range(0, max) how?
                            "type": "bar",
                            "marker": {"color": "#0072D9"},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 300,
                        "margin": {"t": 0, "l": 10, "r": 10},
                    },
                },
            )

        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)













