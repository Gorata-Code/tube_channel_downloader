import sys
from selenium.common.exceptions import WebDriverException
from tube_channel_bot.tube_channel_downloader import TubeChannelDownloader


def script_summary() -> None:
    print('''
        \t\tDUMELANG means GREETINGS! ~ G-CODE\n
        \t"TUBE-CHANNEL-DOWNLOADER" Version 1.0.0\n
        This Program will help you download videos from a YouTube channel of your choosing.\n
        No need for installation. Just put this "tube_channel_downloader.exe" file in the\n
        folder you want to download the files to and then double-click it to run. If you\n
        already have one or more videos from the channel you would like to download from,\n
        you should put this file in the same folder as those files so you do not download\n
        video files you already have. Make sure you have not changed the original file names.\n
        Please make sure you keep this window (the command prompt) open and you don't disturb\n
        the browser window that opens after. Follow the instructions and your mission will be\n
        successful! CHEERS!
    ''')


def the_tube_tuber(channel_name: str) -> None:
    try:

        with TubeChannelDownloader() as tuber_bot:
            tuber_bot.launch_the_browser(channel_name)
            tuber_bot.switch_to_video_tab(f'{channel_name}')
            tuber_bot.load_entire_page()
            tuber_bot.download_the_files(channel_name)

    except Exception as exp:

        if 'in PATH' in str(exp):

            print(''''

                    Please make sure you have not deleted or moved or renamed the "chromedriver.exe"
                    
                    file that is next to the "tube_channel_downloader.exe". The programme needs it 
                    
                    to work.
                    
                    If you still get this error, then you need to download the chromedriver for your 

                    version of Chrome. There are many videos on YouTube about how to get that set up.
                    
                    Once you are done downloading it, you unzip it and then replace the current one.

                    ''')

            input('\nPress Enter To Exit.\n')

        elif 'INTERNET' in str(exp):

            print(''''

                    Please make sure you are connected to the internet and Try again.

                    Cheers!

                    ''')

            input('\nPress Enter To Exit.\n')

        elif WebDriverException:

            if 'version' in str(exp):

                print('\nPlease make sure your version of Google Chrome is at least version 97.\n'

                      'Open your Chrome browser and go to "Menu -> Help -> About Google Chrome"\n'

                      'to update your web browser.\n'

                      'If you get this error message after updating your Google Chrome, then you\n'

                      'will need to download an updated version of chromedriver.\n'

                      'Visit https://chromedriver.chromium.org/downloads and download the chromedriver\n'

                      'that matches your version of Google Chrome. Once downloaded, unzip the download\n'

                      'and copy the file named chromedriver.exe & paste it in the same place as\n'

                      'this tube_channel_downloader.exe. Then you will be good to go!')

            else:
                print('\nSomething went wrong, please make sure you do not disturb the Google Chrome window\n'

                      'while it works when you try again.')

            input('\nPress Enter To Exit & try again.\n')


def main() -> None:
    script_summary()
    channel_name = input('Enter Channel Name: ').strip()
    if len(channel_name) > 0:
        the_tube_tuber(channel_name)
    else:
        print('\n\t\tPlease type something.\n')
        input('Press Enter to quit:')
        sys.exit()


if __name__ == '__main__':
    main()
