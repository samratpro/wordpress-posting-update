import os
import json
import base64
import cloudscraper
import requests
scraper = cloudscraper.create_scraper()

website_name = "website.com"
Username = "username"
App_pass = "p29W j8qd I0hu pPWs HeNm L7ar"
category = "Your Category Name"
tags = "Tag Name"
status = "draft"  # publish

# Wordpress posting code-----------------
json_url = 'https://'+website_name + '/wp-json/wp/v2'
token = base64.standard_b64encode((Username + ':' + App_pass).encode('utf-8'))  # we have to encode the usr and pw
headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

# Uploading Img for post body image
def image_operation(keyword):
  try:
    media = {'file': open('img/' + keyword + '.jpg', 'rb')}
    image = scraper.post(json_url + '/media', headers=headers, files=media)
    image_title = keyword.replace('-', ' ').split('.')[0]
    post_id = str(json.loads(image.content.decode('utf-8'))['id'])
    source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
    image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
    image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
    image3 = '<!-- /wp:image -->'
    image_wp = image1 + image2 + image3
    return image_wp
  except:
    return ''

# Creating Tag
def create_tag(tag_name):
  id = 0
  data = {"name":tag_name}
  try:
    tag = requests.post(json_url + '/tags', headers=headers, json=data)
    id = str(json.loads(tag.content.decode('utf-8'))['id'])
  except KeyError:
    tag = requests.get(json_url + '/tags', headers=headers)
    tag_id = json.loads(tag.content.decode('utf-8'))
    for tag in tag_id:
      if tag_name.lower() == tag['name'].lower():
        id = str(tag['id'])
  return id

# Creating Category
def create_category(cat_name):
  id = 0
  data = {"name":cat_name}
  try:
    cat = requests.post(json_url + '/categories', headers=headers, json=data)
    id = str(json.loads(cat.content.decode('utf-8'))['id'])
  except KeyError:
    cat = requests.get(json_url + '/categories', headers=headers)
    cat_id = json.loads(cat.content.decode('utf-8'))
    for cat in cat_id:
      if cat_name.lower() == cat['name'].lower():
        id = str(cat['id'])
  return id

# Feature image
def feature_image(keyword):
  try:
      feature_image = image_operation(keyword)
      imgurl_raw = feature_image.split('id":')[1]
      img_id = imgurl_raw.split(',')[0]
      return int(img_id)
  except:
      return 0


# It will go under a Loop while keyword reading
title = 'keyword'
keyword = 'keyword'.replace(' ', '-')
post_body = 'post_body'
category_id = create_category('keyword')
tag_id = create_tag('keyword')
img_id = feature_image('keyword')


post = {'title': title,
        'slug': keyword,
        'status': status,
        'content': post_body,
        'categories': [category_id],
        'tags': [tag_id],
        'format': 'standard',
        'featured_media': int(img_id),
        }

# Posting Request
r = scraper.post(json_url + '/posts', headers=headers, json=post)
if r.status_code == 201:
  print('https://' + website_name + '/' + keyword.replace(' ', '-') + ' Has Been Posted')
else:
  print(r.status_code,'error')

