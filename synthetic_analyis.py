import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("products.csv")

df_products = load_data()

# Color themes
color_themes = {
    "ocean": {"primary": "#1ABC9C"},
    "sunset": {"primary": "#E67E22"},
    "forest": {"primary": "#27AE60"},
    "neon": {"primary": "#8E44AD"},
    "monochrome": {"primary": "#7F8C8D"},
    "icecream": {"primary": "#FADBD8"},
    "corporate": {"primary": "#2980B9"},
}

st.title("📊 Product Data Insights Dashboard")

# Global color theme selector
if "global_theme" not in st.session_state:
    st.session_state.global_theme = "ocean"
st.session_state.global_theme = st.selectbox(
    "🎨 Choose a global color theme for all charts:",
    list(color_themes.keys()),
    index=0
)

# Show data sample
st.subheader("📄 Dataset Preview")
st.dataframe(df_products.head())

# CHART 1: Average Price per Manufacturer
def chart_1(chart_type):
    theme = st.session_state.global_theme
    avg_price = df_products.groupby("manufacturer")["price"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type == "Bar":
        ax.barh(avg_price.index, avg_price.values, color=color_themes[theme]["primary"])
    elif chart_type == "Line":
        ax.plot(avg_price.values, avg_price.index, color=color_themes[theme]["primary"], marker="o")
    elif chart_type == "Pie":
        ax.pie(avg_price.values, labels=avg_price.index, autopct="%1.1f%%", colors=[color_themes[theme]["primary"]]*len(avg_price))
        ax.set_aspect('equal')
    if chart_type != "Pie":
        ax.set_xlabel("Average Price (£)")
        ax.set_ylabel("Manufacturer")
        ax.set_title("Average Product Price per Manufacturer", fontsize=14, fontweight="bold")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"£{x:.0f}"))
    else:
        ax.set_title("Average Price Distribution (Pie)", fontsize=14, fontweight="bold")
    st.pyplot(fig)
    st.markdown(f"**Insight:** {avg_price.idxmax()} has the highest average product price: £{avg_price.max():.2f}")

# Chart 1 UI
with st.expander("📌 Chart 1: Average Price per Manufacturer"):
    chart_type_1 = st.selectbox("📊 Choose chart type (default is recommended):", ["Bar", "Line", "Pie"], index=0, key="chart_type_1")
    chart_1(chart_type_1)

# CHART 2: Most Expensive Product per Manufacturer
def chart_2(chart_type):
    theme = st.session_state.global_theme
    max_price = df_products.groupby("manufacturer")["price"].max().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type == "Bar":
        ax.barh(max_price.index, max_price.values, color=color_themes[theme]["primary"])
    elif chart_type == "Line":
        ax.plot(max_price.values, max_price.index, color=color_themes[theme]["primary"], marker="o")
    elif chart_type == "Pie":
        ax.pie(max_price.values, labels=max_price.index, autopct="%1.1f%%", colors=[color_themes[theme]["primary"]]*len(max_price))
        ax.set_aspect('equal')
    if chart_type != "Pie":
        ax.set_xlabel("Maximum Price (£)")
        ax.set_ylabel("Manufacturer")
        ax.set_title("Most Expensive Product per Manufacturer", fontsize=14, fontweight="bold")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"£{x:.0f}"))
    else:
        ax.set_title("Max Price Distribution (Pie)", fontsize=14, fontweight="bold")
    st.pyplot(fig)
    st.markdown(f"**Insight:** {max_price.idxmax()} has the single most expensive product: £{max_price.max():.2f}")

# Chart 2 UI
with st.expander("📌 Chart 2: Most Expensive Product per Manufacturer"):
    chart_type_2 = st.selectbox("📊 Choose chart type (default is recommended):", ["Bar", "Line", "Pie"], index=0, key="chart_type_2")
    chart_2(chart_type_2)

