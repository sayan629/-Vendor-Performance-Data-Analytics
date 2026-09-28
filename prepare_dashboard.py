import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

print("Reading sales.csv...")

sales = pd.read_csv(
    DATA_DIR / "sales.csv",
    usecols=[
        "Brand",
        "SalesQuantity",
        "SalesDollars",
        "VendorNo",
        "VendorName"
    ]
)

print("Reading purchases.csv...")

purchases = pd.read_csv(
    DATA_DIR / "purchases.csv",
    usecols=[
        "Brand",
        "VendorNumber",
        "VendorName",
        "Quantity",
        "Dollars"
    ]
)

print("Aggregating sales by vendor...")

vendor_sales = (
    sales.groupby(
        ["VendorNo", "VendorName"],
        as_index=False
    )
    .agg(
        TotalSales=("SalesDollars", "sum"),
        SalesQuantity=("SalesQuantity", "sum")
    )
)

print("Aggregating purchases by vendor...")

vendor_purchase = (
    purchases.groupby(
        ["VendorNumber", "VendorName"],
        as_index=False
    )
    .agg(
        TotalPurchase=("Dollars", "sum"),
        PurchaseQuantity=("Quantity", "sum")
    )
)

# Rename VendorNumber so both datasets can be merged
vendor_purchase = vendor_purchase.rename(
    columns={"VendorNumber": "VendorNo"}
)

print("Merging vendor data...")

vendor_summary = pd.merge(
    vendor_sales,
    vendor_purchase,
    on=["VendorNo", "VendorName"],
    how="outer"
)

vendor_summary["TotalSales"] = (
    vendor_summary["TotalSales"]
    .fillna(0)
)

vendor_summary["TotalPurchase"] = (
    vendor_summary["TotalPurchase"]
    .fillna(0)
)

vendor_summary["SalesQuantity"] = (
    vendor_summary["SalesQuantity"]
    .fillna(0)
)

vendor_summary["PurchaseQuantity"] = (
    vendor_summary["PurchaseQuantity"]
    .fillna(0)
)

vendor_summary["GrossProfit"] = (
    vendor_summary["TotalSales"]
    - vendor_summary["TotalPurchase"]
)

vendor_summary["ProfitMargin"] = (
    vendor_summary["GrossProfit"]
    / vendor_summary["TotalSales"]
    * 100
)

vendor_summary["ProfitMargin"] = (
    vendor_summary["ProfitMargin"]
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0)
)

# ------------------------------------------------------------
# Brand summary
# ------------------------------------------------------------

print("Aggregating brands...")

brand_sales = (
    sales.groupby("Brand", as_index=False)
    .agg(
        TotalSales=("SalesDollars", "sum"),
        SalesQuantity=("SalesQuantity", "sum")
    )
)

brand_purchase = (
    purchases.groupby("Brand", as_index=False)
    .agg(
        TotalPurchase=("Dollars", "sum"),
        PurchaseQuantity=("Quantity", "sum")
    )
)

brand_summary = pd.merge(
    brand_sales,
    brand_purchase,
    on="Brand",
    how="outer"
)

brand_summary["TotalSales"] = (
    brand_summary["TotalSales"]
    .fillna(0)
)

brand_summary["TotalPurchase"] = (
    brand_summary["TotalPurchase"]
    .fillna(0)
)

brand_summary["GrossProfit"] = (
    brand_summary["TotalSales"]
    - brand_summary["TotalPurchase"]
)

brand_summary["ProfitMargin"] = (
    brand_summary["GrossProfit"]
    / brand_summary["TotalSales"]
    * 100
)

brand_summary["ProfitMargin"] = (
    brand_summary["ProfitMargin"]
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0)
)

# ------------------------------------------------------------
# Save compact files
# ------------------------------------------------------------

print("Saving dashboard files...")

vendor_summary.to_csv(
    DATA_DIR / "dashboard_vendor_summary.csv",
    index=False
)

brand_summary.to_csv(
    DATA_DIR / "dashboard_brand_summary.csv",
    index=False
)

print("\nDone!")
print(
    "Vendor summary:",
    len(vendor_summary),
    "rows"
)

print(
    "Brand summary:",
    len(brand_summary),
    "rows"
)