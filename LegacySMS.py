from colorama import Fore, Style
from time import sleep
from os import system
from sms_api import SendSms
from whatsapp_api import WhatsAppSpam
import threading
import inspect

# --- Başlangıç Bilgilendirme Ekranı ---
system("cls||clear")
print(Fore.LIGHTGREEN_EX + """                   
**************************************************
*               LegacySMS v2 - 2026              *
*      Bu program tamamen egitim amaclidir.      *
*      Tum sorumluluklar kullaniciya aittir.     *
*    Program 10 saniye sonra baslayacaktir...    *
**************************************************
""" + Style.RESET_ALL)

for i in range(10, 0, -1):
    print(Fore.LIGHTGREEN_EX + f"\rBasliyor: {i} saniye ", end="", flush=True)
    sleep(1)
print("\n")

# Servis listelerini yukle
servisler_sms = [
    name for name, method in inspect.getmembers(SendSms, predicate=inspect.isfunction)
    if not name.startswith("_")
]
servisler_wa = [
    name for name, method in inspect.getmembers(WhatsAppSpam, predicate=inspect.isfunction)
    if not name.startswith("_")
]

print(Fore.LIGHTCYAN_EX + f"[i] SMS: {len(servisler_sms)} servis | WhatsApp: {len(servisler_wa)} servis yuklendi." + Style.RESET_ALL)
sleep(2)

# Bu Tool https://github.com/s4m3dnotfound/LegacySMS Adresine Aittir...

# ─────────────────────────────────────────────
#  YARDIMCI FONKSİYONLAR
# ─────────────────────────────────────────────
def _tel_al(prompt="Numarayi yaziniz (basa '0' eklemeden): "):
    """Telefon numarası al ve doğrula. Liste döndürür."""
    system("cls||clear")
    print(Fore.LIGHTWHITE_EX + prompt + Fore.LIGHTGREEN_EX, end="")
    tel_no = input().strip()
    tel_liste = []

    if tel_no == "":
        system("cls||clear")
        print(Fore.LIGHTWHITE_EX + "Numaralarin bulundugu dosya yolunu gir: " + Fore.LIGHTGREEN_EX, end="")
        dizin = input().strip()
        try:
            with open(dizin, "r", encoding="utf-8") as f:
                for line in f.read().strip().split("\n"):
                    line = line.strip()
                    if len(line) == 10 and line.isdigit():
                        tel_liste.append(line)
        except FileNotFoundError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Dosya bulunamadi!")
            sleep(3)
            return None
    else:
        if not tel_no.isdigit() or len(tel_no) != 10:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Gecersiz numara. 10 haneli ve sadece rakam olmali.")
            sleep(3)
            return None
        tel_liste.append(tel_no)

    return tel_liste


def _kere_al():
    system("cls||clear")
    print(Fore.LIGHTWHITE_EX + "Kac adet? [sonsuz icin Enter]: " + Fore.LIGHTGREEN_EX, end="")
    kere_str = input().strip()
    try:
        return int(kere_str) if kere_str else None
    except ValueError:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Hatali sayi.")
        sleep(3)
        return -1  # hata sinyali


def _aralik_al():
    system("cls||clear")
    print(Fore.LIGHTWHITE_EX + "Bekleme suresi (saniye) [0 = araliksiz]: " + Fore.LIGHTGREEN_EX, end="")
    try:
        return int(input().strip() or "0")
    except ValueError:
        return 0


# ─────────────────────────────────────────────
#  SMS GÖNDERİM
# ─────────────────────────────────────────────
def _servisleri_gonder(sms_obj, aralik, kere=None):
    while True:
        for servis_adi in servisler_sms:
            if kere is not None and sms_obj.adet >= kere:
                return
            try:
                getattr(sms_obj, servis_adi)()
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[!] {servis_adi} cagirilamadi: {e}{Style.RESET_ALL}")
            if aralik > 0:
                sleep(aralik)
        if kere is not None and sms_obj.adet >= kere:
            return


