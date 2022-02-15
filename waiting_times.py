import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib 
from datetime import datetime
# streamlit run waiting_times.py

st.set_page_config(page_title="Waiting time NL", 
                   page_icon=":notes:", 
                   layout='wide')

st.markdown("Daniels asking ***'How long are the waiting times for different specialities'***")

df = pd.read_csv('waiting_time_NL.csv', sep=';').dropna()
specialisms = list(np.unique(df['SPECIALISME']))
specialisms.sort()

# choose speciality

st.markdown("### **Select speciality:**")
select_specialism = []

select_specialism.append(st.selectbox('', specialisms))

this_df = df[df['SPECIALISME'] == select_specialism[0]]
mean_WT = np.median(this_df['WACHTTIJD'].values)
n_samples = len(this_df)
first_date, last_date = str(np.min(df['DATUM_ZORGBEELD'])), str(np.max(df['DATUM_ZORGBEELD']))

# convert date to datetime object
first_date = datetime(year=int(first_date[0:4]), month=int(first_date[4:6]), day=int(first_date[6:8]))
last_date = datetime(year=int(last_date[0:4]), month=int(last_date[4:6]), day=int(last_date[6:8]))
# find place with shortest/longest waiting time
wt_by_hospital = this_df.groupby('NAAM_VESTIGING', as_index=False).median()
wt_by_hospital = wt_by_hospital.sort_values('WACHTTIJD')

shortest_df = wt_by_hospital.iloc[0]
short_median = shortest_df['WACHTTIJD']
short_n = len(this_df[this_df['NAAM_VESTIGING'] == shortest_df['NAAM_VESTIGING']])
longest_df = wt_by_hospital.iloc[-1]
long_n = len(this_df[this_df['NAAM_VESTIGING'] == longest_df['NAAM_VESTIGING']])
long_median = longest_df['WACHTTIJD']

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Median waiting time:**\t{mean_WT:.0f} days")
    st.markdown(f"**Number of samples:**\t{n_samples}")
    st.markdown(f"**Between dates:**\t{first_date.strftime('%d-%b-%Y')} - {last_date.strftime('%d-%b-%Y')}\n\n\n")
    f, ax = plt.subplots(1, figsize=(5,3))
    sns.histplot(this_df['WACHTTIJD'].values, ax=ax)
    ax.set_xlabel('Waiting days')
    sns.despine(ax=ax)
    st.pyplot(f)

with col2:
    st.markdown(f"**Fastest caregiver:**\t{shortest_df['NAAM_VESTIGING']}, n = {short_n}")
    st.markdown(f"**Median waiting time:**\t{short_median:.0f} days")
    st.markdown(f"**Slowest caregiver:**\t{longest_df['NAAM_VESTIGING']}, n = {long_n}")
    st.markdown(f"**Median waiting time:**\t{long_median:.0f} days")

    short_df_full = this_df[this_df['NAAM_VESTIGING'] == shortest_df['NAAM_VESTIGING']]
    long_df_full = this_df[this_df['NAAM_VESTIGING'] == longest_df['NAAM_VESTIGING']]
    f, ax = plt.subplots(1, figsize=(5,3))
    sns.histplot(short_df_full['WACHTTIJD'].values, ax=ax,
                label=shortest_df['NAAM_VESTIGING'], color='red')
    sns.histplot(long_df_full['WACHTTIJD'].values, ax=ax, label=longest_df['NAAM_VESTIGING'],
                color='green')
    plt.legend()
    ax.set_xlabel('Waiting days')
    sns.despine(ax=ax)
    st.pyplot(f)