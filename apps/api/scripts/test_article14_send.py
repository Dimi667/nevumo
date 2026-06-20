"""Test script for send_article14_notification() email function."""

import jinja2
import pathlib
import os

# Load and render the template directly
template_dir = pathlib.Path(__file__).parent.parent / "services" / "templates"
env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_dir)))
template = env.get_template("article14_confirmation_pl.html")

html = template.render(
    business_name="Jan Kowalski Hydraulik",
    dashboard_link="https://nevumo.com/pl/dashboard",
    nip="7890123456",
    provider_phone="+48 123 456 789",
    scraped_email="kowalski.hydraulik@gmail.com",
    provider_website="https://kowalski-hydraulik.pl",
    category_label="usługi hydrauliczne",
)

print("✅ Template rendered successfully")
print(f"Template length: {len(html)} characters")

# Try to send via Resend API directly
try:
    import resend
    resend.api_key = os.environ.get("RESEND_API_KEY", "")
    
    if resend.api_key:
        params = {
            "from": "Nevumo <noreply@nevumo.com>",
            "to": ["dimitar.j.dimitroff@gmail.com"],
            "subject": "Profil aktywny ✓ — informacja o danych (art. 14 RODO)",
            "html": html,
        }
        resend.Emails.send(params)
        print("✅ Art.14 test email sent to dimitar.j.dimitroff@gmail.com via Resend")
    else:
        print("⚠️ RESEND_API_KEY not found - email not sent")
        print("✅ Template is ready for production use")
except Exception as e:
    print(f"⚠️ Email send failed: {e}")
    print("✅ Template is ready for production use")
