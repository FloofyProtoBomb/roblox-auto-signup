import asyncio
import warnings
import json
import time
import os
from datetime import datetime
from DrissionPage import Chromium, ChromiumOptions, errors
from DrissionPage.common import wait_until
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm
from lib.lib import Main


warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)


async def main():
    lib = Main()
    co = ChromiumOptions()
    co.auto_port().mute(True)

    print("Checking for updates...")
    await lib.checkUpdate()

    while True:
        browserPath = input(
            "\033[1m"
            "\n(RECOMMENDED) Press enter in order to use the default browser path (If you have Chrome installed)"
            "\033[0m"
            "\nIf you prefer to use other Chromium browser other than Chrome, please enter its executable path here. (e.g: C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe)"
            "\nHere are some supported browsers that are tested and able to use:"
            "\n- Chrome Browser"
            "\n- Brave Browser"
            "\nBrowser executable path: "
        ).replace('"', "").replace("'", "")
        if browserPath != "":
            if os.path.exists(browserPath):
                co.set_browser_path(browserPath)
                break
            else:
                print("Please enter a valid path.")
        else:
            break

    while True:
        passw = (
            input(
                "\033[1m"
                "\n(RECOMMENDED) Press enter in order to use the default password"
                "\033[0m"
                "\nIf you prefer to use your own password, do make sure that your password is strong enough.\nThis script has a built in password complexity checker.\nPassword: "
            )
            or "Qing762.chy"
        )
        if passw != "Qing762.chy":
            result = await lib.checkPassword(lib.usernamecreator(), passw)
            print(result)
            if "Password is valid" in result:
                break
        else:
            break

    while True:
        verification = input(
            "\nWould you like to enable email verification? If no you will risk to lose the account. (Hotfix for people who does not have email verification element) [y/n] (Default: Yes): "
        )
        if verification.lower() in ["y", "n", ""]:
            break
        else:
            print("Please enter a valid option.")

    nameFormat = input(
        "\033[1m"
        "\n(RECOMMENDED) Press enter in order to use randomized name prefix"
        "\033[0m"
        "\nIf you prefer to go by your own name prefix, please enter it here.\nIt will go by this example: (If name prefix is 'qing', then the account generated will be named 'qing_0', 'qing_1' and so on)\nName prefix: "
    )

    while True:
        customization = input(
            "\nWould you like to customize the account after the generation process with a randomizer? [y/n] (Default: Yes): "
        )
        if customization.lower() in ["y", "n", ""]:
            break
        else:
            print("Please enter a valid option.")

    proxyUsage = input(
        "\nWould you like to use a proxy?\nPlease enter the proxy IP and port in the format of IP:PORT (Example: http://localhost:1080). Press enter to skip.\nProxy: "
    )

    incognitoUsage = input(
        "\nWould you like to use incognito mode? [y/n] (Default: Yes): "
    )

    accounts = []
    cookies = []

    while True:
        executionCount = input(
            "\nNumber of accounts to generate (Default: 1): "
        )
        try:
            executionCount = int(executionCount)
            break
        except ValueError:
            if executionCount == "":
                executionCount = 1
                break
            else:
                print("Please enter a valid number.")

    print()

    if customization.lower() == "y" or customization == "":
        customization = True
    else:
        customization = False

    if verification.lower() == "y" or verification == "":
        verification = True
    else:
        verification = False

    if proxyUsage != "":
        if lib.testProxy(proxyUsage)[0] is True:
            co.set_proxy(proxyUsage)
        else:
            print(lib.testProxy(proxyUsage)[1])

    if incognitoUsage.lower() == "y" or incognitoUsage == "":
        co.incognito()

    for x in range(int(executionCount)):
        if nameFormat:
            username = lib.usernamecreator(nameFormat)
        else:
            username = lib.usernamecreator()
        bar = tqdm(total=100)
        bar.set_description(f"Initial setup completed [{x + 1}/{executionCount}]")
        bar.update(20)
        chrome = Chromium(addr_or_opts=co)
        page = chrome.get_tab(id_or_num=1)
        page.set.window.max()
        if verification is True:
            page.get("https://mail.tm/en")
            try:
                frame = page.get_frame('#sp_message_iframe_1301373')
                if frame:
                    frame('xpath://*[@id="notice"]/div[3]/div[2]/button').click()
                    time.sleep(1)
            except errors.ElementNotFoundError:
                pass
            page.ele('xpath://*[@id="__nuxt"]/div[1]/div[2]/div/div/div[2]/button[3]').click()
            while True:
                email = page.ele('xpath://*[@id="reka-dropdown-menu-content-v-1-9"]/div/div[1]/div/div/p[2]').text
                emailPassword = page.ele('xpath://*[@id="reka-dropdown-menu-content-v-1-9"]/div/div[1]/div/div/p[3]/span').text
                if email != "..." and emailPassword != "...":
                    break
            bar.set_description(f"Account generation process [{x + 1}/{executionCount}]")
            bar.update(20)

        try:
            firststart = True
            if firststart == False:
                await asyncio.sleep(20)
            firststart = False
            tab = chrome.new_tab("https://www.roblox.com/CreateAccount")
            lang = tab.run_js_loaded("return window.navigator.userLanguage || window.navigator.language").split("-")[0]
            bdaymonthelement = tab.ele("#MonthDropdown")
            currentMonth = datetime.now().strftime("%b")
            bdaymonthelement.select.by_value(currentMonth)
            bdaydayelement = tab.ele("css:DayDropdown")
            currentDay = datetime.now().day
            if currentDay <= 9:
                bdaydayelement.select.by_value(f"0{currentDay}")
            else:
                bdaydayelement.select.by_value(str(currentDay))
            currentYear = datetime.now().year - 19
            tab.ele("#YearDropdown").select.by_value(str(currentYear))
            tab.ele("#signup-username").input(username)
            tab.ele("#signup-password").input(passw)
            time.sleep(1)
            tab.ele("@@id=signup-button@@text()=Sign Up").click()
        except Exception as e:
            print(f"\nAn error occurred\n{e}\n")
        finally:
            bar.set_description(f"Signup process [{x + 1}/{executionCount}]")
            bar.update(50)
            if lang == "en":
                tab.wait.url_change("https://www.roblox.com/home", timeout=float('inf'))
            else:
                tab.wait.url_change(f"https://www.roblox.com/{lang}/home", timeout=float('inf'))
                
            if verification is True:
                try:

                    tab.ele('xpath://*[@id="rbx-account-info-header"]/div[2]/div[5]/span/button').click()
                    tab.ele('xpath://*[@id="emailAddress"]').input(email)
                    tab.ele('xpath://*[@id="rbx-body"]/div[20]/div[2]/div/div/div[3]/button').click()

                    if tab.ele('xpath://*[@id="rbx-body"]/div[20]/div[2]/div/div/div[3]/button', timeout=60):
                        link = None
                        page.get("https://mail.tm/en")
                        page.ele('xpath://*[@id="__nuxt"]/div[1]/div[1]/div/div[2]/nav/a[2]').click()
                        mail = page.ele('xpath://*[@id="__nuxt"]/div[1]/div[2]/main/div[2]/div[2]/ul/li/a')
                        wait_until(
                            lambda: mail,
                            timeout=100
                        )
                        page.get(mail.attr("href"))
                        link = page.ele('xpath:/html/body/center/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[10]/tbody/tr/td/table/tbody/tr/td/a').attr("href")
                        if link:
                            bar.set_description(
                                f"Verifying email address [{x + 1}/{executionCount}]"
                            )
                            bar.update(20)
                            tab.get(link)
                            bar.set_description("Clearing cache and data")
                            bar.update(9)
                            for i in tab.cookies():
                                cookie = {
                                    "name": i["name"],
                                    "value": i["value"],
                                }
                                cookies.append(cookie)
                            if customization is True:
                                await lib.customization(tab)
                            tab.set.cookies.clear()
                            tab.clear_cache()
                            chrome.set.cookies.clear()
                            chrome.clear_cache()
                            chrome.quit()
                            accounts.append({"username": username, "password": passw, "email": email, "emailPassword": emailPassword})
                            bar.update(1)
                            bar.close()
                    else:
                        bar.set_description("Clearing cache and data")
                        for i in tab.cookies():
                            cookie = {
                                "name": i["name"],
                                "value": i["value"],
                            }
                            cookies.append(cookie)
                        if customization is True:
                            await lib.customization(tab)
                        tab.set.cookies.clear()
                        tab.clear_cache()
                        chrome.set.cookies.clear()
                        chrome.clear_cache()
                        chrome.quit()
                        accounts.append({"username": username, "password": passw, "email": email, "emailPassword": emailPassword})
                        bar.close()
                        print(
                            "\nFailed to find verification email. You may need to verify it manually. Skipping and continuing...\n"
                        )
                except Exception as e:
                    for i in tab.cookies():
                        cookie = {
                            "name": i["name"],
                            "value": i["value"],
                        }
                        cookies.append(cookie)
                    if customization is True:
                        await lib.customization(tab)
                    tab.set.cookies.clear()
                    tab.clear_cache()
                    chrome.set.cookies.clear()
                    chrome.clear_cache()
                    chrome.quit()
                    accounts.append({"username": username, "password": passw, "email": email, "emailPassword": emailPassword})
                    bar.close()
                    print(f"\nFailed to find email verification element. You may need to verify the account manually. Skipping and continuing...\n{e}\n")
            else:
                for i in tab.cookies():
                    bar.update(29)
                    bar.set_description("Clearing cache and data")
                    cookie = {
                        "name": i["name"],
                        "value": i["value"],
                    }
                    cookies.append(cookie)
                if customization is True:
                    await lib.customization(tab)
                tab.set.cookies.clear()
                tab.clear_cache()
                chrome.set.cookies.clear()
                chrome.clear_cache()
                chrome.quit()
                email = "N/A"
                emailPassword = "N/A"
                accounts.append({"username": username, "password": passw, "email": email, "emailPassword": emailPassword})
                bar.update(1)
                bar.close()

    with open("accounts.txt", "a") as f:
        for account in accounts:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(
                f"Username: {account['username']}, Password: {account['password']}, Email: {account['email']}, Email Password: {account['emailPassword']} (Created at {timestamp})\n"
            )
    print("\033[1m" "Credentials:")

    try:
        with open("cookies.json", "r") as file:
            existingData = json.load(file)
    except FileNotFoundError:
        existingData = []

    accountsData = []

    for account in accounts:
        accountData = {
            "username": account["username"],
            "password": account["password"],
            "email": account["email"],
            "emailPassword": account["emailPassword"],
            "cookies": []
        }
        for cookie in cookies:
            accountData["cookies"].append({
                "name": cookie["name"],
                "value": cookie["value"]
            })
        accountsData.append(accountData)

    existingData.extend(accountsData)

    with open("cookies.json", "w") as json_file:
        json.dump(existingData, json_file, indent=4)

    for account in accounts:
        print(f"Username: {account['username']}, Password: {account['password']}, Email: {account['email']}, Email Password: {account['emailPassword']}")
    print("\033[0m" "\nCredentials saved to accounts.txt\nCookies are saved to cookies.json file\n\nHave fun playing Roblox!")


if __name__ == "__main__":
    asyncio.run(main())
