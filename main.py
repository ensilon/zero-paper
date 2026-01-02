#!/usr/bin/env python3

import sys
import re
from icmplib import ping
from datetime import datetime

from epd import EPD
from panel import Panel
from font import Font
from utils import Weather, Ping

if __name__ == "__main__":
    icosolid = Font("fonts/fa/Font Awesome 7 Free-Solid-900.otf")
    icoreg = Font("fonts/fa/Font Awesome 7 Free-Regular-400.otf")
    #fontreg = Font("fonts/google/WalterTurncoat-Regular.ttf")
    fontreg = Font("fonts/google/Amarante-Regular.ttf")
    
    panel = Panel()
    epd = EPD()
    rtt = Ping().rtt()
    forcast = Weather().forcast()
    
    panel.add((5, 5), "Meadowbrook", font=fontreg.size())
    
    ico = "\uF1EB"
    txt = f"{rtt}ms"
    width = 8 + panel.estimate(ico, font=icosolid.size(28)) + panel.estimate(txt, font=fontreg.size(28))
    x = panel.max_x - width
    x += panel.add((x, 5), ico, font=icosolid.size(28))
    x += 8
    x += panel.add((x, 3), txt, font=fontreg.size(28))
    
    
    # if no ping
    #panel.add( (190, 10), '\uF05E', font=icosolid.size())
                
    x = 30
    x += panel.add ((x, 36), f"{forcast['feels']}°", font=fontreg.size(70))
    x -= 4

    if re.search("(broken|few) cloud", forcast['description'], flags=re.IGNORECASE):
        x += panel.add((x, 50), "\uF0C2", font = icoreg.size(60)) # cloud
    
    elif re.search("cloud", forcast['description'], flags=re.IGNORECASE):
        x += panel.add((x, 50), "\uF0C2", font =icosolid.size(60)) # solid cloud
    
    elif re.search("light snow", forcast['description'], flags=re.IGNORECASE):
        x += panel.add((x, 50), "\uf2dc", font =icoreg.size(60)) # solid snowflake
    
    elif re.search("snow", forcast['description'], flags=re.IGNORECASE):
        x += panel.add((x, 50), "\uf2dc", font =icosolid.size(60)) # snowflake
    
    else:
        x += panel.add((x, 50), "\uf057", font =icosolid.size(60))

    time = datetime.fromtimestamp(forcast['sunrise']).strftime('%I:%M %p')
    time = time.lstrip("0")
    ico = "\uf106" # arrow up
    txt = f"{time}"
    width = panel.estimate(txt, font = fontreg.size()) + panel.estimate(ico, icosolid.size())
    x = panel.max_x - width
    x += panel.add((x, 120), txt, font = fontreg.size())
    panel.add((x, 120), ico, font = icosolid.size())

    time = datetime.fromtimestamp(forcast['sunset']).strftime('%I:%M %p')
    time = time.lstrip("0")
    ico = "\uf107" # arrow down
    txt = f"{time}"
    width = panel.estimate(txt, font = fontreg.size()) + panel.estimate(ico, icosolid.size())
    x = panel.max_x - width
    x += panel.add((x, 140), txt, font = fontreg.size())
    panel.add((x, 140), ico, font = icosolid.size())

    time = datetime.now().strftime('%I:%M %p')
    panel.add((0, 120), time.lstrip("0"), font = fontreg.size(40))

    print(f"temp {forcast['temperature']} / {forcast['description']}")

    epd.start()
    epd.refresh(panel.img)
    #panel.save()


