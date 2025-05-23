from datetime import datetime
import asyncio
from dash import State, html, Output, Input
from dash.dash import base64

from i18n.dashboard_labels import get_category_labels
from i18n.upload_labels import get_upload_callback_labels, get_upload_labels
from utils.load_data import load_local_transactions, save_local_transactions, save_transactions, userid
from chrome_lens_py import LensAPI
import re

from utils.url_helpers import get_lang_from_query

def parse_receipt_text(text: str, receipt_type: str, lang= "en"):

    labels = get_upload_labels(lang)
    category_labels = get_category_labels(lang)

    amount_pattern = r'(\d+[.,]\d{1,2})'
    date_pattern = r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b'
    time_pattern = r'SAAT\s*[:\-]?\s*(\d{1,2}:\d{2})'

    all_amounts = re.findall(amount_pattern, text)
    amount = 0.0
    if all_amounts:
        numeric_amounts = [float(a.replace(',', '.')) for a in all_amounts]
        amount = max(numeric_amounts)

    date = ""
    date_matches = re.findall(date_pattern, text)
    if date_matches:
        raw_date = date_matches[0]
        date = convert_ocr_date(raw_date)

    description = labels["unknown_time"]
    time_matches = re.findall(time_pattern, text, re.IGNORECASE)
    
    filtered_receipt_type = category_labels[receipt_type]

    if time_matches:
        receipt_type = receipt_type.upper()
        if receipt_type == "BIM":
            description = f"{labels['time']}: {time_matches[0]} BIM {labels['receipt']}"
        elif receipt_type == "A101":
            description =f"{labels['time']}: {time_matches[0]} A101 {labels['receipt']}"
        elif receipt_type == "EKENT":
            description = f"{labels['time']}: {time_matches[0]} EKENT {labels['receipt']}"
        else:
            description = f"{labels['time']}: {time_matches[0]} {labels['receipt']} ({filtered_receipt_type})"

    return amount, date, description

def convert_ocr_date(raw_date):
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y", "%d.%m.%Y", "%d.%m.%y"):
        try:
            parsed_date = datetime.strptime(raw_date, fmt)
            date = parsed_date.strftime("%Y-%m-%d")
            return date
        except ValueError:
            continue

async def process_image_async(image_path):
    """
    Process image using LensAPI asynchronously
    """
    api = LensAPI()
    try:
        raw_text = await api.get_full_text(image_path)
        return raw_text
    finally:
        # close the session when done
        await api.close_session()

def process_image_with_chrome_lens(image_path, image_type, lang):
    """
    Process the image using Chrome Lens OCR
    
    Args:
        image_path: Path to the image file
        image_type: Type of document (BIM, A101, EKENT)
        
    Returns:
        tuple: (amount, date, description, raw_text)
    """
    try:

        raw_text = asyncio.run(process_image_async(image_path))
        amount, date, description = parse_receipt_text(raw_text, image_type, lang)

        return amount, date, description, raw_text
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return f"Error: {str(e)}", "", "", f"OCR failed: {str(e)}"

def upload_callback(app, use_remote_db=False):
    @app.callback(
        [Output("upload-status", "children"),
         Output("preview-container", "children"),
         Output("uploaded-image-path", "children")],
        [Input("upload-image", "contents")],
        [State("upload-image", "filename"),
        State('url','search')]
    )
    def handle_upload(contents, filename, search):

        lang = get_lang_from_query(search) or "en"
        callback_labels = get_upload_callback_labels(lang)

        if contents is None:
            return "", "", ""
        
        # decode the base64 image
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # generate a unique filename to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"temp_uploads/{timestamp}_{filename}"
        
        # save the file
        with open(unique_filename, 'wb') as f:
            f.write(decoded)
        
        # image preview
        preview = html.Div([
            html.Img(src=contents, style={'maxHeight': '200px', 'maxWidth': '100%'}),
            html.Div(f"{callback_labels['uploaded']}: {filename}", className="text-sm")
        ])
        
        return callback_labels["upload_successful"], preview, unique_filename

    @app.callback(
        [Output("ocr-amount", "value"),
         Output("ocr-date", "value"),
         Output("ocr-category", "value"),
         Output("ocr-description", "value"),
         Output("raw-ocr-text", "children")],
        [Input("ocr-process-button", "n_clicks")],
        [State("uploaded-image-path", "children"),
         State("image-type", "value"),
         State('url', 'search')]
    )
    def process_image(n_clicks, image_path, selected_category, search):
        lang = get_lang_from_query(search) or "en"

        category_map = {
            "BIM": "Miscellaneous",
            "A101": "Miscellaneous",
            "EKENT": "Transportation",
            "OTHER": "Miscellaneous"
        }
        category = category_map[selected_category]
        if n_clicks is None or not image_path:
            return "", "", "", "", ""
            
        try:
            # process the image with chrome-lens-py
            amount, date, description, raw_text = process_image_with_chrome_lens(image_path, category, lang)

            return amount, date, selected_category, description, raw_text

        except Exception as e:
            error_message = f"Processing error: {str(e)}"
            return error_message, "", "", "", error_message

    @app.callback(
        Output('ocr-transaction-status', 'children'),
        Input('ocr-add-transaction', 'n_clicks'),
        [State('ocr-date', 'value'), 
        State('ocr-amount', 'value'), 
        State('ocr-category', 'value'), 
        State('ocr-description', 'value'),
        State('url','search')]
    )
    def add_ocr_transaction(n_clicks, date, amount, selected_category, description, search):

        lang = get_lang_from_query(search) or "en"
        labels = get_upload_labels(lang)
        category_labels = get_category_labels(lang)
        callback_labels = get_upload_callback_labels(lang)

        category_map = {
            "BIM": "Miscellaneous",
            "A101": "Miscellaneous",
            "EKENT": "Transportation",
            "OTHER": "Miscellaneous"
        }
        category = category_map[selected_category]

        current_time = datetime.now().strftime('%H:%M:%S')
        if n_clicks > 0 and date and amount and category:
            new_transaction = {
                'userid': userid(),
                'date': date,
                'categoryname': category,
                'amount': amount, 
                'description': description
            }

            if use_remote_db:
                save_transactions(new_transaction)
            else:
                transactions = load_local_transactions()

                # fix for nan transactionid values
                if 'transactionid' in transactions.columns and not transactions['transactionid'].isnull().all():
                    next_id = transactions['transactionid'].max() + 1
                else:
                    next_id = 0

                new_transaction['transactionid'] = int(next_id)
                transactions['transactionid'] = transactions['transactionid'].astype('Int64')
                #transactions['categoryname'] = transactions['categoryname'].map(category_labels)

                new_transaction.update({'date': f'{date} {current_time}'})
                transactions.loc[len(transactions)] = new_transaction
                save_local_transactions(transactions)

            return f"{labels['transaction_added']}: {date}, {amount}, {category_labels[category]}"

        elif n_clicks > 0:
            if not date:
                return callback_labels["select_date"]
            elif not amount:
                return callback_labels["enter_amount"]
            elif not category:
                return callback_labels["select_category"]
        return "" # button not clicked
