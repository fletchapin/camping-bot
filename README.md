# Install chromedriver
This is the [official documentation](https://chromedriver.chromium.org/), but there are more detailed instructions for various OS:

- Mac: https://www.swtestacademy.com/install-chrome-driver-on-mac/
- Windows: https://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/
- Debian: https://tecadmin.net/setup-selenium-with-chromedriver-on-debian/

# Setting up Text Messaging

You'll have to put in your own keyword arguments to `msg_alert`, according to the following:

- `to` is your number appended by the carrier's SMS Gateway Address:
  - Verizon – number@vtext.com
  - T-Mobile – number@tmomail.net
  - Sprint – number@messaging.sprintpcs.com
  - AT&T – number@txt.att.net
  - Boost Mobile – number@smsmyboostmobile.com
  - Cricket – number@sms.cricketwireless.net
  - U.S. Cellular – number@email.uscc.net
- `email_addr` must be Gmail
- To get `app_pwd`:
  1. Login to Gmail -> Manage your Google Account -> Security -> Signing in to Google -> App passwords
  2. Select app and choose other. Enter "camping-bot" and select generate
  3. DO NOT save this password in plain text. Save it in a password manager, paste it in to the Python application while in use, and delete it afterward.

```python
def msg_alert(
    subject,
    body,
    to="0123456789@vtext.com",
    email_addr="someaddr@gmail.com",
    app_pwd="insert-actual-password"
):
```

# Running on a Server

`python -m messaging_script.py -p <park> -c <campground> -y <year> -m <month1> <month2> -s <sleep>`

- `months` argument can include one or multiple months and is optional. If not included, the whole year is searched.
- `sleep` defines how long to sleep before searching again. Default is 86400 seconds (24 hrs).

# Examples

To search Angel Island's North Garrison Group camp for all of 2022:
`python -m messaging_script.py -p angel-island -c north-garrison-group-camp -y 2022`

To re-run the search every hour instead of every day:
`python -m messaging_script.py -p angel-island -c north-garrison-group-camp -y 2022 -s 3600`

To search Angel Island's North Garrison Group camp for July 2022:
`python -m messaging_script.py -p angel-island -c north-garrison-group-camp -y 2022 -m 7`

To search Angel Island's North Garrison Group camp for July and October 2022:
`python -m messaging_script.py -p angel-island -c north-garrison-group-camp -y 2022 -m 7 10`
