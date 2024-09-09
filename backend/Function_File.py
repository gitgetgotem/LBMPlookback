import pandas as pd
from Static_values import zone_dict, utility_line_loss, icap_line_loss
import pymysql



def replace_zone_names(df):
    df['Name'] = df['Name'].map(zone_dict)

    return df


def divide_last_column(df):
    df.iloc[:, -1] = df.iloc[:, -1] / 1000
    return df


# def apply_icap_line_loss(df):
#     # Ensure the column is converted to float, handling NaNs properly
#     df.iloc[:, -1] = df.iloc[:, -1].astype(float)
#
#     # Fill NaN values with 0 (or another appropriate value) if necessary
#     df.iloc[:, -1] = df.iloc[:, -1].fillna(0)
#
#     # Perform the calculation
#     df.iloc[:, -1] = df.iloc[:, -1] * icap_line_loss[utility]
#
#     return df



def get_data_from_db(connection, query):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(result)

def merge_lbmp_and_curve(df1, df2):
    df = pd.merge(df1, df2, on=['Month', 'Day', 'Hour'], how='left')
    return df


def merge_df_and_drv(df1, df2):
    df = pd.merge(df1, df2, on=['Month', 'Day', 'Hour'], how='left')
    return df


def calculate_discounted_value_stack(df):
    df['Discount_Value_Stack'] = df['Value_Stack'] * 0.95
    return df


def merge_monthly_dataframes(df1, df2):
    # Step 1: Create a temporary column in df1 by extracting Year and Month from 'timestamp'
    df1_temp = df1.copy()  # Make a copy of df1 to avoid modifying the original
    df1_temp['Year'] = df1_temp['Time_Stamp'].dt.year
    df1_temp['Month'] = df1_temp['Time_Stamp'].dt.month

    # Step 2: Merge df1 and df2 on 'Year' and 'Month'
    merged_df = df1_temp.merge(df2, on=['Year', 'Month'], how='left')

    # Step 3: Drop the temporary 'Year' and 'Month' columns from df1_temp
    merged_df = merged_df.drop(columns=['Year', 'Month'])

    return merged_df



# def get_dollar_value(df):
#     df['lbmp_Value'] = df['LBMP'].astype(float) * utility_line_loss[utility] * df['Production'].astype(float)
#     return df


def get_drv_dollar_value(df):
    df['drv_Value'] = df['DRV'].astype(float) * df['Production'].astype(float)
    return df


def add_ENV_value(df):
    df['ENV'] = 0.03103
    return df


def calculate_full_value_stack(df):
    df['ICAP'] = df['ICAP'].fillna(0)
    df["Value_Stack"] = df['LBMP'] + df['DRV'] + df['ICAP'] + df['ENV']
    return df



def basic_grouping(df):
    # Group by Year and Month and calculate mean LBMP

    # Group by Year and Month and calculate sum
    df = df.groupby([df['Time_Stamp'].dt.to_period('M')]).agg(
        Value_Sum=('lbmp_Value', 'sum'),
        Production_Sum=('Production', 'sum'),
        drv_Sum=('drv_Value', 'sum')
    ).reset_index()

    # Sort by Time_Stamp
    df = df.sort_values('Time_Stamp').reset_index(drop=True)
    df['LBMP'] = df['Value_Sum']/df['Production_Sum']
    df['DRV'] = df['drv_Sum']/df['Production_Sum']
    return df


def create_lookbacks(df):
    # Ensure Time_Stamp is treated as a period if it's not already
    if not pd.api.types.is_period_dtype(df['Time_Stamp']):
        df['Time_Stamp'] = pd.to_datetime(df['Time_Stamp'], format='%Y-%m').dt.to_period('M')

    # Calculate the 12-month lookback
    df['12 month lookback'] = (
            df['Discount_Value_Stack'].rolling(window=12).apply(
                lambda x: (x * df['Production_Sum'].iloc[x.index]).sum()
            ) / df['Production_Sum'].rolling(window=12).sum()
    )

    # Calculate the 24-month lookback
    df['24 month lookback'] = (
            df['Discount_Value_Stack'].rolling(window=24).apply(
                lambda x: (x * df['Production_Sum'].iloc[x.index]).sum()
            ) / df['Production_Sum'].rolling(window=24).sum()
    )

    # Sort by Time_Stamp and reset index
    df = df.sort_values('Time_Stamp', ascending=False).reset_index(drop=True)

    # Filter out rows where lookbacks cannot be calculated
    lookback_df = df[
        ['Time_Stamp', 'LBMP', 'DRV', 'ICAP', 'ENV', 'Value_Stack', 'Discount_Value_Stack', '12 month lookback',
         '24 month lookback']].dropna().reset_index(drop=True)

    return lookback_df