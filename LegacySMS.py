from colorama import Fore, Style
from time import sleep
from os import system
from sms_api import SendSms
import threading
import inspect

# --- Başlangıç Bilgilendirme Ekranı ---
system("cls||clear")
print(Fore.LIGHTGREEN_EX + """                   
**************************************************
*               LegacySMS v2 - 2026              *
*      Bu program tamamen eğitim amaçlıdır.      *
*      Tüm sorumluluklar kullanıcıya aittir.     *
*    Program 10 saniye sonra başlayacaktır...    *
**************************************************
""" + Style.RESET_ALL)

for i in range(10, 0, -1):
    print(Fore.LIGHTGREEN_EX + f"\rBaşlıyor: {i} saniye ", end="", flush=True)
    sleep(1)
print("\n")

# ✅ FIX: Private metodları (alt çizgi ile başlayan) ve inspect edilemeyen
# objeleri filtreleyen güvenli servis listesi
servisler_sms = [
    name for name, method in inspect.getmembers(SendSms, predicate=inspect.isfunction)
    if not name.startswith("_")
]

print(Fore.LIGHTCYAN_EX + f"[i] Toplam {len(servisler_sms)} aktif servis yüklendi." + Style.RESET_ALL)
sleep(2)

# Bu Tool https://github.com/s4m3dnotfound/LegacySMS Adresine Aittir...

def _servisleri_gonder(sms_obj, aralik, kere=None):
    """Tüm servisleri sırayla çalıştırır. kere=None → sonsuz."""
    while True:
        for servis_adi in servisler_sms:
            if kere is not None and sms_obj.adet >= kere:
                return
            # ✅ FIX: exec() yerine getattr() — güvenli ve hızlı
            try:
                getattr(sms_obj, servis_adi)()
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[!] {servis_adi} çağrılamadı: {e}{Style.RESET_ALL}")
            if aralik > 0:
                sleep(aralik)
        if kere is not None and sms_obj.adet >= kere:
            return

while 1:
    system("cls||clear")
    
    # ASCII yeşil logo
    print(Fore.LIGHTGREEN_EX + r"""
     _                                ____  __  __ ____    ____   ___ ____   __   
    | |    ___  __ _  __ _  ___ _   _/ ___||  \/  / ___|  |___ \ / _ \___ \ / /_  
    | |   / _ \/ _` |/ _` |/ __| | | \___ \| |\/| \___ \    __) | | | |__) | '_ \ 
    | |__|  __/ (_| | (_| | (__| |_| |___) | |  | |___) |  / __/| |_| / __/| (_) |
    |_____\___|__, |\__,_|\___|__, |____/|_|  |_|____/  |_____|\___|_____|\___ / 
               |___/           |___/                                             
""" + Style.RESET_ALL)
    
    print(
        f"{Fore.LIGHTGREEN_EX}UYARI: Tamamen Eğitim Amaçlıdır.{Style.RESET_ALL}    "
        f"{Fore.LIGHTBLUE_EX}Geliştirici: {Style.RESET_ALL}s4m3dnotfound    "
        f"{Fore.LIGHTRED_EX}Güncel Sürüm:{Style.RESET_ALL} LegacySMS v2    "
        f"{Fore.LIGHTCYAN_EX}Servis Sayısı: {len(servisler_sms)}{Style.RESET_ALL}"
    )
    
    print()  
    
    try:
        menu = input(Fore.LIGHTWHITE_EX + " 1- SMS Gönder\n\n 2- Çıkış\n\n" + Fore.LIGHTGREEN_EX + " Seçim: ")
        if menu == "":
            continue
        menu = int(menu) 
    except ValueError:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Hatalı işlem. Lütfen Tekrar dene.")
        sleep(3)
        continue

    if menu == 1:
        system("cls||clear")
        print(Fore.LIGHTWHITE_EX + "SMS'lerin gönderileceği numarayı yazınız (başına '0' eklemeden): " + Fore.LIGHTGREEN_EX, end="")
        tel_no = input().strip()
        tel_liste = []
        
        if tel_no == "":
            system("cls||clear")
            print(Fore.LIGHTWHITE_EX + "Numaraların bulunduğu dosya yolunu gir: " + Fore.LIGHTGREEN_EX, end="")
            dizin = input().strip()
            try:
                with open(dizin, "r", encoding="utf-8") as f:
                    for line in f.read().strip().split("\n"):
                        line = line.strip()
                        if len(line) == 10 and line.isdigit():
                            tel_liste.append(line)
            except FileNotFoundError:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Dosya bulunamadı!")
                sleep(3)
                continue
        else:
            if not tel_no.isdigit() or len(tel_no) != 10:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Geçersiz telefon numarası. 10 haneli olmalı ve sadece rakam içermeli.")
                sleep(3)
                continue
            tel_liste.append(tel_no)

        system("cls||clear")
        print(Fore.LIGHTWHITE_EX + "E-posta (rastgele için boş bırak): " + Fore.LIGHTGREEN_EX, end="")
        mail = input().strip()
        if mail and ("@" not in mail or "." not in mail.split("@")[-1]):
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Geçersiz e-posta. Boş bırakırsan otomatik üretilir.")
            sleep(3)
            continue

        system("cls||clear")
        print(Fore.LIGHTWHITE_EX + "Kaç adet SMS? [sonsuz için Enter]: " + Fore.LIGHTGREEN_EX, end="")
        kere_str = input().strip()
        try:
            kere = int(kere_str) if kere_str else None
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı sayı girdiniz.")
            sleep(3)
            continue

        system("cls||clear")
        print(Fore.LIGHTWHITE_EX + "Servisler arası bekleme (saniye) [0 = aralıksız]: " + Fore.LIGHTGREEN_EX, end="")
        try:
            aralik = int(input().strip() or "0")
        except ValueError:
            aralik = 0

        system("cls||clear")
        
        # ✅ Threading ile çoklu numara gönderimi
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
            print(Fore.LIGHTYELLOW_EX + "\n[!] İptal edildi." + Style.RESET_ALL)

        print(Fore.LIGHTRED_EX + "\nAna ekrana dönmek için 'Enter' tuşuna bas")
        input()

    elif menu == 2:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Çıkış yapılıyor...")
        break

#Bu Tool https://github.com/s4m3dnotfound/LegacySMS Adresine Aittir...
