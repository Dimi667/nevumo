"""
One-time test script — sends Polish outreach email to 2 test addresses.
Run: railway run python3.13 -m apps.api.scripts.test_outreach_send
"""

import os
from pathlib import Path
from jinja2 import Template
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

TEMPLATE_PATH = Path(__file__).parent / "templates" / "outreach_email_pl.html"

TEST_DATA = {
    "business_name": "Usługi Sprzątające Jan Kowalski",
    "claim_link": "https://nevumo.com/pl/claim/test-00000000-0000-0000-0000-000000000001",
    "provider_phone": "+48 123 456 789",
    "provider_email": "jan.kowalski@example.com",
    "provider_address": "ul. Marszałkowska 12, 00-590 Warszawa",
    "provider_website": "www.sprzatanie-kowalski.pl",
}

TEST_RECIPIENTS = [
    "neli.b.bojilova@gmail.com",
    "dimitar.j.dimitroff@gmail.com",
]

SUBJECT = "7 000 osób szuka sprzątania — ktoś inny je bierze"


def main() -> None:
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    html = Template(template_text).render(**TEST_DATA)

    for email in TEST_RECIPIENTS:
        result = resend.Emails.send({
            "from": "Nevumo <support@nevumo.com>",
            "to": email,
            "subject": SUBJECT,
            "html": html,
        })
        print(f"✅ Sent to {email}: {result}")


if __name__ == "__main__":
    main()