# CHART 3: Cheapest Product per Manufacturer
def chart_3(chart_type):
    theme = st.session_state.global_theme
    min_price = df_products.groupby("manufacturer")["price"].min().sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type == "Bar":
        ax.barh(min_price.index, min_price.values, color=color_themes[theme]["primary"])
    elif chart_type == "Line":
        ax.plot(min_price.values, min_price.index, color=color_themes[theme]["primary"], marker="o")
    elif chart_type == "Pie":
        ax.pie(min_price.values, labels=min_price.index, autopct="%1.1f%%", colors=[color_themes[theme]["primary"]]*len(min_price))
        ax.set_aspect('equal')
    if chart_type != "Pie":
        ax.set_xlabel("Minimum Price (£)")
        ax.set_ylabel("Manufacturer")
        ax.set_title("Cheapest Product per Manufacturer", fontsize=14, fontweight="bold")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"£{x:.0f}"))
    else:
        ax.set_title("Min Price Distribution (Pie)", fontsize=14, fontweight="bold")
    st.pyplot(fig)
    st.markdown(f"**Insight:** {min_price.idxmin()} offers the cheapest product at: £{min_price.min():.2f}")

# Chart 3 UI
with st.expander("📌 Chart 3: Cheapest Product per Manufacturer"):
    chart_type_3 = st.selectbox("📊 Choose chart type (default is recommended):", ["Bar", "Line", "Pie"], index=0, key="chart_type_3")
    chart_3(chart_type_3)




# CHART 4: Top 10 Products by Units Sold
def chart_4(chart_type):
    theme = st.session_state.global_theme
    top_units = df_products.sort_values("units_sold_12m", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(top_units["product_name"], top_units["units_sold_12m"], color=color_themes[theme]["primary"])
        else:
            ax.plot(top_units["units_sold_12m"], top_units["product_name"], marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Units Sold")
        ax.set_title("Top 10 Products by Units Sold")
    else:
        ax.pie(top_units["units_sold_12m"], labels=top_units["product_name"], autopct="%1.1f%%", colors=[color_themes[theme]["primary"]]*10)
        ax.set_title("Top 10 Products by Units Sold (Pie)")
        ax.set_aspect('equal')
    st.pyplot(fig)
    st.markdown("**Insight:** These 10 products had the highest customer demand over the past year.")

# UI block for charts 4
with st.expander("📌 Chart 4: Top 10 Products by Units Sold"):
    chart_type_4 = st.selectbox("📊 Choose chart type (default is recommended):", ["Bar", "Line", "Pie"], index=0, key="chart_type_4")
    chart_4(chart_type_4)


# CHART 5: Total Revenue by Manufacturer
def chart_5(chart_type):
    theme = st.session_state.global_theme
    df_products["revenue"] = df_products["price"] * df_products["units_sold_12m"]
    revenue = df_products.groupby("manufacturer")["revenue"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(revenue.index, revenue.values, color=color_themes[theme]["primary"])
        else:
            ax.plot(revenue.values, revenue.index, marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Total Revenue (£)")
        ax.set_title("Total Revenue by Manufacturer")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"£{x/1000:.0f}K"))
    else:
        ax.pie(revenue.values, labels=revenue.index, autopct="%1.1f%%", colors=[color_themes[theme]["primary"]]*len(revenue))
        ax.set_title("Revenue Share by Manufacturer")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown(f"**Insight:** {revenue.idxmax()} generated the most revenue overall.")

# CHART 5 UI BLOCK
with st.expander("📌 Chart 5: Total Revenue by Manufacturer"):
    chart_type_5 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_5"
    )
    chart_5(chart_type_5)


# CHART 6: Stock Value by Manufacturer
def chart_6(chart_type):
    theme = st.session_state.global_theme
    df_products["stock_value"] = df_products["price"] * df_products["stock_level"]
    stock_value = df_products.groupby("manufacturer")["stock_value"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(stock_value.index, stock_value.values, color=color_themes[theme]["primary"])
        else:
            ax.plot(stock_value.values, stock_value.index, marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Stock Value (£)")
        ax.set_title("Stock Value by Manufacturer")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"£{x/1000:.0f}K"))
    else:
        ax.pie(stock_value.values, labels=stock_value.index, autopct="%1.1f%%", colors=[color_themes[theme]["primary"]]*len(stock_value))
        ax.set_title("Stock Value Distribution")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown(f"**Insight:** {stock_value.idxmax()} is holding the most value in inventory.")

# CHART 6 UI
with st.expander("📌 Chart 6: Stock Value by Manufacturer"):
    chart_type_6 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_6"
    )
    chart_6(chart_type_6)




