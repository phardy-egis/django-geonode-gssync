# django-geonode-gssync
## About gssync
`gssync` stands for GeoServer SYNChronization. It is a Django app for Geonode that enable manual triggering of synchronization between geonode and geoserver from the web interface.

It is released under GNU-GPL licence version 3.

Detailed documentation is in the "docs" directory.

## Installation
### Manual install
Here below are listed the instruction for install:

1. If you are using `docker`, stop services

    ```console
    docker-compose down
    ```

2. Add "gssync" to your INSTALLED_APPS by adding the following lines at the end of `./geonode/settings.py` file:

    ```python
    if "geonode.gssync" in settings.INSTALLED_APPS:
        urlpatterns += [  # '',
            url(r'^gssync/', include('geonode.gssync.urls')),
        ]
    ```

3. Include the gssync URLconf in `./geonode/urls.py` project like this:

    ```python
    # Addition of gssync app
    INSTALLED_APPS += ('geonode.gssync',)
    ```

4. Move `gssync` folder inside `./geonode` django project folder:


5. If you are using `docker`, rebuild geonode and restart services (this may stop the web site for a while):

    ```console
    docker-compose down && docker-compose build && docker-compose up -d
    ```

6. Once geonode has restarted, authneticated users with admins permissions can reach the page `/gsync` to perform synchronisation

### Install with pip

(Section not yet written)