# ─────────────────────────────────────────────
#  ANA MENÜ
# ─────────────────────────────────────────────
while True:
    system("cls||clear")

    print(Fore.LIGHTGREEN_EX + r"""
     _                                ____  __  __ ____    ____   ___ ____   __   
    | |    ___  __ _  __ _  ___ _   _/ ___||  \/  / ___|  |___ \ / _ \___ \ / /_  
    | |   / _ \/ _` |/ _` |/ __| | | \___ \| |\/| \___ \    __) | | | |__) | '_ \ 
    | |__|  __/ (_| | (_| | (__| |_| |___) | |  | |___) |  / __/| |_| / __/| (_) |
    |_____\___|__, |\__,_|\___|__, |____/|_|  |_|____/  |_____|\___|_____|\___ / 
               |___/           |___/                                             
""" + Style.RESET_ALL)

    print(
        f"{Fore.LIGHTGREEN_EX}UYARI: Tamamen Egitim Amaclidir.{Style.RESET_ALL}    "
        f"{Fore.LIGHTBLUE_EX}Gelistirici:{Style.RESET_ALL} s4m3dnotfound    "
        f"{Fore.LIGHTRED_EX}Surum:{Style.RESET_ALL} LegacySMS v2    "
        f"{Fore.LIGHTCYAN_EX}SMS:{len(servisler_sms)} | WA:{len(servisler_wa)}{Style.RESET_ALL}"
    )
    print()

    try:
        menu = input(
            Fore.LIGHTWHITE_EX +
            " 1- SMS Gonder\n\n"
            " 2- WhatsApp Spam\n\n"
            " 3- Cikis\n\n" +
            Fore.LIGHTGREEN_EX + " Secim: "
        )
        if menu == "":
            continue
        menu = int(menu)
    except ValueError:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Hatali islem. Lutfen Tekrar dene.")
        sleep(3)
        continue

    # ── SEÇENEK 1: SMS ──────────────────────────────────────────────
    if menu == 1:
        tel_liste = _tel_al("SMS gonderilecek numarayi yaziniz (basa '0' eklemeden): ")
        if not tel_liste:
            continue

        system("cls||clear")
        print(Fore.LIGHTWHITE_EX + "E-posta (rastgele icin bos birak): " + Fore.LIGHTGREEN_EX, end="")
        mail = input().strip()
        if mail and ("@" not in mail or "." not in mail.split("@")[-1]):
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Gecersiz e-posta.")
            sleep(3)
            continue

        kere = _kere_al()
        if kere == -1:
            continue
        aralik = _aralik_al()

        system("cls||clear")
        print(Fore.LIGHTCYAN_EX + f"[*] {len(tel_liste)} numara icin SMS bombardimani baslatiliyor..." + Style.RESET_ALL)

        threads = []
        for numara in tel_liste:
            sms = SendSms(numara, mail)
            t = threading.Thread(target=_servisleri_gonder, args=(sms, aralik, kere), daemon=True)
            threads.append(t)
            t.start()

        try:
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            print(Fore.LIGHTYELLOW_EX + "\n[!] Iptal edildi." + Style.RESET_ALL)

        print(Fore.LIGHTRED_EX + "\nAna ekrana donmek icin 'Enter' tusuna bas")
        input()

    # ── SEÇENEK 2: WHATSAPP SPAM ───────────────────────────────────
    elif menu == 2:
        tel_liste = _tel_al("WA Spam numarasini yaziniz (basa '0' eklemeden): ")
        if not tel_liste:
            continue

        kere = _kere_al()
        if kere == -1:
            continue
        aralik = _aralik_al()

        system("cls||clear")
        print(Fore.LIGHTGREEN_EX + "[*] WhatsApp spam baslatiliyor..." + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + "[!] Durdurmak icin Ctrl+C\n" + Style.RESET_ALL)

        def _wa_gonder(wa_obj, aralik, kere):
            while True:
                for servis_adi in servisler_wa:
                    if kere is not None and wa_obj.adet >= kere:
                        return
                    try:
                        getattr(wa_obj, servis_adi)()
                    except Exception as e:
                        pass
                    if aralik > 0:
                        sleep(aralik)
                if kere is not None and wa_obj.adet >= kere:
                    return

        threads = []
        for numara in tel_liste:
            wa = WhatsAppSpam(numara)
            t = threading.Thread(target=_wa_gonder, args=(wa, aralik, kere), daemon=True)
            threads.append(t)
            t.start()

        try:
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            print(Fore.LIGHTYELLOW_EX + "\n[!] Iptal edildi." + Style.RESET_ALL)

        print(Fore.LIGHTRED_EX + "\nAna ekrana donmek icin 'Enter' tusuna bas")
        input()

    # ── SEÇENEK 3: ÇIKIŞ ───────────────────────────────────────────
    elif menu == 3:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Cikis yapiliyor...")
        break

#Bu Tool https://github.com/s4m3dnotfound/LegacySMS Adresine Aittir...
