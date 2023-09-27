import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title('Trending Names Data Analysis')
st.markdown('Explore the fascinating journey of baby names over more than a century! Our Trending Names Data Analysis project allows you to delve into the ever-evolving landscape of baby names, spanning from the year 1880 to 2022. Uncover the most popular names, trends, and timeless classics for both genders. From John to Emma, and Michael to Olivia, witness the ebb and flow of names that reflect the culture and preferences of each era. Dive into the data, plot trends, and discover the stories behind the names. Join us on a captivating journey through the world of baby names. Feel free to use or modify this description to make your project more attractive to users.')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Loading the data
all_years = pd.concat(pd.read_csv(f'baby_names/yob{year}.txt', names=['name', 'sex', 'number']).assign(year=year)
                      for year in range(1880, 2023))

# Setting the 'sex', 'name', and 'year' column as index
all_years_indexed = all_years.set_index(['sex', 'name', 'year']).sort_index()

# Setting year as index
all_years_byyears = all_years.set_index(['sex', 'year']).sort_index()

# Define the Streamlit app
def main():
    # Sidebar for user input
    st.sidebar.title("Choose Parameters")
    
    sex = st.sidebar.radio("Select Gender", ("M", "F"))
    names_input = st.sidebar.text_input("Custom Names (comma-separated)", "Michael,John,David,Thomas")
    names = [name.strip() for name in names_input.split(",")]

    selected_year = st.sidebar.selectbox("Select Year to get TOP 10", range(1880, 2023))
    
    # Button to plot names and get top names
    if st.sidebar.button("Compare Names and Get Top 10"):
        plot_comparison(sex, names)
        top_names = getyear(sex, selected_year)
        st.markdown(f"<h2 style='text-align: center;'>Top 10 names for {sex} in {selected_year} are:</h2>", unsafe_allow_html=True)
        display_top_names(top_names)
        plot_top_names(sex, selected_year, top_names)
      
def plot_comparison(sex, names):
    plt.figure(figsize=(12, 6))
    for name in names:
        plotname(sex, name)
    plt.xlabel("Year")
    plt.ylabel("Count")
    st.markdown('<h2 style="text-align: center;">Plot comparing the custom names</h2>', unsafe_allow_html=True)
    plt.legend()
    st.pyplot()

# Plotting number of sex/name babies as a function of year
def plotname(sex, name):
    data = all_years_indexed.loc[(sex, name)]
    plt.plot(data.index.get_level_values('year'), data.values, label=name)
    plt.axis(xmin=1880, xmax=2022)

# Plotting top 10 names by sex for a selected year
def plot_top_names(sex, year, top_names):
    plt.figure(figsize=(12, 6))
    for name in top_names:
        plotname(sex, name)
    plt.xlabel("Year")
    plt.ylabel("Count")
    
    # Set the title using st.markdown
    title_text = f"Top 10 Names for {sex} in {year}"
    st.markdown(f"<h2 style='text-align: center;'>{title_text}</h2>", unsafe_allow_html=True)
    
    plt.legend()
    st.pyplot()

# Display top names with rank
def display_top_names(top_names):
    for i, name in enumerate(top_names, 1):
        st.markdown(f"<h4 style='text-align: center;'>{i}. {name}</h4>", unsafe_allow_html=True)


# Making a function to get top ten names for sex and year
def getyear(sex, selected_year):
    top_names = (all_years_byyears.loc[(sex, selected_year)]
           .sort_values('number', ascending=False)
           .head(10)
           .reset_index()
           .name)
    return top_names

if __name__ == "__main__":
    main()
