import pandas as pd, datetime as dt, numpy as np
from sklearn.preprocessing import StandardScaler
pd.set_option('display.max_columns', None)  # Display all columns
try:
    G3 = pd.read_csv("OnlineRetail.csv", encoding='ISO-8859-1')
    print("Data loaded successfully:")
    Before=len(G3)
    print("Number of rows before cleaning:", Before)
    print("\nFirst 5 rows (head):")
    print(G3.head())
    print("\nLast 5 rows (tail):")
    print(G3.tail())
    print("\nRandom sample:")
    print(G3.sample(5))
    print("\n A summary of the dataset:")
    print(G3.info())
    G3['InvoiceDate'] = pd.to_datetime(G3['InvoiceDate']) #STEP1: Date type conversion
    print("\n Statistical summary of numerical columns:")
    print(G3.describe().round(2))
    print("\n Statistical mode\n")
    mode1=G3.mode()
    print(mode1)
    #STEP 2: Data Cleaning
    print("\n\n Checking for unique values:\n",G3.nunique(),"\nChecking for duplicated rows: ", G3.duplicated().sum(),"\n")
    #Handling missing values
    print(G3.dropna())
    print("\n................................................................................")
    print("................................................................................")
    print("\n Missing values before handling:",G3.isnull().sum())
    #only these two have missing values
    G3["Description"]=G3["Description"].fillna("Missing Info")
    G3=G3.dropna(subset=["CustomerID"])
    print("\n Missing values after handling:",G3.isnull().sum())
    print("\nNew statistical summary:")
    print(G3.describe().round(2))
    print("................................................................................")
    print("................................................................................")
    #STEP 3: Addressing inconsistencies and errors
    #Removal of cancellatons (Negative Quantities)
    G3=G3[G3['Quantity']>0]
    #Removal of price adjustments(Negative Unit Prices)
    G3=G3[G3['UnitPrice']>=0]
    #New statistical summary range
    print("\n Statistical summary after STEP 3:")
    print(G3.describe().round(2))
    #STEP 4 Handling outliers
    print("\n................................................................................\n")
    # We use the 99th percentile or a logical cutoff
    G3 = G3[G3['Quantity'] < 10000] 
    G3 = G3[G3['UnitPrice'] < 1000]
    G3 = G3[G3['UnitPrice'] > 0.001]
    # Check describe one last time
    print("\n Statistical summary after STEP 4:")
    print(G3.describe().round(2))
    #mean ($12.60$) and median ($6.00$) are much closer, meaning the distribution is less skewed.
    #Recheck
    print("\n................................................................................\n")
    duplicate_count = G3.duplicated().sum()
    print(f"Number of duplicate rows found: {duplicate_count}")
    After=len(G3)
    print("Number of rows after cleaning:", After, "\nRows removed during cleaning:", Before-After,"\nRows before cleaning:", Before)
    print("\n Missing values after handling:\n",G3.isnull().sum())
    #LAST STEP: Save cleaned data
    print("\n Saving cleaned data to 'OnlineRetailCleaned.csv'...")
    G3.to_csv('OnlineRetailCleaned.csv', index=False)
    #Shape of the data
    print("\n................................................................................\n")
    print("Final Data Shape:", G3.shape)
    print("Unique Customers:", G3['CustomerID'].nunique())
    #Creating a new column 'TotalPrice'
    G3['TotalPrice'] = G3['Quantity'] * G3['UnitPrice']
    print("\nFirst 5 rows with 'TotalPrice' column added:")
    print(G3.head())
    #RFM construction
    latest_date = G3['InvoiceDate'].max() + pd.Timedelta(days=1)
    print(f'Analysis Refference Date: {latest_date}')
    #Grouping and aggregating
    G3['TotalSum'] = G3['Quantity'] * G3['UnitPrice']
    rfm = G3.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (latest_date - x.max()).days,#Recency
        'InvoiceNo': 'count',#Frequency
        'TotalPrice': 'sum'#Monetary
    })
    rfm.rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency',
        'TotalSum': 'Monetary'
    }, inplace=True)
    print("\n RFM Table (first 5 rows):")
    print(rfm.head())
    #Handling Skewness with log transformation
    rfm_log=np.log(rfm+1) #Adding 1 to avoid log(0)
    print("\n....................................................\n")
    print("Data transformed to Log scale.")
    #Scaling the Data
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_log)
    # Convert back to a DataFrame for easy viewing
    rfm_scaled_df = pd.DataFrame(rfm_scaled, index=rfm.index, columns=rfm.columns)
    print(rfm_scaled_df.describe().round(2))
    print("\n.....................................................\n")

except FileNotFoundError:
    print("Error: 'OnlineRetail.csv' not found. Make sure the file is in the same directory as the script.")
except Exception as e:
    print(f"An error occurred: {e}")
