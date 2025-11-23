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
                body {font-family: Arial, sans-serif; margin: 20px;}
                h2 {color: #2E86C1;}
                table {width: 100%; border-collapse: collapse; margin-top: 20px;}
                th, td {border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top;}
                th {background-color: #f2f2f2; font-weight: bold; text-align: center;}
                img {width: 80px; height: auto; border-radius: 4px;}
                .price {font-weight: bold; color: #27AE60;}
                .garage-yes {color: #27AE60; font-weight: bold;}
                .garage-no {color: #E74C3C;}
                .parish {font-weight: bold; color: #8E44AD;}
                .flag-new {background-color: #D5DBDB; color: #2C3E50; font-weight: bold; padding: 4px 8px; border-radius: 4px;}
                .flag-updated {background-color: #F7DC6F; color: #B7950B; font-weight: bold; padding: 4px 8px; border-radius: 4px;}
                a {color: #2E86C1; text-decoration: none;}
                a:hover {text-decoration: underline;}
            </style>
        </head>
        <body>
            <h2>🏠 Novos Anúncios no/a {LOCATION_NAME}</h2>
            <p><strong>Data:</strong> {time}<br>
            <strong>Total de anúncios:</strong> {updated_df.shape[0]}</p>
            <table>
                <tr>
                    <th>Imagem</th>
                    <th>Título</th>
                    <th>Preço</th>
                    <th>Área</th>
                    <th>Preço/m²</th>
                    <th>Garagem</th>
                    <th>Morada</th>
                    <th>Freguesia</th>
                    <th>Estado</th>
                </tr>
    """

    # Populate the HTML with updated listings
    for index, row in updated_df.iterrows():
        image_url = row['thumbnail'] 
        property_url = row['url']
        address = row['address']
        province = row['province']
        municipality = row['municipality']
        property_type = row['propertyType']
        rooms = row['rooms'] 
        price = row['price']
        area = f"{row['size']} m²"
        price_per_sqm = row['priceByArea']

        formatted_price = f"€ {price:,.2f}"
        formatted_price_per_sqm = f"{price_per_sqm:,.2f} €/m²"
        location_info = f"{address}<br>{municipality}, {province}"  # Format location
        
        # Get garage information (simple True/False)
        garage = row.get('garage', False)
        garage_text = "Sim" if garage else "Não"
        garage_class = "garage-yes" if garage else "garage-no"
        
        # Get parish name (with fallback)
        parish_name = row.get('parish_name', 'N/A')
        
        # Format flag with styling
        flag = row['flag']
        flag_class = f"flag-{flag}" if flag in ['new', 'updated'] else ""
        
        # Translate flag to Portuguese
        flag_text = {
            'new': 'Novo',
            'updated': 'Modificado'
        }.get(flag, flag)

        title = build_title(property_type, rooms, address)

        html_content += f"""
            <tr>
                <td><img src="{image_url}" alt="Property Image"></td>
                <td><a href="{property_url}" target="_blank">{title}</a></td>
                <td class="price">{formatted_price}</td>
                <td>{area}</td>
                <td>{formatted_price_per_sqm}</td>
                <td class="{garage_class}">{garage_text}</td>
                <td>{location_info}</td>
                <td class="parish">{parish_name}</td>
                <td><span class="{flag_class}">{flag_text}</span></td>
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