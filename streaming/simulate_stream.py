"""Real-time simulator: emits one sensor reading/sec, rolling 10-reading avg + alert check."""
import time, random, datetime
from collections import deque
win=deque(maxlen=10)
if __name__=="__main__":
    print("Streaming EarthScape sensor feed (Ctrl+C to stop) — station=Karachi")
    while True:
        temp=round(random.gauss(34,3),2); rain=round(max(0,random.gauss(2,5)),2)
        win.append(temp); avg=sum(win)/len(win)
        flag="  <-- ALERT: heat threshold" if temp>=42 else ""
        print(f"{datetime.datetime.now():%H:%M:%S} temp={temp}°C rain={rain}mm rolling_avg={avg:.2f}{flag}", flush=True)
        time.sleep(1)
