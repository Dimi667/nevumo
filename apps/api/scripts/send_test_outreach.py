import resend
import os
from jinja2 import Template
from pathlib import Path

resend.api_key = os.environ["RESEND_API_KEY"]

template_path = Path(__file__).parent / "templates" / "outreach_email_pl.html"
html_template = template_path.read_text(encoding="utf-8")

template = Template(html_template)
html = template.render(
    business_name="ABC Hydraulika Sp. z o.o.",
    service_label="hydraulika",
    claim_link="https://nevumo.com/pl/claim/test-preview",
    provider_phone="+48 123 456 789",
    provider_email="test@abc-hydraulika.pl",
    provider_address="ul. Marszałkowska 1, 00-001 Warszawa",
    provider_website="www.abc-hydraulika.pl",
)

params = {
    "from": "Nevumo <support@nevumo.com>",
    "to": ["dimitar.j.dimitroff@gmail.com"],
    "subject": "5 400 osób szuka hydraulika — ktoś inny je bierze",
    "html": html,
}

response = resend.Emails.send(params)
print(f"Test email sent! ID: {response['id']}")
