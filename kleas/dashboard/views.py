from django_pandas.io import read_frame
from django.shortcuts import render
from expenses.models import ExpensesRestock, ExpensesStore
from django.contrib.auth.decorators import login_required
import plotly.graph_objects as go
from sales.models import Sale
import plotly.express as px
import pandas as pd
import warnings
import plotly
import json

warnings.simplefilter(action='ignore', category=FutureWarning)

@login_required
def dashboard(request):
    
    # load database models
    sales = Sale.objects.all()
    restock_expenses = ExpensesRestock.objects.all()
    store_expenses = ExpensesStore.objects.all()

    # convert Sale model into dataframes
    sales_df = read_frame(sales)
    sales_df.purchase_date = pd.to_datetime(
        sales_df['purchase_date'], format='%m/%d/%y %I:%M%p')

    # convert Expenses model into dataframes
    restock_expenses_df = read_frame(restock_expenses)
    restock_expenses_df.purchase_date = pd.to_datetime(
        restock_expenses_df['purchase_date'], format='%m/%d/%y %I:%M%p')
    store_expenses_df = read_frame(store_expenses)
    store_expenses_df.date = pd.to_datetime(
        store_expenses_df['date'])

    # compute for gross income
    revenue = get_revenue(sales_df)
    total_expenses = get_expenses(restock_expenses_df, store_expenses_df)
    gross_income = compute_gross_income(revenue, total_expenses)

    # aggregate total number of sales and expenses
    total_num_sales = get_total_sales(sales_df)
    total_num_expenses = get_total_num_expenses(restock_expenses_df, store_expenses_df)

    # generate graphs
    sales_trend_graph = get_sales_trend_graph(sales_df)
    category_item_graph = get_category_item_breakdown_graph(sales_df)
    revenue_trend_graph = get_revenue_trend_graph(sales_df) if sales else None
    

    expenses_trend_graph = get_expenses_trend_graph(restock_expenses_df, 
                    store_expenses_df) if (restock_expenses and store_expenses) else None

    context = {
        'revenue': revenue,
        'total_expenses': total_expenses,
        'gross_income': gross_income,

        'total_num_sales': total_num_sales,
        'total_num_expenses': total_num_expenses,

        'revenue_trend_graph': revenue_trend_graph,
        'expenses_trend_graph': expenses_trend_graph,
        'sales_trend_graph' : sales_trend_graph,
        'category_item_graph': category_item_graph,
    }
    return render(request, 'dashboard/dashboard.html', context=context)

def get_revenue(df):

    # compute for total revenue
    df['total_price'] = df['price'] * df['quantity']
    revenue = float(df['total_price'].sum())
    return revenue

def get_expenses(restock, store):

    # compute expenses on restock
    restock['total_price'] = restock['price'] * restock['quantity']
    restock_expenses = float(restock['total_price'].sum())

    # compute expenses on store
    store_expenses = float(store['amount'].sum())

    # return total expenses
    return float(restock_expenses + store_expenses)


def compute_gross_income(revenue, expenses):

    # compute for gross income
    gross_income = revenue - expenses
    return gross_income


def get_total_sales(df):

    # aggregate total number of sales
    total_sales = int(df['quantity'].sum())
    return total_sales


def get_total_num_expenses(restock, store):

    # aggrate total number of expenses
    total_expenses = int(restock['quantity'].sum())
    total_expenses += store.shape[0]
    return total_expenses


def get_revenue_trend_graph(df):

    # compute for total price
    df['total_price'] = df['price'] * df['quantity']

    # aggregate revenue per day
    revenue_per_day = df[['purchase_date', 'total_price']].resample(
        'D', on='purchase_date').sum().reset_index()
    
    fig = px.bar(revenue_per_day, 
                x='purchase_date',
                y='total_price',
                labels={
                    "value": "Sales",
                    "purchase_date": "Date",
                    "total_price": "Total Revenue (₱)"
                    }, 
                title='Revenue Trend',
                color_discrete_sequence=['#6FBAF7','#007CFF','#002CB8', '#482CAF']
                )

    fig.add_trace(go.Scatter(
                x=revenue_per_day.purchase_date,
                y=revenue_per_day.total_price,
                showlegend=False,
                line_color='#002CB8'
            ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#E2F2FF'
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_expenses_trend_graph(restock, store):
    
    # compute total price
    restock['total_price'] = restock['price'] * restock['quantity']
    # aggregate restock expenses per month
    restock_expenses_per_month = restock[['purchase_date', 'total_price']].resample(
        'M', on='purchase_date').sum().reset_index()
    restock_expenses_per_month['purchase_date'] = restock_expenses_per_month['purchase_date'].apply(
        lambda dt: dt.replace(tzinfo=None))
    
    # aggregate store expenses per month
    store_expenses_per_month = store[['date', 'amount']].resample(
        'M', on='date').sum().reset_index()
    

    merge_data = pd.merge(restock_expenses_per_month, 
                          store_expenses_per_month, 
                          how='outer',
                          left_on='purchase_date',
                          right_on='date')
    merge_data.rename(columns={'amount': 'store', 'total_price': 'restock'}, 
                    inplace=True)
    merge_data.drop(columns=['purchase_date'], inplace=True)

    fig = px.bar(merge_data, 
                x='date',
                y=merge_data.columns,
                labels={
                    "date": "Date",
                    "value": "Total Expenses (₱)"
                    }, 
                title='Expenses Trend',
                barmode='group',
                color_discrete_sequence=['#6FBAF7','#007CFF','#002CB8', '#482CAF'])

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#E2F2FF'
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_sales_trend_graph(df):

    # generate total # of sales per category
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
                barmode='group',
                color_discrete_sequence=['#6FBAF7','#007CFF','#002CB8', '#482CAF'],
                )
    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#E2F2FF'
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    

def get_category_item_breakdown_graph(df):

    # generate total sales by category and item

    fig = px.sunburst(df, path=['category', 'item'], 
                      values='quantity', 
                      title='Sales by Category and Item',
                      color_discrete_sequence=['#482CAF','#002CB8','#6FBAF7','#007CFF'])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#E2F2FF'
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)