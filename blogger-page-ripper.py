import os
import sys
import xmltodict
import requests

# 2020-06-22 18:06:35
# First part is done. It looks up a blog by name (and name alone) and then finds all the posts on that blog and downloads
# them in a semi-reasonable manner, and in order of posting. Things I might like to do in the future though include:
#
#  - order them based on posting order '<post order> <date posted> (<date modified>) <title>.html'
#  - download all image hrefs in each page in a smart way to have backup copies, just in case, and
#    for those instances where the images might be higher resolution and easier to make out (maps)
#  - create a directory based off the blog name and save everything in there

# The alternative feed is based on your blog ID number as follows:
#    www.blogger.com/feeds/ID_NUMBER/posts/default

def read_page(url):
    with requests.Session() as s:
        return s.get(url).text

single_page_call = 'single-file --browser-wait-until load --filename-template "%s (%s) {page-title}.html" --browser-executable-path "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s'

current_index = 1 # never 0
post_count = 0
max_results = 50
blog_name = sys.argv[1]
blog_feed_url = f'https://{blog_name}.blogspot.com/feeds/posts/default?max-results={max_results}&start-index={current_index}'

p = xmltodict.parse(read_page(blog_feed_url))

total_items = int(p['feed']['openSearch:totalResults'])
start_index = int(p['feed']['openSearch:startIndex'])

try:
    os.mkdir(blog_name)
except FileExistsError:
    pass

os.chdir(blog_name)

# do i want to have the items listed in order by post #?
#print(total_items)
print("Start index = ", start_index)
print("Total Items = ", total_items)
print("# of entries = ", len(p['feed']['entry']))

while True:
    for z in p['feed']['entry']:
        entry_info = {'url': z['link'][4]['@href'],
                      'date': z['published'].split('T')[0],
                      'updated': z['updated'].split('T')[0]}

#        print(entry_info['url'], entry_info['date'], entry_info['updated'])
        os.system(single_page_call % (entry_info['date'], entry_info['updated'], entry_info['url']))

        post_count += 1

    if post_count >= total_items or current_index >= total_items:
        print('total_items = %d' % total_items)
        print('post_count = %d' % post_count)
        print('current_index = %d' % current_index)
        break
    else:
        current_index += max_results
        blog_feed_url = f'https://{blog_name}.blogspot.com/feeds/posts/default?max-results={max_results}&start-index={current_index}'
        p = xmltodict.parse(read_page(blog_feed_url))

sys.exit()

