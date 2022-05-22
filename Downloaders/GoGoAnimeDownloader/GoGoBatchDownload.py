#NOTE: Author - Sasank Shouri Yerragolla


'''Command: python "D:\Virtual Assistant\Main\Subsystems\gogoanime.py" "https://gogoanime.gg/category/wan-jie-shen-zhu" "173-232" "1080"'''


import contextlib
import fnmatch
import itertools
import os
import shutil
import sys
import time

from plyer import notification
# Below are added for better terminal experience
from rich.console import Console
from rich.panel import Panel
from rich.progress import (BarColumn, Progress, TextColumn,
                           TimeRemainingColumn, TransferSpeedColumn)
from rich.traceback import install
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# Below two are needed to wait in browser until the button is clickable
from selenium.webdriver.support.ui import WebDriverWait

# ----------------------- Rich - Better terminal stuff ----------------------- #
install()
console = Console()

# ------------------------------ Initialization ------------------------------ #
#vivaldi = "C:/Users/mvhit/AppData/Local/Vivaldi/Application/vivaldi.exe"
vivaldi = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
options = webdriver.ChromeOptions()
options.binary_location = vivaldi
# % Below is need to remove download dialog pop-up. Uses D:\Virtual Assistant\Main\Data\User Data
# % DO NOT DELETE THE USER DATA FILE
options.add_argument("--user-data-dir=C:\\Users\\mvhit\\PycharmProjects\\Pythonanimedownloader\\Data\\User Data")
# % If above is giving trouble, may have to re-copy the folder from vivaldi path
# % Not using headless because, sometimes have to solve captcha manually
# options.add_argument("--headless")  # % Opens webpage and scrapes in the background
# $ options.add_argument("--disable-extensions")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)


# ------------------------------ Getting inputs ------------------------------ #
input_url = sys.argv[1]
input_eps = sys.argv[2]
quality = sys.argv[3]
with contextlib.suppress(IndexError):
    mode = sys.argv[4]
try:
    if mode == 'verbose':
        verbose = True
        print("Script running in verbose mode")
except Exception:
    verbose = False
if int(quality) == 1080:
    quality_preferred = "DOWNLOAD (1080P - MP4)"
    quality_backup = "DOWNLOAD (720P - MP4)"
elif int(quality) == 720:
    quality_preferred = "DOWNLOAD (720P - MP4)"
    quality_backup = "DOWNLOAD (480P - MP4)"
final_eps = []
# % Accepts 5-7 or 1,4,5 episode inputs
# Below calculates the episodes to be downloaded depending on the input
try:
    if '-' in input_eps:
        input_eps = input_eps.split('-')
        input_eps[0] = int(input_eps[0])
        input_eps[1] = int(input_eps[1]) + 1
        final_eps.extend(iter(range(input_eps[0], input_eps[1])))
    elif ',' in input_eps:
        input_eps = input_eps.split(',')
        final_eps.extend(int(i) for i in input_eps)
    else:
        final_eps.append(int(input_eps))
except Exception:
    print("Wrong inputs given")
# ------------------------------ Start scraping ------------------------------ #
# //*[@id="episode_page"]/li[1]/a
# //*[@id="episode_page"]/li[2]/a
browser.get(input_url)
time.sleep(5)
with contextlib.suppress(Exception):
    i = 1
    while True:
        xpath_episodes = f'//*[@id="episode_page"]/li[{i}]/a'
        episodes = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath_episodes)))
        if i == 1:
            episode_start = episodes.get_attribute('ep_start')
        try:
            episode_end = episodes.get_attribute('ep_end')
        except Exception:
            break
        i = i + 1
# $ WebDriverWait(browser, 20).until(
# $     EC.presence_of_element_located((By.CLASS_NAME, "active")))
# $ episodes = browser.find_element(By.CLASS_NAME, "active")
# $ episode_start = episodes.get_attribute('ep_start')
# $ episode_end = episodes.get_attribute('ep_end')
if verbose:
    print(f"Starting episode is {episode_start}")
    print(f"Ending episode is {episode_end}")
anime_name = input_url.replace("https://gogoanime.gg/category/", '')


class MyProgress(Progress):
    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks), title=f'[red]{anime_name}', subtitle="[cyan]Shouri", subtitle_align="right")


