from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Skin Clinic Campaign Analysis API", version="1.0")

# Load and process data on startup
df = pd.read_csv('skin clinic campaign.csv')
df['Response_Binary'] = df['Response_to_Campaign'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)

@app.get("/")
def home():
    return {"message": "Welcome to the Skin Clinic Campaign API. Visit /campaign-analysis for results."}

@app.get("/campaign-analysis")
def get_campaign_analysis():
    # 1. Gender
    gender_df = df.groupby('Gender')['Response_Binary'].agg(['count', 'sum', 'mean']).reset_index()
    gender_df.columns = ['Gender', 'Total_Customers', 'Responded_Customers', 'Response_Rate']
    gender_df['Response_Rate'] = (gender_df['Response_Rate'] * 100).round(2)

    # 2. Age Group
    age_df = df.groupby('AgeGroup')['Response_Binary'].agg(['count', 'sum', 'mean']).reset_index()
    age_df.columns = ['Age_Group', 'Total_Customers', 'Responded_Customers', 'Response_Rate']
    age_df['Response_Rate'] = (age_df['Response_Rate'] * 100).round(2)

    # 3. Purchase Last Quarter
    purchase_df = df.groupby('Purchase_Last_Quarter')['Response_Binary'].agg(['count', 'sum', 'mean']).reset_index()
    purchase_df.columns = ['Purchase_Last_Quarter', 'Total_Customers', 'Responded_Customers', 'Response_Rate']
    purchase_df['Response_Rate'] = (purchase_rate := purchase_df['Response_Rate'] * 100).round(2)
    purchase_df['Response_Rate'] = purchase_rate

    # 4. Product Usage
    def categorize_products(val):
        if val <= 4: return '1-4'
        elif val <= 8: return '5-8'
        else: return '>8'

    df['Product_Category'] = df['Unique_Products_Purchased'].apply(categorize_products)
    product_df = df.groupby('Product_Category')['Response_Binary'].agg(['count', 'sum', 'mean']).reset_index()
    product_df.columns = ['Product_Category', 'Total_Customers', 'Responded_Customers', 'Response_Rate']
    product_df['Response_Rate'] = (product_df['Response_Rate'] * 100).round(2)
    product_df = product_df.sort_values('Product_Category').reset_index(drop=True)

    return {
        "gender_analysis": gender_df.to_dict(orient="records"),
        "age_analysis": age_df.to_dict(orient="records"),
        "purchase_analysis": purchase_df.to_dict(orient="records"),
        "product_analysis": product_df.to_dict(orient="records")
    }