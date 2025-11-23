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
                body {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f8f9fa;}
                .email-container {max-width: 1200px; margin: 0 auto; background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden;}
                .header {background: linear-gradient(135deg, #2E86C1 0%, #3498DB 100%); color: white; padding: 20px 30px; text-align: center;}
                .header h2 {margin: 0; font-size: 28px; font-weight: 700; font-family: 'Nunito', 'Poppins', 'Comfortaa', 'Quicksand', 'Rubik', sans-serif; letter-spacing: 0.5px; border-radius: 50px;}
                .info-section {padding: 20px 30px; background-color: #f8f9fa; border-bottom: 1px solid #e9ecef;}
                .info-section p {margin: 5px 0; color: #6c757d;}
                .table-container {padding: 0; overflow-x: auto;}
                table {width: 100%; border-collapse: collapse; margin: 0;}
                th {background-color: #343a40; color: white; padding: 15px 10px; text-align: center; font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;}
                td {padding: 15px 10px; border-bottom: 1px solid #e9ecef; vertical-align: middle;}
                tr:nth-child(even) {background-color: #f8f9fa;}
                tr:hover {background-color: #e3f2fd; transition: background-color 0.2s ease;}
                img {width: 90px; height: 60px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
                .price {font-weight: bold; color: #27AE60; text-align: right; font-size: 16px;}
                .area, .price-per-sqm {text-align: center; font-weight: 500;}
                .garage-yes {color: #27AE60; font-weight: bold; text-align: center;}
                .garage-no {color: #E74C3C; text-align: center;}
                .parish {font-weight: bold; color: #8E44AD; text-align: center;}
                .flag-new {background-color: #28a745; color: white; font-weight: bold; padding: 6px 12px; border-radius: 20px; font-size: 12px; text-transform: uppercase;}
                .flag-updated {background-color: #ffc107; color: #212529; font-weight: bold; padding: 6px 12px; border-radius: 20px; font-size: 12px; text-transform: uppercase;}
                .status-cell {text-align: center;}
                a {color: #2E86C1; text-decoration: none; font-weight: 500;}
                a:hover {color: #1B4F72; text-decoration: underline;}
                .title-cell {max-width: 250px; word-wrap: break-word;}
                .address-cell {max-width: 200px; word-wrap: break-word; font-size: 13px; color: #6c757d;}
                .footer {padding: 20px 30px; text-align: center; background-color: #f8f9fa; color: #6c757d; font-size: 12px; border-top: 1px solid #e9ecef;}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h2>Novos Anúncios no/a """ + LOCATION_NAME + """</h2>
                </div>
                <div class="info-section">
                    <p><strong>Total de anúncios:</strong> """ + str(updated_df.shape[0]) + """</p>
                    <p><strong>Data:</strong> """ + time + """</p>
                </div>
                <div class="table-container">
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
        
        # Get garage information (check multiple possible fields)
        garage = False
        
        # Check various garage-related fields
        if 'garage' in row and row['garage']:
            garage = True
        elif 'parkingSpace' in row and row['parkingSpace']:
            garage = True
        elif 'hasParkingSpace' in row and row['hasParkingSpace']:
            garage = True
        elif isinstance(row.get('features'), str) and 'parking' in row['features'].lower():
            garage = True
        elif isinstance(row.get('features'), dict) and row['features'].get('hasParkingSpace'):
            garage = True
            
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
                <td class="title-cell"><a href="{property_url}" target="_blank">{title}</a></td>
                <td class="price">{formatted_price}</td>
                <td class="area">{area}</td>
                <td class="price-per-sqm">{formatted_price_per_sqm}</td>
                <td class="{garage_class}">{garage_text}</td>
                <td class="address-cell">{location_info}</td>
                <td class="parish">{parish_name}</td>
                <td class="status-cell"><span class="{flag_class}">{flag_text}</span></td>
            </tr>
        """

    html_content += """
                    </table>
                </div>
                <div class="footer">
                    <p>Idealista Bot - Monitorização Automática de Propriedades</p>
                    <p>Este email foi gerado automaticamente.</p>
                    <p>© 2025 Vítor Narciso. Todos os direitos reservados.</p>
                </div>
            </div>
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