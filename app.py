from flask import Flask, jsonify, request
# from dotenv import load_dotenv
# from swagger.swaggerui import setup_swagger
from datetime import datetime
import requests

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')


@app.route('/create-quote2', methods=['POST'])
def create_quote2():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract relevant values from the webhook data
    customer_id = data.get('customerId')
    contact_id = data.get('contactId')
    site_id = data.get('siteId')
    quote_description = data.get('Quote Description')
    quote_notes = data.get('Quote Notes')
    quote_start_date = data.get('Quote Start Date')
    quote_end_date = data.get('Quote End date')
    invoice_date_issued = data.get('Invoice Date Issued')
    invoice_due_date = data.get('Invoice Due Date')
    quote_name = data.get('Quote Name')
    quote_stage = data.get('Quote Stage')

    # Convert the date format from DD/MM/YYYY to YYYY-MM-DD for start and end dates
    try:
        quote_start_date = datetime.strptime(quote_start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        quote_end_date = datetime.strptime(quote_end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        invoice_date_issued = datetime.strptime(invoice_date_issued, '%d/%m/%Y').strftime('%Y-%m-%d')
        invoice_due_date = datetime.strptime(invoice_due_date, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Error converting date: {e}")
        return jsonify({"status": "error", "message": "Invalid date format"}), 400

    # Define headers
    headers = {
        "Authorization": "Bearer f1062d64733b36d51d35f615e6ebfe5a94a44d2b", 
        "Content-Type": "application/json"
    }

    # Step 1: Create the payload for the quote request
    quote_payload = {
        "Customer": customer_id,
        "CustomerContact": contact_id,
        "Site": site_id,
        "SiteContact": contact_id,  # Use the same contact ID for site contact
        "Description": quote_description,
        "Notes": quote_notes,
        "Type": "Project",
        "DateIssued": quote_start_date,
        "DueDate": quote_end_date,
        "ValidityDays": 30,
        "OrderNo": invoice_date_issued,
        "RequestNo": invoice_due_date,
        "Name": quote_name,
        "Stage": quote_stage,
        "Forecast": {
            "Year": 2022,
            "Month": 5,
            "Percent": 75
        },
        "AutoAdjustStatus": True
    }

    # Step 2: Make the POST request to create the quote
    quote_api_url = "https://craftedgandl.simprosuite.com/api/v1.0/companies/0/quotes/"
    quote_response = requests.post(quote_api_url, json=quote_payload, headers=headers)

    # Step 3: Handle the response
    if quote_response.status_code // 100 != 2:  # checks for 2xx success codes (200, 201)
        print(f"Error in creating quote: {quote_response.status_code} - {quote_response.text}")
        return jsonify({"status": "error", "message": "Failed to create quote"}), 500

    quote_id = quote_response.json().get('ID')
    print(f"Quote created successfully with ID: {quote_id}")
    
    # Step 4: Return the success response
    return jsonify({"status": "success", "quote_id": quote_id}), 200



@app.route('/create-job', methods=['POST'])
def log_post_request():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract relevant values from the webhook data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('full_address')
    city = data.get('location', {}).get('city', '')
    state = data.get('location', {}).get('state', '')
    postalCode = data.get('location', {}).get('postalCode', '')
    country = data.get('country')
    site_name = data.get('location', {}).get('fullAddress', '')
    street_address = data.get('location', {}).get('fullAddress', '')
    site_city = data.get('Site City', '')
    site_postal_code = data.get('Site PostalCode', '')
    site_country = data.get('Site Country', '')
    site_contact_first_name = data.get('Contact Given Name', '')
    site_contact_last_name = data.get('Contact Family Name', '')
    site_contact_email = data.get('Contact Email', '')
    site_contact_phone = data.get('Contact CellPhone', '')
    message = data.get('Quote Notes', '')
    opportunity_name = data.get('opportunity_name', '')
    jobs_name = data.get('Jobs Name', '')
    order_number = data.get('Order Number', '')
    request_number = data.get('Quote Request Number', '')
    date_issued = data.get('Invoice Date Issued', '')
    due_issued = data.get('Invoice Due Date', '')
    quote_description = data.get('Quote Description')
    quote_notes = data.get('Quote Notes')
    quote_start_date = data.get('Quote Start Date')
    quote_end_date = data.get('Quote End date')
    quote_name = data.get('Quote Name ')
    quote_stage = data.get('Quote Stage')

    # Convert the date format from DD/MM/YYYY to YYYY-MM-DD for start and end dates
    try:
        quote_start_date = datetime.strptime(quote_start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        quote_end_date = datetime.strptime(quote_end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        date_issued = datetime.strptime(date_issued, '%d/%m/%Y').strftime('%Y-%m-%d')
        due_issued = datetime.strptime(due_issued, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Error converting date: {e}")
        return jsonify({"status": "error", "message": "Invalid date format"}), 400


    # Convert the date format from DD/MM/YYYY to YYYY-MM-DD
    try:
        date_issued = datetime.strptime(date_issued, '%d/%m/%Y').strftime('%Y-%m-%d')
        due_issued = datetime.strptime(due_issued, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Error converting date: {e}")
        return jsonify({"status": "error", "message": "Invalid date format"}), 400


    headers = {
        "Authorization": "Bearer f1062d64733b36d51d35f615e6ebfe5a94a44d2b", 
        "Content-Type": "application/json"
    }

    # Step 1: Create a new individual customer
    print("Step 1: Creating new individual customer...")
    customer_payload = {
        "GivenName": first_name,
        "FamilyName": last_name,
        "Phone": phone,
        "DoNotCall": True,
        "AltPhone": phone,
        "Address": {
            "Address": address,
            "City": city,
            "State": state,
            "PostalCode": postalCode,
            "Country": country
        },
        "BillingAddress": {
            "Address": address,
            "City": city,
            "State": state,
            "PostalCode": postalCode,
            "Country": country
        },
        "CustomerType": "Customer",
        "Email": email,
        "CellPhone": phone,
        "Archived": True
    }

    customer_api_url = "https://craftedgandl.simprosuite.com/api/v1.0/companies/0/customers/individuals/"
    customer_response = requests.post(customer_api_url, json=customer_payload, headers=headers)
    
    if customer_response.status_code // 100 != 2:  # checks for 2xx success codes (200, 201)
        print(f"Error in Step 1: {customer_response.status_code} - {customer_response.text}")
        return jsonify({"status": "error", "message": "Failed to create customer"}), 500

    customer_id = customer_response.json().get('ID')
    print(f"Customer created successfully with ID: {customer_id}")

    # Step 2: Create a new contact
    print("Step 2: Creating new contact...")
    contact_payload = {
        "GivenName": site_contact_first_name,
        "FamilyName": site_contact_last_name,
        "Email": site_contact_email,
        "WorkPhone": site_contact_phone,
        "CellPhone": site_contact_phone,
        "Notes": "This is a test contact"
    }

    contact_api_url = "https://craftedgandl.simprosuite.com/api/v1.0/companies/0/contacts/"
    contact_response = requests.post(contact_api_url, json=contact_payload, headers=headers)

    if contact_response.status_code // 100 != 2:  # checks for 2xx success codes (200, 201)
        print(f"Error in Step 2: {contact_response.status_code} - {contact_response.text}")
        return jsonify({"status": "error", "message": "Failed to create contact"}), 500

    contact_id = contact_response.json().get('ID')
    print(f"Contact created successfully with ID: {contact_id}")

    # Step 3: Create a new site
    print("Step 3: Creating new site...")
    
    site_payload = {
        "Name": site_name,
        "Address": {
            "Address": street_address,
            "City": site_city,
            "State": state,
            "PostalCode": site_postal_code,
            "Country": site_country
        },
        "PrimaryContact": {
            "Contact": contact_id  # Use the correct structure with Contact as an object
        },
        "PublicNotes": "Public site notes",
        "PrivateNotes": "Private site notes",
        "Archived": False
    }

    site_api_url = "https://craftedgandl.simprosuite.com/api/v1.0/companies/0/sites/"
    site_response = requests.post(site_api_url, json=site_payload, headers=headers)

    if site_response.status_code // 100 != 2:  # checks for 2xx success codes (200, 201)
        print(f"Error in Step 3: {site_response.status_code} - {site_response.text}")
        return jsonify({"status": "error", "message": "Failed to create site"}), 500

    site_id = site_response.json().get('ID')
    print(f"Site created successfully with ID: {site_id}")

    # Step 4: Create a new job with the customerId, contactId, and siteId
    print("Step 4: Creating new job...")
    job_payload = {
        "Type": "Project",
        "Customer": customer_id,
        "Site": site_id,
        "SiteContact": contact_id,
        "OrderNo": order_number,
        "RequestNo": request_number,
        "Name": jobs_name,
        "Description": opportunity_name,
        "Notes": message,
        "AutoAdjustStatus": False,
        "Stage": "Pending",
        "DateIssued": date_issued,
        "DueDate": ""
    }

    job_api_url = "https://craftedgandl.simprosuite.com/api/v1.0/companies/0/jobs/"
    job_response = requests.post(job_api_url, json=job_payload, headers=headers)

    if job_response.status_code // 100 != 2:  # checks for 2xx success codes (200, 201)
        print(f"Error in Step 4: {job_response.status_code} - {job_response.text}")
        return jsonify({"status": "error", "message": "Failed to create job"}), 500

    job_id = job_response.json().get('ID')
    print(f"Job created successfully with ID: {job_id}")
    return jsonify({"status": "success", "job_id": job_id}), 200



@app.route('/create-quote', methods=['POST'])
def create_quote():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract relevant values from the webhook data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('full_address')
    city = data.get('location', {}).get('city', '')
    state = data.get('location', {}).get('state', '')
    postalCode = data.get('location', {}).get('postalCode', '')
    country = data.get('country')
    site_name = data.get('location', {}).get('fullAddress', '')
    street_address = data.get('location', {}).get('fullAddress', '')
    site_city = data.get('Site City', '')
    site_postal_code = data.get('Site PostalCode', '')
    site_country = data.get('Site Country', '')
    site_contact_first_name = data.get('Contact Given Name', '')
    site_contact_last_name = data.get('Contact Family Name', '')
    site_contact_email = data.get('Contact Email', '')
    site_contact_phone = data.get('Contact CellPhone', '')
    message = data.get('Quote Notes', '')
    opportunity_name = data.get('opportunity_name', '')
    jobs_name = data.get('Jobs Name', '')
    order_number = data.get('Order Number', '')
    request_number = data.get('Quote Request Number', '')
    date_issued = data.get('Invoice Date Issued', '')
    due_issued = data.get('Invoice Due Date', '')
    quote_description = data.get('Quote Description', '')
    quote_notes = data.get('Quote Notes', '')
    quote_start_date = data.get('Invoice Date Issued')
    quote_end_date = data.get('Invoice Due Date')
    quote_name = data.get('Quote Name', '')
    quote_stage = data.get('Quote Stage', '')
    site_public_notes = data.get('Site PublicNotes', '')
    site_private_notes = data.get('Site PrivateNotes', '')

    # Convert the date format from DD/MM/YYYY to YYYY-MM-DD for start and end dates
    try:
        quote_start_date = datetime.strptime(quote_start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        quote_end_date = datetime.strptime(quote_end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        date_issued = datetime.strptime(date_issued, '%d/%m/%Y').strftime('%Y-%m-%d')
        due_issued = datetime.strptime(due_issued, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Error converting date: {e}")
        return jsonify({"status": "error", "message": "Invalid date format"}), 400

    # Define headers for the request
    headers = {
        "Authorization": "Bearer f1062d64733b36d51d35f615e6ebfe5a94a44d2b", 
        "Content-Type": "application/json"
    }

    # Step 1: Create a new individual customer
    print("Step 1: Creating new individual customer...")
    customer_payload = {
        "GivenName": first_name,
        "FamilyName": last_name,
        "Phone": phone,
        "DoNotCall": True,
        "AltPhone": phone,
        "Address": {
            "Address": address,
            "City": city,
            "State": state,
            "PostalCode": postalCode,
            "Country": country
        },
        "BillingAddress": {
            "Address": address,
            "City": city,
            "State": state,
            "PostalCode": postalCode,
            "Country": country
        },
        "CustomerType": "Customer",
        "Email": email,
        "CellPhone": phone,
        "Archived": True
    }

    customer_api_url = "https://craftedgandl.simprosuite.com/api/v1.0/companies/0/customers/individuals/"
    customer_response = requests.post(customer_api_url, json=customer_payload, headers=headers)
    
    if customer_response.status_code // 100 != 2:  # checks for 2xx success codes (200, 201)
        print(f"Error in Step 1: {customer_response.status_code} - {customer_response.text}")
        return jsonify({"status": "error", "message": "Failed to create customer"}), 500

    customer_id = customer_response.json().get('ID')
    print(f"Customer created successfully with ID: {customer_id}")

    # Step 2: Create a new contact
    print("Step 2: Creating new contact...")
    contact_payload = {
        "GivenName": site_contact_first_name,
        "FamilyName": site_contact_last_name,
        "Email": site_contact_email,
        "WorkPhone": site_contact_phone,
        "CellPhone": site_contact_phone,
        "Notes": "This is a test contact"
    }

    contact_api_url = "https://craftedgandl.simprosuite.com/api/v1.0/companies/0/contacts/"
    contact_response = requests.post(contact_api_url, json=contact_payload, headers=headers)

    if contact_response.status_code // 100 != 2:  # checks for 2xx success codes (200, 201)
        print(f"Error in Step 2: {contact_response.status_code} - {contact_response.text}")
        return jsonify({"status": "error", "message": "Failed to create contact"}), 500

    contact_id = contact_response.json().get('ID')
    print(f"Contact created successfully with ID: {contact_id}")

    # Step 3: Create a new site
    print("Step 3: Creating new site...")
    site_payload = {
        "Name": site_name,
        "Address": {
            "Address": street_address,
            "City": site_city,
            "State": state,
            "PostalCode": site_postal_code,
            "Country": site_country
        },
        "PrimaryContact": {
            "Contact": contact_id  # Use the correct structure with Contact as an object
        },
        "PublicNotes": site_public_notes,
        "PrivateNotes": site_private_notes,
        "Archived": False
    }

    site_api_url = "https://craftedgandl.simprosuite.com/api/v1.0/companies/0/sites/"
    site_response = requests.post(site_api_url, json=site_payload, headers=headers)

    if site_response.status_code // 100 != 2:  # checks for 2xx success codes (200, 201)
        print(f"Error in Step 3: {site_response.status_code} - {site_response.text}")
        return jsonify({"status": "error", "message": "Failed to create site"}), 500

    site_id = site_response.json().get('ID')
    print(f"Site created successfully with ID: {site_id}")

    # Step 4: Create the quote
    print("Step 4: Creating new quote...")
    quote_payload = {
        "Customer": customer_id,
        "CustomerContact": contact_id,
        "Site": site_id,
        "SiteContact": contact_id,  # Use the same contact ID for site contact
        "Description": quote_description,
        "Notes": quote_notes,
        "Type": "Project",
        "DateIssued": quote_start_date,
        "DueDate": quote_end_date,
        "ValidityDays": 30,
        "OrderNo": date_issued,
        "RequestNo": due_issued,
        "Name": quote_name,
        "Stage": quote_stage,
        "Forecast": {
            "Year": 2022,
            "Month": 5,
            "Percent": 75
        },
        "AutoAdjustStatus": True
    }

    # Make the request to create the quote
    quote_api_url = "https://craftedgandl.simprosuite.com/api/v1.0/companies/0/quotes/"
    quote_response = requests.post(quote_api_url, json=quote_payload, headers=headers)

    if quote_response.status_code // 100 != 2:  # checks for 2xx success codes (200, 201)
        print(f"Error in Step 4: {quote_response.status_code} - {quote_response.text}")
        return jsonify({"status": "error", "message": "Failed to create quote"}), 500

    quote_id = quote_response.json().get('ID')
    print(f"Quote created successfully with ID: {quote_id}")

    return jsonify({"status": "success", "quote_id": quote_id}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({
    "message": {
        "status": "ok",
        "developer": "kayven",
        "email": "yvendee2020@gmail.com"
    }})


if __name__ == '__main__':
    app.run(debug=True)

