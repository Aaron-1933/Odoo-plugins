FROM odoo:17.0
USER root
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/Aaron-1933/Odoo-plugins.git /tmp/plugins && \
    cp -r /tmp/plugins/addons/* /mnt/extra-addons/
USER odoo