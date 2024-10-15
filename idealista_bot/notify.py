from .config import LOCATION_NAME, SENDER_EMAIL, SENDER_APP_PASSWORD, RECIPIENT_EMAIL_ONE, RECIPIENT_EMAIL_TWO, RECIPIENT_EMAIL_THREE
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas as pd
import locale



recipients = [RECIPIENT_EMAIL_ONE, RECIPIENT_EMAIL_TWO, RECIPIENT_EMAIL_THREE]


locale.setlocale(locale.LC_ALL, 'pt_PT.UTF-8')  # Make sure this locale is available on your system



def format_price(price):
    # Format price as a string in euros
    formatted_price = locale.currency(price, grouping=True, symbol=True)
    return formatted_price


def build_title(property_type, rooms, address):
    # Translate property types
    if property_type == 'flat':
        translated_type = "Apartamento"
        prefix = "T"  # For 'T' (number of rooms) in flats
    elif property_type == 'chalet':
        translated_type = "Moradia"
        prefix = "V"  # For 'V' (number of rooms) in chalets
    else:
        translated_type = "Propriedade"
        prefix = "T"  # No prefix for unknown property types

    # Build the title string
    if rooms:
        title = f"{translated_type} {prefix}{rooms} no/a {address}"
    else:
        title = f"{translated_type} no/a {address}"  # If no room info is available

    return title



def send_email(updated_df, time):

    subject = "[Idealista Bot] " + str(updated_df.shape[0]) + f" Novos Anúncios no/a {LOCATION_NAME} ({time})"

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(recipients)

    # HTML Email Body
    html_content = """
    <html>
        <head>
            <style>
                body {font-family: Arial, sans-serif;}
                h2 {color: #2E86C1;}
                table {width: 100%; border-collapse: collapse;}
                th, td {border: 1px solid #ddd; padding: 8px;}
                th {background-color: #f2f2f2;}
                img {width: 100px; height: auto;}
            </style>
        </head>
        <body>
            <table>
                <tr>
                    <th>Imagem</th>
                    <th>Título</th>
                    <th>Preço</th>
                    <th>Morada</th>
                    <th>Estado</th>
                </tr>
    """

    # Populate the HTML with updated listings
    for index, row in updated_df.iterrows():
        image_url = row['thumbnail'] 
        property_url = row['url']  # Assuming there is a 'url' column in updated_df
        address = row['address']  # Assuming there is an 'address' column
        province = row['province']  # Assuming there is a 'province' column
        municipality = row['municipality']  # Assuming there is a 'municipality' column
        property_type = row['propertyType']  # Assuming there is a 'propertyType' column
        rooms = row.get('rooms')  # Assuming there is a 'rooms' column
        price = format_price(float(row['price']))

        location_info = f"{address}<br>{municipality}, {province}"  # Format location

        title = build_title(property_type, rooms, address)

        html_content += f"""
            <tr>
                <td><img src="{image_url}" alt="Property Image"></td>
                <td><a href="{property_url}" target="_blank">{title}</a></td>
                <td>{price}</td>
                <td>{location_info}</td>
                <td>{row['flag']}</td>
            </tr>
        """

    html_content += """
            </table>
        </body>
    </html>
    """

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Usage example
# updated_df = ... # Your updated DataFrame with property data
# send_email(updated_df, ['recipient1@example.com', 'recipient2@example.com'])

# from fetch_listings import daily_fetch

# updated_df = daily_fetch()
# send_email(updated_df)