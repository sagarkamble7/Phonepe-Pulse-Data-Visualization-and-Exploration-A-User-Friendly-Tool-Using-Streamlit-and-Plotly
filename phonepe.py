import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import  mysql.connector
import requests
import json
from PIL import Image

# dataframes
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Sagar72427',
    port=3306,
    database='phonepe_database',
    auth_plugin='mysql_native_password'
)
cursor = mydb.cursor()

# aggregated_insurance:
cursor.execute('''select * from aggregated_insurance_table''')
table1 = cursor.fetchall()
mydb.commit()
aggregated_insurance_df = pd.DataFrame(table1, columns=("States","Years", "Quarter", "name", "Transaction_count", "Transaction_amount"))


# aggregated_transaction:
cursor.execute('''select * from aggregated_transaction_table''')
table2 = cursor.fetchall()
mydb.commit()
aggregated_transaction_df = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


# aggregated_user:
cursor.execute('''select * from aggregated_user_table''')
table3 = cursor.fetchall()
mydb.commit()
aggregated_user_df = pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))


# map_insurance:
cursor.execute('''select * from map_insurance_table''')
table4 = cursor.fetchall()
mydb.commit()
map_insurance_df = pd.DataFrame(table4, columns=("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))


# map_transaction:
cursor.execute('''select * from map_transaction_table''')
table5 = cursor.fetchall()
mydb.commit()
map_transaction_df = pd.DataFrame(table5, columns=("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))


# map_user:
cursor.execute('''select * from map_user_table''')
table6 = cursor.fetchall()
mydb.commit()
map_user_df = pd.DataFrame(table6, columns=("States", "Years", "Quarter", "District", "RegisteredUser", "AppOpens"))


# top_insurance:
cursor.execute('''select * from top_insurance_table''')
table7 = cursor.fetchall()
mydb.commit()
top_insurance_df = pd.DataFrame(table7, columns= ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))
                                

# top_transaction:
cursor.execute('''select * from top_transaction_table''')
table8 = cursor.fetchall()
mydb.commit()
top_transaction_df = pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


# top_user:
cursor.execute('''select * from top_user_table''')
table9 = cursor.fetchall()
mydb.commit()
top_user_df = pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes", "registeredusers"))



def transaction_amount_count_year(df, year):
    tacy = df[df["Years"] == year]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Blues_r,
                            height= 600, width= 650)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(tacyg, x = "States", y = "Transaction_count",title= f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Rainbow,
                            height= 600, width= 650)
        st.plotly_chart(fig_count)

    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_name = []
    for feature in data1["features"]:
         state_name.append(feature["properties"]["ST_NM"])

    state_name.sort()

    col1, col2 = st.columns(2)

    with col1:

        fig_India_1 = px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow", range_color= (tacyg["Transaction_amount"].min(),
                                tacyg["Transaction_amount"].max()), hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 650)
        fig_India_1.update_geos(visible= False)
        st.plotly_chart(fig_India_1)


    with col2:

        fig_India_2 = px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow", range_color= (tacyg["Transaction_count"].min(),
                                tacyg["Transaction_count"].max()), hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 650)
        fig_India_2.update_geos(visible= False)
        st.plotly_chart(fig_India_2)

    return tacy




def transaction_amount_count_year_qaurter(df, quarter):
    tacy = df[df["Quarter"]== quarter]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1, col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_amount",title= f"{tacy['Years'].min()} YEAR {quarter}rd QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count = px.bar(tacyg, x = "States", y = "Transaction_count",title= f"{tacy['Years'].min()} YEAR {quarter}rd QUARTER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_count)

    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_name = []
    for feature in data1["features"]:
         state_name.append(feature["properties"]["ST_NM"])

    state_name.sort()

    col1, col2 = st.columns(2)
    with col1:
        fig_India_1 = px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow", range_color= (tacyg["Transaction_amount"].min(),
                                tacyg["Transaction_amount"].max()), hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter}rd QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 650)
        fig_India_1.update_geos(visible= False)
        st.plotly_chart(fig_India_1)


    with col2:
        fig_India_2 = px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow", range_color= (tacyg["Transaction_count"].min(),
                                tacyg["Transaction_count"].max()), hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter}rd QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 650)
        fig_India_2.update_geos(visible= False)
        st.plotly_chart(fig_India_2)

    return tacy


