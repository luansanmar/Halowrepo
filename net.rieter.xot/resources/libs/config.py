import os
import xml.dom.minidom

import xbmc

from version import Version


class Config:
    """Class with all the configuration constants"""

    def __init__(self):
        pass

    try:
        import xbmcaddon
        # calling xbmcaddon.Addon() only works on newer XBMC's. Should see if it keeps working
        # if not, then the addonId should be hard coded here.
        __addon = xbmcaddon.Addon()
        __path = __addon.getAddonInfo('path')
        __addon = None  # : Free up the static variable to make sure it is garbage collected
        pathDetection = "addon.getAddonInfo('path')"
    except:
        xbmc.log("Retrospect: using os.getcwd()", xbmc.LOGWARNING)
        __path = os.getcwd()
        pathDetection = "os.getcwd()"

    # the XBMC libs return unicode info, so we need to convert this
    #noinspection PyArgumentEqualDefault
    __path = __path.decode('utf-8')

    # get rootDir, addonsDir and profileDir
    rootDir = __path.replace(";", "")                       # : The root directory where XOT resides.
    addonDir = os.path.split(rootDir)[-1]                   # : The add-on directory of XBMC.
    rootDir = os.path.join(rootDir, '')                     # : The root directory where XOT resides.

    # determine the profile directory, where user data is stored.
    if xbmc.getCondVisibility("system.platform.xbox"):
        profileDir = os.path.join(xbmc.translatePath("special://profile/script_data/"), addonDir)
    else:
        profileDir = os.path.join(xbmc.translatePath("special://profile/addon_data/"), addonDir)

    # the XBMC libs return unicode info, so we need to convert this
    #noinspection PyArgumentEqualDefault
    profileDir = profileDir.decode('utf-8')

    cacheDir = os.path.join(profileDir, 'cache', '')        # : The cache directory.
    favouriteDir = os.path.join(profileDir, 'favourites')   # : The favourites directory

    appName = "Retrospect"                                  # : Name of the XOT application (could be overwritten from the addon.xml)
    cacheValidTime = 7 * 24 * 3600                          # : Time the cache files are valid in seconds.
    webTimeOut = 30                                         # : Maximum wait time for HTTP requests.

    logLevel = 10                                           # : Minimum log level that is being logged. (from logger.py) Defaults to Debug
    logFileNameAddon = "retrospect.log"                     # : Filename of the log file of the plugin version

    retroDb = os.path.join(profileDir, "retrospect.db")     # : Filename of the XOT DB file

    # must be single quotes for build script
    __addonXmlPath = os.path.join(rootDir, 'addon.xml')
    __addonXmlcontents = xml.dom.minidom.parse(__addonXmlPath)
    for addonentry in __addonXmlcontents.getElementsByTagName("addon"):
        addonId = str(addonentry.getAttribute("id"))        # : The ID the addon has in XBMC (from addon.xml)
        __version = addonentry.getAttribute("version")      # : The Version of the addon (from addon.xml)
        version = Version(version=__version)                # : The Version of the addon (from addon.xml)
        #noinspection PyRedeclaration
        appName = str(addonentry.getAttribute("name"))      # : The name from the addon (from addon.xml)

    UpdateUrl = "http://www.rieter.net" \
                "/net.rieter.xot.repository" \
                "/addons.xml.md5"                           # : The URL that is called to check for updates.
                                                            # : should return "" if no update is available

    CdnUrl = None                                           # : The URL for the CDN servers (None for local)
    # CdnUrl = "http://cdn.rieter.net/"                       # : The URL for the CDN servers (None for local)