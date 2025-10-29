# import streamlit as st
# import pandas as pd
# import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import matplotlib.pyplot as plt
# import seaborn as sns
# import io # Used for handling byte data for file upload

# # --- NLTK Setup ---
# # Attempt to download VADER lexicon only if it's not already present
# # This uses a simple try/except block to handle the potential LookupError
# try:
#     sid = SentimentIntensityAnalyzer()
# except LookupError:
#     # Use quiet=True so it doesn't clutter the Streamlit app output
#     nltk.download('vader_lexicon', quiet=True)
#     sid = SentimentIntensityAnalyzer()

# # -----------------------------------------------------------------
# # Core Functions
# # -----------------------------------------------------------------

# def analyze_sentiment(text):
#     """Calculates VADER sentiment scores and classifies overall sentiment."""
#     if pd.isna(text) or str(text).strip() == "":
#         return 0, 0, 0, 0, 'Neutral'

#     try:
#         # Ensure text is treated as a string
#         scores = sid.polarity_scores(str(text))
#     except Exception as e:
#         st.error(f"Error analyzing text: {e}")
#         return 0, 0, 0, 0, 'Neutral'

#     compound = scores['compound']
    
#     # Classify sentiment based on compound score
#     # Standard VADER thresholds
#     if compound >= 0.05:
#         sentiment = 'Positive'
#     elif compound <= -0.05:
#         sentiment = 'Negative'
#     else:
#         sentiment = 'Neutral'
    
#     return scores['neg'], scores['neu'], scores['pos'], compound, sentiment

# def load_data(uploaded_file):
#     """Loads CSV or Excel data into a Pandas DataFrame."""
#     try:
#         # Check file type
#         if uploaded_file.name.endswith('.csv'):
#             # Read CSV with a robust encoding fallback
#             df = pd.read_csv(uploaded_file, encoding='utf-8')
#         elif uploaded_file.name.endswith(('.xlsx', '.xls')):
#             # pandas handles .xlsx and .xls, openpyxl is needed in the environment
#             df = pd.read_excel(uploaded_file, engine='openpyxl')
#         else:
#             st.error("Unsupported file type. Please upload a CSV or Excel file (.xlsx, .xls).")
#             return None
#         return df
#     except Exception as e:
#         st.error(f"Error loading file: {e}. Please check file format and encoding.")
#         return None

# # -----------------------------------------------------------------
# # Streamlit UI/Layout
# # -----------------------------------------------------------------

# def main():
#     st.set_page_config(
#         page_title="Feedback Sentiment Analyzer",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

#     st.title("Customer Feedback Analysis Dashboard 📊")
#     st.markdown("Upload your customer feedback data (CSV or Excel) to generate sentiment summaries and visualizations.")
    
#     # --- File Upload Section (Sidebar) ---
#     with st.sidebar:
#         st.header("1. Upload Data")
#         uploaded_file = st.file_uploader(
#             "Upload your CSV or Excel file",
#             type=['csv', 'xlsx', 'xls'],
#             help="Your file should contain a column with customer feedback text."
#         )

#     # Check if a file is uploaded
#     if uploaded_file is not None:
#         df = load_data(uploaded_file)
        
#         if df is not None:
#             # --- Column Selection (Sidebar) ---
#             with st.sidebar:
#                 st.header("2. Configure Analysis")
#                 # Identify potential text columns (object/string types)
#                 text_columns = [col for col, dtype in df.dtypes.items() if dtype == 'object']
                
#                 if not text_columns:
#                     st.error("Could not find any suitable text columns in your data.")
#                     return

#                 text_column = st.selectbox(
#                     "Select the column containing Feedback Text:",
#                     options=text_columns,
#                     index=0, # Default to the first detected text column
#                     help="Choose the column that holds the textual feedback/comments."
#                 )

#                 st.subheader("Processing...")
                
#                 # --- Apply Sentiment Analysis ---
#                 with st.spinner(f"Analyzing sentiment in the '{text_column}' column..."):
#                     # Apply the analysis function
#                     df[['neg', 'neu', 'pos', 'compound', 'Sentiment']] = df[text_column].apply(
#                         lambda x: pd.Series(analyze_sentiment(x))
#                     )
#                 st.success("Analysis Complete!")

