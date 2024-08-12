import pandas as pd
from Static_values import zone_dict, utility_line_loss
import pymysql



def replace_zone_names(df):
    df['Name'] = df['Name'].map(zone_dict)

    return df


def divide_last_column(df):
    df.iloc[:, -1] = df.iloc[:, -1] / 1000
    return df


def get_data_from_db(connection, query):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(result)

def merge_lbmp_and_curve(df1, df2):
    df = pd.merge(df1, df2, on=['Month', 'Day', 'Hour'], how='left')
    return df


def get_dollar_value(df, utility):
    df['Value'] = df['LBMP'].astype(float) * utility_line_loss[utility] * df.iloc[:, -1].astype(float)
    return df


def basic_grouping(df):
    # Group by Year and Month and calculate mean LBMP
    second_to_last_col = df.columns[-2]

    # Group by Year and Month and calculate sum
    df = df.groupby([df['Time_Stamp'].dt.to_period('M')]).agg(
        Value_Sum=('Value', 'sum'),
        Production_Sum=(second_to_last_col, 'sum')
    ).reset_index()

    # Sort by Time_Stamp
    df = df.sort_values('Time_Stamp').reset_index(drop=True)
    df['LBMP'] = df.iloc[:,-2]/df.iloc[:,-1]
    return df

def create_lookbacks(df):
    # Group by Year and Month and calculate mean LBMP
    grouped_df = basic_grouping(df)

    # Calculate the 12-month lookback
    grouped_df['12 month lookback'] = (
        grouped_df['LBMP'].rolling(window=12).apply(lambda x: (x * grouped_df['Production_Sum'].iloc[x.index]).sum()) /
        grouped_df['Production_Sum'].rolling(window=12).sum()
    )

    # Calculate the 24-month lookback
    grouped_df['24 month lookback'] = (
        grouped_df['LBMP'].rolling(window=24).apply(lambda x: (x * grouped_df['Production_Sum'].iloc[x.index]).sum()) /
        grouped_df['Production_Sum'].rolling(window=24).sum()
    )

    # Sort by Time_Stamp
    grouped_df = grouped_df.sort_values('Time_Stamp', ascending=False).reset_index(drop=True)

    # Filter out rows where there are not enough months left for the lookback periods
    lookback_df = grouped_df[['Time_Stamp', '12 month lookback', '24 month lookback']].dropna().reset_index(drop=True)
    return lookback_df





