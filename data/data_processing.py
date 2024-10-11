import pandas as pd

# Load data from the CSV file
file_path = 'data/ai_patents.csv'  # Update with your actual file path
df = pd.read_csv(file_path)

# Display the column names
print("Column names in the DataFrame:\n", df.columns)

# Clean column names by stripping whitespace and converting to lowercase
df.columns = df.columns.str.strip().str.lower()

# Display cleaned column names
print("Cleaned column names:\n", df.columns)

# Check for missing values
print("Missing values before cleaning:\n", df.isnull().sum())

# Fill missing values in numerical columns
df['pages'] = df['pages'].fillna(df['pages'].mean())  # Fill with mean
df['relevency'] = df['relevency'].fillna(0)  # Assuming relevency can be 0

# Fill missing values in categorical columns
df['inventer'] = df['inventer'].fillna('Unknown')
df['applicant name'] = df['applicant name'].fillna('Unknown')

# Convert date columns to datetime format
df['date published'] = pd.to_datetime(df['date published'], errors='coerce')
df['filing date'] = pd.to_datetime(df['filing date'], errors='coerce')

# Check for missing values after cleaning
print("Missing values after cleaning:\n", df.isnull().sum())

# Summary statistics function
def summary_statistics(df):
    """Returns summary statistics for numerical columns."""
    stats = {
        'mean_pages': df['pages'].mean(),
        'median_pages': df['pages'].median(),
        'std_pages': df['pages'].std(),
        'mean_relevency': df['relevency'].mean(),
        'median_relevency': df['relevency'].median(),
        'std_relevency': df['relevency'].std(),
    }
    return stats

# Frequency counts function
def frequency_counts(df, column_name):
    """Returns frequency counts for a specified categorical column."""
    if column_name in df.columns:
        return df[column_name].value_counts().to_dict()
    else:
        raise ValueError(f"Column '{column_name}' does not exist in DataFrame.")


# Identify duplicates
def identify_duplicates(df):
    return df[df.duplicated()]

# Analyze correlations
def correlation_analysis(df):
    # Select only numeric columns for correlation analysis
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    correlation_matrix = numeric_df.corr()
    return correlation_matrix

# Group data for aggregation (e.g., count of patents per applicant)
def group_by_applicant(df):
    return df.groupby('applicant name').size().reset_index(name='patent_count')

# Identify outliers based on IQR (Interquartile Range)
def identify_outliers(df, column_name):
    if column_name in df.columns:
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[column_name] < (Q1 - 1.5 * IQR)) | (df[column_name] > (Q3 + 1.5 * IQR))]
        return outliers
    else:
        raise ValueError(f"Column '{column_name}' does not exist in DataFrame.")

# Data type conversions (e.g., converting 'pages' to integer if it's float)
def convert_data_types(df):
    df['pages'] = df['pages'].astype(int)
    df['relevency'] = df['relevency'].astype(float)
    return df

# Execute all functions and print results
# Summary statistics
stats = summary_statistics(df)
print("Summary Statistics:\n", stats)

# Frequency counts
inventer_counts = frequency_counts(df, 'inventer')
applicant_name_counts = frequency_counts(df, 'applicant name')
print("Inventer Counts:\n", inventer_counts)
print("Applicant Name Counts:\n", applicant_name_counts)

# Identify duplicates
duplicates = identify_duplicates(df)
print("Duplicates Found:\n", duplicates)

# Correlation analysis
correlation_matrix = correlation_analysis(df)
print("Correlation Matrix:\n", correlation_matrix)

# Group by applicant
grouped_by_applicant = group_by_applicant(df)
print("Grouped by Applicant:\n", grouped_by_applicant)

# Identify outliers in 'relevency'
outliers = identify_outliers(df, 'relevency')
print("Outliers in Relevency:\n", outliers)

# Convert data types
df = convert_data_types(df)
print("Data types after conversion:\n", df.dtypes)