#             # --- Main Dashboard Layout ---
#             st.header("Analysis Results")
            
#             # 1. Summary Metrics & Data Preview
#             col1, col2 = st.columns([1, 2])
            
#             with col1:
#                 total_feedback = len(df)
#                 st.metric("Total Feedback Items", f"{total_feedback:,}")
                
#                 sentiment_counts = df['Sentiment'].value_counts()
                
#                 # Find most common sentiment
#                 if not sentiment_counts.empty:
#                     most_common_sentiment = sentiment_counts.idxmax()
#                     st.markdown(f"**Dominant Sentiment:** <span style='font-size: 1.5rem; font-weight: bold;'>{most_common_sentiment}</span>", unsafe_allow_html=True)
                
#                 st.subheader("Raw Data Preview")
#                 st.dataframe(df.head(5), use_container_width=True)
            
#             with col2:
#                 st.subheader("Overall Sentiment Distribution")
                
#                 # --- Sentiment Distribution Chart (Pie Chart) ---
#                 if not sentiment_counts.empty:
#                     fig, ax = plt.subplots(figsize=(8, 8))
                    
#                     # Define colors for better visualization
#                     colors = {
#                         'Positive': '#4CAF50',
#                         'Negative': '#F44336',
#                         'Neutral': '#FFC107'
#                     }
                    
#                     # Ensure all categories are present for consistent coloring
#                     categories = ['Positive', 'Negative', 'Neutral']
#                     sizes = [sentiment_counts.get(cat, 0) for cat in categories]
#                     plot_colors = [colors.get(cat) for cat in categories if sentiment_counts.get(cat, 0) > 0]
#                     labels = [f'{cat} ({count})' for cat, count in zip(categories, sizes) if count > 0]

#                     ax.pie(
#                         sizes,
#                         labels=labels,
#                         autopct='%1.1f%%',
#                         startangle=90,
#                         colors=plot_colors,
#                         wedgeprops={'edgecolor': 'black'}
#                     )
#                     ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
#                     st.pyplot(fig, use_container_width=True)
#                 else:
#                     st.info("No sentiment data found to visualize.")


#             # 2. Detailed Sentiment Breakdown
#             st.markdown("---")
#             st.header("Detailed Insights")
            
#             col3, col4 = st.columns(2)
            
#             with col3:
#                 st.subheader("Compound Score Histogram")
                
#                 # Histogram of the compound score
#                 fig, ax = plt.subplots(figsize=(10, 6))
#                 sns.histplot(df['compound'], bins=30, kde=True, ax=ax, color='#1E88E5')
#                 ax.set_title('Distribution of Compound Sentiment Scores', fontsize=14)
#                 ax.set_xlabel('Compound Score', fontsize=12)
#                 ax.set_ylabel('Frequency', fontsize=12)
#                 ax.axvline(0.05, color='green', linestyle='--', label='Positive Threshold (0.05)')
#                 ax.axvline(-0.05, color='red', linestyle='--', label='Negative Threshold (-0.05)')
#                 ax.legend()
#                 st.pyplot(fig, use_container_width=True)

#             with col4:
#                 st.subheader("Average Polarity Scores by Sentiment")
                
#                 # Average polarity scores for each sentiment category
#                 sentiment_avg = df.groupby('Sentiment')[['neg', 'neu', 'pos']].mean().reset_index()
#                 sentiment_avg_melt = sentiment_avg.melt(
#                     id_vars='Sentiment', 
#                     var_name='Polarity Type', 
#                     value_name='Average Score'
#                 )

#                 fig, ax = plt.subplots(figsize=(10, 6))
#                 sns.barplot(
#                     x='Sentiment', 
#                     y='Average Score', 
#                     hue='Polarity Type', 
#                     data=sentiment_avg_melt,
#                     palette={'neg': '#F44336', 'neu': '#FFC107', 'pos': '#4CAF50'},
#                     ax=ax
#                 )
#                 ax.set_title('Average Neg, Neu, and Pos Scores per Sentiment Category', fontsize=14)
#                 ax.set_xlabel('Sentiment Category', fontsize=12)
#                 ax.set_ylabel('Average Score', fontsize=12)
#                 ax.legend(title='Polarity Type')
#                 st.pyplot(fig, use_container_width=True)


