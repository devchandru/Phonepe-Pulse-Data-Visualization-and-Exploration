import json
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu


# Dataframe Creation

# sql connection

mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = 5432,
                        database = "phonepe_data_1",
                        password = 3159)

cursor = mydb.cursor()



# aggregated_insurance_df

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()


Aggre_insurance = pd.DataFrame(table1, columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


# aggregated_transaction_df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()


Aggre_transaction = pd.DataFrame(table2, columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


# aggregated_user_df

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 = cursor.fetchall()


Aggre_user = pd.DataFrame(table3, columns = ("States", "Years", "Quarter", "Brands","Transaction_count","Percentage"))

# map_insurance_df

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 = cursor.fetchall()

map_insurance = pd.DataFrame(table4, columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))


# map_transaction_df

cursor.execute("SELECT * FROM map_transation")
mydb.commit()
table5 = cursor.fetchall()

map_transaction = pd.DataFrame(table5, columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))


# map_user_df

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6 = cursor.fetchall()

map_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Districts", "RegisteredUsers", "AppOpens"))


# top_insurance_df

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7 = cursor.fetchall()

top_insurance = pd.DataFrame(table7, columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


# top_transaction_df

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8 = cursor.fetchall()

top_transaction = pd.DataFrame(table8, columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


# top_user_df

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9 = cursor.fetchall()

top_user = pd.DataFrame(table9, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUsers"))


###################################################

def Transaction_amount_count_Y(df, year):
    
    tacy = df[df["Years"] == year].reset_index(drop=True)
    
    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount",
                            title=f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=650, width=600)
        st.plotly_chart(fig_amount)
    
    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count",
                           title=f"{year} TRANSACTION COUNT",
                           color_discrete_sequence=px.colors.sequential.Bluered_r,
                           height=650, width=600)
        st.plotly_chart(fig_count)
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    states_name = sorted([feature["properties"]["ST_NM"] for feature in data1["features"]])

    fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                height=600, width=600)
    fig_india_1.update_geos(visible=False)

    fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                height=600, width=600)
    fig_india_2.update_geos(visible=False)

    with st.container():
        st.plotly_chart(fig_india_1, use_container_width=True)
        st.plotly_chart(fig_india_2, use_container_width=True)

    return tacy

#----------------------------------------------------------------------------------------------------------------------

def Transaction_amount_count_Y_Q(df, quarter):
    
    tacy = df[df["Quarter"] == quarter].reset_index(drop=True)
    
    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum().reset_index()
    
    min_year = tacy['Years'].min()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount",
                            title=f"{min_year} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count",
                           title=f"{min_year} YEAR {quarter} QUARTER TRANSACTION COUNT",
                           color_discrete_sequence=px.colors.sequential.Bluered_r,
                           height=650, width=600)
        st.plotly_chart(fig_count)
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    states_name = sorted([feature["properties"]["ST_NM"] for feature in data1["features"]])

    fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{min_year} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                                fitbounds="locations", height=700, width=600)
    fig_india_1.update_geos(visible=False)

    fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{min_year} YEAR {quarter} QUARTER TRANSACTION COUNT",
                                fitbounds="locations", height=700, width=600)
    fig_india_2.update_geos(visible=False)

    with st.container():
        st.plotly_chart(fig_india_1, use_container_width=True)
        st.plotly_chart(fig_india_2, use_container_width=True)

    return tacy

#------------------------------------------------------------------------------------------------------------------------------------------------

# Aggregated_tran_Transaction_type

def Aggre_tran_Transaction_type(df, state):
   
    tacy = df[df["States"] == state].reset_index(drop=True)
    
    tacyg = tacy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie_1 = px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_amount",
                           width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_count",
                           width=600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)

        
        
# Aggregated_Usar_analysis_1

