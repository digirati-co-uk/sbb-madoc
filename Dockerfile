# This is a pre-release
FROM digirati/madoc-platform:1.2.0

# Add our theme
ADD --chown=www-data:www-data ./custom-madoc-theme /srv/omeka/themes/custom-madoc-theme

# Add custom translations
ADD --chown=www-data:www-data ./translations/s/ /srv/omeka/translations/s/

# Add any other configuration needed.
