import requests
import os
from colorama import Fore, Style

#Bu Tool "https://github.com/s4m3dnotfound/LegacySMS" adresine aittir.

# API key dosyalari
KEY_FILE_TB  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anon_key_textbelt.txt")
KEY_FILE_S7  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anon_key_sevenio.txt")


def _oku(path):
    return open(path).read().strip() if os.path.exists(path) else ""

def _kaydet(path, key):
    with open(path, "w") as f:
        f.write(key.strip())


# ─────────────────────────────────────────────────────────────────
#  GÖNDERME FONKSİYONLARI
# ─────────────────────────────────────────────────────────────────

def _textbelt_gonder(telefon, mesaj, api_key):
    """TextBelt — 50 SMS/gun ucretsiz hesap, textbelt.com"""
    r = requests.post("https://textbelt.com/text", data={
        "phone": telefon, "message": mesaj, "key": api_key
    }, timeout=15)
    d = r.json()
    return {"ok": d.get("success", False),
            "kota": d.get("quotaRemaining", "?"),
            "hata": d.get("error", "")}


def _sevenio_gonder(telefon, mesaj, api_key):
    """seven.io — 10 SMS ucretsiz, app.seven.io"""
    # seven.io numarayi +90... formatinda istiyor
    r = requests.post("https://gateway.seven.io/api/sms",
        headers={"SentWith": "Python", "X-Api-Key": api_key},
        data={"to": telefon, "from": "LegacySMS", "text": mesaj},
        timeout=15)
    # 100 = basarili, diger = hata
    ok = r.text.strip() == "100"
    return {"ok": ok, "kota": "?", "hata": "" if ok else f"Kod: {r.text.strip()}"}


# ─────────────────────────────────────────────────────────────────
#  ANA MENÜ
# ─────────────────────────────────────────────────────────────────

