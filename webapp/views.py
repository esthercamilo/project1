import os

import numpy
import pandas as pandas
import scipy
from django.shortcuts import render
import plotly.graph_objects as go
import plotly as plotly
from scipy.stats import ttest_ind, mannwhitneyu

from project1.settings import BASE_DIR
from scipy import stats


def statistics_view(request):

    path_to_sav = os.path.join(BASE_DIR, 'dataset/archive/1ResearchProjectData.sav')
    df = pandas.read_spss(path_to_sav)
    df = df[~df['Score'].isna()]

    wesson = pandas.to_numeric(df[df['wesson'] == 'Wesson']['Score'], errors="coerce")
    rug_smith = pandas.to_numeric(df[df['wesson'] == 'Ruger_Smith']['Score'], errors="coerce")

    fig_dist_wesson = go.Figure(
        data=[go.Histogram(x=wesson)],
        layout_title_text="Distribuição Wesson"
    )

    fig_dist_rug_smith = go.Figure(
        data=[go.Histogram(x=rug_smith)],
        layout_title_text="Distribuição Ruger_Smith"
    )
    graph_div_dist_wesson = plotly.offline.plot(fig_dist_wesson, auto_open=False, output_type="div")
    graph_div_dist_rug_smith = plotly.offline.plot(fig_dist_rug_smith, auto_open=False, output_type="div")

    mtc = ["count", "min", "max", "median", "mean"]
    metrics_wesson = wesson.agg(mtc)
    fig_summ_wesson = go.Figure(data=[go.Table(header=dict(values=mtc),
                                   cells=dict(values=[[x] for x in metrics_wesson.values]))])
    tbl_summ_wesson = plotly.offline.plot(fig_summ_wesson, auto_open=False, output_type="div")

    metrics_rugsmith = rug_smith.agg(mtc)
    fig_summ_rugsmith = go.Figure(data=[go.Table(header=dict(values=mtc),
                                   cells=dict(values=[[x] for x in metrics_rugsmith.values]))])
    tbl_summ_rugsmith = plotly.offline.plot(fig_summ_rugsmith, auto_open=False, output_type="div")

    # Calculando significância Mann-Whitney
    l1 = [x for x in list(wesson) if x]
    l2 = [x for x in list(rug_smith) if x != numpy.nan]
    stat, p = mannwhitneyu(l1,l2)


    context = {"graph_dist_wesson": graph_div_dist_wesson,
               "metrics_agg_wesson": tbl_summ_wesson,
               "metrics_agg_rugsmith": tbl_summ_rugsmith,
               "graph_div_dist_rug_smith": graph_div_dist_rug_smith,
               "p_value": p}
    return render(request, "statistics.html", context)