# CHART 7: Average Discount % per Manufacturer
def chart_7(chart_type):
    theme = st.session_state.global_theme
    df_products["discount_pct"] = ((df_products["price"] - df_products["discount_price"]) / df_products["price"]) * 100
    avg_discount = df_products.groupby("manufacturer")["discount_pct"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(avg_discount.index, avg_discount.values, color=color_themes[theme]["primary"])
        else:
            ax.plot(avg_discount.values, avg_discount.index, marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Discount %")
        ax.set_title("Average Discount % per Manufacturer")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    else:
        ax.pie(avg_discount.values, labels=avg_discount.index, autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(avg_discount))
        ax.set_title("Average Discount Share")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown(f"**Insight:** {avg_discount.idxmax()} gives the steepest average discounts.")

# CHART 7 UI
with st.expander("📌 Chart 7: Average Discount % per Manufacturer"):
    chart_type_7 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_7"
    )
    chart_7(chart_type_7)


# CHART 8: Products with Stock Level < 10
def chart_8(chart_type):
    theme = st.session_state.global_theme
    low_stock = df_products[df_products["stock_level"] < 10]

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        stock_counts = low_stock["stock_level"].value_counts().sort_index()
        if chart_type == "Bar":
            ax.barh(stock_counts.index, stock_counts.values, color=color_themes[theme]["primary"])
        else:
            ax.plot(stock_counts.index, stock_counts.values, marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Stock Level")
        ax.set_ylabel("Number of Products")
        ax.set_title("Products with Stock Level < 10")
    else:
        pie_data = low_stock["stock_level"].value_counts().sort_index()
        ax.pie(pie_data.values, labels=pie_data.index, autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(pie_data))
        ax.set_title("Distribution of Low Stock Levels")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown(f"**Insight:** {len(low_stock)} products are at risk of stock-out (stock < 10).")

# CHART 8 UI
with st.expander("📌 Chart 8: Products with Stock Level < 10"):
    chart_type_8 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_8"
    )
    chart_8(chart_type_8)


# CHART 9: Best Bulk Deals (Per Unit Price)
def chart_9(chart_type):
    theme = st.session_state.global_theme
    best_bulk = df_products.sort_values("bulk_price_per_unit").head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(best_bulk["product_name"], best_bulk["bulk_price_per_unit"], color=color_themes[theme]["primary"])
        else:
            ax.plot(best_bulk["bulk_price_per_unit"], best_bulk["product_name"], marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Bulk Price Per Unit (£)")
        ax.set_title("Top 10 Best Bulk Deals (Per Unit)")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"£{x:.0f}"))
    else:
        ax.pie(best_bulk["bulk_price_per_unit"], labels=best_bulk["product_name"], autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(best_bulk))
        ax.set_title("Bulk Deal Distribution")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown("**Insight:** These products offer the best value when bought in bulk.")

# CHART 9 UI
with st.expander("📌 Chart 9: Best Bulk Deals (Per Unit Price)"):
    chart_type_9 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_9"
    )
    chart_9(chart_type_9)


