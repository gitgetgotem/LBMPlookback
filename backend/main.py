from flask import Flask, request, jsonify
from Function_File import get_data_from_db, divide_last_column, replace_zone_names, merge_lbmp_and_curve, \
    get_dollar_value, create_lookbacks
from Static_values import connection, reverse_zone_dict
from flask_cors import CORS
import pandas as pd
import pymysql

app = Flask(__name__)
CORS(app)

# Global variables to hold selected values
zone = 'c'  # Default value
curve = 'Kirkland'  # Default value
utility = 'NYSEG'  # Default value


@app.route('/update', methods=['POST'])
def update_variables():
    global zone, curve, utility
    data = request.get_json()
    zone = data['zone']
    curve = data['curve']
    utility = data['utility']

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
    lbmp_query = f"SELECT Time_Stamp, Year, Month, Day, Hour, Name, LBMP FROM nyiso.lbmp WHERE Name='{query_zone}'"
    curve_query = f"SELECT Month, Day, Hour, {curve} FROM nyiso.curves"

    curve_df = divide_last_column(get_data_from_db(connection, curve_query))
    lbmp_df = replace_zone_names(divide_last_column(get_data_from_db(connection, lbmp_query)))
    df = merge_lbmp_and_curve(lbmp_df, curve_df)
    df = get_dollar_value(df, utility)
    df = create_lookbacks(df)

    df = df.round(6)

    return df


if __name__ == "__main__":
    app.run(port=5000, debug=True)  # Ensure this line specifies port 5000


