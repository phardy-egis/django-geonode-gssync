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
    # Addition of gssync app
    INSTALLED_APPS += ('geonode.gssync',)
    ```

3. Include the gssync URLconf in `./geonode/urls.py` file like this:

    ```python
    if "geonode.gssync" in settings.INSTALLED_APPS:
        urlpatterns += [  # '',
            url(r'^gssync/', include('geonode.gssync.urls')),
        ]
    ```

4. Move `gssync` folder inside `./geonode` django project folder:


5. If you are using `docker`, rebuild geonode and restart services (this may stop the web site for a while):

    ```console
    docker-compose down && docker-compose build && docker-compose up -d
    ```

6. Once geonode has restarted, authneticated users with admins permissions can reach the page `/gsync` to perform synchronisation

### Install with pip

(Section not yet written)

## How to use

Once the app is running, go through the following steps :

1. [Publish a PostGIS table with GeoServer](https://docs.geoserver.org/stable/en/user/gettingstarted/postgis-quickstart/index.html)

2. With admin permissions, go to `example.com/gsync/` (replace `example.com` by your own domain name). 
    
    - You should reach the page below:
    ![Preview image](https://user-images.githubusercontent.com/111574152/193546103-6ca375c7-aff6-48ad-ac2f-1fb9bc70daca.png)

    - If 404 is returned, check if your user has administration rights.

3. Click on the button `Sync with GeoServer`. Once the green chekmark appear, you can navigate to the `Data` page. Your layers should be available here.

4. Be careful, these layers are published with Geonode's default permissions. <span style="color: red;">**So you must check the layer permissions right after publication.**</span>