def aggre_tran_transaction_type(df, state):
    tacy = df[df["States"]== state]
    tacy.reset_index(drop= True, inplace= True)


    tacyg = tacy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    google_colors = ["#4285F4", "#34A853", "#FBBC05", "#EA4335", "#FF6D00", "#1A73E8", "#DB4437", "#F4B400", "#0F9D58"]

    col1, col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_amount",
                        width=650, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5, color_discrete_sequence=google_colors )
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_count",
                        width=650, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5, color_discrete_sequence=google_colors)
        st.plotly_chart(fig_pie_2)


def aggre_user_plot_1(df, year):
    aguy = df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count", ].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyg, x= "Brands", y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline_r,
                    hover_name= "Brands")

    st.plotly_chart(fig_bar_1)

    return aguy


# aggregater user analysis 2
def aggre_user_plot_2(df, quarter):
    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop= True, inplace= True)
    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)


    fig_bar_1 = px.bar(aguyqg, x= "Brands", y= "Transaction_count", title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                    width= 800, color_discrete_sequence= px.colors.sequential.GnBu_r, hover_name = "Brands")

    st.plotly_chart(fig_bar_1)

    return aguyq


# aggre_user_analysis_
def aggre_user_plot_3(df, state):
    auyqs = df[df["States"] == state]
    auyqs.reset_index(drop = True, inplace = True)

    fig_line_1 = px.line(auyqs, x = "Brands", y = "Transaction_count", hover_data= ["Percentage"],
                        title = f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width = 1000, markers = True)
    st.plotly_chart(fig_line_1)



    # map_insurance_district
def map_insur_Districts(df, state):
    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    # tacyg = tacy.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    # tacyg.reset_index(inplace=True)

    google_colors = ["#4285F4", "#34A853", "#FBBC05", "#EA4335", "#FF6D00", "#1A73E8", "#DB4437", "#F4B400", "#0F9D58"]

    col1, col2 = st.columns(2)

    with col1:
        fig_bar_1 = px.bar(data_frame=tacy, x="Transaction_amount", y = "District", orientation="h",
                        height= 600,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=google_colors
                        )
        st.plotly_chart(fig_bar_1)
    
    with col2:
        fig_bar_2 = px.bar(data_frame=tacy, x="Transaction_count", y = "District", orientation="h",
                        height= 600,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=google_colors)
        st.plotly_chart(fig_bar_2)


# map user plot 1
def map_user_plot_1(df, year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)


    muyg = muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1 = px.line(muyg, x = "States", y = ["RegisteredUser", "AppOpens"],
                        title = f"{year} REGISTERED USER AND APPOPENS", width = 1000, height= 800, markers = True)
    st.plotly_chart(fig_line_1)

    return muy



# map user plot 2
def map_user_plot_2(df, quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)


    muyqg = muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1 = px.line(muyqg, x = "States", y = ["RegisteredUser", "AppOpens"],
                        title = f"{quarter} QUARTER REGISTERED USER AND APPOPENS", width = 1000, height= 800, markers = True)
    st.plotly_chart(fig_line_1)

    return muyq



# map_user_plot_3
def map_user_plot_3(df, state):
    muyqs = df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x= 'RegisteredUser', y= "District", orientation= "h",
                                    title = "REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Blues)

        st.plotly_chart(fig_map_user_bar_1)


    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x= 'AppOpens', y= "District", orientation= "h",
                                    title = "APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Blues)

        st.plotly_chart(fig_map_user_bar_2)
    


