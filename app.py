import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import os

# Load the CSV from a relative path (ensure 'ROP_Final.csv' is in the same directory)
df = pd.read_csv('ROP_Final.csv')

app = dash.Dash(__name__)
app.title = "Inventory Dashboard"

app.layout = html.Div([
    html.H2("📋 Vendors' ROP and Replenishment Table", style={"textAlign": "center"}),

    dash_table.DataTable(
        id="inventory-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),

        # Enable Excel export
        export_format="xlsx",  # Adds an "Export" button for XLSX download
        export_headers="display",  # Uses display names in the exported file

        # Filtering & Sorting
        filter_action="native",
        sort_action="native",
        sort_mode="multi",

        # Pagination
        page_action="native",
        page_size=50,

        # Scroll with fixed header
        fixed_rows={"headers": True},
        style_table={"overflowX": "auto", "maxHeight": "2000px", "overflowY": "scroll"},

        # Default column style
        style_cell={
            "textAlign": "center",       # horizontal center
            "verticalAlign": "middle",   # vertical center
            "border": "1px solid #ddd",
            "padding": "6px",
            "fontFamily": "Arial",
            "fontSize": "14px",
            "minWidth": "100px",  # default min width for all
            "maxWidth": "100px",
            "whiteSpace": "normal",  # allow wrapping
            "height": "50px"
        },

        # Fixed column widths per column
        style_cell_conditional=[
            {"if": {"column_id": "vendor_product_id"}, "minWidth": "100px", "maxWidth": "100px", "whiteSpace": "nowrap"},
            {"if": {"column_id": "Vendor Title"}, "minWidth": "200px", "maxWidth": "200px"},
            {"if": {"column_id": "Product Title"}, "minWidth": "200px", "maxWidth": "200px"},
            {"if": {"column_id": "Product Category"}, "minWidth": "100px", "maxWidth": "100px"},
            {"if": {"column_id": "Re_Order_Point"}, "minWidth": "120px", "maxWidth": "120px"},
            {"if": {"column_id": "total_quantity_to_send"}, "minWidth": "120px", "maxWidth": "120px"},
            {"if": {"column_id": "total_inventory"}, "minWidth": "120px", "maxWidth": "120px"},
            {"if": {"column_id": "State"}, "minWidth": "120px", "maxWidth": "120px"}
        ],

        # Header style
        style_header={
            "backgroundColor": "#f4f4f4",
            "fontWeight": "bold",
            "border": "1px solid #ccc",
            "whiteSpace": "normal",
            "textAlign": "center",
            "verticalAlign": "middle"
        },

        # Row striping + Conditional formatting
        style_data_conditional=[
            # Stripe odd rows
            {"if": {"row_index": "odd"}, "backgroundColor": "#f9f9f9"},

            # Conditional: Rows where State contains "Send"
            {
                "if": {
                    "filter_query": '{State} contains "Send"'
                },
                "backgroundColor": "#FEEBE7",  # light red background
                "color": "black",  # text color
                "fontWeight": "bold"
            }
        ]
    )
])

# Expose the server for production (e.g., Gunicorn on Render)
server = app.server

if __name__ == "__main__":
    # For local development only
    app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)), debug=True)
