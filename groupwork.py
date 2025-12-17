import pandas as pd
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
except FileNotFoundError:
    print("Error: 'OnlineRetail.csv' not found. Make sure the file is in the same directory as the script.")
except Exception as e:
    print(f"An error occurred: {e}")
