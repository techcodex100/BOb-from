from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

# 🔹 Input data structure
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
    signature: str
    page2_date: str
    page2_signature: str

# 🔹 Draw digits in boxes
def draw_digits_in_boxes(draw, value, start_x, y, spacing=22, font=None):
    for i, digit in enumerate(value):
        draw.text((start_x + i * spacing, y), digit, font=font, fill="black")

# 🔹 Generate PDF
@app.post("/generate", response_class=FileResponse)
def generate_pdf(data: Form144Data):
    # Load page images
    page1 = Image.open("bankof baroda 1.jpg").convert("RGB")
    page2 = Image.open("bank of baroda 2.jpg").convert("RGB")
    draw1 = ImageDraw.Draw(page1)
    draw2 = ImageDraw.Draw(page2)
    font = ImageFont.truetype("arial.ttf", 18)

    # Field coordinates
    positions = {
        "branch_name": (1000, 100),
        "beneficiary_name": (280, 175),
        "account_number": (295, 220),
        "line_of_business": (400, 265),
        "commodity_service": (975, 265),
        "bill_currency": (310, 325),
        "amount_figures": (300, 375),
        "amount_words": (700, 375),
        "remitter_name": (300, 410),
        "remitter_address": (300, 475),
        "purpose_code": (200, 550),
        "purpose_description": (540, 550),
        "shipment_date": (920, 590),
        "credit_currency": (800, 682),
        "max_amount": (950, 682),
        "convert_100_percent_inr": (740, 790),
        "convert_partial_and_hold": (740, 830),
        "hold_in_nostro": (740, 875),
        "credit_as_per_a2": (740, 920),
        "credit_my_PCFC_acc": (742, 990),
        "debit_charges_account": (270, 1050),
        "fc_number": (400, 1175),
        "booking_date": (940, 1175),
        "fc_amount": (400, 1225),
        "due_date": (940, 1225),
        "amount_utilized": (400, 1275),
        "exchange_rate": (1050, 1275),
        "signature": (700, 1375),
        "page2_date": (120, 1400),
        "page2_signature": (700, 1400)
    }

    # Fields that need box-wise writing
    box_fields = [
        "shipment_date", "convert_100_percent_inr", "convert_partial_and_hold",
        "hold_in_nostro", "credit_as_per_a2", "credit_my_PCFC_acc",
        "debit_charges_account", "booking_date", "due_date", "page2_date"
    ]

    # Draw on both pages
    for key, value in data.dict().items():
        if key in positions:
            x, y = positions[key]
            draw = draw1 if "page2" not in key else draw2
            if key in box_fields:
                draw_digits_in_boxes(draw, value, x, y, spacing=34, font=font)
            else:
                for i, line in enumerate(value.split("\n")):
                    draw.text((x, y + i * 20), line, font=font, fill="black")

    # Merge both pages into one PDF
    pdf_path = "generated_remittance_form.pdf"
    final_pdf = Image.new("RGB", (page1.width, page1.height * 2), "white")
    final_pdf.paste(page1, (0, 0))
    final_pdf.paste(page2, (0, page1.height))
    final_pdf.save(pdf_path)

    return FileResponse(pdf_path, media_type="application/pdf", filename=pdf_path)