# CHART 10: Overall Product Size Distribution
def chart_10(chart_type):
    theme = st.session_state.global_theme
    size_counts = df_products["size"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(size_counts.index, size_counts.values, color=color_themes[theme]["primary"])
        else:
            ax.plot(size_counts.index, size_counts.values, marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Size")
        ax.set_ylabel("Number of Products")
        ax.set_title("Overall Product Size Distribution")
    else:
        ax.pie(size_counts.values, labels=size_counts.index, autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(size_counts))
        ax.set_title("Product Size Share")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown(f"**Insight:** Most products are '{size_counts.idxmax()}' size.")

# CHART 10 UI
with st.expander("📌 Chart 10: Overall Product Size Distribution"):
    chart_type_10 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_10"
    )
    chart_10(chart_type_10)


# CHART 11: Average Product Weight by Manufacturer
def chart_11(chart_type):
    theme = st.session_state.global_theme
    avg_weight = df_products.groupby("manufacturer")["weight"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(avg_weight.index, avg_weight.values, color=color_themes[theme]["primary"])
        else:
            ax.plot(avg_weight.values, avg_weight.index, marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Average Weight (kg)")
        ax.set_title("Average Product Weight by Manufacturer")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.1f} kg"))
    else:
        ax.pie(avg_weight.values, labels=avg_weight.index, autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(avg_weight))
        ax.set_title("Average Weight Share")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown(f"**Insight:** {avg_weight.idxmax()} has the heaviest average products.")

# CHART 11 UI
with st.expander("📌 Chart 11: Average Product Weight by Manufacturer"):
    chart_type_11 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_11"
    )
    chart_11(chart_type_11)


# CHART 12: Overall Product Price Distribution
def chart_12(chart_type):
    theme = st.session_state.global_theme
    prices = df_products["price"]

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type == "Bar":
        ax.hist(prices, bins=30, color=color_themes[theme]["primary"], edgecolor="black")
        ax.set_title("Product Price Distribution (Histogram)")
    elif chart_type == "Line":
        ax.plot(sorted(prices), color=color_themes[theme]["primary"])
        ax.set_title("Product Price Distribution (Line)")
    elif chart_type == "Pie":
        price_ranges = pd.cut(prices, bins=[0, 50, 100, 150, 200, prices.max()], right=False)
        price_counts = price_ranges.value_counts().sort_index()
        ax.pie(price_counts.values, labels=[f"{i.left:.0f}–{i.right:.0f}" for i in price_counts.index],
               autopct="%1.1f%%", colors=[color_themes[theme]["primary"]]*len(price_counts))
        ax.set_title("Price Range Distribution (Pie)")
        ax.set_aspect("equal")

    if chart_type in ["Bar", "Line"]:
        ax.set_xlabel("Price (£)")
        ax.set_ylabel("Product Count")
    st.pyplot(fig)
    st.markdown("**Insight:** Most products are priced between £50–£150.")

# CHART 12 UI
with st.expander("📌 Chart 12: Overall Product Price Distribution"):
    chart_type_12 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_12"
    )
    chart_12(chart_type_12)

# CHART 13: Revenue Distribution (Pareto Principle)
def chart_13(chart_type):
    theme = st.session_state.global_theme
    df_products["revenue"] = df_products["price"] * df_products["units_sold_12m"]
    product_revenue = df_products[["product_name", "revenue"]].sort_values("revenue", ascending=False).reset_index(drop=True)
    product_revenue["cum_pct"] = product_revenue["revenue"].cumsum() / product_revenue["revenue"].sum() * 100
    top_20_cutoff = int(len(product_revenue) * 0.2)
    actual_pct = product_revenue.loc[top_20_cutoff - 1, "cum_pct"]

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type == "Line":
        ax.plot(product_revenue.index + 1, product_revenue["cum_pct"], color=color_themes[theme]["primary"])
        ax.axvline(x=top_20_cutoff, color="red", linestyle="--")
        ax.text(top_20_cutoff + 5, actual_pct - 10, f"Top 20% = {actual_pct:.1f}%", color="red")
        ax.set_ylabel("Cumulative % of Total Revenue")
        ax.set_xlabel("Product Rank (Sorted by Revenue)")
        ax.set_title("Pareto Principle - Testing the 80/20 Rule")
        ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    else:
        ax.text(0.5, 0.5, "Only available as a Line Chart", ha="center", va="center", fontsize=12)
        ax.set_title("Pareto Plot")
        ax.axis("off")

    st.pyplot(fig)
    st.markdown(f"**Insight:** Top 20% of products generate {actual_pct:.1f}% of revenue.")

