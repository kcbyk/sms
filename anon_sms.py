import requests
import json
import os
from colorama import Fore, Style

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.

# API key dosyasının yolu
KEY_FILE = os.path.join(os.path.dirname(__file__), "anon_key.txt")


def _key_oku() -> str:
    """Kayıtlı API key'i oku."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    return ""


def _key_kaydet(key: str):
    """API key'i kaydet."""
    with open(KEY_FILE, "w") as f:
        f.write(key.strip())


def anon_sms_gonder(telefon: str, mesaj: str, api_key: str) -> dict:
    """
    TextBelt API ile anonim SMS gonder.
    telefon: +90XXXXXXXXXX formatinda
    """
    try:
        r = requests.post(
            "https://textbelt.com/text",
            data={
                "phone": telefon,
                "message": mesaj,
                "key": api_key
            },
            timeout=15
        )
        data = r.json()
        return {
            "ok": data.get("success", False),
            "quotaRemaining": data.get("quotaRemaining", "?"),
            "textId": data.get("textId", ""),
            "error": data.get("error", "")
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "quotaRemaining": "?"}


def anon_sms_menu(system_fn, sleep_fn):
    """Anonim SMS arayüzü — LegacySMS.py'den çağrılır."""
    from os import system as _sys

    while True:
        _sys("cls||clear")
        print(Fore.LIGHTCYAN_EX + """
+==================================================+
|          ANONIM SMS GONDERI MODULU               |
|                                                  |
|  Istedigin metni istedigin numaraya gonder.      |
|  Gonderen numara gizlenir.                       |
|                                                  |
|  [TextBelt API - textbelt.com]                   |
|  Ucretsiz hesap: 50 SMS/gun                      |
+==================================================+
""" + Style.RESET_ALL)

        api_key = _key_oku()
        if api_key:
            print(Fore.LIGHTGREEN_EX + f"[*] Kayitli API Key: {api_key[:8]}{'*' * (len(api_key)-8)}" + Style.RESET_ALL)
        else:
            print(Fore.LIGHTYELLOW_EX + "[!] API Key bulunamadi." + Style.RESET_ALL)

        print()
        print(Fore.LIGHTWHITE_EX + " 1- SMS Gonder")
        print(" 2- API Key Ayarla")
        print(" 3- Kalan Kota Goruntule")
        print(" 4- Ana Menuye Don" + Style.RESET_ALL)
        print()

        try:
            secim = input(Fore.LIGHTGREEN_EX + " Secim: " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            return

        # ── 1: SMS Gönder ──────────────────────────────────────────
        if secim == "1":
            if not api_key:
                _sys("cls||clear")
                print(Fore.LIGHTRED_EX + "[!] Once API Key ayarlayin (Secim 2)." + Style.RESET_ALL)
                sleep_fn(2)
                continue

            _sys("cls||clear")
            print(Fore.LIGHTWHITE_EX + "Hedef numara (+90 ile): " + Fore.LIGHTGREEN_EX, end="")
            tel = input().strip()

            # Format düzelt
            if tel.startswith("0"):
                tel = "+90" + tel[1:]
            elif tel.startswith("5") and len(tel) == 10:
                tel = "+90" + tel
            elif not tel.startswith("+"):
                tel = "+90" + tel

            print(Fore.LIGHTWHITE_EX + "Mesajini yaz: " + Fore.LIGHTGREEN_EX, end="")
            mesaj = input().strip()

            if not mesaj:
                print(Fore.LIGHTRED_EX + "Bos mesaj gonderilemez!" + Style.RESET_ALL)
                sleep_fn(2)
                continue

            print()
            print(Fore.LIGHTYELLOW_EX + f"[*] Gonderiliyor: {tel}" + Style.RESET_ALL)
            print(Fore.LIGHTYELLOW_EX + f"[*] Mesaj: {mesaj}" + Style.RESET_ALL)
            print()

            sonuc = anon_sms_gonder(tel, mesaj, api_key)

            if sonuc["ok"]:
                print(Fore.LIGHTGREEN_EX + f"[+] SMS GONDERILDI!" + Style.RESET_ALL)
                print(Fore.LIGHTGREEN_EX + f"    Kalan kota: {sonuc['quotaRemaining']} SMS" + Style.RESET_ALL)
                if sonuc.get("textId"):
                    print(Fore.LIGHTGREEN_EX + f"    Mesaj ID   : {sonuc['textId']}" + Style.RESET_ALL)
            else:
                print(Fore.LIGHTRED_EX + f"[-] GONDERILEMEDI: {sonuc.get('error', 'Bilinmeyen hata')}" + Style.RESET_ALL)
                print(Fore.LIGHTRED_EX + f"    Kalan kota : {sonuc['quotaRemaining']}" + Style.RESET_ALL)

            print()
            input(Fore.LIGHTYELLOW_EX + "Devam icin Enter'a basin..." + Style.RESET_ALL)

        # ── 2: API Key Ayarla ───────────────────────────────────────
        elif secim == "2":
            _sys("cls||clear")
            print(Fore.LIGHTCYAN_EX + """
  Ucretsiz API Key nasil alinir?
  --------------------------------
  1. https://textbelt.com adresine git
  2. 'Get API Key' butonuna tikla
  3. E-postanla ucretsiz kaydol
  4. 50 SMS/gun ucretsiz hak alirsin
  --------------------------------
""" + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + "API Key girin: " + Fore.LIGHTGREEN_EX, end="")
            yeni_key = input().strip()
            if yeni_key:
                _key_kaydet(yeni_key)
                print(Fore.LIGHTGREEN_EX + "[+] API Key kaydedildi!" + Style.RESET_ALL)
            else:
                print(Fore.LIGHTRED_EX + "[-] Bos key kabul edilmedi." + Style.RESET_ALL)
            sleep_fn(2)

        # ── 3: Kota Görüntüle ───────────────────────────────────────
        elif secim == "3":
            if not api_key:
                print(Fore.LIGHTRED_EX + "API Key yok!" + Style.RESET_ALL)
                sleep_fn(2)
                continue
            try:
                r = requests.get(
                    f"https://textbelt.com/quota/{api_key}",
                    timeout=10
                )
                data = r.json()
                kalan = data.get("quotaRemaining", "?")
                print()
                if data.get("success"):
                    print(Fore.LIGHTGREEN_EX + f"[+] Kalan SMS kotasi: {kalan}" + Style.RESET_ALL)
                else:
                    print(Fore.LIGHTRED_EX + f"[-] Hata: {data}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.LIGHTRED_EX + f"[-] Baglanti hatasi: {e}" + Style.RESET_ALL)
            print()
            input(Fore.LIGHTYELLOW_EX + "Devam icin Enter'a basin..." + Style.RESET_ALL)

        elif secim == "4":
            return
