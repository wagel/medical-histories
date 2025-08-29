import pandas as pd
from openai import OpenAI
import logging

# =========================================
# File utils ==============================
# =========================================


def upload_file_to_openai(client: OpenAI, path_to_file: str):
    return client.files.create(
        file=open(path_to_file, "rb"),
        purpose="user_data"
    )


def delete_file_from_openai(client: OpenAI, file_id: str):
    return client.files.delete(file_id)


def generate_pdf_input(client: OpenAI, file_id: str, prompt: str = "Attached is the PDF document:"):
    return {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": prompt
            },
            {
                "type": "input_file",
                "file_id": file_id,
            },

        ]
    }


# =========================================
# File utils ==============================
# =========================================


def load_lexicon_from_csv(path_to_lexicon_csv: str):
    lexicon = pd.read_csv(path_to_lexicon_csv)
    return lexicon.to_dict(orient="records")


def fetch_lexicon():
    return {
        "A": "A",
        "AD": "AD",
        "ADV": "ADV",
        "AIHA": "AIHA",
        "AMD": "AMD",
        "AME": "AME",
        "AS": "AS",
        "ATE": "ATE",
        "AU": "AU",
        "ausc": "ausc",
        "B": "B",
        "BIOP": "BIOP",
        "BP": "BP",
        "BPH": "BPH",
        "BV": "BV",
        "C": "C",
        "CAM": "CAM",
        "CBA": "CBA",
        "CDI": "CDI",
        "CFA": "CFA",
        "COHAT": "COHAT",
        "D": "D",
        "DMITO": "DMITO",
        "DOA": "DOA",
        "DTO": "DTO",
        "DUDE": "DUDE",
        "E": "E",
        "MEEN": "MEEN",
        "NEEM": "NEEM",
        "EEMN": "EEMN",
        "EENT": "EENT",
        "F": "F",
        "FATE": "FATE",
        "FIA": "FIA",
        "FIC": "FIC",
        "FLUTD": "FLUTD",
        "FNA": "FNA",
        "G": "G",
        "Gastro": "Gastro",
        "GI": "GI",
        "H": "H",
        "HC": "HC",
        "HCM": "HCM",
        "HR": "HR",
        "I": "I",
        "IFHA": "IFHA",
        "IMHA": "IMHA",
        "IMPA": "IMPA",
        "IOP": "IOP",
        "J": "J",
        "K": "K",
        "L": "L",
        "M": "M",
        "MSK": "MSK",
        "MUO": "MUO",
        "MUO-ON": "MUO-ON",
        "N": "N",
        "NAD": "NAD",
        "NSF": "NSF",
        "NWB": "NWB",
        "O": "O",
        "OA": "OA",
        "OCNE": "OCNE",
        "OD": "OD",
        "OFMES": "OFMES",
        "OR": "OR",
        "OS": "OS",
        "OSA": "OSA",
        "OU": "OU",
        "OU tel": "OU tel",
        "P": "P",
        "pabs": "pabs",
        "PABT": "PABT",
        "PDE": "PDE",
        "PITA": "PITA",
        "POU": "POU",
        "PP": "PP",
        "PPDH": "PPDH",
        "PPS": "PPS",
        "PSS": "PSS",
        "Q": "Q",
        "QMA": "QMA",
        "R": "R",
        "S": "S",
        "SAI": "SAI",
        "SCREED": "SCREED",
        "SIBO": "SIBO",
        "SL": "SL",
        "SLJ": "SLJ",
        "SMLN": "SMLN",
        "STARWHEEL": "STARWHEEL",
        "SWO": "SWO",
        "STOOP": "STOOP",
        "STT": "STT",
        "SUSP": "SUSP",
        "T": "T",
        "TC": "TC",
        "3EL": "3EL",
        "TEL": "TEL",
        "TGH": "TGH",
        "THR": "THR",
        "TID": "TID",
        "TRA": "TRA",
        "TTF": "TTF",
        "U": "U",
        "UPCR": "UPCR",
        "V": "V",
        "VDCS": "VDCS",
        "VMB": "VMB",
        "VTSH": "VTSH",
        "W": "W",
        "W/O": "W/O",
        "wt": "wt",
        "X": "X",
        "Y": "Y",
        "Z": "Z"
    }


def fetch_prompt():
    return """
    Extract the following critical information from the supplied medical history documents.  
    Return the result in a Markdown table with columns: **Info | Value**.  

    Required fields:  
        - "From" Date (claim start date)  
        - DOB (pet)  
        - Condition (what is being claimed)  
        - Animal's name, address, breed, DOB  
        - Specific treatment dates  
        - When issue was noticed  
        - Accident/Injury type  
        - Sex, breed, age  
        - Pre-existing condition?  
        - Incomplete history (missing records)  
        - Policy wording (exact clause)  
        - Last paid date (for continuations)  
        - Diagnosis of past episodes  
        - Related symptoms  
        - Clinical history summary  
        - Invoice content (treatments, pricing, anomalies)  
        - Policy limit/money left 

    Note:
        - Use the lexicon where applicable to ensure consistent terminology.
        - If the data is not available, return "N/A"
        - This medical history is supplied to support an insurance claim.
        It is used to analysie the state of the claim and determine if the claim is valid.
    """


def setup_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger