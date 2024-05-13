# Importing Libraries
import pandas as pd
import  mysql.connector
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo

google_colors = ["#4285F4", "#34A853", "#FBBC05", "#EA4335", "#FF6D00", "#1A73E8", "#DB4437", "#F4B400", "#0F9D58"]

# Setting up page configuration
icon = Image.open("ICN.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")

# #To clone the Github Pulse repository use the following code
# Reference Syntax - Repo.clone_from("Clone Url", "Your working directory")
# Repo.clone_from("https://github.com/PhonePe/pulse.git", "Project_3_PhonepePulse/Phonepe_data/data")

# Creating connection with mysql workbench
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Sagar72427',
    port=3306,
    database='phonepe_database',
    auth_plugin='mysql_native_password'
)
cursor = mydb.cursor()


# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
# MENU 1 - HOME
if selected == "Home":
    st.image("C:\\Users\\sagar\\Desktop\\Projects\\img.png")
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("home.png")
        

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("Select Type", ("Insurance","Transactions", "Users"))
    


       
# Top Charts - INSURANCE  
    if Type == "Insurance":
        cursor.execute('''select * from aggregated_insurance_table''')
        table1 = cursor.fetchall()
        mydb.commit()
        aggregated_insurance_df = pd.DataFrame(table1, columns=("States","Years", "Quarter", "name", "Transaction_count", "Transaction_amount"))

        col1, col2 = st.columns([1,1.5],gap="large")
        with col1:
            Year = st.selectbox("**Year**", aggregated_insurance_df["Years"].unique())
            Quarter = st.selectbox("Quarter", aggregated_insurance_df["Quarter"].unique())
            state = st.selectbox("States", aggregated_insurance_df["States"].unique())
        with col2:
            st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top State, District based on Total number of transaction and Total amount spent on phonepe.
            
                """,icon="🔍"
                )
            
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### :violet[STATE]")
            cursor.execute(f'''select States, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total 
                            from map_insurance_table 
                            where Years = {Year} and Quarter = {Quarter} 
                            group by States 
                            order by Total desc limit 10''')
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=google_colors,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'}
                                )

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
        with col2:
            st.markdown("### :violet[ DISTRICTS ]")
            cursor.execute(f'''SELECT District, SUM(Transaction_count) AS Total_Count, SUM(Transaction_amount) AS Total 
                                FROM map_insurance_table
                                WHERE  Years = {Year} AND Quarter = {Quarter}
                                GROUP BY District
                                ORDER BY Total_Count DESC
                                LIMIT 10''')
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, 
                        values='Total_Amount', 
                        names='District', 
                        title='Top 10', 

                        color='District', 
                        color_discrete_sequence=google_colors,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count':'Transactions_Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        
        st.markdown("### :violet[State Wise District]")
        cursor.execute(f'''select District , sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total 
                    from map_transaction_table 
                    where States = '{state}'
                    and Years = {Year} and Quarter = {Quarter}
                        group by District
                        order by Total desc 
                        ''')
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

        fig = px.bar(df, x='District', y='Total_Amount',
            title='Top  Districts by Total Amount',
            labels={'Total_Amount':'Total Amount'},
            hover_data={'Total_Amount': True, 'Transactions_Count': True, 'District': True},
            color='District',
            color_discrete_sequence=google_colors)

        fig.update_traces(texttemplate='%{y}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig.update_layout(height= 500, width= 1200)

        st.plotly_chart(fig)



        


# ------------------------------------------------------------------------------------------------------------------------------------------#
# Top Charts - TRANSACTION 

    if Type == "Transactions":
        cursor.execute('''select * from aggregated_transaction_table''')
        table2 = cursor.fetchall()
        mydb.commit()
        aggregated_transaction_df = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


        col1, col2 = st.columns([1,1.5],gap="large")
        with col1:
            Year = st.selectbox("**Year**", aggregated_transaction_df["Years"].unique())
            Quarter = st.selectbox("Quarter", aggregated_transaction_df["Quarter"].unique())
            state = st.selectbox("States", aggregated_transaction_df["States"].unique())
        with col2:
            st.info(
                        """
                        #### From this menu we can get insights like :
                        - Top 10 States based on transaction Count and transaction Amount.
                        - Percnetage of Transaction Type.
                        - Top Districts in a particular selected state.
                        - Top 10 pincodes
                        - Top State, District based on Total number of transaction and Total amount spent on phonepe.
                    
                        """,icon="🔍"
                        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### :violet[State]")
            cursor.execute(f'''select States, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total 
                            from aggregated_transaction_table 
                            where Years = {Year} and Quarter = {Quarter} 
                            group by States 
                            order by Total desc limit 10''')
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=google_colors,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'}
                                )

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[Transaction Type]")
            cursor.execute(f'''select Transaction_type, sum(Transaction_count) as Transaction_count, sum(Transaction_amount) as Transaction_amount
                                from aggregated_transaction_table
                                where Quarter = {Quarter} and Years = {Year}
                                group by Transaction_type;''')
            df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                                    names='Transaction_type',
                                    title='Top 10',
                                    color_discrete_sequence=google_colors,
                                    hover_data=['Transactions_Count'],
                                    labels={'Transactions_Count':'Transactions_Count'})
                                

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

            
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### :violet[State Wise District]")
            cursor.execute(f'''select District , sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total 
                        from map_transaction_table 
                        where States = '{state}'
                        and Years = {Year} and Quarter = {Quarter}
                            group by District
                            order by Total desc 
                            ''')
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.bar(df, x='District', y='Total_Amount',
                title='Top  Districts by Total Amount',
                labels={'Total_Amount':'Total Amount'},
                hover_data={'Total_Amount': True, 'Transactions_Count': True, 'District': True},
                color='District',
                color_discrete_sequence=google_colors)

            fig.update_traces(texttemplate='%{y}', textposition='outside')
            fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            fig.update_layout(height= 500, width= 1200)

            st.plotly_chart(fig)

        
        st.markdown("### :violet[Pincodes top 10]")
        cursor.execute(f'''select Pincodes , sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total 
                    from top_transaction_table
                    where States = '{state}'
                    and Years = {Year} and Quarter = {Quarter}
                        group by Pincodes
                        order by Total_Count desc limit 10
                        ''')
        df = pd.DataFrame(cursor.fetchall(), columns=['Pincodes', 'Transactions_Count','Total_Amount'])

        fig = px.bar(df, x='Pincodes', y='Total_Amount',
            title='Pincodes top 10',
            labels={'Total_Amount':'Total Amount'},
            hover_data={'Total_Amount': True, 'Transactions_Count': True, 'Pincodes': True},
            color='Pincodes',
            color_discrete_sequence=google_colors)

        fig.update_traces(texttemplate='%{y}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig.update_layout(height= 500, width= 1200)

        st.plotly_chart(fig)


            
# Top Charts - USERS          
    if Type == "Users":
        cursor.execute('''select * from aggregated_user_table''')
        table3 = cursor.fetchall()
        mydb.commit()
        aggregated_user_df = pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

        col1, col2 = st.columns([1,1.5],gap="large")
        with col1:
            Year = st.selectbox("**Year**", aggregated_user_df["Years"].unique())
            Quarter = st.selectbox("Quarter", aggregated_user_df["Quarter"].unique())
            state = st.selectbox("States", aggregated_user_df["States"].unique())
        with col2:
            st.info(
                """
                #### From this menu we can get insights like :
                - Top Brands based and its percentage 
                - Top States based on total registered user.
                - Top pincodes based on total registered user.
                - Top districts for overall india and state wise districts.
            
                """,icon="🔍"
                )
            
        col1,col2 = st.columns(2)
        
        with col1:
            st.markdown("### :violet[Brands]")
            
            cursor.execute(f'''select Brands, sum(Transaction_count) as Total_Count, sum(Percentage)*100 as total_percenatge 
                        from aggregated_user_table 
                        where Years = {Year} and Quarter = {Quarter} 
                        group by brands 
                        order by Total_Count desc limit 10''')
            df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','total_percenatge'])
            fig = px.pie(df, 
                names="Brand", 
                values="Total_Users", 
                hover_data=["Brand", "total_percenatge"], 
                title='Top 10 Brands by Total Users',
                color_discrete_sequence= google_colors,
                )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


        with col2:
            st.markdown("### :violet[State]")
            cursor.execute(f'''select States, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens 
                        from map_user_table 
                        where Years = {Year} and Quarter = {Quarter}
                        group by States 
                        order by Total_Users desc limit 10''')
            df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                                names='States',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data={'Total_Appopens':True},
                                labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)




        st.markdown("### :violet[Pincodes]")
        cursor.execute(f'''SELECT Pincodes, SUM(registeredusers) AS Total_Users 
                        FROM top_user_table 
                        WHERE Years = {Year} AND Quarter = {Quarter} 
                        GROUP BY Pincodes 
                        ORDER BY Total_Users DESC 
                        LIMIT 10''')
        
        df = pd.DataFrame(cursor.fetchall(), columns=['Pincodes', 'Total_Users'])
        fig = px.pie(df,
                    values='Total_Users',
                    names='Pincodes',
                    title='Top 10 Pincodes by Total Users',
                    color_discrete_sequence=google_colors,
                    hover_data=['Total_Users'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        
        
        st.markdown("### :violet[District]")
        cursor.execute(f'''select District, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens 
                        from map_user_table
                        where Years = {Year} and Quarter = {Quarter} 
                        group by District 
                        order by Total_Users desc limit 10''')
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(float)
        fig = px.bar(df,
                        title='Top 10',
                        x="Total_Users",
                        y="District",
                        orientation='h',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)


    
        st.markdown("### :violet[State Wise District]")
        cursor.execute(f'''select District , sum(RegisteredUser) as Registered_user, sum(AppOpens) as Total_app_opens
                    from map_user_table 
                    where States = '{state}'
                    and Years = {Year} and Quarter = {Quarter}
                        group by District
                        order by Registered_user desc 
                        ''')
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Registered_user','Total_app_opens'])

        fig = px.bar(df, x='District', y='Registered_user',
            title='Top  Districts by Total Registered_user',
            labels={'Registered_user':'Total Registered_user'},
            hover_data={'Registered_user': True, 'Total_app_opens': True, 'District': True},
            color='District',
            color_discrete_sequence=google_colors)

        fig.update_traces(texttemplate='%{y}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig.update_layout(height= 500, width= 1200)

        st.plotly_chart(fig)
              
    

   
            
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    cursor.execute('''select * from aggregated_transaction_table''')
    table2 = cursor.fetchall()
    mydb.commit()
    aggregated_transaction_df = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))
    
    Year = st.sidebar.selectbox("**Year**", aggregated_transaction_df["Years"].unique())
    Quarter = st.sidebar.selectbox("Quarter", aggregated_transaction_df["Quarter"].unique())
    Type = st.sidebar.selectbox("**Type**", ("Insurance", "Transactions", "Users"))



    if Type == "Insurance":
        # Check if there is data for the selected year and quarter
        cursor.execute(f'''SELECT COUNT(*) 
                         FROM aggregated_insurance_table 
                         WHERE Years = '{Year}' AND Quarter = '{Quarter}' ''')
        
        if cursor.fetchone()[0] == 0:
            st.write("No data available for the selected year and quarter.")
        else:
            # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("## :violet[Overall State Data - Transactions Amount]")
                cursor.execute(f'''select States, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount 
                                from map_insurance_table 
                                where Years = '{Year}' and Quarter = '{Quarter}'
                                group by States 
                                order by States''')
                df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.State = df2

                fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM',
                                    locations='State',
                                    color='Total_amount',
                                    color_continuous_scale='sunset',
                                    height=600, width=650)

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig, use_container_width=True)

            # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
            with col2:
                st.markdown("## :violet[Overall State Data - Transactions Count]")
                cursor.execute(f'''select States, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount 
                                from map_insurance_table 
                                where Years = '{Year}' and Quarter = '{Quarter}' 
                                group by States 
                                order by States''')
                df1 = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.Total_Transactions = df1.Total_Transactions.astype(float)
                df1.State = df2

                fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM',
                                    locations='States',
                                    color='Total_Transactions',
                                    color_continuous_scale='sunset',
                                    height=600, width=650)

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig, use_container_width=True)



                # BAR CHART - TOP States
        st.markdown("## :violet[Top States - Transaction Count]")
        cursor.execute(f'''select States, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount 
                       from aggregated_insurance_table 
                       where Years= '{Year}' and Quarter = '{Quarter} '
                       group by States
                       order by Total_amount desc''')
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Top States',
                     x="States",
                     y="Total_Transactions",
                     orientation='v',
                     color='States',
                     color_continuous_scale=px.colors.sequential.Agsunset,
                     width= 1000, height= 700,
                     hover_name= "States")
        st.plotly_chart(fig,use_container_width=False)



        st.markdown("## :violet[Top States - Transaction Amount]")
        cursor.execute(f'''select States, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount 
                       from aggregated_insurance_table 
                       where Years= '{Year}' and Quarter = '{Quarter} '
                       group by States
                       order by Total_amount desc''')
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Top States',
                     x="States",
                     y="Total_amount",
                     orientation='v',
                     color='States',
                     color_continuous_scale=px.colors.sequential.Agsunset,
                     width= 1000, height= 700,
                     hover_name= "States")
        st.plotly_chart(fig,use_container_width=False)
    




        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        aggregated_transaction_df = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))
        selected_state = state = st.selectbox("States", aggregated_transaction_df["States"].unique())
         
        cursor.execute(f'''select States, District,Years,Quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount 
                       from map_insurance_table 
                       where Years = '{Year} 'and Quarter = '{Quarter}' and States = '{selected_state}' 
                       group by States, District,Years,Quarter 
                       order by States, District''')
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        df1.Total_Transactions = df1.Total_Transactions.astype(int)

        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='District',
                     color_continuous_scale=google_colors)
        st.plotly_chart(fig,use_container_width=True)
        



    if Type == "Transactions":
        # Check if there is data for the selected year and quarter
        cursor.execute(f'''SELECT COUNT(*) 
                         FROM map_transaction_table 
                         WHERE Years = '{Year}' AND Quarter = '{Quarter}' ''')
        
        if cursor.fetchone()[0] == 0:
            st.write("No data available for the selected year and quarter.")
        else:
            # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("## :violet[Overall State Data - Transactions Amount]")
                cursor.execute(f'''select States, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount 
                                from map_transaction_table 
                                where Years = '{Year}' and Quarter = '{Quarter}'
                                group by States 
                                order by States''')
                df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.State = df2

                fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM',
                                    locations='State',
                                    color='Total_amount',
                                    color_continuous_scale='sunset',
                                    height=600, width=650)

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig, use_container_width=True)

            # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
            with col2:
                st.markdown("## :violet[Overall State Data - Transactions Count]")
                cursor.execute(f'''select States, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount 
                                from map_transaction_table 
                                where Years = '{Year}' and Quarter = '{Quarter}' 
                                group by States 
                                order by States''')
                df1 = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.Total_Transactions = df1.Total_Transactions.astype(float)
                df1.State = df2

                fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM',
                                    locations='States',
                                    color='Total_Transactions',
                                    color_continuous_scale='sunset',
                                    height=600, width=650)

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig, use_container_width=True)
            
   

    
        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        cursor.execute(f'''select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount 
                       from aggregated_transaction_table 
                       where Years= '{Year}' and Quarter = '{Quarter} '
                       group by Transaction_type 
                       order by Total_amount desc''')
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Transaction_type',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        


        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        aggregated_transaction_df = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))
        selected_state = state = st.selectbox("States", aggregated_transaction_df["States"].unique())
         
        cursor.execute(f'''select States, District,Years,Quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount 
                       from map_transaction_table 
                       where Years = '{Year} 'and Quarter = '{Quarter}' and States = '{selected_state}' 
                       group by States, District,Years,Quarter 
                       order by States, District''')
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        df1.Total_Transactions = df1.Total_Transactions.astype(int)

        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='District',
                     color_continuous_scale=google_colors)
        st.plotly_chart(fig,use_container_width=True)


    

    # EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        cursor.execute(f'''select States, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from 
                         map_user_table 
                         where Years = '{Year}' and Quarter = '{Quarter}'
                           group by States 
                           order by States''')
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)




         # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        cursor.execute('''select * from map_user_table''')
        table6 = cursor.fetchall()
        mydb.commit()
        map_user_df = pd.DataFrame(table6, columns=("States", "Years", "Quarter", "District", "RegisteredUser", "AppOpens"))
        selected_state = selected_state = state = st.selectbox("States", aggregated_transaction_df["States"].unique())
        
        cursor.execute(f'''select States,Years,Quarter,District,sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens 
                         from map_user_table 
                         where Years = {Year} and Quarter = {Quarter} and States = '{selected_state}' 
                         group by States, District,Years,Quarter 
                         order by States, District''')
        
        df = pd.DataFrame(cursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=google_colors)
        st.plotly_chart(fig,use_container_width=True)



# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("Pulseimg.jpg")