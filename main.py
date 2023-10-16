import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 82.8628  # Your latitude
MY_LONG = 135.0000  # Your longitude
USER_GMAIL = "YOUR GMAIL"
PASS = "PASSWORD"
TO_GMAIL = "TO GMAIL"

def check_iss():
    response_iss_loc = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss_loc.raise_for_status()
    data = response_iss_loc.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # test
    # iss_latitude = MY_LAT
    # iss_longitude = MY_LONG

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        print("check_iss True")
        return True
    else:
        print("check_iss False")
        return False


def check_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response_sr_ss = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_sr_ss.raise_for_status()
    data = response_sr_ss.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 5
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 5

    time_now = datetime.now().hour

    # test
    # time_now = 3

    if not sunrise <= time_now <= sunset:
        print("check_dark True")
        return True
    else:
        print("check_dark False")
        return False


while True:
    time.sleep(60)
    # test
    # print(f"Sunrise {sunrise}\nSunset {sunset}\nTime now {time_now}")
    if check_dark() and check_iss():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=USER_GMAIL, password=PASS)
            connection.sendmail(from_addr=USER_GMAIL,
                                to_addrs=TO_GMAIL,
                                msg="Subject:ISS overhead.\n\n"
                                    "Get out and look at the sky, International space station is above you.")
        # print("Email sent.")
