
# Health Checker

It checks if a website is up or down, and if it's down, it sends a text message and makes a phone call to the specified phone number.

It uses Twilio RESTAPI to send message and make phone calls.




## Run Locally

Clone the project

```bash
  git clone https://github.com/SkMishra77/Health_check.git
```

Go to the project directory

```bash
  cd Health_check
```

Install dependencies

```bash
  pip install -r requirements.txt
```
Update the environment variables

### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`ACCOUNT_SID`

`AUTH_TOKEN`

Run the project:

```bash
  python ping.py
```





 

