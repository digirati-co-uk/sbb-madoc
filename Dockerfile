# This is a pre-release
FROM digirati/madoc-platform:v1.3.x-917e3d2

# Add our theme
ADD --chown=www-data:www-data ./sbb-madoc-theme /srv/omeka/themes/sbb-madoc-theme

# Add custom translations
ADD --chown=www-data:www-data ./translations/s/ /srv/omeka/translations/s/

# Memory limit
ADD --chown=www-data:www-data ./etc/php.ini /etc/php.d/custom.ini

# Add any other configuration needed.
