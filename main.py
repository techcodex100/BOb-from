from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

# 📝 Input model
class Form144Data(BaseModel):
    branch_name: str
    beneficiary_name: str
    account_number: str
    line_of_business: str
    commodity_service: str
    bill_currency: str
    amount_figures: str
    amount_words: str
    remitter_name: str
    remitter_address: str
    purpose_code: str
    purpose_description: str
    shipment_date: str
    credit_currency: str
    max_amount: str
    convert_100_percent_inr: str
    convert_partial_and_hold: str
    hold_in_nostro: str
    credit_as_per_a2: str
    credit_my_PCFC_acc: str
    debit_charges_account: str
    fc_number: str
    booking_date: str
    fc_amount: str
    due_date: str
    amount_utilized: str
    exchange_rate: str
    date:str
    signature: str
    page2_date: str
    page2_signature: str

# ✏️ Function to draw digit boxes
def draw_digits_in_boxes(draw, value, start_x, y, spacing=34, font=None):
    for i, digit in enumerate(value):
        draw.text((start_x + i * spacing, y), digit, font=font, fill="black")

# 🧾 Generate PDF
@app.post("/generate", response_class=FileResponse)
def generate_pdf(data: Form144Data):
    # Load 5 scanned images
    pages = [Image.open(f"bank of baroda {i}.jpg").convert("RGB") for i in range(1, 7)]
    draws = [ImageDraw.Draw(page) for page in pages]

    # Use larger font
    try:
        font = ImageFont.truetype("arial.ttf", size=24)  # if Arial is available
    except:
        font = ImageFont.load_default()

    # Position mapping (x, y, page_index)
    positions = {
        "branch_name": (1000, 100, 0),
        "beneficiary_name": (280, 175, 0),
        "account_number": (295, 210, 0),
        "line_of_business": (400, 265, 0),
        "commodity_service": (975, 265, 0),
        "bill_currency": (310, 325, 0),
        "amount_figures": (300, 375, 0),
        "amount_words": (700, 360, 0),
        "remitter_name": (300, 410, 0),
        "remitter_address": (300, 475, 0),
        "purpose_code": (200, 550, 0),
        "purpose_description": (540, 550, 0),
        "shipment_date": (930, 590, 0),
        "credit_currency": (800, 682, 0),
        "max_amount": (950, 682, 0),
        "convert_100_percent_inr": (740, 790, 0),
        "convert_partial_and_hold": (740, 830, 0),
        "hold_in_nostro": (740, 865, 0),
        "credit_as_per_a2": (740, 910, 0),
        "credit_my_PCFC_acc": (742, 975, 0),
        "debit_charges_account": (270, 1040, 0),
        "fc_number": (400, 1175, 0),
        "booking_date": (950, 1175, 0),
        "fc_amount": (400, 1225, 0),
        "due_date": (950, 1225, 0),
        "amount_utilized": (400, 1275, 0),
        "exchange_rate": (1050, 1265, 0),
        "date":(160,1370,0),
        "signature": (700, 1375, 0),
        "page2_date": (120, 1400, 1),
        "page2_signature": (700, 1400, 1)
        # 🔔 You can add more fields for page3, page4, page5 as needed
    }

    # Fields with boxes (draw digits with spacing)
    box_fields = [
        "shipment_date", "convert_100_percent_inr", "convert_partial_and_hold",
        "hold_in_nostro", "credit_as_per_a2", "credit_my_PCFC_acc",
        "debit_charges_account", "booking_date","date", "due_date", "page2_date"
    ]

    # Draw fields on images
    for key, value in data.dict().items():
        if key in positions:
            x, y, page_idx = positions[key]
            draw = draws[page_idx]
            if key in box_fields:
                draw_digits_in_boxes(draw, value, x, y, spacing=34, font=font)
            else:
                for i, line in enumerate(value.split("\n")):
                    draw.text((x, y + i * 40), line, font=font, fill="black")

    # Combine all 5 pages into single vertical PDF
    width = pages[0].width
    total_height = sum(page.height for page in pages)
    final_pdf = Image.new("RGB", (width, total_height), "white")

    current_y = 0
    for page in pages:
        final_pdf.paste(page, (0, current_y))
        current_y += page.height

    output_path = "generated_remittance_form.pdf"
    final_pdf.save(output_path)

    return FileResponse(output_path, media_type="application/pdf", filename=output_path)

# Swagger redirect
@app.get("/")
def root():
    return RedirectResponse(url="/docs")
