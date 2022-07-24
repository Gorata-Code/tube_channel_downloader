import sys
from win32com.client import Dispatch
from selenium.common.exceptions import WebDriverException
from tube_channel_bot.tube_channel_downloader import TubeChannelDownloader


def script_summary() -> None:
    print('''
              ***----------------------------------------------------------------------------------------***
         \t***------------------------ DUMELANG means GREETINGS! ~ G-CODE -----------------------***
                   \t***------------------------------------------------------------------------***\n
        
        \t\t"TUBE-CHANNEL-DOWNLOADER" Version 1.1.0\n
        
        This Program will help you download videos from a YouTube channel of your choosing.\n
        No need for installation. Just put this "Tube Channel Downloader.exe" file in the\n
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

        if 'executable needs to be in PATH' in str(exp):
            print('''
                Please make sure you have not deleted or moved or renamed the "chromedriver.exe"

                file that is next to the "Tube Channel Downloader.exe". The programme needs it

                to work.
            
                ''')

            input('\nPress Enter To Exit.\n')
            sys.exit(1)

        elif 'version of ChromeDriver only supports Chrome version' in str(exp):
            message: str = str(exp).split('\n')[0].split(':')[-1]
            print(f'''
               {message}.
                
                You need to download the ChromeDriver version compatible with your version of Chrome.
                
                Please refer to the information about GOOGLE CHROME & CHROME_DRIVER above. 
                
                Once you are done downloading the ChromeDriver, you unzip it and then 
                
                replace the current one by placing the new one in the same folder as
                
                this "Tube Channel Downloader.exe".

            ''')
            input('\nPress Enter To Exit.\n')
            sys.exit(1)

        elif 'INTERNET' in str(exp):

            print(''''

                    Please make sure you are connected to the internet and Try again.

                    Cheers!

                    ''')

            input('\nPress Enter To Exit.\n')
            sys.exit(1)

        elif WebDriverException:

            if 'version' in str(exp):

                print('\nPlease make sure your version of Google Chrome is at least version 103.\n'

                      'Open your Chrome browser and go to "Menu -> Help -> About Google Chrome"\n'

                      'to update your web browser.\n')

            else:
                print('\nSomething went wrong, please make sure you do not disturb the Google Chrome window\n'

                      'while it works when you try again.')

            input('\nPress Enter To Exit & try again.\n')
            sys.exit(1)

        elif 'Timed out receiving message from renderer' or 'cannot determine loading status' in str(exp):
            print('Google Chrome is taking too long to respond :( .')

        elif 'ERR_NAME_NOT_RESOLVED' or 'ERR_CONNECTION_CLOSED' or 'unexpected command response' in str(exp):
            print('Your internet connection may have been interrupted.')
            print('Please make sure you\'re still connected to the internet and try again.')

        else:
            print('\nSomething went wrong, please make sure you do not disturb the Google Chrome window\n'
                  'while it works when you try again.')

        input('\nPress Enter to Exit & Try Again.')
        sys.exit(1)


def detect_browser_version(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


if __name__ == "__main__":
    script_summary()
    absolute_paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                      r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    users_browser_version = list(filter(None, [detect_browser_version(p) for p in absolute_paths]))[0]
    print('YOUR GOOGLE CHROME VERSION: ' + users_browser_version)
    print(f'IF YOU NEED TO DOWNLOAD THE CHROME_DRIVER: https://chromedriver.chromium.org/downloads\n')


def main() -> None:
    channel_name: str = input('Type a Channel Name & Press Enter: ').strip()
    if len(channel_name) > 0:
        the_tube_tuber(channel_name)
    else:
        print('\n\t\tPlease type something.\n')
        input('Press Enter to quit:')
        sys.exit()


if __name__ == '__main__':
    main()
