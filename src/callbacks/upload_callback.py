from datetime import datetime
import asyncio
from dash import Dash, State, html, dcc, Output, Input
import dash
from dash.dash import base64
from flask import session
from flask_caching import Cache
from chrome_lens_py import LensAPI
import re

def parse_receipt_text(text: str, receipt_type: str):
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

    description = "Unknown Time"
    time_matches = re.findall(time_pattern, text, re.IGNORECASE)
    if time_matches:
        receipt_type = receipt_type.upper()
        if receipt_type == "BIM":
            description = f"Time: {time_matches[0]} BIM Receipt"
        elif receipt_type == "A101":
            description =f"Time: {time_matches[0]} A101 Receipt"
        elif receipt_type == "EKENT":
            description = f"Time: {time_matches[0]} EKENT Receipt"
        else:
            description = f"Time: {time_matches[0]} Receipt ({receipt_type})"

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

def process_image_with_chrome_lens(image_path, image_type):
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
        amount, date, description = parse_receipt_text(raw_text, image_type)

        return amount, date, description, raw_text
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return f"Error: {str(e)}", "", "", f"OCR failed: {str(e)}"

def upload_callback(app):
    @app.callback(
        [Output("upload-status", "children"),
         Output("preview-container", "children"),
         Output("uploaded-image-path", "children")],
        [Input("upload-image", "contents")],
        [State("upload-image", "filename")]
    )
    def handle_upload(contents, filename):
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
            html.Div(f"Uploaded: {filename}", className="text-sm")
        ])
        
        return f"Upload successful!", preview, unique_filename

    @app.callback(
        [Output("ocr-amount", "value"),
         Output("ocr-date", "value"),
         Output("ocr-category", "value"),
         Output("ocr-description", "value"),
         Output("raw-ocr-text", "children")],
        [Input("process-button", "n_clicks")],
        [State("uploaded-image-path", "children"),
         State("image-type", "value")]
    )
    def process_image(n_clicks, image_path, selected_category):
        if n_clicks is None or not image_path:
            return "", "", "", "", ""
            
        try:
            # process the image with chrome-lens-py
            amount, date, description, raw_text = process_image_with_chrome_lens(image_path, selected_category)

            return amount, date, selected_category, description, raw_text

        except Exception as e:
            error_message = f"Processing error: {str(e)}"
            return error_message, "", "", "", error_message
