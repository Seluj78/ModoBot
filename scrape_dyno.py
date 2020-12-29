from time import sleep

from dateutil import parser
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select

from modobot.models.actionlog import ActionLog
from modobot.models.userban import UserBan
from modobot.models.usermute import UserMute
from modobot.models.userwarn import UserWarn

# from modobot.models.usernote import UserNote


firefox_binary = FirefoxBinary("/Applications/Firefox.app/Contents/MacOS/firefox")

driver = webdriver.Firefox(firefox_binary=firefox_binary)


def is_attribute_present(element, attribute):
    result = False
    try:
        val = element.get_attribute(attribute)
        if val:
            result = True
    except:  # noqa
        pass
    return result


def has_class(element, class_name):
    classes = element.get_attribute("class")
    for c in classes.split(" "):
        if c == class_name:
            return True
    return False


if __name__ == "__main__":
    driver.get("https://dyno.gg")
    sleep(10)
    driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/div/div[2]/div/button[2]"
    ).click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/nav/nav/div[2]/div[2]/div/a[2]").click()
    sleep(20)
    driver.find_element_by_xpath(
        "/html/body/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[5]/a"
    ).click()
    sleep(5)
    driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div/div/div/div[1]/aside/div[3]/ul/li[8]/a"
    ).click()
    sleep(2)
    driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/div[1]/div/ul/li[2]/a"
    ).click()
    sleep(2)

    page_selector = Select(
        driver.find_element_by_xpath(
            "/html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/span[2]/select"
        )
    )
    page_selector.select_by_value("5")
    while has_class(
        driver.find_element_by_xpath(
            "/html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[3]"
        ),
        "-active",
    ):
        sleep(0.5)
    next_button = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/button"
    )
    while True:
        table = driver.find_element_by_xpath(
            "/html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]"
        )
        for item in table.find_elements_by_class_name("rt-tr-group"):
            all_columns = item.find_elements_by_class_name("rt-td")
            date = str(all_columns[0].text)
            num = str(all_columns[1].text)
            action = str(all_columns[2].text)
            user_id = str(all_columns[3].text)
            user_name = str(all_columns[4].text)
            moderator_name = str(all_columns[5].text)
            reason = str(all_columns[6].text)

            try:
                parsed_dt = parser.parse(date)
            except:  # noqa
                print(f"Error on {item.xpath}")
                continue
            ActionLog.create(
                moderator_name=moderator_name,
                moderator_id="-1",
                user_name=user_name,
                user_id=user_id,
                dt_action=parsed_dt,
                action=action.lower(),
                comments=reason,
            )

            if action == "Warn":
                UserWarn.create(
                    warned_id=user_id,
                    warned_name=user_name,
                    dt_warned=parsed_dt,
                    moderator_name=moderator_name,
                    moderator_id="-1",
                    reason=reason,
                )
            elif action == "Mute":
                last_mute = (
                    UserMute.select()
                    .where(UserMute.muted_id == user_id)
                    .order_by(UserMute.id.desc())
                    .get()
                )
                last_mute.dt_muted = parsed_dt
                last_mute.save()
            elif action == "Ban":
                banned_user = (
                    UserBan.select()
                    .where(UserBan.banned_id == user_id)
                    .order_by(UserBan.id.desc())
                    .get()
                )
                banned_user.dt_banned = parsed_dt
                banned_user.save()
            elif action == "Unmute":
                UserMute.create(
                    muted_id=user_id,
                    muted_name=user_name,
                    dt_muted=parsed_dt,
                    moderator_id="-1",
                    moderator_name=moderator_name,
                    reason=reason,
                    user_roles="/",
                    is_unmuted=True,
                    dt_unmute=parsed_dt,
                )
            elif action == "Unban":
                UserBan.create(
                    banned_id=user_id,
                    banned_name=user_name,
                    dt_banned=parsed_dt,
                    dt_unbanned=parsed_dt,
                    moderator_name=moderator_name,
                    moderator_id="-1",
                    reason=reason,
                    is_unbanned=True,
                )
            else:
                print(f"Unknown action {action}")

        if not is_attribute_present(next_button, "disabled"):
            next_button.click()
            while has_class(
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[3]"
                ),
                "-active",
            ):
                sleep(0.5)
        else:
            break
