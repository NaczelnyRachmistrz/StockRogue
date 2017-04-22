import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as off
def plot_preprocess(company_data, predicted_data, start_data):
    """Preprocessing function for plot creation. It returns only data from some period of time
    (beginning from start_data)"""
    preprocessed_data = []
    for el in company_data:
        if el["data"] >= start_data:
            preprocessed_data.append(el)

    preprocessed_data += predicted_data

    return preprocessed_data

def create_plot(plot_data, company):

    pl_data = [el["data"] for el in plot_data]
    pl_kurs_max = [el["kurs_max"] for el in plot_data]
    pl_kurs_min = [el["kurs_min"] for el in plot_data]

    trace_max = go.Scatter(
        x=pl_data,
        y=pl_kurs_max,
        name=company + "- kurs maksymalny",
        line=dict(color='#17BECF'),
        opacity=0.8)

    trace_min = go.Scatter(
        x=pl_data,
        y=pl_kurs_min,
        name=company + "- kurs minimalny",
        line=dict(color='#7F7F7F'),
        opacity=0.8)

    data = [trace_max, trace_min]

    layout = dict(
        title='Notowania spółki' + company,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        )
    )

    fig = dict(data=data, layout=layout)
    off.plot(fig, filename="Notowania spółki " + company + ".html")

    off.offline.plot(data)
