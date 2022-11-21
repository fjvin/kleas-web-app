from django.shortcuts import render
from sales.models import Sale

from django_pandas.io import read_frame
import plotly.express as px
import pandas as pd
import plotly
import json

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Create your views here.

def dashboard(request):
    
    sales = Sale.objects.all()
    df = read_frame(sales)
    df.purchase_date = pd.to_datetime(df['purchase_date'],format='%m/%d/%y %I:%M%p')
    
    sales_graph = get_sales_trend_graph(df)
    category_item_graph = get_category_item_breakdown_graph(df)


    context = {
        'sales_graph' : sales_graph,
        'category_item_graph': category_item_graph,
    }
    return render(request, 'dashboard/dashboard.html', context=context)


def get_sales_trend_graph(df):
    sales_df = df[['purchase_date', 'category', 'quantity']]
    sales_df = df.assign(key=df.groupby('category').cumcount()).pivot(
        'purchase_date','category','quantity')
    sales_df = sales_df.groupby(pd.Grouper(freq='D')).sum().reset_index()
    
    fig = px.line(sales_df, 
                x='purchase_date',
                y=sales_df.columns,
                labels={
                    "value": "Sales",
                    "purchase_date": "Date",
                    "category": "Clothes Category"
                    }, 
                title='Sales Trend')
    fig.update_xaxes(rangeslider_visible=True)
    

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_category_item_breakdown_graph(df):
    fig = px.sunburst(df, path=['category', 'item'], 
                      values='quantity', 
                      title='Sales by Category and Item Breakdown')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)