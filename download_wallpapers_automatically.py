## Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally
import re
from string import Template

#asdfasdf

IM_FOLDER = "C:/Users/smatthew/Downloads/wallpapers"
HOME_URL = "http://wallpaperswide.com/3440x1440-wallpapers-r/page/"
LIMIT = None
DONT_DOWNLOAD_SET = {'latest_wallpapers', 'aero-desktop-wallpapers', 'animals-desktop-wallpapers',
                     'architecture-desktop-wallpapers', 'army-desktop-wallpapers', 'artistic-desktop-wallpapers',
                     'awareness-desktop-wallpapers', 'black_and_white-desktop-wallpapers',
                     'cartoons-desktop-wallpapers', 'celebrities-desktop-wallpapers', 'city-desktop-wallpapers',
                     'computers-desktop-wallpapers', 'cute-desktop-wallpapers', 'elements-desktop-wallpapers',
                     'food_and_drink-desktop-wallpapers', 'funny-desktop-wallpapers', 'games-desktop-wallpapers',
                     'girls-desktop-wallpapers', 'holidays-desktop-wallpapers', 'love-desktop-wallpapers',
                     'motors-desktop-wallpapers', 'movies-desktop-wallpapers', 'music-desktop-wallpapers',
                     'nature-desktop-wallpapers', 'seasons-desktop-wallpapers', 'space-desktop-wallpapers',
                     'sports-desktop-wallpapers', 'travel-desktop-wallpapers', 'vintage-desktop-wallpapers'}


pattern = '<a href="/((?!\d*x\d*).{15,90}).html" title='
pattern = re.compile(pattern)
t = Template('http://wallpaperswide.com/download/$wall_name-$resolution.jpg')

def download_image(image_url):
    filename = image_url.split("/")[-1]
    file_path = IM_FOLDER + "/" + filename

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

def process_page(page_url):
    r = requests.get(page_url)
    page_text = r.text

    image_name_list = pattern.findall(page_text)
    image_name_set = {x[:-1] for x in image_name_list if x not in DONT_DOWNLOAD_SET}
    print(f"Page Processed: {page_url}")
    return image_name_set

def process_image_downloads(image_name_set):
    for image_name in image_name_set:
        for resolution in ["5120x2160","3840x2160", "3840x1600"]:
            image_url = t.substitute(wall_name=image_name, resolution=resolution)
            if download_image(image_url):
                break
        else:
            print("WARNING:No url found for image_name: {}".format(image_name))

# def test():
#     pass
#     text = """
#     <a href="/chamarel_waterfalls_mauritius-wallpapers.html" title="View Chamarel Waterfalls, Mauritius Ultra HD Wallpaper for 4K UHD Widescreen desktop, tablet & smartphone" itemprop="significantLinks">
#     <a href="/chamarel_waterfalls_mauritius-wallpapers.html" title="Chamarel Waterfalls, Mauritius Ultra HD Wallpaper for 4K UHD Widescreen desktop, tablet & smartphone">
#     <a href="/shanto.html" title="Chamarel Waterfalls, Mauritius Ultra HD Wallpaper for 4K UHD Widescreen desktop, tablet & smartphone">
#     <a href="/3840x1600-wallpapers-r.html" title="Chamarel Waterfalls, Mauritius Ultra HD Wallpaper for 4K UHD Widescreen desktop, tablet & smartphone">
# """
#     pattern = '<a href="/(.*).html" title='
#     pattern = '<a href="/((?!\d*x\d*).{15,}).html" title='
#
#     pattern = re.compile(pattern)
#     result = pattern.findall(text)
#     print("done")

def main():
    page_num = 1
    page_url = HOME_URL + str(page_num)
    image_name_set = set()

    while (page_image_name_set:=process_page(page_url)) and (LIMIT is None or page_num<=LIMIT):
        print(f"Page number processing : {page_num}")
        if len(page_image_name_set)!=18:
            print("WARNING: Found length not equal to 18: Length: {}".format(len(page_image_name_set)))
        image_name_set.update(page_image_name_set)
        page_num +=1
        page_url = HOME_URL + str(page_num)

    process_image_downloads(image_name_set)



# test()
main()
print("DONE!!!")