def Aggre_user_plot_1(df, year):
   
    aguy = df[df["Years"] == year].reset_index(drop=True)

    aguyg = aguy.groupby("Brands")[["Transaction_count", "Percentage"]].sum().reset_index()

    fig_bar_1 = px.bar(aguyg, x="Brands", y="Transaction_count",
                       title=f"{year} BRANDS AND TRANSACTION COUNT",
                       width=1200, color_discrete_sequence=px.colors.sequential.haline_r,
                       hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy
    
    
# Aggregated_Usar_analysis_2

def Aggre_user_plot_2(df, quarter):
   
    aguyq = df[df["Quarter"] == quarter].reset_index(drop=True)

    aguyqg = aguyq.groupby("Brands")["Transaction_count"].sum().reset_index()

    fig_bar_1 = px.bar(aguyqg, x="Brands", y="Transaction_count",
                       title=f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                       width=1200, color_discrete_sequence=px.colors.sequential.Magenta_r,
                       hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq


# Aggregated_user_analysis_3

def Aggre_user_plot_3(df, state):
   
    auyqs = df[df["States"] == state].reset_index(drop=True)

    fig_line_1 = px.line(auyqs, x="Brands", y="Transaction_count", hover_data="Percentage",
                         title=f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",
                         width=1200, markers=True)

    st.plotly_chart(fig_line_1)

    return auyqs

    
 # Map insurance districts

def Map_insur_Districts(df, state):
    
    tacy = df[df["States"] == state].reset_index(drop=True)

    tacyg = tacy.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum().reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig_bar_1 = px.bar(tacyg, x="Transaction_amount", y="Districts", orientation="h",
                           height=600, hover_name="Districts",
                           title=f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT",
                           color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(tacyg, x="Transaction_count", y="Districts", orientation="h",
                           height=600, hover_name="Districts",
                           title=f"{state.upper()} DISTRICTS AND TRANSACTION COUNT",
                           color_discrete_sequence=px.colors.sequential.Mint)
        st.plotly_chart(fig_bar_2)

    return tacy
    
    

#map_user_plot_1

def map_user_plot_1(df, year):
   
    muy = df[df["Years"] == year].reset_index(drop=True)

    muyg = muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum().reset_index()

    fig_line_1 = px.line(muyg, x="States", y=["RegisteredUsers", "AppOpens"], hover_name="States",
                         title=f"{year} REGISTERED USERS AND APP OPENS",
                         width=1200, height=900, markers=True)

    st.plotly_chart(fig_line_1)

    return muy
 
#map_user_plot_2

def map_user_plot_2(df, quarter):
    
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop = True, inplace = True)


    muyqg = muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace = True)


    fig_line_1 = px.line(muyqg, x = "States", y = ["RegisteredUsers", "AppOpens"], hover_name = "States", 
                        color_discrete_sequence = px.colors.sequential.Rainbow_r,
                        title = f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTEREDUSERS APPOPENS", width = 1200, height = 900, markers = True)

    st.plotly_chart(fig_line_1)
    
    
    return muyq   

# Map_user_plot_3

def map_user_plot_3(df, states):

    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop = True, inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x = "RegisteredUsers", y = "Districts", orientation = "h", hover_name = "Districts",
                                    title = f"{states.upper()} REGISTERED USER", height = 1000, width = 800, color_discrete_sequence = px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_map_user_bar_1)
        
    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x = "AppOpens", y = "Districts", orientation = "h", hover_name = "Districts",
                                    title = f"{states.upper()} APPOPENS", height = 1000, width = 800, color_discrete_sequence = px.colors.sequential.Cividis_r)

        st.plotly_chart(fig_map_user_bar_2)
    
#top_insurance_plot_1

def Top_insurance_plot_1(df, quarter):
    
    tiy = df[df["States"] == quarter]
    tiy.reset_index(drop = True, inplace = True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig_top_insur_bar_1 = px.bar(tiy, x = "Quarter", y = "Transaction_amount", hover_data = "Pincodes", hover_name = "States",
                                    title = f"TRANSACTION AMOUNT", width = 800, color_discrete_sequence = px.colors.sequential.GnBu_r)

        st.plotly_chart(fig_top_insur_bar_1)
        
    with col2:
        fig_top_insur_bar_2 = px.bar(tiy, x = "Quarter", y = "Transaction_count", hover_data = "Pincodes", hover_name = "States",
                                    title = f"TRANSACTION COUNT", width = 800, color_discrete_sequence = px.colors.sequential.Agsunset_r)

        st.plotly_chart(fig_top_insur_bar_2)

# Top_Usar_analysis_1

def top_user_plot_1(df, year):

    tuy = df[df["Years"] == year]
    tuy.reset_index(drop = True, inplace = True)


    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace = True)


    fig_top_plot_1 = px.bar(tuyg, x = "States", y = "RegisteredUsers", color = "Quarter", width = 1000, height= 800,
                            color_discrete_sequence = px.colors.sequential.Burgyl, hover_name = "States",
                            title = f"{year} REGISTERED USERS")

    st.plotly_chart(fig_top_plot_1)
    
    return tuy