# CHART 13 UI
with st.expander("📌 Chart 13: Revenue Distribution (Pareto Principle)"):
    chart_type_13 = st.selectbox(
        "📊 Choose chart type (only Line Chart supported):",
        ["Line", "Bar", "Pie"],
        index=0,
        key="chart_type_13"
    )
    chart_13(chart_type_13)


# CHART 14: Top 10 Products by % Discount
def chart_14(chart_type):
    theme = st.session_state.global_theme
    df_products["discount_amount_pct"] = ((df_products["price"] - df_products["discount_price"]) / df_products["price"]) * 100
    top_discount = df_products.sort_values("discount_amount_pct", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(top_discount["product_name"], top_discount["discount_amount_pct"], color=color_themes[theme]["primary"])
        else:
            ax.plot(top_discount["discount_amount_pct"], top_discount["product_name"], marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Discount %")
        ax.set_title("Top 10 Products by % Discount")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    else:
        ax.pie(top_discount["discount_amount_pct"], labels=top_discount["product_name"], autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(top_discount))
        ax.set_title("Share of Biggest Discounts")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown("**Insight:** These products are the most heavily discounted.")

# CHART 14 UI
with st.expander("📌 Chart 14: Top 10 Products by % Discount"):
    chart_type_14 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_14"
    )
    chart_14(chart_type_14)


# CHART 15: Cheapest Product by Size Group
def chart_15(chart_type):
    theme = st.session_state.global_theme
    cheapest_by_size = df_products.groupby("size")["price"].min().sort_values()

    fig, ax = plt.subplots(figsize=(8, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(cheapest_by_size.index, cheapest_by_size.values, color=color_themes[theme]["primary"])
        else:
            ax.plot(cheapest_by_size.index, cheapest_by_size.values, marker="o", color=color_themes[theme]["primary"])
        ax.set_ylabel("Price (£)")
        ax.set_xlabel("Size")
        ax.set_title("Cheapest Product by Size Group")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"£{x:.0f}"))
    else:
        ax.pie(cheapest_by_size.values, labels=cheapest_by_size.index, autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(cheapest_by_size))
        ax.set_title("Share of Lowest Prices by Size")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown("**Insight:** Small size group offers the lowest price product.")

# CHART 15 UI
with st.expander("📌 Chart 15: Cheapest Product by Size Group"):
    chart_type_15 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_15"
    )
    chart_15(chart_type_15)



# CHART 16: Manufacturer with Most Reviews (Proxy by Product Count)
def chart_16(chart_type):
    theme = st.session_state.global_theme
    review_counts = df_products.groupby("manufacturer").size().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(review_counts.index, review_counts.values, color=color_themes[theme]["primary"])
        else:
            ax.plot(review_counts.values, review_counts.index, marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Number of Products")
        ax.set_ylabel("Manufacturer")
        ax.set_title("Product Count per Manufacturer (Proxy for Review Volume)")
    else:
        ax.pie(review_counts.values, labels=review_counts.index, autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(review_counts))
        ax.set_title("Review Volume by Manufacturer")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown(f"**Insight:** {review_counts.idxmax()} has the most products — likely most reviews.")

# CHART 16 UI
with st.expander("📌 Chart 16: Manufacturer with Most Reviews (Proxy by Product Count)"):
    chart_type_16 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_16"
    )
    chart_16(chart_type_16)