# top insurnace plot 1
def top_insurance_plot_1(df, state):
    tiy = df[df["States"] == "West Bengal"]
    tiy.reset_index(drop= True, inplace= True)

    # tiyg = tiy.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    # tiyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_top_insur_bar_1 = px.bar(tiy, x= 'Quarter', y= "Transaction_amount",
                                    title = "TRANSACTION AMOUNT", height= 650,width=600, color_discrete_sequence= px.colors.sequential.Darkmint)

        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2 = px.bar(tiy, x= 'Quarter', y= "Transaction_count",
                                    title = "TRANSACTION COUNT", height= 650, width= 600,color_discrete_sequence= px.colors.sequential.Redor_r)

        st.plotly_chart(fig_top_insur_bar_2)


def top_user_plot_1(df, year):
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)
    

    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarter"])["registeredusers", ].sum())
    tuyg.reset_index(inplace=True)


    fig_top_plot_1 = px.bar(data_frame= tuyg, x = "States", y="registeredusers", color="Quarter",width=1000, height= 800,
                            color_discrete_sequence= px.colors.sequential.Rainbow_r, hover_name= "States",
                            title= f"{year} REGISTERED USER")

    st.plotly_chart(fig_top_plot_1)

    return tuy
   

# top_user_plot_2
def top_user_plot_2(df, state):
    tuys = df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2 = px.bar(data_frame= tuys, x = "Quarter", y= "registeredusers", title= "REGISTERED USERS, PINCODE, QUARTER",
                            width= 1000, height= 800, color= "registeredusers", hover_name= "Pincodes", color_continuous_scale= px.colors.sequential.deep)

    st.plotly_chart(fig_top_plot_2)


# top chart :
def top_chart_transaction_amount(table_name):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sagar72427',
        port=3306,
        database='phonepe_database',
        auth_plugin='mysql_native_password'
    )
    cursor = mydb.cursor()

    # plot 1
    query1 = f'''SELECT States, sum(Transaction_amount) as Transaction_amount 
                FROM {table_name}
                group by States
                order by Transaction_amount desc
                limit 10;'''

    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("State", "Transaction amount"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "State", y = "Transaction amount",title= "Top 10 Transaction Amount.",hover_name= "State",
                            height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_amount)

    # plot 2
    query2 = f'''SELECT States, sum(Transaction_amount) as Transaction_amount 
                FROM {table_name}
                group by States
                order by Transaction_amount
                limit 10;'''

    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("State", "Transaction amount"))

    with col2:
        fig_amount_2 = px.bar(df_2, x = "State", y = "Transaction amount",title= "Least 10 Transaction amount.",hover_name= "State",
                              height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_amount_2)


    # plot 3
    query3 = f'''SELECT States, avg(Transaction_amount) as Transaction_amount 
                FROM {table_name}
                group by States
                order by Transaction_amount desc;'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("State", "Transaction amount"))
    fig_amount_3 = px.bar(df_3, x = "State", y = "Transaction amount",title= "Average Transaction Amount.",hover_name= "State",
                          width= 1000, height= 800,
                            color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig_amount_3)




def top_chart_transaction_count(table_name):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sagar72427',
        port=3306,
        database='phonepe_database',
        auth_plugin='mysql_native_password'
    )
    cursor = mydb.cursor()

    # plot 1
    query1 = f'''SELECT States, sum(Transaction_count) as Transaction_count 
                FROM {table_name}
                group by States
                order by Transaction_count desc
                limit 10;'''

    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("State", "Transaction count"))

    col1, col2 = st.columns(2)
    with col1:
        fig_count = px.bar(df_1, x = "State", y = "Transaction count",title= "Top 10 Transaction count.",hover_name= "State",
                            height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_count)

    # plot 2
    query2 = f'''SELECT States, sum(Transaction_count) as Transaction_count 
                FROM {table_name}
                group by States
                order by Transaction_count
                limit 10;'''

    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("State", "Transaction count"))

    with col2:
        fig_count_2 = px.bar(df_2, x = "State", y = "Transaction count",title= "Lat 10 Transaction count.",hover_name= "State",
                              height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_count_2)


    # plot 3
    query3 = f'''SELECT States, avg(Transaction_count) as Transaction_count 
                FROM {table_name}
                group by States
                order by Transaction_count desc;'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("State", "Transaction count"))
    fig_count_3 = px.bar(df_3, x = "State", y = "Transaction count",title= "Average Transaction count.",hover_name= "State",
                          width= 1000, height= 800,
                            color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig_count_3)



