import fitz
import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Tuple, Optional

FILES = {
    "uro_Checkout": r"Uro_checkout.pdf",
    "gyn_Checkout": r"Gyn_checkout.pdf",
    "Female_Incontinence": "UDI6.pdf",
    "Intake": "Intake_ Form.pdf",
    "Prostate": "IPSS.pdf",
    "MA": "SAME_DAY_MA.pdf",
    "Sexual": "SHIM.pdf",
    "ERROR": "ERROR.pdf",
}

complete_doc = fitz.open()

def overlay_stickers(
        pt_info: str,
    	file_type: str=None,
    	document: fitz.Document=None,
	    x=30,
	    y=10,
	    insert_date=True
    ) -> fitz.Document:
    """Functionally equivalent to putting the patient checkout sticker on top of the document in the top left corner."""
    if document is None:
        document = fitz.open(os.path.join("documents", FILES.get(file_type, FILES['ERROR'])))
    document[0].clean_contents()
    # Input sticker information
    textbox = fitz.Rect(x, y, x+150, y+20)
    document[0].draw_rect(textbox, color=1, fill=1)
    textbox = fitz.Rect(x, y, x+500, y+70)
    document[0].insert_textbox(textbox, pt_info['Name'].upper(), fontsize=10, fontname='times-bold')
    textbox = fitz.Rect(x, y+15, x+150, y+60)
    document[0].draw_rect(textbox, color=1, fill=1)
    pt_text = f"MRN: {pt_info['MRN']}\nDOB: {pt_info['DOB']}\nMD: {pt_info['Physician'].upper()}"
    document[0].insert_textbox(textbox, pt_text, fontname='times-roman', fontsize=8)

    # Input date + time
    if insert_date:
        datebox = fitz.Rect(500, y, 650, y+40)
        datetime_text = f"{pt_info['Appt Date']}\n{pt_info['Appt Time']}"
        document[0].draw_rect(datebox, color=1, fill=1)
        document[0].insert_textbox(datebox, datetime_text, fontname='times-bold', fontsize=12)
    return document


def create_packet(df: pd.DataFrame, physician: str) -> Tuple[fitz.Document, Optional[fitz.Document]]:
    """
    Creates a packet containing all the information needed.
    Returns: tuple containing the PDF files:
                - The standard packet
                - The MA packet. May be `None` if physician is "Danielle Taylor"
    """
    printout = fitz.open()
    if physician in ["Danielle Taylor", " Urodynamics"]: # Taylor and Urodynamics only do intake and GYN outake forms
        for _, patient in df.iterrows():
            printout.insert_pdf(overlay_stickers(patient, 'Intake'))
            printout.insert_pdf(overlay_stickers(patient, 'gyn_Checkout'))
        printout.ez_save(os.path.join("output", f"{physician.split(' ')[1]}.pdf"))
        complete_doc.insert_pdf(printout)
        return

    for _, patient in df.iterrows(): # All other physicians
        if patient['Gender'] == '##ERROR' or patient['DOB'] == '##ERROR':
            printout.insert_pdf(overlay_stickers(patient, 'ERROR'))
            continue

        if patient['Gender'] == 'F':
            printout.insert_pdf(overlay_stickers(patient, 'Female_Incontinence'))
        elif patient['Gender'] == 'M':
            age = (datetime.today() - datetime.strptime(patient['DOB'], '%m/%d/%Y')).days//365
            if age >= 50:
                printout.insert_pdf(overlay_stickers(patient, 'Prostate'))
            if age >= 15:
                printout.insert_pdf(overlay_stickers(patient, 'Sexual'))
        printout.insert_pdf(overlay_stickers(patient, 'Intake'))
        printout.insert_pdf(overlay_stickers(patient, 'uro_Checkout'))
                
    printout.ez_save(os.path.join("output", f"{physician.split(' ')[1]}.pdf" if physician else "Other.pdf"))
    complete_doc.insert_pdf(printout)

    MA_printout = fitz.open() # Put together the MA forms. Two forms per paper, hence why they are created separately
    doc = fitz.open(os.path.join('documents', FILES['MA']))
    for i, patient in df.iterrows():
        if not i%2:
            if i:
                MA_printout.insert_pdf(doc)
            doc = fitz.open(os.path.join('documents', FILES['MA']))
            overlay_stickers(patient, document=doc)
        else:
            overlay_stickers(patient, document=doc, y=400)
    MA_printout.insert_pdf(doc)
    MA_printout.ez_save(os.path.join("output", f"MA_{physician.split(' ')[1]}.pdf" if physician else "MA_Other.pdf"))
    complete_doc.insert_pdf(MA_printout)


def format_df(df):
    "Miscellaneous formatting that is difficult to do in SQL"
    # Sort and reformat Date and Time
    df = df.sort_values("ApptTime")
    df['Appt Date'] = df['ApptTime'].dt.strftime("%m/%d/%Y")
    df['Appt Time'] = df['ApptTime'].dt.strftime("%I:%M")
    # Format DOB, Gender, and Physician to how it should appear on the sticker
    df['DOB'] = df['DOB'].str.extract(r'(.*) .*')
    df['Gender'] = df['Gender'].str[0]
    df['Physician'] = df['Physician'].str.replace(r'([^ ]+).*, (.*)', r'\2 \1', regex=True)
    df.loc[df['ApptType'] == 'Urodynamics - EC', 'Physician'] = ' Urodynamics' # Yes, the space is important b/c of lines 83 and 97
    df = df.drop('ApptTime', axis=1)
    return df

def run_overlay_stickers(input_file):
    print(os.listdir())
    df = pd.read_csv(input_file, parse_dates=['ApptTime'])
    df = format_df(df)
    for physician, patients in df.groupby("Physician"):
        # Print to terminal to make sure the schedule is correct
        print(">",physician,"<")
        print(patients.set_index('Appt Time',drop=True)['Name'].to_string())
        print()
        create_packet(patients.reset_index(drop=True), physician)
    complete_doc.ez_save(out_path := os.path.join("output", "complete_doc.pdf"))
    return out_path

