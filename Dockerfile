FROM odoo:17.0
USER root
RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/Aaron-1933/Odoo-plugins.git /tmp/plugins && \
    cp -r /tmp/plugins/addons/mt_odoo_shopify_connector /usr/lib/python3/dist-packages/odoo/addons/ && \
    pip3 install ShopifyAPI
USER odoo