# top chart registered user:

def top_chart_registered_user(table_name, state):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sagar72427',
        port=3306,
        database='phonepe_database',
        auth_plugin='mysql_native_password'
    )
    cursor = mydb.cursor()

    # plot 1
    query1 = f'''SELECT District, sum(RegisteredUser) as RegisteredUser
                    FROM {table_name}
                    where States = '{state}'
                    group by District 
                    order by RegisteredUser desc
                    limit 10;'''

    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("districts", "registered user"))

    col1, col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(df_1, x = "districts", y = "registered user",title= "Top 10 REGISTERED USERS",hover_name= "districts",
                            height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_amount)

    # plot 2
    query2 = f'''SELECT District, sum(RegisteredUser) as RegisteredUser
                    FROM {table_name}
                    where States = '{state}'
                    group by District 
                    order by RegisteredUser 
                    limit 10;'''

    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("districts", "registered user"))

    with col2:

        fig_amount_2 = px.bar(df_2, x = "districts", y = "registered user",title= "BOTTOM 10 REGISTERED USER",hover_name= "districts",
                            height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_amount_2)


    # plot 3
    query3 = f'''SELECT District, avg(RegisteredUser) as RegisteredUser
                    FROM {table_name}
                    where States = '{state}'
                    group by District 
                    order by RegisteredUser;'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("districts", "registered user"))
    fig_amount_3 = px.bar(df_3, x = "districts", y = "registered user",title= "AVREAGE REGISTERED USER",hover_name= "districts",
                          height= 800, width= 1000,
                            color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig_amount_3)


# top chart appoens:

def top_chart_AppOpens(table_name, state):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sagar72427',
        port=3306,
        database='phonepe_database',
        auth_plugin='mysql_native_password'
    )
    cursor = mydb.cursor()

    # plot 1
    query1 = f'''SELECT District, sum(AppOpens) as AppOpens
                    FROM {table_name}
                    where States = '{state}'
                    group by District 
                    order by AppOpens desc
                    limit 10;'''

    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("districts", "AppOpens"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "districts", y = "AppOpens",title= "Top 10 AppOpens",hover_name= "districts",
                            height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_amount)

    # plot 2
    query2 = f'''SELECT District, sum(AppOpens) as AppOpens
                    FROM {table_name}
                    where States = '{state}'
                    group by District 
                    order by AppOpens 
                    limit 10;'''

    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("districts", "AppOpens"))

    with col2:
        fig_amount_2 = px.bar(df_2, x = "districts", y = "AppOpens",title= "BOTTOM 10 AppOpens",hover_name= "districts",
                            height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_amount_2)



    # plot 3
    query3 = f'''SELECT District, avg(AppOpens) as AppOpens
                    FROM {table_name}
                    where States = '{state}'
                    group by District 
                    order by AppOpens;'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("districts", "AppOpens"))
    fig_amount_3 = px.bar(df_3, x = "districts", y = "AppOpens",title= "AVREAGE registered user",hover_name= "districts",
                          height= 800, width= 1000,
                            color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig_amount_3)



    # top chart appoens:

