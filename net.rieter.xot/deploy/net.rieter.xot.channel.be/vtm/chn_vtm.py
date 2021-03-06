# coding:Cp1252
from datetime import datetime

import mediaitem
import chn_class
from logger import Logger


class Channel(chn_class.Channel):
    """
    main class from which all channels inherit
    """

    def __init__(self, channelInfo):
        """Initialisation of the class.

        Arguments:
        channelInfo: ChannelInfo - The channel info object to base this channel on.

        All class variables should be instantiated here and this method should not
        be overridden by any derived classes.

        """

        chn_class.Channel.__init__(self, channelInfo)

        # ============== Actual channel setup STARTS here and should be overwritten from derived classes ===============
        self.noImage = "vtmimage.png"

        # setup the urls
        self.mainListUri = "http://nieuws.vtm.be/herbekijk"
        self.baseUrl = "http://nieuws.vtm.be"

        # setup the main parsing data
        self.episodeItemRegex = '<li class="menu[^"]*"><a href="/([^l4"][^"]+)"[^>]+>([^>]+)</a></li>'
        self.videoItemRegex = 'is-video">\W+<a[^>]+>(?:<img src="([^"]+/videocms/image/)(\d+)([^"]+)"[^>]+></a>\W+</div>\W+){0,1}<div[^>]+>([^<]+)</div>\W+<h3 class="pagemanager-item-title">\W*<span>\W*<a href="/([^"]+)">([^<]+)'
        self.mediaUrlRegex = '<source src="([^"]+)" type="video/mp4"[^>]+>'
        self.pageNavigationRegex = ''
        self.pageNavigationRegexIndex = 0

        #===============================================================================================================
        # non standard items

        #===============================================================================================================
        # Test cases:

        # ====================================== Actual channel setup STOPS here =======================================
        return

    def CreateEpisodeItem(self, resultSet):
        """Creates a new MediaItem for an episode

        Arguments:
        resultSet : list[string] - the resultSet of the self.episodeItemRegex

        Returns:
        A new MediaItem of type 'folder'

        This method creates a new MediaItem from the Regular Expression or Json
        results <resultSet>. The method should be implemented by derived classes
        and are specific to the channel.

        """

        # dummy class
        item = mediaitem.MediaItem(resultSet[1], "%s/%s" % (self.baseUrl, resultSet[0]))
        item.complete = True
        item.icon = self.icon
        item.thumb = self.noImage
        item.complete = True
        return item

    def CreateVideoItem(self, resultSet):
        """Creates a MediaItem of type 'video' using the resultSet from the regex.

        Arguments:
        resultSet : tuple (string) - the resultSet of the self.videoItemRegex

        Returns:
        A new MediaItem of type 'video' or 'audio' (despite the method's name)

        This method creates a new MediaItem from the Regular Expression or Json
        results <resultSet>. The method should be implemented by derived classes
        and are specific to the channel.

        If the item is completely processed an no further data needs to be fetched
        the self.complete property should be set to True. If not set to True, the
        self.UpdateVideoItem method is called if the item is focussed or selected
        for playback.

        """
        thumbUrl = "%s%s%s" % (resultSet[0], resultSet[1], resultSet[2])
        year = resultSet[1]
        dayOrTime = resultSet[3]
        url = resultSet[4]
        title = resultSet[5]

        item = mediaitem.MediaItem(title, "%s/%s" % (self.baseUrl, url))
        item.type = 'video'

        if thumbUrl:
            item.thumb = thumbUrl
        else:
            item.thumb = self.noImage

        item.icon = self.icon

        if "/" in dayOrTime and year:
            # date found
            (day, month) = dayOrTime.split("/")
            item.SetDate(year, month, day, 0, 0, 0)
        elif "." in dayOrTime:
            # time found for today
            date = datetime.now()
            day = date.day
            month = date.month
            year = date.year
            (hour, minutes) = dayOrTime.split(".")
            item.SetDate(year, month, day, hour, minutes, 0)
        else:
            Logger.Warning("Could not determine date for item '%s' with datestring='%s'", title, dayOrTime)

        item.complete = False
        return item