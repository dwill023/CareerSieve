"""
# Job Scraper App
This streamlit app utilizes a job scraper to combine a job search across multiple job sites into one table.
"""
import streamlit as st
from jobspy import scrape_jobs
import pandas as pd
import base64
from PIL import Image, ImageEnhance


# Streamlit Page Configuration
st.set_page_config(
    page_title="CareerSieve",
    page_icon="imgs/logo.jpg",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": "https://github.com/dwill023/CareerSieve",
        "Report a bug": "https://github.com/dwill023/CareerSieve/issues",
        "About": """
            ## CareerSieve
            [![Github](https://skillicons.dev/icons?i=github)](https://github.com/dwill023/CareerSieve)

            With CareerSieve, you can specify key criteria—such as job title, location, or industry—and let the app do the heavy lifting, eliminating the noise and delivering a refined list of openings directly to your screen. 
        """
    }
)

def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logging.error(f"Error converting image to base64: {str(e)}")
        return None

def custom_function(selected_sources, role, loc, dist, numeric_input, is_remote):
    """
    A custom function that creates a DataFrame from the user inputs.
    
    Parameters:
    - selected_sources: list of selected source labels from the checkbox input.
    - role: text input string from the role input.
    - loc: text input string from the loc input.
    - numeric_input: numeric input value (hours).
    
    Returns:
    - A pandas DataFrame.
    """

    if is_remote:
        jobs = scrape_jobs(
            site_name = selected_sources,
            search_term = role,
            google_search_term = role,
            location = loc,
            distance = dist,
            is_remote = True,
            results_wanted = 50,
            hours_old = numeric_input,
            country_indeed = 'USA')
    else:
        jobs = scrape_jobs(
            site_name = selected_sources,
            search_term = role,
            google_search_term = role,
            location = loc,
            distance = dist,
            is_remote = False,
            results_wanted = 50,
            hours_old = numeric_input,
            country_indeed = 'USA')

    jobs = pd.DataFrame(jobs)
    return jobs

def main():
    st.title("CareerSieve")
    st.write("Your personal assistant in the quest for career success, ensuring you never miss the perfect opportunity. It actively sifts through multiple job boards and aggregators, using advanced web scraping techniques to filter and curate the most relevant career opportunities based on your preferences.")

    # Load and display sidebar image
    img_path = "imgs/logo_sidebar.jpg"
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
            unsafe_allow_html=True,
        )

    # Define checkbox options
    options = {
        "indeed": "Indeed",
        "linkedin": "LinkedIn",
        "zip_recruiter": "Zip Recruiter",
        "glassdoor": "Glassdoor",
        "google": "Google"
    }
    
    st.sidebar.subheader("Select Job Site")
    # Create checkboxes for each option and collect selected sources.
    selected_sources = []
    for key, label in options.items():
        if st.sidebar.checkbox(label, key=key):
            selected_sources.append(label)
    
    #st.sidebar.subheader("Text Inputs")
    # Two text inputs.
    role = st.sidebar.text_input("The Role You're Looking For", key = "Web Developer")
    loc = st.sidebar.text_input("Location of the Job Role", key = "Los Angeles, CA")
    dist = st.sidebar.number_input("Distance from location (in miles)", min_value=10, max_value=200, value=50, step=1, help = "Min distance is 10 and max distance is 200.")
    
    #st.sidebar.subheader("Numeric Input")
    # Numeric input: value in hours with minimum 24 and maximum 168.
    numeric_input = st.sidebar.number_input("How Long the Role Has Been Posted (in hours)", min_value=24, max_value=168, value=24, step=1)
    is_remote = st.sidebar.checkbox("Remote Roles Only", value=True, help="If you only want remote roles select checkbox. Desselect for non-remote roles.", label_visibility="visible")
    
    # Action button to run the custom function.
    if st.sidebar.button("Generate Jobs"):
        with st.spinner('Generating Jobs Table...'):
            df = custom_function(selected_sources, role, loc, dist, numeric_input, is_remote)
            st.success('Done!')
            st.write("### Jobs Table")
            st.dataframe(df, hide_index=True)

if __name__ == "__main__":
    main()