# CHART 17: Price vs. Weight Scatter Plot
def chart_17(chart_type):
    theme = st.session_state.global_theme
    fig, ax = plt.subplots(figsize=(10, 6))

    if chart_type == "Scatter":
        ax.scatter(df_products["weight"], df_products["price"], c=df_products["manufacturer"].astype("category").cat.codes,
                   cmap="tab10", edgecolors="k", alpha=0.7)
        ax.axhspan(0, 150, xmin=0, xmax=0.4, facecolor="yellow", alpha=0.2)
        ax.axvspan(0, 2, ymin=0, ymax=0.6, facecolor="yellow", alpha=0.2)
        ax.set_title("Price vs. Weight (Shaded Area = Dense Cluster)", fontsize=14, fontweight="bold")
        ax.set_xlabel("Weight (kg)")
        ax.set_ylabel("Price (£)")
    else:
        ax.text(0.5, 0.5, "This chart only supports Scatter Plot", ha="center", va="center", fontsize=12)
        ax.set_title("Price vs. Weight")
        ax.axis("off")

    st.pyplot(fig)
    st.markdown("**Insight:** Most products cluster in the shaded area under 2kg and £150.")

# CHART 17 UI
with st.expander("📌 Chart 17: Price vs. Weight (Scatter Plot)"):
    chart_type_17 = st.selectbox(
        "📊 Choose chart type (only Scatter Plot supported):",
        ["Scatter", "Bar", "Line"],
        index=0,
        key="chart_type_17"
    )
    chart_17(chart_type_17)

# CHART 18: Top 10 High-Volume Products at the Lowest Prices
def chart_18(chart_type):
    theme = st.session_state.global_theme
    value_hits = df_products.sort_values(by=["units_sold_12m", "price"], ascending=[False, True]).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(value_hits["product_name"], value_hits["units_sold_12m"], color=color_themes[theme]["primary"])
        else:
            ax.plot(value_hits["units_sold_12m"], value_hits["product_name"], marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Units Sold")
        ax.set_title("Top 10 High-Volume Products at the Lowest Prices", fontsize=14, fontweight="bold")
    else:
        ax.pie(value_hits["units_sold_12m"], labels=value_hits["product_name"], autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(value_hits))
        ax.set_title("Best-Selling Cheap Products (Pie)")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown("**Insight:** These products sold the most while also being among the cheapest — high demand for low-cost items.")

# CHART 18 UI
with st.expander("📌 Chart 18: Top 10 High-Volume Products at the Lowest Prices"):
    chart_type_18 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_18"
    )
    chart_18(chart_type_18)

# CHART 19: Products Over £200 per Manufacturer
def chart_19(chart_type):
    theme = st.session_state.global_theme
    high_price_counts = df_products[df_products["price"] > 200].groupby("manufacturer").size().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type in ["Bar", "Line"]:
        if chart_type == "Bar":
            ax.barh(high_price_counts.index, high_price_counts.values, color=color_themes[theme]["primary"])
        else:
            ax.plot(high_price_counts.values, high_price_counts.index, marker="o", color=color_themes[theme]["primary"])
        ax.set_xlabel("Product Count")
        ax.set_ylabel("Manufacturer")
        ax.set_title("Products Over £200 per Manufacturer")
    else:
        ax.pie(high_price_counts.values, labels=high_price_counts.index, autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(high_price_counts))
        ax.set_title("Share of High-End Products")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown(f"**Insight:** {high_price_counts.idxmax()} offers the most high-end items.")

# CHART 19 UI
with st.expander("📌 Chart 19: Products Over £200 per Manufacturer"):
    chart_type_19 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_19"
    )
    chart_19(chart_type_19)

