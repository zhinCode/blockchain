from colorama import Fore, Style, init

# 색상 초기화
init(autoreset=True)

# ASCII 로고
ASCII_LOGO = """
 ______ _      _                 _____         _        
|___  /| |    (_)               /  __ \       (_)       
   / / | |__   _  _ __   ______ | /  \/  ___   _  _ __  
  / /  | '_ \ | || '_ \ |______|| |     / _ \ | || '_ \ 
./ /___| | | || || | | |        | \__/\| (_) || || | | |
\_____/|_| |_||_||_| |_|         \____/ \___/ |_||_| |_|
                                         
"""

def display_logo():
    colors = [Fore.BLUE, Fore.MAGENTA]
    for i, line in enumerate(ASCII_LOGO.splitlines()):
        color = colors[i % len(colors)]
        print(f'{color}{line}{Style.RESET_ALL}')

def display_app_info(version, author, year):
    print(f'{Fore.CYAN}App Version: {version}{Style.RESET_ALL}')
    print(f'{Fore.CYAN}Author: {author}{Style.RESET_ALL}')
    print(f'{Fore.CYAN}Year: {year}{Style.RESET_ALL}')