progress = MyProgress(
    TextColumn("{task.fields[filename]}", justify="left"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "â€¢",
    TransferSpeedColumn(),
    "â€¢",
    TimeRemainingColumn(),
    # $ transient=True,  # clears the progress after completion
)


# Checking if input is valid
def valid_range():
    if len(final_eps) == 1:
        return True
    if verbose:
        print(f"User starting episode is {final_eps[0]}")
        print(f"User ending episode is {final_eps[-1]}")
        print(f"Website starting episode is {episode_start}")
        print(f"Website ending episode is {episode_end}")
    return (final_eps[0] >= int(episode_start)) and (final_eps[-1] <= int(episode_end))


def find_files(search_string, search_path):
    matches = []
    for (root, dirnames, filenames), extensions in itertools.product(os.walk(search_path), search_string):
        matches.extend(
            os.path.join(root, filename)
            for filename in fnmatch.filter(filenames, extensions)
        )
    return matches


def download_progress(full_size, episode):
    # $ console.log(full_size)
    timeout = 0
    file_not_found = False
    while 1:
        timeout = timeout + 1
        files = find_files([f"*EP.{episode}*"], "C:/Users/mvhit/Downloads")
        if timeout == 500:
            file_not_found = True
            break
        if files:
            break
        time.sleep(0.02)
    if not file_not_found:
        progress_calculation(episode, full_size)


def progress_calculation(episode, full_size):
    task1 = progress.add_task("Download", filename=f"[green]Episode-{episode}", total=full_size)
    # % Can add arg start=False --> if don't want to start the task immediately
    # % Then have to use progress.start_task to start and then update the task
    previous_size = 0
    progress_timeout = 0
    while not progress.finished:
        files = find_files([f"*EP.{episode}*"], "C:/Users/mvhit/Downloads")
        try:
            current_size = os.path.getsize(files[0])  # gives size in bytes
        except Exception:
            # $ console.log(f"[green] Episode {episode} is downloaded")
            break
        if current_size == previous_size:
            if ".crdownload" not in files[0]:
                # $ console.log("Entered mp4 loop to break")
                break  # Download completed
            progress_timeout += 1
        if progress_timeout >= 50000:  # Waiting for 15 mins
            # $ console.log(f"[red] Could not download Episode {episode}")
            break  # Breaking the loop because of no progress in download and moving on to next download
        # $ progress.update(task1, advance=0.5)
        progress.update(task1, completed=current_size)
        previous_size = current_size
        time.sleep(0.02)
    # $ console.log("Exited the completed loop")
    # if progress calc is wrong, then writing logic to wait until a completed file is found
    progress_timeout = 0
    while 1:
        files = find_files([f"*EP.{episode}*"], "C:/Users/mvhit/Downloads")
        if "crdownload" not in files[0]:
            break
        if progress_timeout >= 150:
            break
        time.sleep(0.5)
        progress_timeout = + 1
    # $ console.log("Exited while 1 loop")


# To send notification to complete captcha
def send_notification():
    notification.notify(
        title="Gogoanime Downloader",
        message="Need to complete the captcha",
        timeout=15
    )


# Used to add the right quality to the file name
def quality_selected(quality):
    if "1080" in quality:
        return "1080p"
    elif "720" in quality:
        return "720p"
    elif "480" in quality:
        return "480p"


def gogoanime_download(url, current_ep):
    if verbose:
        print(f"Episode link is : {url}")
    try:
        browser.get(url)
    except Exception:
        # % If the page is not loading properly,
        # % Then reloading the page again
        with contextlib.suppress(Exception):
            browser.navigate().refresh()
    xpath_download = '//*[@id="wrapper_bg"]/section/section[1]/div[1]/div[2]/div[3]/div/ul/li[1]/a'
    # $ time.sleep(5)
    download = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath_download)))
    download_page = download.get_attribute('href')
    # $ console.log(download_page)
    try:
        browser.get(download_page)
    except Exception:
        # % If the page is not loading properly,
        # % Then reloading the page again
        with contextlib.suppress(Exception):
            browser.get(download_page)
    time.sleep(5)
    # Waiting for page to load
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.ID, "content-download")))  # waiting up to 10 mins to complete captcha
    xpath_filesize = '//*[@id="filesize"]'
    file_size = browser.find_element(By.XPATH, xpath_filesize).text
    file_size = file_size.split(' ')
    # Size calculation
    if file_size[1] == 'GB':
        final_size = float(file_size[0]) * (1024 * 1024 * 1024)  # GB to bytes
    else:  # for MB
        final_size = float(file_size[0]) * (1024 * 1024)  # MB to bytes
    time.sleep(5)
    try:
        WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "P - MP4)")))
    except Exception:
        send_notification()
        try:
            WebDriverWait(browser, 600).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "P - MP4)")))
        except Exception:
            input("Pausing the program, press ENTER to continue")
            WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "P - MP4)")))
    try:
        WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, quality_preferred))).click()
        # forwarding data to calculate progress
        download_progress(final_size, current_ep)
        return quality_selected(quality_preferred)
    except Exception:
        try:
            WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, quality_backup))).click()
            # forwarding data to calculate progress
            download_progress(final_size, current_ep)
            return quality_selected(quality_preferred)
        except Exception:
            console.log(f"Did not find preferred quality video for episode-{current_ep}")


base_url = input_url.replace('category/', '') + '-episode-'
# Stuff needed for renaming and moving files to folder
folder_path_check = f"C:/Users/mvhit/Downloads/{anime_name}"
file_exists = os.path.exists(folder_path_check)
if not file_exists:
    os.mkdir(folder_path_check)
if valid_range():
    with progress:
        for i in final_eps:
            # $ console.log(f"Web scraping for episode {i}")
            current_url = base_url + str(i)
            if verbose:
                print(f"Current downloading episode link is {current_url}")
            # $ console.log(current_url)
            video_quality = gogoanime_download(current_url, str(i))
            # Moving the downloaded file to the respective folder
            try:
                # $ console.log("Trying to rename the file")
                files = find_files([f"*EP.{i}*"], "C:/Users/mvhit/Downloads")
                # os.rename(files[0], f"C:/Users/mvhit/Downloads/{anime_name}-ep{i}.mp4")
                shutil.move(files[0], f"C:/Users/mvhit/Downloads/{anime_name}/{anime_name}-ep{i}-{video_quality}.mp4")
            except Exception:
                console.log(f"Episode-{i} not found. Moving on.")
            # $ console.log("Completed for loop")
else:
    print("Episode range provided by user doesn't match with website")
    print(f"User starting episode is {final_eps[0]}")
    print(f"User ending episode is {final_eps[-1]}")
    print(f"Website starting episode is {episode_start}")
    print(f"Website ending episode is {episode_end}")
browser.close()
browser.quit()
