import streamlit as st
import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine

# Configure Streamlit page
PAGE_CONFIG = {
    "page_title": "Streamlit with SQLite",
    "page_icon": ":smiley:",
    "layout": "centered"
}
st.set_page_config(**PAGE_CONFIG)

# Create or connect to SQLite database
def init_database():
    """Initialize the SQLite database with sample movie data."""
    db_path = 'movies.db'
    
    # Only create if it doesn't exist
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS movies
                     (title text, rating real, year integer)''')
        
        # Insert sample data
        sample_movies = [
            ('Inception', 8.8, 2010),
            ('The Dark Knight', 9.0, 2008),
            ('Interstellar', 8.6, 2014),
            ('The Matrix', 8.7, 1999),
            ('Pulp Fiction', 8.9, 1994),
            ('Forrest Gump', 8.8, 1994),
            ('The Shawshank Redemption', 9.3, 1994)
        ]
        c.executemany('INSERT INTO movies VALUES (?,?,?)', sample_movies)
        conn.commit()
        conn.close()
    
    return create_engine('sqlite:///movies.db')

# Initialize database
engine_imdb = init_database()

def hist_all_movies(sql, engine):
    """Display histogram of movie ratings from SQL query."""
    try:
        df_movies = pd.read_sql_query(sql, con=engine)
        if not df_movies.empty and 'rating' in df_movies.columns:
            fig = df_movies['rating'].hist().get_figure()
            st.pyplot(fig)
        else:
            st.warning("No data found for this query or 'rating' column not found.")
    except Exception as e:
        st.error(f"Error executing query: {e}")

def main():
    """Main application function."""
    st.title("Streamlit with SQLite")
    st.subheader("Running from Vercel using local DB")
    
    # Sidebar menu
    menu = ["Page 1", "Page 2", "Page 3"]
    choice = st.sidebar.selectbox('Menu', menu)
    
    if choice == 'Page 1':
        st.subheader("Welcome")
        st.write(
            "This app uses a local SQLite database with sample movie data. "
            "Navigate through the menu to explore different features."
        )
        
    elif choice == 'Page 2':
        st.subheader("SQL Query Interface")
        st.write("Enter a SQL query to analyze movie ratings.")
        SQL_script = st.text_area(
            label='SQL Input',
            value='SELECT rating FROM movies',
            height=100
        )
        
        if st.button("Execute Query"):
            hist_all_movies(SQL_script, engine_imdb)
    
    elif choice == 'Page 3':
        st.subheader("Movie Data Explorer")
        slider_value = st.slider('Number of rows to display', min_value=1, max_value=10)
        
        try:
            df_movies = pd.read_sql(
                f"SELECT * FROM movies LIMIT {slider_value}",
                con=engine_imdb
            )
            
            if not df_movies.empty and 'rating' in df_movies.columns:
                st.write("Movie Ratings Visualization:")
                fig = df_movies['rating'].plot(kind='bar').get_figure()
                st.pyplot(fig)
            
            show_dataframe = st.checkbox('Display Dataframe')
            if show_dataframe and not df_movies.empty:
                st.dataframe(df_movies)
        except Exception as e:
            st.error(f"Error loading data: {e}")

if __name__ == '__main__':
    main()
