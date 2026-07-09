import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

phone = "+905459402927"
msg = "Test mesaji buraya"

results = {}

# 1. TextBelt - ucretsiz 1 SMS/gun per IP
try:
    r = requests.post('https://textbelt.com/text', data={
        'phone': phone, 'message': msg, 'key': 'textbelt'
    }, timeout=10)
    results["TextBelt"] = f"HTTP {r.status_code} | {r.text[:150]}"
except Exception as e:
    results["TextBelt"] = f"ERROR: {e}"

# 2. Anonym-SMS.com
try:
    r = requests.post('https://anonym-sms.com/send.php', data={
        'to': phone, 'msg': msg
    }, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    results["AnonymSMS"] = f"HTTP {r.status_code} | {r.text[:150]}"
except Exception as e:
    results["AnonymSMS"] = f"ERROR: {type(e).__name__}"

# 3. SMSGatewayHub free
try:
    r = requests.get('https://www.smsgateway.me/send_message.php', params={
        'phone': phone, 'message': msg
    }, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    results["SMSGatewayHub"] = f"HTTP {r.status_code} | {r.text[:150]}"
except Exception as e:
    results["SMSGatewayHub"] = f"ERROR: {type(e).__name__}"

# 4. sms24.me free
try:
    r = requests.post('https://sms24.me/en/messages', data={
        'phone_number': phone, 'message': msg
    }, headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"}, timeout=10)
    results["SMS24"] = f"HTTP {r.status_code} | {r.text[:150]}"
except Exception as e:
    results["SMS24"] = f"ERROR: {type(e).__name__}"

# 5. Way2SMS
try:
    r = requests.post('https://www.way2sms.com/api/v1/sendCampaign', json={
        'userId': 'free', 'password': 'free', 'senderId': 'ANON',
        'mobiles': phone, 'message': msg
    }, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    results["Way2SMS"] = f"HTTP {r.status_code} | {r.text[:150]}"
except Exception as e:
    results["Way2SMS"] = f"ERROR: {type(e).__name__}"

# 6. seven.io (sms77) free
try:
    r = requests.post('https://gateway.seven.io/api/sms', data={
        'p': 'demo', 'to': phone, 'from': 'Bilgi', 'text': msg
    }, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    results["SevenIO"] = f"HTTP {r.status_code} | {r.text[:150]}"
except Exception as e:
    results["SevenIO"] = f"ERROR: {type(e).__name__}"

print("\n====== ANONIM SMS TEST ======")
for name, result in results.items():
    tag = "[OK]" if "200" in result or "success" in result.lower() or "queued" in result.lower() else "[XX]"
    print(f"{tag} {name}: {result}")
    print("---")
