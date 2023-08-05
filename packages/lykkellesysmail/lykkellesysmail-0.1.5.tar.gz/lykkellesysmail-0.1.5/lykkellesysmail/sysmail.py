import requests

url = 'https://api.sendinblue.com/v3/smtp/email'
password = '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'

class emaildailyjobs:
    def __init__(self, sendername, sender_email, receivers,subject, template):
        headers = {'api-key': password, 'Accept': 'application/json', 'content-type': 'application/json'}
        data = {"sender": {"name": sendername, "email": sender_email},
                "to": receivers,
                "subject":subject,
                "params": template,
                "templateId": 3}
        try:
            val = list(template.keys())
        except AttributeError:
            val = []
        if val == ['jobname','jobdetails']:
            response = requests.post(url, headers=headers, json=data)
            status = response.status_code
            if str(status)[:2] == "20":
                pass
            else:
                print("error details:\n",response.json())
        else:
            print("""incorrect parameter provided for the email format. Use 'jobname' and 'jobdetails'""")

class emailpwreset:
    def __init__(self, sendername, sender_email, receivers,template):
        headers = {'api-key': password, 'Accept': 'application/json', 'content-type': 'application/json'}
        data = {"sender": {"name": sendername, "email": sender_email},
                "to": receivers,
                "params": template,
                "templateId": 2}
        try:
            val = list(template.keys())
        except AttributeError:
            val = []
        if val == ['firstname', 'password']:
            response = requests.post(url, headers=headers, json=data)
            status = response.status_code
            if str(status)[:2] == "20":
                pass
            else:
                print("error details:\n",response.json())
        else:
            print("""incorrect parameter provided for the email format. Use 'firstname' and 'password'""")


# sendername="Lykkelle Automated services"
# sender_email="systemservices@lykkelle.com"
# receivers=[{"email":"systemstatistics@lykkelle.com","name":"System statistics"}]
# subject="Updating the daily maintainance jobs"
# template = {"jobname":"sample job name","jobdetails":"sample job details"}
# template2 = {"firstname":"Deb","password":"123456"}
#
# emaildailyjobs(sendername,sender_email,receivers,subject,template)
# emailpwreset(sendername,sender_email,receivers,template2)