#             # 3. Top/Bottom Feedback Examples
#             st.markdown("---")
#             st.subheader("Extreme Feedback Examples")
            
#             col5, col6 = st.columns(2)
            
#             with col5:
#                 st.markdown("#### Top 5 Most Positive Feedback")
#                 # Sort by compound score descending
#                 top_positive = df.sort_values(by='compound', ascending=False).head(5)
#                 # Display only the relevant text and score
#                 for index, row in top_positive.iterrows():
#                     st.info(f"**Score:** {row['compound']:.4f} \n\n *{row[text_column]}*")
            
#             with col6:
#                 st.markdown("#### Top 5 Most Negative Feedback")
#                 # Sort by compound score ascending
#                 top_negative = df.sort_values(by='compound', ascending=True).head(5)
#                 # Display only the relevant text and score
#                 for index, row in top_negative.iterrows():
#                     st.warning(f"**Score:** {row['compound']:.4f} \n\n *{row[text_column]}*")
            
#             st.markdown("---")
            
#             st.subheader("Complete Processed Data")
#             st.markdown("The table below includes the calculated `neg`, `neu`, `pos`, `compound`, and final `Sentiment` columns.")
#             # Display the full processed table
#             st.dataframe(df, use_container_width=True)

#     else:
#         # Initial state before file upload
#         st.info("Awaiting file upload. Please use the sidebar to upload your data.")
#         st.markdown(
#             """
#             ### Quick Start Guide:
#             1. Go to the **'1. Upload Data'** section in the left sidebar.
#             2. Upload your **CSV or Excel** file containing customer feedback.
#             3. In the **'2. Configure Analysis'** section, select the column that holds the **textual feedback**.
#             4. The dashboard will automatically update with sentiment analysis, charts, and summaries!
#             """
#         )

# if __name__ == '__main__':
#     main()








import streamlit as st
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import io 

# --- NLTK Setup ---

# Use st.cache_resource to initialize the SentimentIntensityAnalyzer once.
# This prevents re-downloading/re-initializing NLTK components on every rerun.
@st.cache_resource
def setup_nltk():
    """Initializes NLTK VADER and downloads the lexicon if missing."""
    try:
        # Check if the lexicon is available
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        # Download the lexicon if not found
        nltk.download('vader_lexicon', quiet=True)
    
    # Return the initialized analyzer
    return SentimentIntensityAnalyzer()

sid = setup_nltk()

# -----------------------------------------------------------------
# Core Functions - Use Caching for computationally heavy steps
# -----------------------------------------------------------------

@st.cache_data(show_spinner=False)
def analyze_sentiment(text):
    """Calculates VADER sentiment scores and classifies overall sentiment.
    
    Caching this function ensures that the VADER analysis is only run once
    for any given piece of text across all streamlit runs.
    """
    # Use the global sid object initialized via @st.cache_resource
    
    if pd.isna(text) or str(text).strip() == "":
        return 0.0, 0.0, 0.0, 0.0, 'Neutral'

    try:
        # Ensure text is treated as a string
        scores = sid.polarity_scores(str(text))
    except Exception as e:
        # Log error but return neutral to prevent app crash
        # st.error(f"Error analyzing text: {e}") # Removed to avoid cluttering UI on mass apply
        return 0.0, 0.0, 0.0, 0.0, 'Neutral'

    compound = scores['compound']
    
    # Classify sentiment based on compound score (Standard VADER thresholds)
    if compound >= 0.05:
        sentiment = 'Positive'
    elif compound <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    # Return floats with consistent type for pandas Series
    return scores['neg'], scores['neu'], scores['pos'], compound, sentiment

@st.cache_data(show_spinner=False)
def load_data(uploaded_file):
    """Loads CSV or Excel data into a Pandas DataFrame."""
    try:
        # Check file type
        file_name = uploaded_file.name.lower()
        if file_name.endswith('.csv'):
            # Read CSV with a robust encoding fallback
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        elif file_name.endswith(('.xlsx', '.xls')):
            # pandas handles .xlsx and .xls, openpyxl is needed in the environment
            # NOTE: You must ensure 'openpyxl' is in your requirements.txt!
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file (.xlsx, .xls).")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}. Please check file format, encoding, or ensure 'openpyxl' is installed for Excel files.")
        return None

