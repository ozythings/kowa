import dash
from dash import html, dcc, Output, Input, State
import os

from flask import session

from i18n.upload_labels import get_upload_labels
from pages.unauthorized import unauthorized_layout

dash.register_page(__name__, "/upload")

if not os.path.exists("temp_uploads"):
    os.makedirs("temp_uploads")

def upload_layout(lang="en"):
    labels = get_upload_labels(lang)

    return html.Div(
        className="flex flex-col lg:flex-row p-5 space-y-4 lg:space-x-4",
        children=[
            # left section: upload and type selection
            html.Div(
                className="lg:w-1/3 p-5 border-r border-gray-300 space-y-4",
                children=[
                    html.H3(labels["upload_title"], className="text-xl font-bold"),
                    dcc.Upload(
                        id="upload-image",
                        children=html.Div([
                            labels["drag_and_drop"],
                            html.Button(labels["upload_button"], className="px-2 py-1 bg-blue-500 text-white rounded")
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
                    html.H3(labels["select_type_title"], className="text-xl font-bold mt-4"),
                    dcc.Dropdown(
                        id="image-type",
                        options=[
                            {"label": "BIM", "value": "Miscellaneous"},
                            {"label": "A101", "value": "Miscellaneous"},
                            {"label": "EKENT", "value": "Transportation"},
                            {"label": "OTHER", "value": "Miscellaneous"},
                        ],
                        value="BIM",  # Default value
                        className="w-full p-2 border rounded",
                    ),
                    html.Button(
                        labels["process_button"],
                        id="ocr-process-button",
                        className="w-full px-4 py-2 bg-green-500 text-white rounded mt-4",
                    ),
                    html.Div(children=[

                        html.Button(
                            labels["add_transaction_button"],
                            id="ocr-add-transaction",
                            className="w-full px-4 py-2 bg-gray-500 text-white rounded mt-4",
                        ),
                    ]),
                    html.Div(id='ocr-transaction-status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600")
                ]
            ),

            # right section: display processed data
            html.Div(
                className="lg:w-2/3 p-5",
                children=[
                    html.H3(labels["processed_data_title"], className="text-xl font-bold mb-4"),
                    html.Div(
                        id="processed-data",
                        className="space-y-4",
                        children=[
                            html.Div(
                                className="flex justify-between",
                                children=[html.Label(labels["amount_label"]), dcc.Input(id="ocr-amount",
                                            className="bg-gray-50 border border-gray-300 text-black text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 w-72")]
                            ),
                            html.Div(
                                className="flex justify-between",
                                children=[html.Label(labels["date_label"]), dcc.Input(id="ocr-date",
                                            className="bg-gray-50 border border-gray-300 text-black text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 w-72")]
                            ),
                            html.Div(
                                className="flex justify-between",
                                children=[html.Label(labels["category_label"]), dcc.Input(id="ocr-category",
                                            className="bg-gray-50 border border-gray-300 text-black text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 w-72")]
                            ),
                            html.Div(
                                className="flex justify-between",
                                children=[html.Label(labels["description_label"]), dcc.Input(id="ocr-description",
                                            className="bg-gray-50 border border-gray-300 text-black text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 w-72")]
                            ),
                        ]
                    ),
                    # display the raw OCR text for debugging
                    html.Div(
                        id="raw-ocr-container",
                        className="mt-8",
                        children=[
                            html.H4(labels["raw_ocr_text_title"], className="text-lg font-bold"),
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

def layout(**page_args):
    if session.get("logged_in"):
        return upload_layout(page_args.get("lang"))
    else:
        return unauthorized_layout(page_args.get("lang"))
