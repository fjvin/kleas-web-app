from django_pandas.io import read_frame
from django.shortcuts import render
from expenses.models import ExpensesRestock, ExpensesStore
from django.contrib.auth.decorators import login_required
from sales.models import Sale
import plotly.express as px
import pandas as pd
import warnings
import plotly
import json

warnings.simplefilter(action='ignore', category=FutureWarning)

@login_required
def dashboard(request):
    
    sales = Sale.objects.all()
    restock_expenses = ExpensesRestock.objects.all()
    store_expenses = ExpensesStore.objects.all()

    sales_df = read_frame(sales)
    sales_df.purchase_date = pd.to_datetime(
        sales_df['purchase_date'],format='%m/%d/%y %I:%M%p')

    restock_expenses_df = read_frame(restock_expenses)
    store_expenses_df = read_frame(store_expenses)

    revenue = get_revenue(sales_df)
    total_sales = get_total_sales(sales_df)
    total_expenses = get_total_expenses(restock_expenses_df,
                                        store_expenses_df)

    sales_graph = get_sales_trend_graph(sales_df)
    category_item_graph = get_category_item_breakdown_graph(sales_df)

    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'revenue': revenue,
        'sales_graph' : sales_graph,
        'category_item_graph': category_item_graph,
    }
    return render(request, 'dashboard/dashboard.html', context=context)

def get_revenue(df):
    df['total_price'] = df['price'] * df['quantity']
    revenue = float(df['total_price'].sum())
    return revenue

def get_total_sales(df):
    total_sales = int(df['quantity'].sum())
    return total_sales

def get_total_expenses(restock, store):
    total_expenses = int(restock['quantity'].sum())
    total_expenses += store.shape[0]
    return total_expenses


def get_sales_trend_graph(df):
    sales_df = df[['purchase_date', 'category', 'quantity']]
    sales_df = df.assign(key=df.groupby('category').cumcount()).pivot(
        'purchase_date','category','quantity')
    sales_df = sales_df.groupby(pd.Grouper(freq='D')).sum().reset_index()
    
    fig = px.bar(sales_df, 
                x='purchase_date',
                y=sales_df.columns,
                labels={
                    "value": "Sales",
                    "purchase_date": "Date",
                    "category": "Clothes Category"
                    }, 
                title='Sales Trend',
                barmode='group')
    fig.update_xaxes(rangeslider_visible=True)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_category_item_breakdown_graph(df):
    fig = px.sunburst(df, path=['category', 'item'], 
                      values='quantity', 
                      title='Sales by Category and Item')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
