import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px  # Unused, but kept if needed
import os
import openpyxl  # For XLSX export
import threading
import webbrowser

# Load the Excel file with dtype=str for filter columns to avoid type issues
df = pd.read_excel('ROP_Final.xlsx', dtype={
    'vendorId': str,
    'productId': str,
    'Vendor Title': str,
    'Account Manager Name': str,
    'Product Title': str,
    'Product Category': str,
    'Brand': str,
    'Subcategory': str,
    'State': str
})

# Prepare unique values for dropdown filters (convert to str to handle mixed types)
unique_vendor_ids = ['All'] + sorted(str(x) for x in df['vendorId'].unique())
unique_product_ids = ['All'] + sorted(str(x) for x in df['productId'].unique())
unique_vendors = ['All'] + sorted(str(x) for x in df['Vendor Title'].unique())
unique_managers = ['All'] + sorted(str(x) for x in df['Account Manager Name'].unique())
unique_products = ['All'] + sorted(str(x) for x in df['Product Title'].unique())
unique_categories = ['All'] + sorted(str(x) for x in df['Product Category'].unique())
unique_brands = ['All'] + sorted(str(x) for x in df['Brand'].unique())
unique_subcategories = ['All'] + sorted(str(x) for x in df['Subcategory'].unique())
unique_states = ['All'] + sorted(str(x) for x in df['State'].unique())

# Initialize the Dash app
app = dash.Dash(__name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no",
        }
    ],)

app.title = "Inventory Dashboard"

app.config["suppress_callback_exceptions"] = True

