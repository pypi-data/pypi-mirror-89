# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['facebook_feed_sync', 'facebook_feed_sync.packages']

package_data = \
{'': ['*']}

install_requires = \
['gspread-dataframe>=3.1.1,<4.0.0',
 'gspread>=3.6.0,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pandas>=1.1.3,<2.0.0',
 'plenty_api>=0.2.4,<0.3.0',
 'pytest_describe>=1.0.0,<2.0.0',
 'pytest_mock>=3.3.1,<4.0.0',
 'pytest_sugar>=0.9.4,<0.10.0']

setup_kwargs = {
    'name': 'facebook-feed-sync',
    'version': '0.2.0',
    'description': 'Lightweight connector of PlentyMarkets to Facebook Catalogs via a google-spreadsheet. Update product information regulary and import data to facebook.',
    'long_description': "# facebook_feed_sync\nUpdate a google sheet with data from the Plentymarkets API for a Facebook catalog feed.\n\n## Installation:\n\n**Prepare the folder structure and get google sheet API access**\n1. Place the credentials file from : [Google Sheet API](https://developers.google.com/sheets/api/quickstart/python) as **'credentials.json'** (example: mv ~/Downloads/credentials.json /home/$USER/.config/gspread/credentials.json) into the config folder for `gspread`.\n2. Place the `config.ini` file into the `facebook_feed_sync` config folder\n    + Linux: /home/$USER/.config/facebook_feed_sync/config.ini\n    + Windows: C:\\\\\\\\$USER\\\\.config\\\\facebook_feed_sync\\\\config.ini\n\nHere is an example for the config file:\n```ini\n[General]\ngoogle_sheet_id=\nplenty_api_url=\nlang=\n[Mapping]\nfacebook_referrer=\nimage_match_criteria=\nitem_name_number=\ngender_item_property=\nage_item_property=\ngoogle_product_category_item_property=\nmaterial_variation_property=\nurl_variation_property=\nsales_price_id=\ncolor_attribute_id=\nsize_attribute_id=\nmain_warehouse=\n```\n3. Get the ID of the target marketplace or Create a new marketplace availability:\n    + `{plenty-cloud-domain}/plenty/terra/system/orders/referrer`\n    + activate it and add the ID to the configuration.\n4. Set the marketplace availability for every variation you want to present on facebook.\n5. Create new variation or item properties(characteristics) for these fields or link existing properties:\n    + Item properties (characteristics)  \n    `{plenty-cloud-domain}/plenty/terra/system/item/character`\n        * **gender_item_property** [facebook: `gender`] (target audience gender: 'Men', 'Women', 'Unisex')\n        * **age_item_property** [facebook: `age_group`] (target audience age group: 'Adult' or 'Child')\n        * **google_product_category_item_property** [facebook: `google_product_category`] (Text value of your google product category, see: [list](https://www.google.com/basepages/producttype/taxonomy-with-ids.en-US.txt))\n    + Variation properties  \n     `{plenty-cloud-domain}/plenty/terra/system/settings/properties/configuration/overview`\n        * **material_variation_property** [facebook: `material`] (material type of the product e.g. Cotton, Hemp etc.)\n        * **url_variation_property** [facebook: `link`] (Link to your webshop)\n6. Choose the criteria by which valid pictures are chosen for each variation, the picture with the lowest position of the images found is used for Facebook.  \n   Example values: `image_match_criteria=mandant;12345`, `image_match_criteria=marketplace;4.01`.\n7. Add the IDs of the properties to the matching configuration entry\n8. Assign the facebook market availability to on of your prices: `{plenty-cloud-domain}/plenty/terra/system/item/sales-price` and make sure that all variations contain a price. Then add the ID of the price to the configuration field: `sales_price_id`\n9. Choose one of the three possible item names: `name1`, `name2` or `name3` and add the number of the name to the configuration field: `item_name_number`\n10. Assign the IDs of your color and size attribute to the configuration fields: `color_attribute_id` and `size_attribute_id`\n11. Assign the ID of the warehouse used for shipping to the configuration field: `main_warehouse`\n12. Fill the properties with values and then add the IDs of the properties to the configuration\n13. Create a google sheet and add the following header to it:\n    - `id,title,description,availability,inventory,condition,price,link,image_link,brand,google_product_category,sale_price,sale_price_effective_date,item_group_id,gender,color,size,age_group,material,pattern,product_type,shipping,shipping_weight`\n    - Insert the text then select the field and go to **Data->Split text into columns**\n14. Get your Google Sheet ID:\n    + Example URL: `https://docs.google.com/spreadsheets/d/`**{SHEET ID}**`/edit?pli=1#gid=0`\n    + Insert it into the configuration.\n15. Make an initial setup of the sheet with: `python3 -m facebook_feed_sync -t all`\n16. Check if the google sheet looks good and go on **Share** at the top right and change access rights to anyone with the link\n17. Go to your business manager (catalogs) [https://business.facebook.com/products/catalogs/](https://business.facebook.com/products/catalogs/), create a new datafeed: Catalog -> data-feeds -> Add products -> Use bulk upload -> Google Spreadsheets -> Next -> Insert the full link -> Choose the upload schedule.\n18. Setup the cronjob to run the script preferably on a device, which has a constant uptime (I use a raspberry Pi for example)\n",
    'author': 'Sebastian Fricke',
    'author_email': 'sebastian.fricke.linux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/initBasti/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