def anon_sms_menu(system_fn, sleep_fn):
    from os import system as _sys

    while True:
        _sys("cls||clear")

        tb_key = _oku(KEY_FILE_TB)
        s7_key = _oku(KEY_FILE_S7)

        print(Fore.LIGHTCYAN_EX + """
+====================================================+
|           ANONIM SMS GONDERI MODULU                |
|  Istedigin metni, istedigin numaraya gonder.       |
|  Gonderen numara gizlenir.                         |
+====================================================+
""" + Style.RESET_ALL)

        # Kayıtlı key özeti
        if tb_key:
            print(Fore.LIGHTGREEN_EX + f"  TextBelt  : {tb_key[:6]}{'*'*6} [aktif]" + Style.RESET_ALL)
        else:
            print(Fore.LIGHTYELLOW_EX + "  TextBelt  : [key yok]" + Style.RESET_ALL)

        if s7_key:
            print(Fore.LIGHTGREEN_EX + f"  Seven.io  : {s7_key[:6]}{'*'*6} [aktif]" + Style.RESET_ALL)
        else:
            print(Fore.LIGHTYELLOW_EX + "  Seven.io  : [key yok]" + Style.RESET_ALL)

        print()
        print(Fore.LIGHTWHITE_EX +
              " 1- SMS Gonder (TextBelt)\n"
              " 2- SMS Gonder (Seven.io)\n"
              " 3- TextBelt Key Ayarla  [textbelt.com - 50 SMS/gun bedava]\n"
              " 4- Seven.io Key Ayarla  [app.seven.io - 10 SMS bedava]\n"
              " 5- Ana Menuye Don" + Style.RESET_ALL)
        print()

        try:
            secim = input(Fore.LIGHTGREEN_EX + " Secim: " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            return

        # ── SMS Gönder (TextBelt) ────────────────────────────
        if secim == "1":
            if not tb_key:
                print(Fore.LIGHTRED_EX + "[!] Once TextBelt key girin (Secim 3)." + Style.RESET_ALL)
                sleep_fn(2); continue
            tel, mesaj = _tel_mesaj_al(_sys)
            if not tel: continue
            print(Fore.LIGHTYELLOW_EX + "\n[*] Gonderiliyor..." + Style.RESET_ALL)
            sonuc = _textbelt_gonder(tel, mesaj, tb_key)
            _sonuc_yazdir(sonuc)
            input(Fore.LIGHTYELLOW_EX + "\nDevam icin Enter'a basin..." + Style.RESET_ALL)

        # ── SMS Gönder (Seven.io) ────────────────────────────
        elif secim == "2":
            if not s7_key:
                print(Fore.LIGHTRED_EX + "[!] Once Seven.io key girin (Secim 4)." + Style.RESET_ALL)
                sleep_fn(2); continue
            tel, mesaj = _tel_mesaj_al(_sys)
            if not tel: continue
            print(Fore.LIGHTYELLOW_EX + "\n[*] Gonderiliyor..." + Style.RESET_ALL)
            sonuc = _sevenio_gonder(tel, mesaj, s7_key)
            _sonuc_yazdir(sonuc)
            input(Fore.LIGHTYELLOW_EX + "\nDevam icin Enter'a basin..." + Style.RESET_ALL)

        # ── TextBelt Key Ayarla ──────────────────────────────
        elif secim == "3":
            _sys("cls||clear")
            print(Fore.LIGHTCYAN_EX + """
  TextBelt - Ucretsiz API Key nasil alinir?
  ------------------------------------------
  1. https://textbelt.com adresine git
  2. 'Get a free key' butonuna tikla
  3. E-posta gir (kredi karti yok!)
  4. Gunde 50 SMS ucretsiz - Turkiye destekli
  ------------------------------------------
""" + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + "TextBelt API Key: " + Fore.LIGHTGREEN_EX, end="")
            k = input().strip()
            if k:
                _kaydet(KEY_FILE_TB, k)
                print(Fore.LIGHTGREEN_EX + "[+] Kaydedildi!" + Style.RESET_ALL)
            sleep_fn(2)

        # ── Seven.io Key Ayarla ──────────────────────────────
        elif secim == "4":
            _sys("cls||clear")
            print(Fore.LIGHTCYAN_EX + """
  Seven.io - Ucretsiz API Key nasil alinir?
  ------------------------------------------
  1. https://app.seven.io adresine git
  2. 'Register' ile ucretsiz kayit ol
  3. Dashboard'dan 'API Keys' bolumune git
  4. Yeni key olustur - 10 SMS ucretsiz verilir
  5. Kredi karti GEREKMEZ
  ------------------------------------------
""" + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + "Seven.io API Key: " + Fore.LIGHTGREEN_EX, end="")
            k = input().strip()
            if k:
                _kaydet(KEY_FILE_S7, k)
                print(Fore.LIGHTGREEN_EX + "[+] Kaydedildi!" + Style.RESET_ALL)
            sleep_fn(2)

        elif secim == "5":
            return


def _tel_mesaj_al(_sys):
    _sys("cls||clear")
    print(Fore.LIGHTWHITE_EX + "Hedef numara (5XXXXXXXXX): " + Fore.LIGHTGREEN_EX, end="")
    tel = input().strip()
    if tel.startswith("0"): tel = "+90" + tel[1:]
    elif len(tel) == 10 and tel.startswith("5"): tel = "+90" + tel
    elif not tel.startswith("+"): tel = "+90" + tel

    print(Fore.LIGHTWHITE_EX + "Mesajin: " + Fore.LIGHTGREEN_EX, end="")
    mesaj = input().strip()
    if not mesaj:
        print(Fore.LIGHTRED_EX + "Bos mesaj!" + Style.RESET_ALL)
        return None, None
    return tel, mesaj


def _sonuc_yazdir(sonuc):
    if sonuc["ok"]:
        print(Fore.LIGHTGREEN_EX + "\n[+] SMS GONDERILDI!" + Style.RESET_ALL)
        if sonuc["kota"] != "?":
            print(Fore.LIGHTGREEN_EX + f"    Kalan kota: {sonuc['kota']} SMS" + Style.RESET_ALL)
    else:
        print(Fore.LIGHTRED_EX + f"\n[-] GONDERILEMEDI: {sonuc.get('hata', 'Hata')}" + Style.RESET_ALL)
