import sys
import requests
import xmltodict

def read_page(url):
    with requests.Session() as s:
        return s.get(url).text


current_index = 1
post_count = 0
max_results = 50
blog_name = sys.argv[1]
blog_feed_url = f'https://{blog_name}.blogspot.com/feeds/posts/default?max-results={max_results}&start-index={current_index}'

p = xmltodict.parse(read_page(blog_feed_url))

total_items = int(p['feed']['openSearch:totalResults'])
start_index = int(p['feed']['openSearch:startIndex'])

while True:
    for z in p['feed']['entry']:
        entry_info = {'url': z['link'][4]['@href'],
                      'date': z['published'].split('T')[0],
                      'updated': z['updated'].split('T')[0]}

        print(entry_info['url'])

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

