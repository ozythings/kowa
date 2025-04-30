import dash
from dash import html, dcc, Output, Input, State
import os

dash.register_page(__name__, "/upload")

if not os.path.exists("temp_uploads"):
    os.makedirs("temp_uploads")

layout = html.Div(
    className="flex flex-col lg:flex-row p-5 space-y-4 lg:space-x-4",
    children=[
        # left section: upload and type selection
        html.Div(
            className="lg:w-1/3 p-5 border-r border-gray-300 space-y-4",
            children=[
                html.H3("Upload Image", className="text-xl font-bold"),
                dcc.Upload(
                    id="upload-image",
                    children=html.Div([
                        'Drag and Drop or ',
                        html.Button("Select a File", className="px-2 py-1 bg-blue-500 text-white rounded")
                    ]),
                    className="border-2 border-dashed border-gray-300 rounded p-4 text-center",
                    style={
                        'height': '100px',
                        'lineHeight': '60px',
                    },
                    multiple=False,
                ),
                html.Div(id="upload-status", className="mt-2 text-sm"),
                html.Div(id="preview-container", className="mt-4"),
                html.H3("Select Type", className="text-xl font-bold mt-4"),
                dcc.Dropdown(
                    id="image-type",
                    options=[
                        {"label": "BIM", "value": "BIM"},
                        {"label": "A101", "value": "A101"},
                        {"label": "EKENT", "value": "EKENT"},
                    ],
                    value="BIM",  # Default value
                    className="w-full p-2 border rounded",
                ),
                html.Button(
                    "Process",
                    id="process-button",
                    className="w-full px-4 py-2 bg-green-500 text-white rounded mt-4",
                ),
            ]
        ),
        
        # right section: display processed data
        html.Div(
            className="lg:w-2/3 p-5",
            children=[
                html.H3("Processed Data", className="text-xl font-bold mb-4"),
                html.Div(
                    id="processed-data",
                    className="space-y-4",
                    children=[
                        html.Div(
                            className="flex justify-between",
                            children=[html.Label("Amount:"), html.Div(id="ocr-amount")]
                        ),
                        html.Div(
                            className="flex justify-between",
                            children=[html.Label("Date:"), html.Div(id="ocr-date")]
                        ),
                        html.Div(
                            className="flex justify-between",
                            children=[html.Label("Category:"), html.Div(id="ocr-category")]
                        ),
                        html.Div(
                            className="flex justify-between",
                            children=[html.Label("Description:"), html.Div(id="ocr-description")]
                        ),
                    ]
                ),
                # display the raw OCR text for debugging
                html.Div(
                    id="raw-ocr-container",
                    className="mt-8",
                    children=[
                        html.H4("Raw OCR Text", className="text-lg font-bold"),
                        html.Pre(id="raw-ocr-text", className="p-4 bg-gray-100 rounded overflow-auto max-h-96")
                    ]
                )
            ]
        ),
        # TODO: refactor
        # i might use dcc.Store here
        # hidden div to store the uploaded image path
        html.Div(id='uploaded-image-path', style={'display': 'none'})
    ]
)
