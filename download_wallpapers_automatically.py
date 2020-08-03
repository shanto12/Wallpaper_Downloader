## Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally
from bs4 import BeautifulSoup

IM_FOLDER1 = "C:/Data/Wallpapers/3840"
IM_FOLDER2 = "C:/Data/Wallpapers/5120"
HOME_URL = "https://superultrawidewallpaper.com"
LIMIT = None


def download_image(image_url, folder_path):
    filename = image_url.split("/")[-1]
    file_path = folder_path + "/" + filename

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200 and not r.history:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', image_url)

        return True
    else:
        # print('Image Couldn\'t be retreived')

        return False

def get_wallpaper_pages(main_page_url):
    r = requests.get(main_page_url)
    page_text = r.text

    url_set = set()

    soup = BeautifulSoup(page_text, 'html.parser')
    for link in soup.find_all('a'):
        url = link.get('href')
        if "-and-" in url:
            url_set.add(url)

    print(f"Page Processed: {main_page_url}")
    return url_set

def process_image_downloads(image_name_set):
    for image_name in image_name_set:
        r = requests.get(image_name)
        page_text = r.text

        # url_set = set()

        soup = BeautifulSoup(page_text, 'html.parser')
        # found = False
        for link in soup.find_all('form'):
            url = link.get('action')
            if "5120x1440" in url:
                if download_image(url, IM_FOLDER1):
                    pass
            elif "3840x1080" in url:
                if download_image(url, IM_FOLDER2):
                    pass
            else:
                print("Found another url: {}".format(url))

        else:
            print("WARNING:No url found for image_name: {}".format(image_name))


def main():
    page_num = 1
    page_url = HOME_URL + "/page/" + str(page_num)
    image_name_set = set()

    while (page_image_name_set:=get_wallpaper_pages(page_url)) and (LIMIT is None or page_num<=LIMIT):
        print(f"Page number processing : {page_num}")
        # if len(page_image_name_set)!=18:
        #     print("WARNING: Found length not equal to 18: Length: {}".format(len(page_image_name_set)))
        image_name_set.update(page_image_name_set)
        page_num +=1
        page_url = HOME_URL + "/page/" + str(page_num)

    process_image_downloads(image_name_set)



# test()
main()
print("DONE!!!")

