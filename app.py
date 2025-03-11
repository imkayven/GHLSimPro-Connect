from flask import Flask, jsonify, request
# from dotenv import load_dotenv
# from swagger.swaggerui import setup_swagger
import requests

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')



@app.route('/connect', methods=['POST'])
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
    site_name = data.get('site_name', '')
    street_address = data.get('street_address', '')
    site_city = data.get('site_city', '')
    site_postal_code = data.get('site_postal_code', '')
    site_country = data.get('site_country', '')
    site_contact_first_name = data.get('site_contact_first_name', '')
    site_contact_last_name = data.get('site_contact_last_name', '')
    site_contact_email = data.get('site_contact_email', '')
    site_contact_phone = data.get('site_contact_phone', '')
    message = data.get('message', '')
    opportunity_name = data.get('opportunity_name', '')
    jobs_name = data.get('jobs_name', '')

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
        "OrderNo": "ORD123",
        "RequestNo": "REQ456",
        "Name": jobs_name,
        "Description": opportunity_name,
        "Notes": message,
        "AutoAdjustStatus": False,
        "Stage": "Pending",
        "DateIssued": "",
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

