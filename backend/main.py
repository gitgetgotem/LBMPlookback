from flask import Flask, request, jsonify
from Function_File import get_data_from_db, divide_last_column, replace_zone_names, merge_lbmp_and_curve, \
    create_lookbacks, merge_df_and_drv, merge_monthly_dataframes, get_drv_dollar_value, basic_grouping, add_ENV_value, calculate_full_value_stack, calculate_discounted_value_stack
from Static_values import connection, reverse_zone_dict, icap_line_loss, utility_line_loss
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Global variables to hold selected values
zone = 'c'  # Default value
curve = 'Kirkland'  # Default value
utility = 'NYSEG'  # Default value


def apply_icap_line_loss(df):
    # Ensure the column is converted to float, handling NaNs properly
    df.iloc[:, -1] = df.iloc[:, -1].astype(float)

    # Fill NaN values with 0 (or another appropriate value) if necessary
    df.iloc[:, -1] = df.iloc[:, -1].fillna(0)

    # Perform the calculation
    df.iloc[:, -1] = df.iloc[:, -1] * icap_line_loss[utility]

    return df


def get_dollar_value(df):
    df['lbmp_Value'] = df['LBMP'].astype(float) * utility_line_loss[utility] * df['Production'].astype(float)
    return df


@app.route('/update', methods=['POST'])
def update_variables():
    global zone, curve, utility
    data = request.get_json()
    zone = data.get('zone', zone)
    curve = data.get('curve', curve)
    utility = data.get('utility', utility)

    result = run_program()  # Call your main function to process data

    # Convert any non-serializable types to strings before returning
    if isinstance(result, pd.DataFrame):
        for col in result.columns:
            if pd.api.types.is_period_dtype(result[col]):
                result[col] = result[col].astype(str)
            elif pd.api.types.is_datetime64_any_dtype(result[col]):
                result[col] = result[col].astype(str)
            # Add more conditions as needed for other types

    return jsonify(result.to_dict(orient='records'))

def run_program():
    query_zone = reverse_zone_dict[zone]

    selected_curve = curve

    lbmp_query = f"SELECT Time_Stamp, Year, Month, Day, Hour, Name, LBMP FROM nyiso.lbmp WHERE Name='{query_zone}'"

    curve_query = f"SELECT Month, Day, Hour, {selected_curve} AS Production FROM nyiso.curves;"

    icap_query = f"SELECT Year, Month, {utility}_ICAP AS ICAP FROM nyiso.icap;"

    drv_query = f"SELECT Month, Day, Hour, {utility} AS DRV FROM nyiso.drv;"

    curve_df = divide_last_column(get_data_from_db(connection, curve_query))
    lbmp_df = replace_zone_names(divide_last_column(get_data_from_db(connection, lbmp_query)))
    icap_df = apply_icap_line_loss(get_data_from_db(connection, icap_query))
    drv_df = get_data_from_db(connection, drv_query)

    df = merge_lbmp_and_curve(lbmp_df, curve_df)
    df = get_dollar_value(df)
    df = basic_grouping(get_drv_dollar_value(merge_df_and_drv(df, drv_df)))
    df = merge_monthly_dataframes(df, icap_df)
    df = calculate_discounted_value_stack(calculate_full_value_stack(add_ENV_value(df)))
    df = create_lookbacks(df)

    df = df.round(6)

    print(df)
    return df

if __name__ == "__main__":
    app.run(port=5000, debug=True)  # Ensure this line specifies port 5000

