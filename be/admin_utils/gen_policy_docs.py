import os
from fpdf import FPDF

# --- Configuration ---
# Directory to save the generated PDF files
COMPANY_NAME = "Digital Harbor"
SUPPORT_EMAIL = "support@digitalharbor.mock"
WEBSITE_URL = "www.digitalharbor.mock"


class PolicyPDF(FPDF):
    """
    Custom PDF class to handle headers and footers for our policy documents.
    """

    def header(self):
        self.set_font('Arial', 'B', 16)
        # Calculate width of title and position
        title_w = self.get_string_width(self.title) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)  # Blue
        self.set_fill_color(230, 230, 230)  # Light Grey
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(title_w, 10, self.title, border=1, ln=1, align='C', fill=1)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        # Company name
        self.cell(0, 10, f'{COMPANY_NAME}', 0, 0, 'R')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body_text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body_text)
        self.ln()

    def add_policy_chapter(self, title, body):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)


def generate_returns_policy(output_dir):
    """Generates the Returns & Refunds Policy PDF."""
    pdf = PolicyPDF()
    pdf.set_title("Returns & Refunds Policy")
    pdf.set_author(COMPANY_NAME)

    # Page 1
    pdf.add_page()
    pdf.chapter_title("Our Commitment to Satisfaction")
    pdf.chapter_body(
        f"At {COMPANY_NAME}, we stand behind the quality of our products and want every purchase to be a positive experience. We hope you love your purchase, but if you are not completely satisfied, we are here to help."
    )

    pdf.chapter_title("30-Day Return Policy")
    pdf.chapter_body(
        "You have 30 calendar days from the date you received your item to initiate a return. To be eligible for a return, your item must be unused, in the same condition that you received it, and in its original packaging with all original tags and accessories included."
    )

    pdf.chapter_title("How to Initiate a Return")
    pdf.chapter_body(
        f"1. Visit our Returns Portal on our website at {WEBSITE_URL}/returns.\n"
        f"2. Enter your order number and the email address used to place the order.\n"
        f"3. Select the item(s) you wish to return and the reason for the return.\n"
        f"4. Once your request is approved, you will receive a confirmation email with a pre-paid shipping label and detailed instructions.\n\n"
        f"If you encounter any issues, please contact our customer support team at {SUPPORT_EMAIL} for assistance."
    )

    # Page 2
    pdf.add_page()
    pdf.chapter_title("Faulty or Damaged Items")
    pdf.chapter_body(
        "If you receive an item that is defective, damaged, or incorrect, please contact our customer support team within 7 days of delivery. We will arrange for a pre-paid return and, upon inspection, will send you a replacement or issue a full refund, including any original shipping costs."
    )

    pdf.chapter_title("Refunds")
    pdf.chapter_body(
        "Once we receive your item, we will inspect it and notify you that we have received your returned item. We will immediately notify you on the status of your refund after inspecting the item.\n\n"
        "If your return is approved, we will initiate a refund to your original method of payment. You will receive the credit within a certain amount of days, depending on your card issuer's policies (typically 5-10 business days)."
    )

    pdf.chapter_title("Non-Returnable Items")
    pdf.chapter_body(
        "Certain items are not eligible for return, including:\n"
        "- Gift cards\n"
        "- Downloadable software products\n"
        "- Some health and personal care items"
    )

    filepath = os.path.join(output_dir, "Returns_Policy.pdf")
    pdf.output(filepath)
    print(f"Successfully generated: {filepath}")


def generate_shipping_policy(output_dir):
    """Generates the Shipping Information PDF."""
    pdf = PolicyPDF()
    pdf.set_title("Shipping Information")
    pdf.set_author(COMPANY_NAME)

    # Page 1
    pdf.add_page()
    pdf.chapter_title("Order Processing Times")
    pdf.chapter_body(
        "All orders are processed within 1-2 business days (excluding weekends and holidays) after you receive your order confirmation email. You will receive another notification when your order has shipped."
    )

    pdf.chapter_title("Domestic Shipping (UK)")
    pdf.chapter_body(
        "We offer the following shipping options within the United Kingdom:\n\n"
        "**Standard Shipping:**\n"
        "- Cost: £4.99 (Free for orders over £50)\n"
        "- Estimated Delivery Time: 3-5 business days\n\n"
        "**Express Shipping:**\n"
        "- Cost: £9.99\n"
        "- Estimated Delivery Time: 1-2 business days"
    )

    # Page 2
    pdf.add_page()
    pdf.chapter_title("International Shipping")
    pdf.chapter_body(
        "We currently ship to countries within the European Union. Shipping charges for your order will be calculated and displayed at checkout.\n\n"
        "Your order may be subject to import duties and taxes (including VAT), which are incurred once a shipment reaches your destination country. {COMPANY_NAME} is not responsible for these charges if they are applied; they are your responsibility as the customer."
    )

    pdf.chapter_title("How to Check Order Status")
    pdf.chapter_body(
        "When your order has shipped, you will receive an email notification from us which will include a tracking number you can use to check its status. Please allow 48 hours for the tracking information to become available.\n\n"
        f"If you haven't received your order within 10 days of receiving your shipping confirmation email, please contact us at {SUPPORT_EMAIL} with your name and order number, and we will look into it for you."
    )

    filepath = os.path.join(output_dir, "Shipping_Information.pdf")
    pdf.output(filepath)
    print(f"Successfully generated: {filepath}")


def generate_faq(output_dir):
    """Generates the Frequently Asked Questions PDF."""
    pdf = PolicyPDF()
    pdf.set_title("Frequently Asked Questions (FAQ)")
    pdf.set_author(COMPANY_NAME)

    # Page 1
    pdf.add_page()
    pdf.chapter_title("ORDERING")
    pdf.chapter_body(
        "**Q: How do I track my order?**\n"
        "A: Once your order ships, you'll receive an email with a tracking number. You can use this number on the carrier's website to see the latest updates on your shipment.\n\n"
        "**Q: What payment methods do you accept?**\n"
        "A: We accept all major credit cards (VISA, MasterCard, American Express) as well as PayPal."
    )

    pdf.chapter_title("PRODUCTS")
    pdf.chapter_body(
        "**Q: The item I want is out of stock. What do I do?**\n"
        "A: You can sign up for 'Back in Stock' notifications on the product page. We'll email you as soon as the item is available again.\n\n"
        "**Q: Do your products come with a warranty?**\n"
        "A: Yes, all our electronic products come with a standard one-year manufacturer's warranty. Please see the product manual for specific warranty details."
    )

    # Page 2
    pdf.add_page()
    pdf.chapter_title("RETURNS & REFUNDS")
    pdf.chapter_body(
        "**Q: What is your return policy?**\n"
        "A: We offer a 30-day return policy for unused items in their original packaging. Please refer to our full 'Returns & Refunds Policy' document for complete details.\n\n"
        "**Q: How long does it take to process a refund?**\n"
        "A: Once we receive and inspect your return, a refund is typically processed within 3-5 business days to your original payment method."
    )

    pdf.chapter_title("ACCOUNT MANAGEMENT")
    pdf.chapter_body(
        "**Q: How do I reset my password?**\n"
        f"A: You can click the 'Forgot Password' link on the login page at {WEBSITE_URL}/account. An email will be sent to you with instructions.\n\n"
        "**Q: How do I update my shipping address?**\n"
        "A: You can update your saved addresses in the 'My Account' section of our website."
    )

    filepath = os.path.join(output_dir, "Frequently_Asked_Questions.pdf")
    pdf.output(filepath)
    print(f"Successfully generated: {filepath}")
