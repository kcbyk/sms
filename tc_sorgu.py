import requests
from colorama import Fore, Style

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.

# ─────────────────────────────────────────
#  TC KİMLİK DOĞRULAMA - tc_sorgu.py
# ─────────────────────────────────────────

def tc_format_kontrol(tc: str) -> bool:
    """TC kimlik numarasının matematiksel olarak geçerli olup olmadığını kontrol eder."""
    if not tc.isdigit() or len(tc) != 11 or tc[0] == '0':
        return False
    rakamlari = [int(c) for c in tc]
    tek  = rakamlari[0]+rakamlari[2]+rakamlari[4]+rakamlari[6]+rakamlari[8]
    cift = rakamlari[1]+rakamlari[3]+rakamlari[5]+rakamlari[7]
    if (tek*7 - cift) % 10 != rakamlari[9]:
        return False
    if sum(rakamlari[:10]) % 10 != rakamlari[10]:
        return False
    return True


def tc_dogrula_nvi(tc: str, ad: str, soyad: str, dogum_yili: int) -> dict:
    """
    T.C. NVI (Nüfus ve Vatandaşlık İşleri) KPS SOAP servisi üzerinden
    TC + Ad + Soyad + Doğum Yılı kombinasyonunu doğrular.
    """
    soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
      <TCKimlikNo>{tc}</TCKimlikNo>
      <Ad>{ad.upper()}</Ad>
      <Soyad>{soyad.upper()}</Soyad>
      <DogumYili>{dogum_yili}</DogumYili>
    </TCKimlikNoDogrula>
  </soap:Body>
</soap:Envelope>"""

    try:
        r = requests.post(
            "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx",
            data=soap_body.encode("utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://tckimlik.nvi.gov.tr/WS/TCKimlikNoDogrula",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            },
            timeout=10,
            verify=False  # NVI bazen SSL sorunu yaratır
        )
        if "true" in r.text.lower():
            return {"durum": True,  "mesaj": "TC kimlik bilgileri ESLESTIRILDI"}
        elif "false" in r.text.lower():
            return {"durum": False, "mesaj": "TC kimlik bilgileri ESLESMEDI"}
        else:
            return {"durum": None, "mesaj": f"Sunucu yaniti anlasilamadi: {r.text[:100]}"}
    except requests.exceptions.Timeout:
        return {"durum": None, "mesaj": "NVI sunucusu zaman asimina ugradi"}
    except Exception as e:
        return {"durum": None, "mesaj": f"Baglanti hatasi: {type(e).__name__}"}


def toplu_tc_kontrol(tc_listesi: list) -> None:
    """Birden fazla TC'nin format geçerliliğini kontrol eder."""
    gecerli = [tc for tc in tc_listesi if tc_format_kontrol(tc)]
    gecersiz = [tc for tc in tc_listesi if not tc_format_kontrol(tc)]
    print(f"\n{Fore.LIGHTGREEN_EX}Gecerli TC sayisi  : {len(gecerli)}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}Gecersiz TC sayisi : {len(gecersiz)}{Style.RESET_ALL}")
    if gecerli:
        print(f"\n{Fore.LIGHTWHITE_EX}Gecerli TC'ler:{Style.RESET_ALL}")
        for tc in gecerli:
            print(f"  {Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} {tc}")
    if gecersiz:
        print(f"\n{Fore.LIGHTWHITE_EX}Gecersiz TC'ler:{Style.RESET_ALL}")
        for tc in gecersiz:
            print(f"  {Fore.LIGHTRED_EX}[-]{Style.RESET_ALL} {tc}")