@st.cache_data(show_spinner="Applying sentiment analysis...")
def apply_analysis_to_df(df, text_column):
    """Applies the sentiment analysis function to the selected column of the DataFrame.
    
    Caching this function ensures the long analysis process doesn't repeat 
    unless the input DataFrame or column selection changes.
    """
    df_copy = df.copy() # Work on a copy to ensure immutability for caching
    
    # Apply the analysis function
    df_copy[['neg', 'neu', 'pos', 'compound', 'Sentiment']] = df_copy[text_column].apply(
        lambda x: pd.Series(analyze_sentiment(x))
    )
    return df_copy

# -----------------------------------------------------------------
# Streamlit UI/Layout
# -----------------------------------------------------------------

def main():
    # Configure page settings
    st.set_page_config(
        page_title="Feedback Sentiment Analyzer",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Customer Feedback Analysis Dashboard 📊")
    st.markdown("Upload your customer feedback data (CSV or Excel) to generate sentiment summaries and visualizations.")
    
    # --- File Upload Section (Sidebar) ---
    with st.sidebar:
        st.header("1. Upload Data")
        uploaded_file = st.file_uploader(
            "Upload your CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Your file should contain a column with customer feedback text."
        )

    # Check if a file is uploaded
    if uploaded_file is not None:
        # Load data (cached)
        df = load_data(uploaded_file)
        
        if df is not None:
            # --- Column Selection & Analysis (Sidebar) ---
            with st.sidebar:
                st.header("2. Configure Analysis")
                # Identify potential text columns (object/string types)
                text_columns = [col for col, dtype in df.dtypes.items() if dtype == 'object']
                
                if not text_columns:
                    st.error("Could not find any suitable text columns in your data.")
                    return

                text_column = st.selectbox(
                    "Select the column containing **Feedback Text**:",
                    options=text_columns,
                    index=0, # Default to the first detected text column
                    help="Choose the column that holds the textual feedback/comments."
                )

                # Apply Sentiment Analysis (cached)
                # The caching decorator handles the spinner display
                processed_df = apply_analysis_to_df(df, text_column)
                
                st.success("Analysis Complete!")


            # --- Main Dashboard Layout ---
            st.header("Analysis Results")
            
            # 1. Summary Metrics & Data Preview
            col1, col2 = st.columns([1, 2])
            
            # Calculate metrics
            total_feedback = len(processed_df)
            sentiment_counts = processed_df['Sentiment'].value_counts()
            
            with col1:
                st.metric("Total Feedback Items", f"{total_feedback:,}")
                
                # Find most common sentiment
                if not sentiment_counts.empty:
                    most_common_sentiment = sentiment_counts.idxmax()
                    st.markdown(f"**Dominant Sentiment:** <span style='font-size: 1.5rem; font-weight: bold;'>{most_common_sentiment}</span>", unsafe_allow_html=True)
                
                st.subheader("Raw Data Preview")
                st.dataframe(processed_df.head(5), use_container_width=True)
            
            with col2:
                st.subheader("Overall Sentiment Distribution")
                
                # --- Sentiment Distribution Chart (Pie Chart) ---
                if not sentiment_counts.empty:
                    # Use st.cache_data for chart generation as well
                    @st.cache_data
                    def plot_pie_chart(counts):
                        fig, ax = plt.subplots(figsize=(8, 8))
                        colors = {
                            'Positive': '#4CAF50', # Green
                            'Negative': '#F44336', # Red
                            'Neutral': '#FFC107' # Yellow
                        }
                        
                        categories = ['Positive', 'Negative', 'Neutral']
                        sizes = [counts.get(cat, 0) for cat in categories]
                        # Filter out zero-sized slices for cleaner plotting
                        plot_colors = [colors.get(cat) for cat, size in zip(categories, sizes) if size > 0]
                        labels = [f'{cat} ({count})' for cat, count in zip(categories, sizes) if count > 0]

                        ax.pie(
                            [size for size in sizes if size > 0],
                            labels=labels,
                            autopct='%1.1f%%',
                            startangle=90,
                            colors=plot_colors,
                            wedgeprops={'edgecolor': 'black'}
                        )
                        ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
                        return fig

                    st.pyplot(plot_pie_chart(sentiment_counts), use_container_width=True)
                else:
                    st.info("No sentiment data found to visualize.")


            # 2. Detailed Sentiment Breakdown
            st.markdown("---")
            st.header("Detailed Insights")
            
            col3, col4 = st.columns(2)
            
            # Use a cached function for plotting to speed up reruns
            @st.cache_data
            def plot_detailed_charts(df_input, text_col):
                # --- Compound Score Histogram ---
                fig1, ax1 = plt.subplots(figsize=(10, 6))
                sns.histplot(df_input['compound'], bins=30, kde=True, ax=ax1, color='#1E88E5')
                ax1.set_title('Distribution of Compound Sentiment Scores', fontsize=14)
                ax1.set_xlabel('Compound Score', fontsize=12)
                ax1.set_ylabel('Frequency', fontsize=12)
                ax1.axvline(0.05, color='green', linestyle='--', label='Positive Threshold (0.05)')
                ax1.axvline(-0.05, color='red', linestyle='--', label='Negative Threshold (-0.05)')
                ax1.legend()

                # --- Average Polarity Scores by Sentiment ---
                sentiment_avg = df_input.groupby('Sentiment')[['neg', 'neu', 'pos']].mean().reset_index()
                sentiment_avg_melt = sentiment_avg.melt(
                    id_vars='Sentiment', 
                    var_name='Polarity Type', 
                    value_name='Average Score'
                )

                fig2, ax2 = plt.subplots(figsize=(10, 6))
                sns.barplot(
                    x='Sentiment', 
                    y='Average Score', 
                    hue='Polarity Type', 
                    data=sentiment_avg_melt,
                    palette={'neg': '#F44336', 'neu': '#FFC107', 'pos': '#4CAF50'},
                    ax=ax2
                )
                ax2.set_title('Average Neg, Neu, and Pos Scores per Sentiment Category', fontsize=14)
                ax2.set_xlabel('Sentiment Category', fontsize=12)
                ax2.set_ylabel('Average Score', fontsize=12)
                ax2.legend(title='Polarity Type')

                return fig1, fig2

            hist_fig, bar_fig = plot_detailed_charts(processed_df, text_column)
            
            with col3:
                st.subheader("Compound Score Histogram")
                st.pyplot(hist_fig, use_container_width=True)

            with col4:
                st.subheader("Average Polarity Scores by Sentiment")
                st.pyplot(bar_fig, use_container_width=True)


            # 3. Top/Bottom Feedback Examples
            st.markdown("---")
            st.subheader("Extreme Feedback Examples")
            
            col5, col6 = st.columns(2)
            
            # Sort data once for efficiency
            top_positive = processed_df.sort_values(by='compound', ascending=False).head(5)
            top_negative = processed_df.sort_values(by='compound', ascending=True).head(5)

            with col5:
                st.markdown("#### Top 5 Most **Positive** Feedback")
                # Display only the relevant text and score
                for index, row in top_positive.iterrows():
                    # Check for non-null/non-empty text before displaying
                    if pd.notna(row[text_column]) and str(row[text_column]).strip() != "":
                        st.info(f"**Score:** `{row['compound']:.4f}` \n\n *{row[text_column]}*")
            
            with col6:
                st.markdown("#### Top 5 Most **Negative** Feedback")
                # Display only the relevant text and score
                for index, row in top_negative.iterrows():
                    # Check for non-null/non-empty text before displaying
                    if pd.notna(row[text_column]) and str(row[text_column]).strip() != "":
                        st.warning(f"**Score:** `{row['compound']:.4f}` \n\n *{row[text_column]}*")
            
            st.markdown("---")
            
            st.subheader("Complete Processed Data")
            st.markdown("The table below includes the calculated `neg`, `neu`, `pos`, `compound`, and final `Sentiment` columns.")
            # Display the full processed table
            st.dataframe(processed_df, use_container_width=True)

    else:
        # Initial state before file upload
        st.info("Awaiting file upload. Please use the sidebar to upload your data.")
        st.markdown(
            """
            ### Quick Start Guide:
            1. Go to the **'1. Upload Data'** section in the left sidebar.
            2. Upload your **CSV or Excel** file containing customer feedback.
            3. In the **'2. Configure Analysis'** section, select the column that holds the **textual feedback**.
            4. The dashboard will automatically update with sentiment analysis, charts, and summaries!
            """
        )

if __name__ == '__main__':
    main()