# top_user_plot_2

def top_user_plot_2(df,state):
    tuys = df[df["States"] == state]
    tuys.reset_index(drop = True, inplace = True)


    fig_top_pot_2 = px.bar(tuys, x = "Quarter", y = "RegisteredUsers", title = "REGISTERED USERS, PINCODES, QUARTER",
                        width = 1000, height = 800, color = "RegisteredUsers", hover_data = "Pincodes", 
                        color_continuous_scale = px.colors.sequential.Magenta)

    st.plotly_chart(fig_top_pot_2)


# sql connection

def top_chart_transaction_amount(table_name):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = 5432,
                            database = "phonepe_data_1",
                            password = 3159)

    cursor = mydb.cursor()

    # plot_1
    quary1 = f'''select states, sum(transaction_amount) AS transaction_amount
                from {table_name}
                GROUP BY states
                order by transaction_amount desc
                limit 10;'''

    cursor.execute(quary1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("states", "transaction_amount"))

    col1, col2 = st.columns(2)
    with col1:
    
        fig_amount = px.bar(df_1, x = "states", y = "transaction_amount", title = "TOP 10 OF TRANSACTION AMOUNT", hover_name = "states", # DESC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    quary2 = f'''select states, sum(transaction_amount) AS transaction_amount
                from {table_name}
                GROUP BY states
                order by transaction_amount
                limit 10;'''

    cursor.execute(quary2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("states", "transaction_amount"))

    with col2:
        fig_amount_2 = px.bar(df_2, x = "states", y = "transaction_amount", title = "LAST 10 OF TRANSACTION AMOUNT", hover_name = "states", # ASC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl_r, height = 650, width = 600)
        st.plotly_chart(fig_amount_2)


    # plot_3
    quary3 = f'''select states, avg(transaction_amount) AS transaction_amount
                from {table_name}
                GROUP BY states
                order by transaction_amount;'''

    cursor.execute(quary3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("states", "transaction_amount"))


    fig_amount_3 = px.bar(df_3, x = "transaction_amount", y = "states", title = "AVERAGE OF TRANSACTION AMOUNT", hover_name = "states", # ASC top 10
                        orientation="h", color_discrete_sequence = px.colors.sequential.Bluered_r, height = 800, width = 1000)
    st.plotly_chart(fig_amount_3)
    
    
# sql connection

def top_chart_transaction_count(table_name):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = 5432,
                            database = "phonepe_data_1",
                            password = 3159)

    cursor = mydb.cursor()

    # plot_1
    quary1 = f'''select states, sum(transaction_count) AS transaction_count
                from {table_name}
                GROUP BY states
                order by transaction_count desc
                limit 10;'''

    cursor.execute(quary1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("states", "transaction_count"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "states", y = "transaction_count", title = "TOP 10 OF TRANSACTION COUNT", hover_name = "states", # DESC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    quary2 = f'''select states, sum(transaction_count) AS transaction_count
                from {table_name}
                GROUP BY states
                order by transaction_count
                limit 10;'''

    cursor.execute(quary2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("states", "transaction_count"))

    with col2:
        fig_amount_2 = px.bar(df_2, x = "states", y = "transaction_count", title = "LAST 10 OF TRANSACTION COUNT", hover_name = "states", # ASC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl_r, height = 650, width = 600)
        st.plotly_chart(fig_amount_2)


    # plot_3
    quary3 = f'''select states, avg(transaction_count) AS transaction_count
                from {table_name}
                GROUP BY states
                order by transaction_count;'''

    cursor.execute(quary3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("states", "transaction_count"))


    fig_amount_3 = px.bar(df_3, x = "transaction_count", y = "states", title = "AVERAGE OF TRANSACTION COUNT", hover_name = "states",
                        orientation="h", color_discrete_sequence = px.colors.sequential.Bluered_r, height = 800, width = 1000)
    st.plotly_chart(fig_amount_3)
    

# sql connection

def top_chart_registered_user(table_name, state):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = 5432,
                            database = "phonepe_data_1",
                            password = 3159)

    cursor = mydb.cursor()

    # plot_1
    quary1 = f'''select districts, sum(registeredusers) as registereduser
                 from {table_name}
                 where states = '{state}'
                 group by districts
                 order by registereduser desc
                 limit 10;'''

    cursor.execute(quary1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("districts", "registereduser"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "districts", y = "registereduser", title = "TOP 10 OF REGISTERED USER", hover_name = "districts", # DESC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    quary2 = f'''select districts, sum(registeredusers) as registereduser
                 from {table_name}
                 where states = '{state}'
                 group by districts
                 order by registereduser asc
                 limit 10;'''

    cursor.execute(quary2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("districts", "registereduser"))

    with col2:
        fig_amount_2 = px.bar(df_2, x = "districts", y = "registereduser", title = "LAST 10 OF REGISTERED USER", hover_name = "districts", # ASC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl_r, height = 650, width = 600)
        st.plotly_chart(fig_amount_2)


    # plot_3
    quary3 = f'''select districts, avg(registeredusers) as registereduser
                 from {table_name}
                 where states = '{state}'
                 group by districts
                 order by registereduser;'''

    cursor.execute(quary3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("districts", "registereduser"))


    fig_amount_3 = px.bar(df_3, x = "registereduser", y = "districts", title = "AVERAGE OF REGISTERED USER", hover_name = "districts",
                        orientation="h", color_discrete_sequence = px.colors.sequential.Bluered_r, height = 900, width = 1000)
    st.plotly_chart(fig_amount_3)
    

# sql connection

def top_chart_appopens(table_name, state):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = 5432,
                            database = "phonepe_data_1",
                            password = 3159)

    cursor = mydb.cursor()

    # plot_1
    quary1 = f'''select districts, sum(appopens) as appopens
                 from {table_name}
                 where states = '{state}'
                 group by districts
                 order by appopens desc
                 limit 10;'''

    cursor.execute(quary1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("districts", "appopens"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "districts", y = "appopens", title = "TOP 10 OF APPOPENS", hover_name = "appopens", # DESC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    quary2 = f'''select districts, sum(appopens) as appopens
                 from {table_name}
                 where states = '{state}'
                 group by districts
                 order by appopens asc
                 limit 10;'''

    cursor.execute(quary2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("districts", "appopens"))

    with col2:
        fig_amount_2 = px.bar(df_2, x = "districts", y = "appopens", title = "LAST 10 OF appopens", hover_name = "appopens", # ASC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl_r, height = 650, width = 600)
        st.plotly_chart(fig_amount_2)


    # plot_3
    quary3 = f'''select districts, avg(appopens) as appopens
                 from {table_name}
                 where states = '{state}'
                 group by districts
                 order by appopens;'''

    cursor.execute(quary3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("districts", "appopens"))


    fig_amount_3 = px.bar(df_3, x = "appopens", y = "districts", title = "AVERAGE OF APPOPENS", hover_name = "appopens",
                        orientation="h", color_discrete_sequence = px.colors.sequential.Bluered_r, height = 900, width = 1000)
    st.plotly_chart(fig_amount_3)
    

# sql connection

def top_chart_registered_users(table_name):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = 5432,
                            database = "phonepe_data_1",
                            password = 3159)

    cursor = mydb.cursor()

    # plot_1
    quary1 = f'''SELECT states, SUM(registeredusers::numeric) AS registeredusers
             FROM {table_name}
             GROUP BY states
             ORDER BY registeredusers DESC
             LIMIT 10;'''


    cursor.execute(quary1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("states", "registeredusers"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "states", y = "registeredusers", title = "TOP 10 OF REGISTERED USERS", hover_name = "states", # DESC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    quary2 = f'''select states, sum(registeredusers::numeric) as registeredusers
                 from {table_name}
                 group by states
                 order by registeredusers 
                 limit 10;'''

    cursor.execute(quary2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("states", "registeredusers"))

    with col2:
        fig_amount_2 = px.bar(df_2, x = "states", y = "registeredusers", title = "LAST 10 OF REGISTERED USERS", hover_name = "states", # ASC top 10
                            color_discrete_sequence = px.colors.sequential.Aggrnyl_r, height = 650, width = 600)
        st.plotly_chart(fig_amount_2)


    # plot_3
    quary3 = f'''select states, avg(registeredusers::numeric) as registeredusers
                 from {table_name}
                 group by states
                 order by registeredusers;'''

    cursor.execute(quary3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("states", "registeredusers"))


    fig_amount_3 = px.bar(df_3, x = "registeredusers", y = "states", title = "AVERAGE OF REGISTERED USERS", hover_name = "states",
                        orientation="h", color_discrete_sequence = px.colors.sequential.Bluered_r, height = 800, width = 1000)
    st.plotly_chart(fig_amount_3)
    
      
    
# Streamlit part

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])
    
if select == "Home":
    
    col1,col2= st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        
    with col2:
        st.video(r"F:\Phonepe_2\htp-Pay-by-PhonePe-Web.mp4")

    col3,col4= st.columns(2)
    
    with col3:
        st.video(r"F:\Phonepe_2\home-fast-secure-v3.mp4")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.video("F:\Phonepe_2\GPGTaBlvqa12nEQDABgFiNDM8HI6bmdjAAAF.mp4")
    
elif select == "Data Exploration":
        
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        
        method = st.radio("Select the Analysis Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y = Transaction_amount_count_Y(Aggre_insurance, years)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarters", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)   
            
        elif method == "Transaction Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(), Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y = Transaction_amount_count_Y(Aggre_transaction, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", Aggre_tran_tac_Y["States"].unique())
                
            Aggre_tran_Transaction_type(Aggre_tran_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarters", Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(), Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Ty", Aggre_tran_tac_Y["States"].unique())
                
            Aggre_tran_Transaction_type(Aggre_tran_tac_Y, states)
    
        elif method == "User Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", Aggre_user["Years"].min(), Aggre_user["Years"].max(), Aggre_user["Years"].min())
            Aggre_user_Y = Aggre_tran_tac_Y = Aggre_user_plot_1(Aggre_user, years)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarters", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Ty", Aggre_user_Y_Q["States"].unique())
                
            Aggre_user_plot_3(Aggre_user_Y_Q, states)
        
        
    with tab2:
        
        method_2 = st.radio("Select the Method",["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":
            
            col1, col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", map_insurance["Years"].min(), map_insurance["Years"].max(), map_insurance["Years"].min(),
                                  key="unique_key_for_years_slider")
            map_insur_tac_Y = Transaction_amount_count_Y(map_insurance, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_mi", map_insur_tac_Y["States"].unique())
                
            Map_insur_Districts(map_insur_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarters", map_insur_tac_Y["Quarter"].min(), map_insur_tac_Y["Quarter"].max(), map_insur_tac_Y["Quarter"].min(),
                                     key="unique_key_for_years_quarter_slider")
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Ty", map_insur_tac_Y_Q ["States"].unique())
                
            Map_insur_Districts(map_insur_tac_Y_Q , states)

        
        elif method_2 == "Map Transaction":
            
            col1, col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", map_transaction["Years"].min(), map_transaction["Years"].max(), map_transaction["Years"].min(),
                                  key="unique_key_for_years_slider")
            map_tran_tac_Y = Transaction_amount_count_Y(map_transaction, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_mi", map_tran_tac_Y["States"].unique())
                
            Map_insur_Districts(map_tran_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarters", map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(), map_tran_tac_Y["Quarter"].min(),
                                     key="unique_key_for_years_quarter_slider")
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Ty", map_tran_tac_Y_Q["States"].unique())
                
            Map_insur_Districts(map_tran_tac_Y_Q, states)
        
        elif method_2 == "Map User":
            
            col1, col2 = st.columns(2)
            with col1:
            
                years = st.slider("Select The Year", map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min(),
                                key="unique_key_for_years_slider")
            map_user_Y = map_user_plot_1(map_user, years)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarters", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min(),
                                     key="unique_key_for_years_quarter_slider")
            map_user_Y_Q = map_user_plot_2(map_user_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Mu", map_user_Y_Q["States"].unique())
                
            map_user_plot_3(map_user_Y_Q, states)
        
    with tab3:
        
        method_3 = st.radio("Select the Method",["Top Insurance", "Top Transaction", "Top User"])

        if method_3 == "Top Insurance":
            
            col1, col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", top_insurance["Years"].min(), top_insurance["Years"].max(), top_insurance["Years"].min(),
                                  key="unique_key_for_years_slider_user_2")
            top_insur_tac_Y = Transaction_amount_count_Y(top_insurance, years)
        
        
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", top_insur_tac_Y["States"].unique())
                
            Top_insurance_plot_1(top_insur_tac_Y, states)
        
            col1, col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarters", top_insur_tac_Y["Quarter"].min(), top_insur_tac_Y["Quarter"].max(), top_insur_tac_Y["Quarter"].min(),
                                     key="unique_key_for_years_quarter_slider_2")
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)
        
        elif method_3 == "Top Transaction":
            
            col1, col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", top_transaction["Years"].min(), top_transaction["Years"].max(), top_transaction["Years"].min(),
                                  key="unique_key_for_years_slider_user_3")
            top_tran_tac_Y = Transaction_amount_count_Y(top_transaction, years)
        
        
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", top_tran_tac_Y["States"].unique())
                
            Top_insurance_plot_1(top_tran_tac_Y, states)
        
            col1, col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarters", top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(), top_tran_tac_Y["Quarter"].min(),
                                     key="unique_key_for_years_quarter_slider_3")
            top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)

        
        elif method_3 == "Top User":
            
            col1, col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", top_user["Years"].min(), top_user["Years"].max(), top_user["Years"].min(),
                                  key="unique_key_for_years_slider_user_4")
            top_user_Y = top_user_plot_1(top_user, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", top_user_Y ["States"].unique())
                
            top_user_plot_2(top_user_Y , states)
        
        
        
        
elif select == "Top Charts":
    
    question = st.selectbox("Select the Question",[ "1. Transation Amount and Count of Count of Aggregated Insurance",
                                                    "2. Transation Amount and Count of Count of Map Insurance",
                                                    "3. Transation Amount and Count of Count of Top insurance",
                                                    "4. Transation Amount and Count of Count of Aggregated Transation",
                                                    "5. Transation Amount and Count of Count of Map Transaction",
                                                    "6. Transation Amount and Count of Count of Top Transaction",
                                                    "7. Transation Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. app opens users of Top User",
                                                    "10. Registered users of Top User",
                                                    ])
    
    if question == "1. Transation Amount and Count of Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
        
    elif question == "2. Transation Amount and Count of Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")
        
        
    elif question == "3. Transation Amount and Count of Count of Top insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")
        
        
    elif question == "4. Transation Amount and Count of Count of Aggregated Transation":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
        
        
    elif question == "5. Transation Amount and Count of Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transation")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transation")
        
        
    elif question == "6. Transation Amount and Count of Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")
        
        
    elif question == "7. Transation Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    
    elif question == "8. Registered users of Map User":
       
       states = st.selectbox("Select the State", map_user["States"].unique())
       st.subheader("REGISTERED USERS")
       top_chart_registered_user("map_user", states)
       
       
    elif question == "9. app opens users of Top User":
       
       states = st.selectbox("Select the State", map_user["States"].unique())
       st.subheader("APPOPENS")
       top_chart_appopens("map_user", states)
       
       
    elif question == "10. Registered users of Top User":
       
       st.subheader("REGISTERES USERS")
       top_chart_registered_users("top_user")