# CHART 20: Product Size Diversity per Manufacturer
def chart_20(chart_type):
    theme = st.session_state.global_theme
    size_dist = df_products.groupby(["manufacturer", "size"]).size().unstack().fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))
    if chart_type == "Bar":
        size_dist.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
        ax.set_title("Product Size Diversity per Manufacturer")
        ax.set_ylabel("Product Count")
        ax.legend(title="Size", bbox_to_anchor=(1.05, 1), loc="upper left")
    elif chart_type == "Line":
        size_dist.plot(kind="line", ax=ax, marker="o", colormap="viridis")
        ax.set_title("Size Trends Across Manufacturers")
        ax.set_ylabel("Product Count")
        ax.legend(title="Size", bbox_to_anchor=(1.05, 1), loc="upper left")
    else:
        total_sizes = size_dist.sum()
        ax.pie(total_sizes.values, labels=total_sizes.index, autopct="%1.1f%%",
               colors=[color_themes[theme]["primary"]]*len(total_sizes))
        ax.set_title("Overall Size Share (All Manufacturers)")
        ax.set_aspect("equal")

    st.pyplot(fig)
    st.markdown("**Insight:** This shows how varied each manufacturer’s product sizing is.")

# CHART 20 UI
with st.expander("📌 Chart 20: Product Size Diversity per Manufacturer"):
    chart_type_20 = st.selectbox(
        "📊 Choose chart type (default is recommended):",
        ["Bar", "Line", "Pie"],
        index=0,
        key="chart_type_20"
    )
    chart_20(chart_type_20)


import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import warnings

# Suppress seaborn/pandas warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Section title
st.markdown("## 🧠 Sentiment Analysis")

# Session state for chart toggle
if "show_sentiment_chart_1" not in st.session_state:
    st.session_state.show_sentiment_chart_1 = False

# Button to toggle chart display
if st.button("Show Chart 1: Top 10 Best-Rated Products by Sentiment"):
    st.session_state.show_sentiment_chart_1 = not st.session_state.show_sentiment_chart_1

# Display chart if active
if st.session_state.show_sentiment_chart_1:
    st.subheader("📊 Choose chart type (default is recommended):")
    chart_type = st.selectbox("Chart type:", ["Bar", "Line", "Pie"], index=0, key="sentiment_chart_1_type")

    # Prepare data
    top_happy = df_products.sort_values("avg_sentiment", ascending=False).head(10)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type == "Bar":
        ax.barh(top_happy["product_name"], top_happy["avg_sentiment"], color="#1ABC9C")
        ax.set_xlabel("Average Sentiment Score (-1 = very negative, +1 = very positive)")
        ax.set_ylabel("Product")
        ax.set_title("Top 10 Best-Rated Products (Avg Sentiment Score)", fontsize=14, fontweight="bold")
        ax.set_xlim(-1, 1)
    elif chart_type == "Line":
        ax.plot(top_happy["avg_sentiment"], top_happy["product_name"], marker="o", color="#1ABC9C")
    elif chart_type == "Pie":
        ax.pie(top_happy["avg_sentiment"], labels=top_happy["product_name"], autopct="%1.1f%%", colors=["#1ABC9C"] * len(top_happy))
        ax.set_aspect("equal")
        ax.set_title("Top 10 Best-Rated Products (Avg Sentiment Score)", fontsize=14, fontweight="bold")

    st.pyplot(fig)

    # Insight
    st.markdown(f"📊 **Insight:** {top_happy.iloc[0]['product_name']} has the highest average sentiment score: **{top_happy.iloc[0]['avg_sentiment']:.2f}**")


# Streamlit: Title for the page
st.title("Sentiment Analysis: Worst-Rated Products")

# Streamlit: Button to trigger chart display
if st.button("Show Top 10 Worst-Rated Products by Sentiment"):
    
    # Sort the products by average sentiment score in ascending order (worst-rated products first)
    top_unhappy = df_products.sort_values("avg_sentiment", ascending=True).head(10)

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    plt.barh(top_unhappy["product_name"], top_unhappy["avg_sentiment"], color="#E74C3C")
    plt.title("Top 10 Worst-Rated Products (Avg Sentiment Score)")
    plt.xlabel("Average Sentiment Score (-1 = very negative, +1 = very positive)")  # Adding label for sentiment score range
    plt.ylabel("Product")  # Label for products
    plt.xlim(-1, 1)  # Set x-axis to range from -1 to 1
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)

    # Display insight text below the plot
    insight = f"📊 Insight: {top_unhappy.iloc[0]['product_name']} has the lowest average sentiment score: {top_unhappy.iloc[0]['avg_sentiment']:.2f}"
    st.markdown(insight)