def tc_sorgu_menu(system_fn, sleep_fn):
    """TC sorgu arayüzü — LegacySMS.py'den çağrılır."""
    from os import system as _sys

    while True:
        _sys("cls||clear")
        print(Fore.LIGHTCYAN_EX + """
+--------------------------------------------------+
|           TC KIMLIK SORGU MODULU                 |
|                                                  |
|  1- TC Format Kontrolu (tek numara)              |
|  2- TC Dogrulama (Ad + Soyad + Dogum Yili)       |
|  3- Toplu TC Format Kontrolu (dosyadan)          |
|  4- Ana Menuye Don                               |
+--------------------------------------------------+
""" + Style.RESET_ALL, end="")

        try:
            secim = input(Fore.LIGHTGREEN_EX + " Secim: " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            return

        # ── 1: Tek TC Format Kontrolü ──
        if secim == "1":
            _sys("cls||clear")
            print(Fore.LIGHTWHITE_EX + "TC Kimlik Numarasini girin: " + Fore.LIGHTGREEN_EX, end="")
            tc = input().strip()
            print()
            if tc_format_kontrol(tc):
                print(Fore.LIGHTGREEN_EX + f"[+] {tc} --> GECERLI TC numarasi" + Style.RESET_ALL)
            else:
                print(Fore.LIGHTRED_EX + f"[-] {tc} --> GECERSIZ TC numarasi" + Style.RESET_ALL)
            print()
            input(Fore.LIGHTYELLOW_EX + "Devam icin Enter'a basin..." + Style.RESET_ALL)

        # ── 2: NVI Doğrulama ──
        elif secim == "2":
            _sys("cls||clear")
            print(Fore.LIGHTWHITE_EX + "TC Kimlik No   : " + Fore.LIGHTGREEN_EX, end=""); tc = input().strip()
            print(Fore.LIGHTWHITE_EX + "Ad             : " + Fore.LIGHTGREEN_EX, end=""); ad = input().strip()
            print(Fore.LIGHTWHITE_EX + "Soyad          : " + Fore.LIGHTGREEN_EX, end=""); soyad = input().strip()
            print(Fore.LIGHTWHITE_EX + "Dogum Yili     : " + Fore.LIGHTGREEN_EX, end="")
            try:
                yil = int(input().strip())
            except ValueError:
                print(Fore.LIGHTRED_EX + "Gecersiz yil!" + Style.RESET_ALL)
                sleep_fn(2)
                continue

            if not tc_format_kontrol(tc):
                print(Fore.LIGHTRED_EX + "\n[-] TC numarasi matematiksel olarak GECERSIZ, sorgu yapilmiyor." + Style.RESET_ALL)
                sleep_fn(3)
                continue

            print(Fore.LIGHTYELLOW_EX + "\n[*] NVI sunucusuna sorgu gonderiliyor..." + Style.RESET_ALL)
            sonuc = tc_dogrula_nvi(tc, ad, soyad, yil)

            print()
            if sonuc["durum"] is True:
                print(Fore.LIGHTGREEN_EX + f"[+] {sonuc['mesaj']}" + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX + f"    TC: {tc}  |  Ad: {ad}  |  Soyad: {soyad}  |  Yil: {yil}" + Style.RESET_ALL)
            elif sonuc["durum"] is False:
                print(Fore.LIGHTRED_EX + f"[-] {sonuc['mesaj']}" + Style.RESET_ALL)
            else:
                print(Fore.LIGHTYELLOW_EX + f"[!] {sonuc['mesaj']}" + Style.RESET_ALL)

            print()
            input(Fore.LIGHTYELLOW_EX + "Devam icin Enter'a basin..." + Style.RESET_ALL)

        # ── 3: Toplu TC Format Kontrolü ──
        elif secim == "3":
            _sys("cls||clear")
            print(Fore.LIGHTWHITE_EX + "TC listesinin dosya yolunu girin: " + Fore.LIGHTGREEN_EX, end="")
            yol = input().strip()
            try:
                with open(yol, "r", encoding="utf-8") as f:
                    tc_listesi = [line.strip() for line in f if line.strip()]
                print(Fore.LIGHTYELLOW_EX + f"\n[*] {len(tc_listesi)} adet TC kontrol ediliyor..." + Style.RESET_ALL)
                toplu_tc_kontrol(tc_listesi)
            except FileNotFoundError:
                print(Fore.LIGHTRED_EX + "Dosya bulunamadi!" + Style.RESET_ALL)
                sleep_fn(2)
                continue
            print()
            input(Fore.LIGHTYELLOW_EX + "Devam icin Enter'a basin..." + Style.RESET_ALL)

        elif secim == "4":
            return
