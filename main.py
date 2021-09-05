import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('S&P 500 App')


st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
* Attempted By: [Sarthak Sen](https://www.linkedin.com/in/sarthak-sen-657a131a2)
""")

st.sidebar.header('User Input Features')

flag = 0


@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df


df = load_data()
sector = df.groupby('GICS Sector')

sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(
    df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)


def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href


st.markdown(file_download(df_selected_sector), unsafe_allow_html=True)

user_symbol = st.sidebar.text_input('Enter Company Sticker for Graph Plot')
user_symbol = user_symbol.upper()

data = yf.download(
    tickers=list(df_selected_sector[:].Symbol),
    period="ytd",
    interval="1d",
    group_by='ticker',
    auto_adjust=True,
    prepost=True,
    threads=True,
    proxy=None
)


def price_plot(symbol):
    df2 = pd.DataFrame(data[symbol].Close)
    df2['Date'] = df2.index
    plt.fill_between(df2.Date, df2.Close, color='green', alpha=0.3)
    plt.plot(df2.Date, df2.Close, color='green', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    return st.pyplot()


if user_symbol:
    try:
        price_plot(user_symbol)
    except:
        st.markdown("""**Error Fetching Data**""")