# Streamlit: Title for the page
st.title("Average Sentiment Score per Manufacturer")

# Streamlit: Button to trigger chart display
if st.button("Show Average Sentiment by Manufacturer"):
    
    # Calculate the average sentiment score per manufacturer
    avg_sentiment_manufacturer = df_products.groupby("manufacturer")["avg_sentiment"].mean().sort_values()

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    plt.barh(avg_sentiment_manufacturer.index, avg_sentiment_manufacturer.values, color="#3498DB")  # solid blue
    plt.title("Average Sentiment Score per Manufacturer", fontsize=14, fontweight="bold")
    plt.xlabel("Average Sentiment Score (-1 = very negative, +1 = very positive)")  # Adding label for sentiment score range
    plt.xlim(-1, 1)  # Set x-axis to range from -1 to 1
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)

    # Display insight text below the plot
    insight = f"📊 Insight: {avg_sentiment_manufacturer.idxmax()} has the most positively rated products on average, while {avg_sentiment_manufacturer.idxmin()} has the worst."
    st.markdown(insight)


# Streamlit: Title for the page
st.title("Best and Worst Sentiment Score per Manufacturer")

# Streamlit: Button to trigger chart display
if st.button("Show Best and Worst Sentiment per Manufacturer"):
    
    # Calculate best and worst sentiment per manufacturer
    summary = df_products.groupby("manufacturer").agg(
        best_sentiment=('avg_sentiment', 'max'),
        worst_sentiment=('avg_sentiment', 'min')
    ).reset_index()

    manufacturers = summary["manufacturer"]
    best = summary["best_sentiment"]
    worst = summary["worst_sentiment"]

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(manufacturers, best, marker='o', label="Best Sentiment", color="#1ABC9C")
    plt.plot(manufacturers, worst, marker='o', label="Worst Sentiment", color="#E74C3C")

    plt.title("Best and Worst Sentiment Score per Manufacturer", fontsize=14, fontweight="bold")
    plt.xlabel("Manufacturer", fontsize=12)
    plt.ylabel("Sentiment Score (-1 = very negative, +1 = very positive)", fontsize=12)
    plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
    plt.ylim(-1, 1)  # Set y-axis range from -1 to 1
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)

    # Display the insight text below the plot
    st.markdown("📊 Insight: This chart shows each manufacturer's best and worst product sentiment scores.")


# Streamlit: Title for the page
st.title("Sentiment Distribution of Products")

# Streamlit: Button to trigger chart display
if st.button("Show Sentiment Distribution by Product"):
    
    # Create sentiment bands
    df_products["sentiment_band"] = pd.cut(
        df_products["avg_sentiment"], 
        bins=[-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1],
        labels=["-1 to -0.8", "-0.8 to -0.6", "-0.6 to -0.4", "-0.4 to -0.2", "-0.2 to 0",
                "0 to 0.2", "0.2 to 0.4", "0.4 to 0.6", "0.6 to 0.8", "0.8 to 1"],
        include_lowest=True
    )

    # Count products in each sentiment band
    sentiment_distribution = df_products["sentiment_band"].value_counts().sort_index()

    # Plot the distribution
    plt.figure(figsize=(12, 6))
    plt.barh(avg_sentiment_manufacturer.index, avg_sentiment_manufacturer.values, color="#3498DB")  # solid blue
    plt.title("Distribution of Products by Sentiment Band", fontsize=14, fontweight="bold")
    plt.xlabel("Sentiment Score Range")
    plt.ylabel("Number of Products")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)

    # Optional cleanup
    df_products.drop(columns="sentiment_band", inplace=True)

    # Insight
    most_popular = sentiment_distribution.idxmax()
    st.markdown(f"📊 Insight: Most products fall into the sentiment range: {most_popular}.")

