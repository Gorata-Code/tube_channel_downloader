import os
import sys
import time
from selenium import webdriver
import tube_channel_bot.constants as const
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement


def resource_path(relative_path) -> [bytes, str]:
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class TubeChannelDownloader(webdriver.Chrome):
    def __init__(self, driver_path=resource_path(r"./SeleniumDrivers"), teardown=False) -> None:
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.page_load_strategy = 'normal'
        super(TubeChannelDownloader, self).__init__(options=options)
        self.implicitly_wait(45)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.teardown:
            self.quit()

    def launch_the_browser(self, channel_name: str) -> None:
        print('\n\tLaunching Google Chrome...')
        self.get(const.BASE_URL + f'/results?search_query={channel_name}')

    def switch_to_video_tab(self, channel_name: str) -> None:
        name_found = []
        try:
            channels = self.find_elements(By.ID, 'channel-name')
            for channel in channels:
                if channel.find_element(By.ID, 'text').find_element(By.TAG_NAME, 'a').get_attribute("innerHTML"). \
                        casefold() == f'{channel_name.casefold()}':
                    print(f'''\nWe have found your channel: "{channel.find_element(By.ID, "text").
                          find_element(By.TAG_NAME, "a").get_attribute("innerHTML")}"!''')
                    channel_link = channel.find_element(By.ID, 'text').find_element(By.TAG_NAME, 'a').get_attribute(
                        'href')

                    self.get(channel_link)
                    print('\n\tSwitching to the "VIDEOS" tab. Please wait...\n')
                    print('Chrome browser tends to be slow at times, sometimes it appears as if nothing is '
                          'happening\nwhile it is actually still loading. Please beware.')
                    video_tab = self.find_element(By.XPATH, '//*[@id="tabsContent"]/tp-yt-paper-tab[2]/div')
                    video_tab.click()
                    name_found.append(channel)
                    input('\nAfter your browser has switched to the "VIDEOS" tab and the video thumbnails on\nthe '
                          'first '
                          'row are showing,\nPress Enter to continue: ')
                    break
                elif channel.find_element(By.ID, 'text').find_element(By.TAG_NAME, 'a').get_attribute('innerHTML'). \
                        casefold() != f'{channel_name.casefold()}' and channels.index(channel) == -1:
                    print(
                        f'\n\t\tSorry, we could not find any channel with the name "{channel_name}".\n\t\tPlease '
                        f'check your spelling and try again.')
                    input('\nPress Enter to quit: ')
                    sys.exit()
        except WebDriverException as exp1:
            if 'no such element' in str(exp1):
                print('\nNo such channel exists. Please try a different channel name.')
                input('\nPress Enter to quit: ')
            sys.exit()

        if len(name_found) < 1:
            print('\nNo matching channel name found. Please try a different one.\n')
            input('Press Enter to quit: \n')
            sys.exit()

    def load_entire_page(self) -> None:
        self.find_element(By.TAG_NAME, 'html').send_keys(Keys.CONTROL + Keys.HOME)
        print('\n\tLoading all the channel\'s videos...\n')
        start_size = self.execute_script("return document.documentElement.scrollHeight")

        while True:
            self.execute_script("window.scrollTo(0, " + str(start_size) + ");")
            time.sleep(6)

            scroll_size = self.execute_script("return document.documentElement.scrollHeight")

            if scroll_size == start_size:
                break

            start_size = scroll_size

    def download_the_files(self, channel_name: str) -> None:

        urls_collected = self.collect_the_urls(channel_name)

        if len(urls_collected) > 0:
            print(f'\t\t** TOTAL FILES TO BE DOWNLOADED: {len(urls_collected)} Video Files **')
            print('\n\tGoing to y2mate to download your files...\n')

            self.get(const.Y2M8is_URL)
            input('After the y2mate page has finished loading, press Enter to continue: \n')

            video_log = 0

            for url in urls_collected:
                video_log += 1
                search_box = self.find_element(By.ID, 'txtUrl')
                search_box.click()
                search_box.clear()
                search_box.send_keys(url)
                search_box.send_keys(Keys.ENTER)
                convert_button = self.find_element(By.XPATH, '/html/body/section[1]/div/div[2]/div['
                                                             '2]/div/div[2]/div/div[2]/table/tbody/tr[2]/td['
                                                             '3]/button')
                convert_button.click()
                download_button = self.find_element(By.XPATH, '/html/body/section[1]/div/div[2]/div[2]/div/div['
                                                              '2]/div/div[2]/table/tbody/tr[2]/td[3]/button/a')
                download_button.click()
                print(f'--> Video {video_log} of {len(urls_collected)} Downloaded.')
                self.page_detour_killer()

            input('\nAfter all your downloads have completed, press Enter to quit: ')

        else:
            print(f'\n\tYour current folder already contains all the videos from the channel {channel_name}')
            input('\nPress Enter to Exit.')

    def collect_the_urls(self, channel_name) -> [str]:

        available_files = files_already_downloaded()
        the_channel_files = self.get_all_channel_files(channel_name)

        print('\n\tDownloading all the videos you don\'t already have from this channel...')

        print(f'\n\t\t\t** NAMES & URLs OF THE VIDEOS TO BE DOWNLOADED **\n')

        url_list = []
        video_count = 0

        for video in the_channel_files:

            # When you are a noob who can't even figure-out Regex and or OOPs :(
            # But it works though, right? ;) No such thing as clean-code :)

            video_title = video.text.replace('?', '').replace('|', '').replace('\\', '').replace(':', '').replace('>',
                                                                                                                  ''). \
                replace('<', '').replace('*', '').replace('"', '').replace('/', '')

            if video_title not in available_files:
                video_count += 1
                print(f'VIDEO {video_count}: ' + video_title)
                video_url = video.get_attribute('href')
                url_list.append(video_url)
                print(f'\n\tURL LINK --> {video_url}\n')

        if video_count == 0:
            print('\tThere are no new videos to download since your folder contains all the videos on this channel.')

        return url_list

    def get_all_channel_files(self, channel_name: str) -> [WebElement]:
        video_list = self.find_elements(By.TAG_NAME, 'ytd-grid-video-renderer')
        video_num = 0
        channel_files = []

        print(f'\n\t\t** ALL THE VIDEOS ON THE CHANNEL "{channel_name}" **\n')

        for video in video_list:
            video_num += 1
            video_title = video.find_element(By.ID, 'video-title')
            print(f'VIDEO NO. {video_num}: {video_title.text}')
            channel_files.append(video_title)
        print(f'\n\t\t** TOTAL NUMBER OF VIDEOS: {len(channel_files)} Videos! **')

        return channel_files

    def page_detour_killer(self):
        while len(self.window_handles) > 1:
            self.switch_to.window(self.window_handles[1])
            self.close()
            self.switch_to.window(self.window_handles[0])
        self.refresh()


def files_already_downloaded() -> [str]:
    current_working_directory = os.listdir()

    target_files = []

    for file in current_working_directory:
        file_name = os.path.splitext(file)
        target_files.append(file_name[0])

    return target_files
