import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF

# Mapping of PhoneNumberType enum values to their corresponding names
PHONE_TYPE_NAMES = {
    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
    phonenumbers.PhoneNumberType.MOBILE: "Mobile",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
    phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-Free",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
    phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
    phonenumbers.PhoneNumberType.VOIP: "VoIP",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
    phonenumbers.PhoneNumberType.PAGER: "Pager",
    phonenumbers.PhoneNumberType.UAN: "UAN",
    phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
    phonenumbers.PhoneNumberType.UNKNOWN: "Unknown"
}

# Function to get the phone number type name
def get_phone_type_name(parsed_number):
    number_type = phonenumbers.number_type(parsed_number)
    return PHONE_TYPE_NAMES.get(number_type, "Unknown")

# Function to generate the PDF report
def generate_pdf_report():
    # Get the phone number from the input field
    phone_number = phone_number_entry.get()

    # Parse the phone number
    parsed_number = phonenumbers.parse(phone_number, "US")  # Assuming US format

    # Create a PDF report
    pdf_filename = "phone_number_report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []

    # Title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title = Paragraph("Phone Number Report", title_style)
    story.append(title)

    # Add a separator line
    story.append(Spacer(1, 12))

    # Phone Number
    phone_number_paragraph = Paragraph("Phone Number: " + phone_number, styles['Normal'])
    story.append(phone_number_paragraph)

    # Timezone
    timezone_info = timezone.time_zones_for_number(parsed_number)
    timezone_paragraph = Paragraph("Timezone: " + ', '.join(timezone_info), styles['Normal'])
    story.append(timezone_paragraph)

    # Carrier
    carrier_name = carrier.name_for_number(parsed_number, "en")
    carrier_paragraph = Paragraph("Carrier: " + carrier_name, styles['Normal'])
    story.append(carrier_paragraph)

    # Region
    region_info = geocoder.description_for_number(parsed_number, "en")
    region_paragraph = Paragraph("Region: " + region_info, styles['Normal'])
    story.append(region_paragraph)

    # Validating Mobile Number
    is_valid = phonenumbers.is_valid_number(parsed_number)
    validation_paragraph = Paragraph("Validating Mobile Number: " + str(is_valid), styles['Normal'])
    story.append(validation_paragraph)

    # Phone Number Type
    number_type_str = get_phone_type_name(parsed_number)
    number_type_paragraph = Paragraph("Number Type: " + number_type_str, styles['Normal'])
    story.append(number_type_paragraph)

    # Pie Chart Data
    valid_percentage = phonenumbers.is_valid_number(parsed_number) * 100
    invalid_percentage = 100 - valid_percentage

    # Create a Pie Chart
    d = Drawing(400, 200)
    data = [valid_percentage, invalid_percentage]
    labels = ['Valid', 'Invalid']

    pc = Pie()
    pc.x = 150
    pc.y = 50
    pc.data = data
    pc.labels = labels
    pc.slices.strokeWidth = 0.5
    pc.slices[0].popout = 10  # Explode the first slice (Valid) for emphasis

    d.add(pc)

    # Add the Pie Chart to the PDF report
    story.append(Spacer(1, 12))
    chart_title = Paragraph("Validation Distribution", styles['Normal'])
    story.append(chart_title)
    story.append(Spacer(1, 6))
    story.append(d)

    # Save the PDF
    doc.build(story)
    messagebox.showinfo("PDF Generated", f"PDF report has been generated as '{pdf_filename}'")

# Create the main window
root = tk.Tk()
root.title("Phone Number Information")

# Create and place widgets
phone_number_label = ttk.Label(root, text="Enter the Phone No you want to track:")
phone_number_label.pack(pady=10)
phone_number_entry = ttk.Entry(root)
phone_number_entry.pack()

generate_button = ttk.Button(root, text="Generate Report", command=generate_pdf_report)
generate_button.pack(pady=10)

# Start the main event loop
root.mainloop()