def top_chart_registered_users(table_name):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sagar72427',
        port=3306,
        database='phonepe_database',
        auth_plugin='mysql_native_password'
    )
    cursor = mydb.cursor()

    # plot 1
    query1 = f'''SELECT States, sum(registeredusers) as registeredusers
                  FROM {table_name}
                  group by States
                  order by registeredusers desc
                  limit 10;'''

    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("States", "registeredusers"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "States", y = "registeredusers",title= "Top 10 REGISTERED USERS",hover_name= "States",
                            height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_amount)

    # plot 2
    query2 = f'''SELECT States, sum(registeredusers) as registeredusers
                  FROM {table_name}
                  group by States
                  order by registeredusers
                  limit 10;'''

    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("States", "registeredusers"))

    with col2:
        fig_amount_2 = px.bar(df_2, x = "States", y = "registeredusers",title= "BOTTOM 10 REGISTERED USERS",hover_name= "States",
                            height= 600, width= 650,
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_amount_2)


    # plot 3
    query3 = f'''SELECT States, avg(registeredusers) as registeredusers
                  FROM {table_name}
                  group by States
                  order by registeredusers;'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("States", "registeredusers"))
    fig_amount_3 = px.bar(df_3, x = "States", y = "registeredusers",title= "AVREAGE REGISTERED USER",hover_name= "States",
                          height= 800, width= 1000,
                            color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig_amount_3)


# streamlit:
st.set_page_config(page_title= 'phonepe', layout= 'wide', page_icon= "P")
st.title("Phonepe Pulse Data Visualization and Exploration:")

with st.sidebar:
    select = option_menu("menu",["HOME", "EXPLORE DATA","TOP CHARTS", "ABOUT"],
                        icons= ["house", "graph-up-arrow","bar-chart-line", "exclamation-circle"])
    
if select == "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.subheader("TECHNOLOGIES USED: ")
        st.write("****Github Cloning,****")
        st.write("****Python****")
        st.write("****Pandas****")
        st.write("****MySQL****")
        st.write("****Streamlit****")
        st.write("****Plotly****")
        
    with col2:
        st.image(Image.open(r"C:\Users\sagar\Desktop\Projects\phonepe.jpg"), width= 400)


elif select == "EXPLORE DATA":
    tab1, tab2, tab3 = st.tabs(["Aggregate", "Map", "Top"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            method1 = st.selectbox("select One",["Aggregate Insurance", "Aggregate Transaction", "Aggregate User"])
        
        if method1 == "Aggregate Insurance":

            col1, col2 = st.columns(2)

            with col1:
                years = st.selectbox("Select the Year",aggregated_insurance_df["Years"].unique())
            tac_y = transaction_amount_count_year(aggregated_insurance_df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select the Quarter",tac_y["Quarter"].unique())
            transaction_amount_count_year_qaurter(tac_y, quarters)


        elif method1 == "Aggregate Transaction":
            
            col1, col2 = st.columns(2)

            with col1:
                years = st.selectbox("Select the Year",aggregated_transaction_df["Years"].unique())
            aagre_tran_tac_y = transaction_amount_count_year(aggregated_transaction_df, years)

            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State", aagre_tran_tac_y["States"].unique())
            aggre_tran_transaction_type(aagre_tran_tac_y, state)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select the Quarter",aagre_tran_tac_y["Quarter"].unique())
            aggre_tran_tac_y_Q = transaction_amount_count_year_qaurter(aagre_tran_tac_y, quarters)

            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State_ty", aggre_tran_tac_y_Q["States"].unique())
            aggre_tran_transaction_type(aggre_tran_tac_y_Q, state)


        elif method1 == "Aggregate User":
            col1, col2 = st.columns(2)

            with col1:
                years = st.selectbox("Select the Year",aggregated_user_df["Years"].unique())
            aggre_user_Y = aggre_user_plot_1(aggregated_user_df, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select the Quarter",aggre_user_Y["Quarter"].unique())
            aggre_tran_user_y_Q = aggre_user_plot_2(aggre_user_Y, quarters)

            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State", aggre_tran_user_y_Q["States"].unique())
            aggre_user_plot_3(aggre_tran_user_y_Q, state)




    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            method2 = st.selectbox("select One",["Map Insurance", "Map Transaction", "Map User"])

        if method2 == "Map Insurance":
            
            col1, col2 = st.columns(2)

            with col1:
                years = st.selectbox("Select the Years",map_insurance_df["Years"].unique())
            map_insur_tac_Y = transaction_amount_count_year(map_insurance_df, years)

            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State", map_insur_tac_Y["States"].unique())
            map_insur_Districts(map_insur_tac_Y, state)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select the Quarters",map_insur_tac_Y["Quarter"].unique())
            map_insur_tac_Y_Q  = transaction_amount_count_year_qaurter(map_insur_tac_Y, quarters)

            
            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State_ty", map_insur_tac_Y_Q["States"].unique())
            map_insur_Districts(map_insur_tac_Y_Q, state)



        elif method2 == "Map Transaction":
            
            col1, col2 = st.columns(2)

            with col1:
                years = st.selectbox("Select the Years",map_transaction_df["Years"].unique())
            map_tran_tac_Y = transaction_amount_count_year(map_transaction_df, years)

            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State", map_tran_tac_Y["States"].unique())
            map_insur_Districts(map_tran_tac_Y, state)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select the Quarters",map_tran_tac_Y["Quarter"].unique())
            map_tran_tac_Y_Q  = transaction_amount_count_year_qaurter(map_tran_tac_Y, quarters)

            
            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State_ty", map_tran_tac_Y_Q["States"].unique())
            map_insur_Districts(map_tran_tac_Y_Q, state)



        elif method2 == "Map User":
            col1, col2 = st.columns(2)

            with col1:
                years = st.selectbox("Select the Years_mu",map_user_df["Years"].unique())
            map_user_Y = map_user_plot_1(map_user_df, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select the Quarters_mu",map_user_Y["Quarter"].unique())
            map_user_Y_Q  = map_user_plot_2(map_user_Y, quarters)

            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State_mu", map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state)


    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            method3 = st.selectbox("select One",["Top Insurance", "Top Transaction", "Top User"])

        if method3 == "Top Insurance":
            
            col1, col2 = st.columns(2)

            with col1:
                years = st.selectbox("Select the Years_ti",top_insurance_df["Years"].unique())
            top_insur_tac_Y = transaction_amount_count_year(top_insurance_df, years)

            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State_mu", top_insur_tac_Y["States"].unique())
            top_insurance_plot_1(top_insur_tac_Y, state)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select the Quarters_mu",top_insur_tac_Y["Quarter"].unique())
            top_insur_tac_Y_Q  = transaction_amount_count_year_qaurter(top_insur_tac_Y, quarters)




        elif method3 == "Top Transaction":
            
            col1, col2 = st.columns(2)

            with col1:
                years = st.selectbox("Select the Years_tt",top_transaction_df["Years"].unique())
            top_tran_tac_Y = transaction_amount_count_year(top_transaction_df, years)

            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State_tt", top_tran_tac_Y["States"].unique())
            top_insurance_plot_1(top_tran_tac_Y, state)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select the Quarters_mu",top_tran_tac_Y["Quarter"].unique())
            top_tran_tac_Y_Q  = transaction_amount_count_year_qaurter(top_tran_tac_Y, quarters)



        elif method3 == "Top User":
            ol1, col2 = st.columns(2)

            with col1:
                years = st.selectbox("Select the Years_tu",top_user_df["Years"].unique())
            top_user_Y = top_user_plot_1(top_user_df, years)

            col1, col2 = st.columns(2)

            with col1:
                state = st.selectbox("select the State_tu", top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y, state)

elif select == "TOP CHARTS":
    
    question = st.selectbox("select the question", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered user of Map User",
                                                    "9. Appopens and Map User",
                                                    "10. Registered User of Top User"])

    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance_table")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance_table")

    
    elif question == "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNTt")
        top_chart_transaction_amount("map_insurance_table")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance_table")

    elif question == "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance_table")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance_table")


    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction_table")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction_table")

    elif question == "5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction_table")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction_table")

    elif question ==  "6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction_table")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction_table")

    elif question ==  "7. Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user_table")


    elif question ==   "8. Registered user of Map User":
        
        states= st.selectbox("select a state",map_user_df["States"].unique()) 
        st.subheader("registered user")
        top_chart_registered_user("map_user_table", "states")


    elif question ==   "9. Appopens and Map User":
        
        states= st.selectbox("select a state",map_user_df["States"].unique()) 
        st.subheader("APPOPENS")
        top_chart_AppOpens("map_user_table", "states")

    elif question == "10. Registered User of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user_table")

    
    