app.layout = html.Div([
    html.H2("🛞Vendors' Re-Order Point and Replenishment Table🛢️", style={"textAlign": "center"}),

    # New: Beautifully organized dropdown filters in a grid (3 per row)
    html.Div([
        # Row 1
        html.Div([
            html.Label("🏪Filter by Vendor ID:", style={'fontWeight': 'bold', "fontSize": "12px", "fontFamily": "Monaco"}),
            dcc.Dropdown(
                id='vendor-id-filter',
                options=[{'label': v, 'value': v} for v in unique_vendor_ids],
                value=['All'],
                multi=True,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'margin': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.Label("🛠️Filter by Product ID:", style={'fontWeight': 'bold', "fontSize": "12px", "fontFamily": "Monaco"}),
            dcc.Dropdown(
                id='product-id-filter',
                options=[{'label': p, 'value': p} for p in unique_product_ids],
                value=['All'],
                multi=True,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'margin': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.Label("🏪Filter by Vendor Title:", style={'fontWeight': 'bold', "fontSize": "12px", "fontFamily": "Monaco"}),
            dcc.Dropdown(
                id='vendor-filter',
                options=[{'label': v, 'value': v} for v in unique_vendors],
                value=['All'],
                multi=True,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'margin': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        # Row 2
        html.Div([
            html.Label("🧑🏼‍💼Filter by Account Manager Name:", style={'fontWeight': 'bold', "fontSize": "12px", "fontFamily": "Monaco"}),
            dcc.Dropdown(
                id='manager-filter',
                options=[{'label': m, 'value': m} for m in unique_managers],
                value=['All'],
                multi=True,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'margin': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.Label("🛠️Filter by Product Title:", style={'fontWeight': 'bold', "fontSize": "12px", "fontFamily": "Monaco"}),
            dcc.Dropdown(
                id='product-filter',
                options=[{'label': p, 'value': p} for p in unique_products],
                value=['All'],
                multi=True,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'margin': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.Label("🗂️Filter by Product Category:", style={'fontWeight': 'bold', "fontSize": "12px", "fontFamily": "Monaco"}),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': c, 'value': c} for c in unique_categories],
                value=['All'],
                multi=True,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'margin': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        # Row 3
        html.Div([
            html.Label("🔤Filter by Brand:", style={'fontWeight': 'bold', "fontSize": "12px", "fontFamily": "Monaco"}),
            dcc.Dropdown(
                id='brand-filter',
                options=[{'label': b, 'value': b} for b in unique_brands],
                value=['All'],
                multi=True,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'margin': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.Label("🔧Filter by Subcategory:", style={'fontWeight': 'bold', "fontSize": "12px", "fontFamily": "Monaco"}),
            dcc.Dropdown(
                id='subcategory-filter',
                options=[{'label': s, 'value': s} for s in unique_subcategories],
                value=['All'],
                multi=True,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'margin': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.Label("⚠️Filter by State:", style={'fontWeight': 'bold', "fontSize": "12px", "fontFamily": "Monaco"}),
            dcc.Dropdown(
                id='state-filter',
                options=[{'label': s, 'value': s} for s in unique_states],
                value=['All'],
                multi=True,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'margin': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center', 'marginBottom': '20px'}),

    dash_table.DataTable(
        id="inventory-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),

        # Enable Excel export
        export_format="xlsx",
        export_headers="display",

        # Filtering & Sorting: Disable native filters (using custom dropdowns)
        filter_action="none",
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
            "textAlign": "center",
            "verticalAlign": "middle",
            "border": "1px solid #ddd",
            "padding": "6px",
            "fontFamily": "Monaco",
            "fontSize": "12px",
            "minWidth": "100px",
            "maxWidth": "100px",
            "whiteSpace": "normal",
            "height": "50px"
        },

        # Fixed column widths and custom fonts/sizes per column
        style_cell_conditional=[
            {"if": {"column_id": "vendorId"},"wordBreak": "break-word", "minWidth": "100px", "maxWidth": "100px", "whiteSpace": "nowrap", "fontFamily": "Courier New, monospace", "fontSize": "8px"},
            {"if": {"column_id": "productId"},"wordBreak": "break-word", "minWidth": "100px", "maxWidth": "100px", "whiteSpace": "nowrap", "fontFamily": "Courier New, monospace", "fontSize": "8px"},
            {"if": {"column_id": "Vendor Title"}, "minWidth": "200px", "maxWidth": "200px", "fontFamily": "Georgia, serif", "fontSize": "12px", "fontStyle": "normal"},
            {"if": {"column_id": "Account Manager Name"}, "minWidth": "180px", "maxWidth": "180px", "fontFamily": "Georgia, serif", "fontSize": "13px"},
            {"if": {"column_id": "Product Title"}, "minWidth": "200px", "maxWidth": "200px", "fontFamily": "Georgia, serif", "fontSize": "12px", "fontStyle": "normal"},
            {"if": {"column_id": "Product Category"}, "minWidth": "150px", "maxWidth": "150px", "fontFamily": "Arial", "fontSize": "12px"},
            {"if": {"column_id": "Brand"}, "minWidth": "90px", "maxWidth": "90px", "fontFamily": "Arial", "fontSize": "12px", "fontStyle": "normal"},
            {"if": {"column_id": "Subcategory"}, "minWidth": "100px", "maxWidth": "100px", "fontFamily": "Arial", "fontSize": "12px", "fontStyle": "normal"},
            {"if": {"column_id": "Inventory"}, "minWidth": "100px", "maxWidth": "100px", "fontFamily": "Courier New, monospace", "fontSize": "12px", "color": "blue"},
            {"if": {"column_id": "Re-Order_Point"}, "minWidth": "120px", "maxWidth": "120px", "fontFamily": "Courier New, monospace", "fontSize": "12px", "color": "blue"},
            {"if": {"column_id": "Quantity to Send"}, "minWidth": "120px", "maxWidth": "120px", "fontFamily": "Courier New, monospace", "fontSize": "12px", "fontWeight": "bold", "color": "blue"},
            {"if": {"column_id": "State"}, "minWidth": "120px", "maxWidth": "120px", "fontFamily": "Arial", "fontSize": "12px", "fontStyle": "bold"},
            {"if": {"column_id": "#Shipment_in_Progress"}, "minWidth": "150px", "maxWidth": "150px", "fontFamily": "Courier New, monospace", "fontSize": "12px", "fontStyle": "italic"},
            {"if": {"column_id": "City"}, "minWidth": "80px", "maxWidth": "80px", "fontSize": "12px"},
            {"if": {"column_id": "Warehouse Name"}, "minWidth": "150px", "maxWidth": "150px", "fontSize": "13px"},
            {"if": {"column_id": "Warehouse Availability"}, "minWidth": "120px", "maxWidth": "120px", "fontSize": "13px"}
        ],

        # Header style
        style_header={
            "backgroundColor": "#FFFFFF",
            "fontWeight": "bold",
            "color" : "black",
            "fontFamily": "Arial",
            "fontSize": "13px",
            "fontStyle": "normal",
            "border": "1px solid #ccc",
            "whiteSpace": "normal",
            "textAlign": "center",
            "verticalAlign": "middle"
        },

        # Row striping + Conditional formatting
        style_data_conditional=[
            
            {
                "if": {
                    "filter_query": '{State} contains "Supply Needed"'
                },
                "backgroundColor": "#FFF2F0",
                "color": "DarkRed",
                "fontWeight": "bold",
                "fontFamily": "Arial"
            }
        ]
    )
],
    style={
        "backgroundColor": "#f8f9fa",  # Light gray example - change this to your desired color
        "height": "100vh",  # Full viewport height
        "width": "100vw",   # Full viewport width
        "margin": "0",      # No outer margins
        "padding": "20px",  # Optional: Inner padding for content spacing
        "boxSizing": "border-box"  # Ensures padding doesn't add to width/height
    }                     
)

# Callback to filter the table based on all dropdown selections
@app.callback(
    Output('inventory-table', 'data'),
    [Input('vendor-id-filter', 'value'),
     Input('product-id-filter', 'value'),
     Input('vendor-filter', 'value'),
     Input('manager-filter', 'value'),
     Input('product-filter', 'value'),
     Input('category-filter', 'value'),
     Input('brand-filter', 'value'),
     Input('subcategory-filter', 'value'),
     Input('state-filter', 'value')]
)
def update_table(vendor_ids, product_ids, vendors, managers, products, categories, brands, subcategories, states):
    dff = df.copy()

    if vendor_ids and 'All' not in vendor_ids:
        dff = dff[dff['vendorId'].isin(vendor_ids)]
    if product_ids and 'All' not in product_ids:
        dff = dff[dff['productId'].isin(product_ids)]
    if vendors and 'All' not in vendors:
        dff = dff[dff['Vendor Title'].isin(vendors)]
    if managers and 'All' not in managers:
        dff = dff[dff['Account Manager Name'].isin(managers)]
    if products and 'All' not in products:
        dff = dff[dff['Product Title'].isin(products)]
    if categories and 'All' not in categories:
        dff = dff[dff['Product Category'].isin(categories)]
    if brands and 'All' not in brands:
        dff = dff[dff['Brand'].isin(brands)]
    if subcategories and 'All' not in subcategories:
        dff = dff[dff['Subcategory'].isin(subcategories)]
    if states and 'All' not in states:
        dff = dff[dff['State'].isin(states)]

    return dff.to_dict('records')

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)

# Expose the server for production (e.g., Gunicorn on Render)
server = app.server

if __name__ == "__main__":
    # For local development only
    app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)), debug=True)
