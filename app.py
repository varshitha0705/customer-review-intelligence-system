import streamlit as st
import plotly.express as px
from utils.preprocess import load_amazon_reviews

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Customer Review Intelligence",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Customer Review Intelligence System")

# -----------------------------
# Load Dataset
# -----------------------------
df = load_amazon_reviews("data/All_Beauty.json.gz")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.title("🔍 Filters")

selected_rating = st.sidebar.selectbox(
    "⭐ Select Rating",
    ["All", 1, 2, 3, 4, 5]
)

selected_verified = st.sidebar.selectbox(
    "✔ Verified Purchase",
    ["All", True, False]
)

search_review = st.sidebar.text_input(
    "🔍 Search Review"
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

# Filter by Rating
if selected_rating != "All":
    filtered_df = filtered_df[
        filtered_df["Rating"] == selected_rating
    ]

# Filter by Verified
if selected_verified != "All":
    filtered_df = filtered_df[
        filtered_df["Verified"] == selected_verified
    ]

# Filter by Search
if search_review:
    filtered_df = filtered_df[
        filtered_df["Review"].str.contains(
            search_review,
            case=False,
            na=False
        )
    ]

# -----------------------------
# KPI Cards
# -----------------------------
total_reviews = len(filtered_df)

average_rating = round(filtered_df["Rating"].mean(), 2)

verified_reviews = filtered_df["Verified"].sum()

unique_products = filtered_df["Product_ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("📝 Total Reviews", total_reviews)

col2.metric("⭐ Average Rating", average_rating)

col3.metric("✔ Verified Reviews", verified_reviews)

col4.metric("📦 Products", unique_products)

# -----------------------------
# Rating Distribution
# -----------------------------
st.divider()

st.subheader("⭐ Rating Distribution")

rating_counts = (
    filtered_df["Rating"]
    .value_counts()
    .sort_index()
)

fig = px.bar(
    x=rating_counts.index,
    y=rating_counts.values,
    labels={
        "x": "Rating",
        "y": "Number of Reviews"
    },
    title="Distribution of Customer Ratings"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Review Table
# -----------------------------
st.subheader("📋 Reviews")

st.dataframe(
    filtered_df,
    use_container_width=True
)