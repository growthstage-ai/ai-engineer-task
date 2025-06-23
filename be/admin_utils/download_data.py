import os
import requests
import time

from admin_utils.gen_policy_docs import generate_faq, generate_returns_policy, generate_shipping_policy

# --- Configuration ---
# Directory to save the downloaded PDF files
DOWNLOAD_DIR = "pdfs"

# List of URLs to download. Each tuple contains:
# (Product Name, URL, Desired Filename)
# Note: Some URLs point to web pages. These will be flagged for manual download.
PDF_LINKS = [
    # Direct PDF Links
    ("Sony WH-1000XM5 Headphones", "https://helpguide.sony.net/mdr/wh1000xm5/v1/en/print.pdf",
     "Sony_WH-1000XM5_Manual.pdf"),
    ("Bose QuietComfort Ultra Headphones", "https://assets.bose.com/content/dam/Bose_DAM/Web/consumer_electronics/global/products/headphones/QCUH-HEADPHONEARN/pdf/884885_OG_QCUH-HEADPHONEARN_en.pdf", "Bose_QC_Ultra_Headphones_Manual.pdf"),
    ("Sennheiser Momentum 4 Wireless", "https://media.graphassets.com/CJdvxcJRTVROai9rHI3r",
     "Sennheiser_Momentum_4_Manual.pdf"),
    ("JBL Charge 5 Speaker", "https://www.jbl.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dwfbb17c7b/pdfs/PA_JBL_Charge%205%20Wi-Fi_QSG_Global.pdf", "JBL_Charge_5_QSG.pdf"),
    ("Sony Alpha a7 IV", "https://helpguide.sony.net/ilc/2110/v1/en/print.pdf",
     "Sony_a7_IV_Manual.pdf"),
    ("Fujifilm X-T5", "https://fujifilm-dsc.com/en-int/manual/x-t5/x-t5_manual_en_s_f.pdf",
     "Fujifilm_XT5_Manual.pdf"),
    ("Samsung Galaxy S24 Ultra", "https://www.galaxys24manual.com/wp-content/uploads/pdf/galaxy-s24-manual-SAM-S921-S926-S928-OS14-011824-FINAL-US-English.pdf",
     "Samsung_Galaxy_S24_Ultra_Manual.pdf"),
    ("Dell XPS 15 Laptop", "https://dl.dell.com/content/manual13137258-xps-15-9530-service-manual.pdf?language=en-us",
     "Dell_XPS_15_Service_Manual.pdf"),
    ("Sony PlayStation 5", "https://www.playstation.com/content/dam/global_pdc/en/corporate/support/manuals/ps5-docs/1000a/MEA_EN_PS5_Disc_Web_Quick_Start_Guide_ENGMEA_7033912.pdf",
     "Sony_PlayStation_5_Safety_Guide.pdf"),
    ("DJI Mini 4 Pro Drone", "https://dl.djicdn.com/downloads/DJI_Mini_4_Pro/DJI_Mini_4_Pro_User_Manual_EN.pdf",
     "DJI_Mini_4_Pro_Manual.pdf"),
    ("Garmin Fenix 7", "https://www8.garmin.com/manuals/webhelp/GUID-C001C335-A8EC-4A41-AB0E-BAC434259F92/EN-US/fenix_7_Series_OM_EN-US.pdf", "Garmin_Fenix_7_Manual.pdf")
]


def download_pdfs():
    """
    Downloads PDFs from a list of URLs into a specified directory.
    Handles web pages by printing instructions for manual download.
    """

    manual_downloads = []
    failed_downloads = []

    print("\nStarting PDF download process...")
    for name, url, filename in PDF_LINKS:
        # Check if the URL is likely a direct PDF link
        if url.endswith('.pdf') or 'print.pdf' in url:
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            # Skip if file already exists
            if os.path.exists(filepath):
                print(f"SKIPPING '{filename}' (already exists).")
                continue

            print(f"Downloading '{name}'...")
            try:
                # Use a user-agent to avoid being blocked
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                response = requests.get(
                    url, headers=headers, stream=True, timeout=30)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

                # Write the content to a file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f" -> Saved as '{filename}'")

                # Be a good citizen and wait a moment between requests
                time.sleep(1)

            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response else "N/A"
                reason = e.response.reason if e.response else str(e)
                print(
                    f" -> ERROR: Failed to download {name}. HTTP {status_code} {reason}")
                failed_downloads.append(
                    (name, url, filename, f"HTTP {status_code} {reason}"))
            except requests.exceptions.RequestException as e:
                print(f" -> ERROR: Failed to download {name}. Reason: {e}")
                failed_downloads.append((name, url, filename, str(e)))
        else:
            # If it's not a direct PDF link, add to the manual download list
            manual_downloads.append((name, url, filename))

    # Print summary and instructions for manual downloads
    print("\n--- Download Complete ---")
    if manual_downloads:
        print("\nACTION REQUIRED: The following guides are web pages and must be saved manually:")
        for name, url, filename in manual_downloads:
            print(f"\n- Product: {name}")
            print(f"  Filename: {filename}")
            print(f"  URL: {url}")
            print(
                f"  Instructions: Open the URL in your browser, go to File -> Print, and select 'Save as PDF'.")
    else:
        print("All documents were downloaded successfully.")

    # Print summary of failed downloads
    if failed_downloads:
        print("\n--- Failed Downloads Summary ---")
        for name, url, filename, reason in failed_downloads:
            print(f"\n- Product: {name}")
            print(f"  Filename: {filename}")
            print(f"  URL: {url}")
            print(f"  Error: {reason}")
        print("\nPlease check the above errors. Some files may need manual download or updated URLs.")


if __name__ == "__main__":

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        print(f"Created directory: '{DOWNLOAD_DIR}'")

    download_pdfs()

    print("Generating policy documents...")
    generate_returns_policy(DOWNLOAD_DIR)
    generate_shipping_policy(DOWNLOAD_DIR)
    generate_faq(DOWNLOAD_DIR)
    print("\nAll policy documents generated successfully.")
