import os
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from imapclient import imap_utf7


class EmailService:
    def __init__(self):
        self.sender_address = os.getenv('EMAIL_ADDRESS')
        self.sender_app_password = os.getenv('EMAIL_APP_PASSWORD')
        self.sender_smtp_server = os.getenv('EMAIL_SMTP_SERVER')
        self.sender_imap_server = os.getenv('EMAIL_IMAP_SERVER')
        self.sender_smtp_port = int(os.getenv('EMAIL_SMTP_PORT'))
        self.sender_imap_port = int(os.getenv('EMAIL_IMAP_PORT'))

    def send_email(self, receiver_address, subject, text, html):
        message = MIMEMultipart('alternative')
        message['From'] = self.sender_address
        message['To'] = receiver_address
        message['Subject'] = Header(subject, 'utf-8')

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        message.attach(part1)
        message.attach(part2)

        smtp = smtplib.SMTP_SSL(self.sender_smtp_server, self.sender_smtp_port)
        smtp.login(self.sender_address, self.sender_app_password)
        smtp.sendmail(self.sender_address, receiver_address, message.as_string())
        smtp.quit()

        imap = imaplib.IMAP4_SSL(self.sender_imap_server, self.sender_imap_port)
        imap.login(self.sender_address, self.sender_app_password)
        imap.append(
            mailbox=str(imap_utf7.encode('Отправленные'))[2:-1],
            flags=None,
            date_time=None,
            message=message.as_bytes())
        imap.logout()

    @staticmethod
    def get_text_to_verify_email(name: str, url: str) -> str:
        return f"""
        {name}, Вы получили это письмо, 
        так как зарегистрировались в нашем приложении для управления данными о техническом обслуживании автомобилей.

        Для завершения регистрации перейдите по ссылке:
        {url}
        (Ссылка действительна в течение 24 часов)
        
        Если ссылка не кликабельна, скопируйте ее и вставьте в адресную строку браузера.
        
        Если Вы не регистрировались в приложении, проигнорируйте это письмо.
        """

    @staticmethod
    def get_html_to_verify_email(name: str, url: str) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="
                width: 80%;
                margin: 0 auto; 
                font-family: Times New Roman, sans-serif;
                line-height: 1.6;
        ">
            <p style="color: #000000 !important; font-size: 16pt;">
                <strong>{name}</strong>, Вы получили это письмо, так как зарегистрировались в нашем приложении 
                для управления данными о техническом обслуживании автомобилей.
            </p>            
            <p style="color: #000000 !important; font-size: 16pt; margin-bottom: 0px">
                Для завершения регистрации подтвердите Ваш email:
            </p>
            <a
                href="{url}"
                style="
                    display: inline-block;
                    background-color: #4430E0B2;
                    color: #FFFFFF !important;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 18pt;
                    padding: 10px;
                    margin-top: 5px;
                "
            >
                Подтвердить email
            </a>
            <p style="color: #000000 !important; font-size: 14pt; margin-top: 0px;">
                <em>Кнопка активна в течение 24 часов</em>
            </p>
            <p style="color: #000000 !important; font-size: 16pt; margin-bottom: 0px">
                Если кнопка не работает, скопируйте ссылку и вставьте ее в адресную строку браузера:
            </p>
            <a style="font-size: 16pt;" href="{url}">{url}</a>

            <p style="color: #000000 !important; font-size: 14pt;">
                <em>Если письмо пришло Вам по ошибке, проигнорируйте его.</em>
            </p>
        </body>
        </html>
        """

    @staticmethod
    def get_text_to_invite_worker(name: str, commercial_name: str, position: str, url: str) -> str:
        return f"""           
        Здравствуйте, {name}!  
        
        Вас приглашают в команду автосервиса «{commercial_name}» на должность «{position}».  

        Для присоединения перейдите по ссылке: 
        {url} 
        (Ссылка действительна в течение 24 часов) 
        
        Если ссылка не кликабельна, скопируйте ее и вставьте в адресную строку браузера.
        
        Если письмо пришло Вам по ошибке, проигнорируйте его.  
        """

    @staticmethod
    def get_html_to_invite_worker(name: str, commercial_name: str, position: str, url: str) -> str:
        return f""" 
         <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body style="
                width: 80%;
                margin: 0 auto; 
                font-family: Times New Roman, sans-serif;
                line-height: 1.6;
            ">
                <p style="color: #000000 !important; font-size: 16pt;">
                    Здравствуйте, <strong>{name}</strong>!  
                    
                    <br>Вас приглашают в команду автосервиса <strong>{commercial_name}</strong> 
                    на должность <strong>{position}</strong>.
                </p>
                <a
                    href="{url}"
                    style="
                        display: inline-block;
                        background-color: #4430E0B2;
                        color: #FFFFFF !important;
                        text-decoration: none;
                        border-radius: 4px;
                        font-weight: bold;
                        font-size: 18pt;
                        padding: 10px;
                        margin-top: 5px;
                    "
                >
                    Принять приглашение
                </a>
                <p style="color: #000000 !important; font-size: 14pt; margin-top: 0px;">
                    <em>Кнопка активна в течение 24 часов</em>
                </p>
                <p style="color: #000000 !important; font-size: 16pt; margin-bottom: 0px">
                    Если кнопка не работает, скопируйте ссылку и вставьте ее в адресную строку браузера:
                </p>
                <a style="font-size: 16pt;" href="{url}">{url}</a>

                <p style="color: #000000 !important; font-size: 14pt;">
                    <em>Если письмо пришло Вам по ошибке, проигнорируйте его.</em>
                </p>
            </body>
            </html>     
            """

    @staticmethod
    def get_text_to_invite_client(name: str, commercial_name: str, url: str) -> str:
        return f"""
        Здравствуйте, {name}!

        Вас приглашают стать клиентом автосервиса «{commercial_name}».

        Для подтверждения перейдите по ссылке:
        {url}
        (Ссылка действительна в течение 24 часов)

        Если ссылка не кликабельна, скопируйте ее и вставьте в адресную строку браузера.

        Если письмо пришло Вам по ошибке, проигнорируйте его.
        """

    @staticmethod
    def get_html_to_invite_client(name: str, commercial_name: str, url: str) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="
                width: 80%;
                margin: 0 auto; 
                font-family: Times New Roman, sans-serif;
                line-height: 1.6;
            ">
            <p style="color: #000000 !important; font-size: 16pt;">
                Здравствуйте, <strong>{name}</strong>!

                <br>Вас приглашают стать клиентом автосервиса <strong>{commercial_name}</strong>.
            </p>
            <a
                href="{url}"
                style="
                    display: inline-block;
                    background-color: #4430E0B2;
                    color: #FFFFFF !important;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 18pt;
                    padding: 10px;
                    margin-top: 5px;
                "
            >
                Принять приглашение
            </a>
            <p style="color: #000000 !important; font-size: 14pt; margin-top: 0px;">
                <em>Кнопка активна в течение 24 часов</em>
            </p>
            <p style="color: #000000 !important; font-size: 16pt; margin-bottom: 0px">
                Если кнопка не работает, скопируйте ссылку и вставьте ее в адресную строку браузера:
            </p>
            <a style="font-size: 16pt;" href="{url}">{url}</a>

            <p style="color: #000000 !important; font-size: 14pt;">
                <em>Если письмо пришло Вам по ошибке, проигнорируйте его.</em>
            </p>
        </body>
        </html>
        """

    @staticmethod
    def get_text_to_init_vehicle_transfer(
            name: str, make: str, model: str, registration_plate: str, url: str
    ) -> str:
        return f"""
        Здравствуйте, {name}!

        Вам хотят передать историю технического обслуживания автомобиля {make} {model} 
        с регистрационным знаком {registration_plate}.

        Для подтверждения передачи истории перейдите по ссылке:
        {url}
        (Ссылка действительна в течение 24 часов)

        Если ссылка не кликабельна, скопируйте ее и вставьте в адресную строку браузера.

        Если письмо пришло Вам по ошибке, проигнорируйте его.
        """

    @staticmethod
    def get_html_to_init_vehicle_transfer(
            name: str, make: str, model: str, registration_plate: str, url: str
    ) -> str:
        return f"""
        <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body style="
                width: 80%;
                margin: 0 auto; 
                font-family: Times New Roman, sans-serif;
                line-height: 1.6;
            ">
                <p style="color: #000000 !important; font-size: 16pt;"> 
                    Здравствуйте, <strong>{name}</strong>!

                    <br>
                    Вам хотят передать историю технического обслуживания автомобиля <strong>{make} {model}</strong>
                    с регистрационным знаком <strong>{registration_plate}</strong>.
                </p>
                <a
                    href="{url}"
                    style="
                        display: inline-block;
                        background-color: #4430E0B2;
                        color: #FFFFFF !important;
                        text-decoration: none;
                        border-radius: 4px;
                        font-weight: bold;
                        font-size: 18pt;
                        padding: 10px;
                        margin-top: 5px;
                    "
                >
                    Подтвердить передачу истории
                </a>
                <p style="color: #000000 !important; font-size: 14pt; margin-top: 0px;">
                    <em>Кнопка активна в течение 24 часов</em>
                </p>
                <p style="color: #000000 !important; font-size: 16pt; margin-bottom: 0px">
                    Если кнопка не работает, скопируйте ссылку и вставьте ее в адресную строку браузера:
                </p>
                <a style="font-size: 16pt;" href="{url}">{url}</a>

                <p style="color: #000000 !important; font-size: 14pt;">
                    <em>Если письмо пришло Вам по ошибке, проигнорируйте его.</em>
                </p>
            </body>
            </html>
            """
