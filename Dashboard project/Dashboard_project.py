#Task1: Importing the libraries
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

st.set_page_config(page_title="Supermarket Dashboard", page_icon=":bar_chart:", layout="wide")

#Task2: Initial Data exploration
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sale3.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    #Adding the 'hour' column to the data frame to  improve schematic
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR PANEL-------
st.sidebar.header("Sidebar Filter")
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)
branch=st.sidebar.multiselect(
    "Select the Branch",
    options=df["Branch"].unique(),
    default=df["Branch"].unique()
)
Payments= st.sidebar.multiselect(
    "Select the Payment Type",
    options=df["Payment"].unique(),
    default=df["Payment"].unique()
)
product_line = st.sidebar.multiselect(
    "Select the Product line",
    options=df["Product_line"].unique(),
    default=df["Product_line"].unique()
)
#Data filter
df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender & Branch ==@branch & Product_line == @product_line & Payment == @Payments"
)
st.dataframe(df_selection)
# ---- MAINPAGE ----
st.title(":bar_chart: Supermarket Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product_line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product_Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# SALES BY BRANCH [BAR CHART]
sales_by_Branch = (
    df_selection.groupby(by=["Branch"]).sum()[["Total"]].sort_values(by="Total")
)
fig_Branch_sales = px.bar(
    sales_by_Branch,
    x="Total",
    y=sales_by_Branch.index,
    orientation="h",
    title="<b>Sales by Branch</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_Branch),
    template="plotly_white",
)
fig_Branch_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
# SALES BY PAYMENT [BAR CHART]
sales_by_Payment = (
    df_selection.groupby(by=["Payment"]).sum()[["Total"]].sort_values(by="Total")
)
fig_Payment_sales = px.bar(
    sales_by_Payment,
    x="Total",
    y=sales_by_Payment.index,
    orientation="h",
    title="<b>Sales by Payment</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_Branch),
    template="plotly_white",
)
fig_Payment_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#Gender Distribution[BAR CHART]
Genderdist = (
    df_selection.groupby(by=["Gender"]).sum()[["Total"]].sort_values(by="Total")
)
fig_Genderdist = px.histogram(
    Genderdist,
    x="Total",
    y=Genderdist.index,
    orientation="h",
    title="<b> Gender distribution </b>",
    color_discrete_sequence=["#0083B8"] * len(Genderdist),
    template="plotly_white",
)
fig_Genderdist.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#GRAPHS LAYOUT
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
left_column.plotly_chart(fig_Branch_sales, use_container_width=True)
left_column.plotly_chart(fig_Genderdist, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_Payment_sales, use_container_width=True)
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)