"""
This file defines patterns and destination directories for files and directories matching the
given pattern.

    - Directory names can be assumed to always end in a `/`
    - For file rules, when the destination ends in  a `/`, the file would be placed
      inside the destination with that name. If the destination did not end in a `/`
      then the file will be renamed to the given destination, for example assume the
      following directory that is to be sorted.

      directory/
        - file1.pdf

    Consider the following rules and corresponding behaviour
        - RULE:      (r'.*\.pdf', 'pdfs/')
          BEHAVIOUR: file1.pdf --> pdfs/file1.pdf

        - RULE:      (r'.*\.pdf', 'pdfs')
          BEHAVIOUR: file1.pdf --> pdfs

    This applies similarly to directories

    More Examples:
        - Use predefined actions:
          - RULE:      (r'file1\.pdf', rules.Skip)
          BEHAVIOUR: file1.pdf --> No action
          - RULE:      (r'/pdfs/', rules.SkipRecure)
          BEHAVIOUR: /pdfs/file1.pdf --> No action
          BEHAVIOUR: /pdfs/another/file1.pdf --> No action
        - Numerical matching group
          - RULE:      (r'^(\d{4})-(\d{2})-.+?\.jpg$', 'images/{0}/{1}')
          BEHAVIOUR: 2016-03-12 13.34.21.jpg --> images/2016/03/2016-03-12 13.34.21.jpg
        - Named matching group
          - RULE:      (r'^(?P<year>\d{4})-(?P<month>\d{2})-.+?\.jpg$', 'images/{year}/{month}')
          BEHAVIOUR: 2016-03-12 13.34.21.jpg --> images/2016/03/2016-03-12 13.34.21.jpg
"""
# XXX Make sure all imports are absolute in this file, otherwise there will be
# problems using exec in rules.py
from pysorter import rules

import mimetypes
import re
mimetypes.init()

def normalize_mimetype(mt):
    """Normalization operations to make MIME types more human-friendly"""

    # remove x- in mime type, e.g. application/x-pdf -> application/pdf
    mt = mt.replace('/x-', '/')

    return mt

MIMETYPE_FALLBACKS = [
    ('{}$'.format(re.escape(ext)), '{}/'.format(normalize_mimetype(mt)))
    for ext, mt in mimetypes.types_map.items()
]

# general matching rule
DIRECTORIES = (r'(^|/)(?P<name>[^/]+)/$', 'directories/{name}')
FILES_WITH_EXTENSION = (r'(^|/)(?P<name>[^/]+)\.(?P<ext>[^/]+)$', 'other/{ext}_files/')
FILES_WITHOUT_EXTENSION = (r'(^|/)(?P<name>[^/]+)$', 'other/')


def impossible(match, path):
    raise RuntimeError("This pattern should never match a path: {}".format(path)) # pragma: no cover


RULES = [
    (r'\.(?i)a2w$', 'alice_projects/'),
    (r'\.(?i)gz$', 'archives/'),
    (r'\.(?i)ace$', 'archives/'),
    (r'\.(?i)zip$', 'archives/'),
    (r'\.(?i)cab$', 'archives/cab/'),
    (r'\.(?i)tar$', 'archives/'),
    (r'\.(?i)rar$', 'archives/'),
    (r'\.(?i)7z$', 'archives/'),
    (r'\.(?i)bz2$', 'archives/'),
    (r'\.(?i)jar$', 'archives/jar/'),
    (r'\.(?i)iso$', 'archives/iso/'),
    (r'\.(?i)aup$', 'projects/audacity_projects/'),
    (r'\.(?i)bwg$', 'projects/brain_wave_generator_projects/'),
    (r'\.(?i)sbk$', 'projects/scrapbook_factory/'),
    (r'\.(?i)cdr$', 'projects/corel/'),
    (r'\.(?i)mp3$', 'audio/'),
    (r'\.(?i)amr$', 'audio/amr/'),
    (r'\.(?i)m3u$', 'audio/playlist/'),
    (r'\.(?i)wav$', 'audio/'),
    (r'\.(?i)ogg$', 'audio/'),
    (r'\.(?i)midi$', 'audio/midi/'),
    (r'\.(?i)mid$', 'audio/midi/'),
    (r'\.(?i)wma$', 'audio/'),
    (r'\.(?i)flac$', 'audio/'),
    (r'\.(?i)m4a$', 'audio/'),
    (r'\.(?i)m4p$', 'audio/'),
    (r'\.(?i)m4r$', 'audio/'),
    (r'\.(?i)mp4$', 'videos/'),
    (r'\.(?i)wmv$', 'videos/'),
    (r'\.(?i)flv$', 'videos/flash/'),
    (r'\.(?i)avi$', 'videos/'),
    (r'\.(?i)3gp$', 'videos/3gp/'),
    (r'\.(?i)swf$', 'flash/swf/'),
    (r'\.(?i)m2ts$', 'videos/'),
    (r'\.(?i)m1v$', 'videos/'),
    (r'\.(?i)m2v$', 'videos/'),
    (r'\.(?i)mkv$', 'videos/'),
    (r'\.(?i)mov$', 'videos/'),
    (r'\.(?i)mp2$', 'videos/'),
    (r'\.(?i)mpe$', 'videos/'),
    (r'\.(?i)mpg$', 'videos/'),
    (r'\.(?i)mpeg$', 'videos/'),
    (r'\.(?i)svi$', 'videos/'),
    (r'\.(?i)vob$', 'videos/'),
    (r'\.(?i)webm$', 'videos/'),
    (r'\.(?i)srt$', 'videos/subtitles/'),
    (r'\.(?i)sub$', 'videos/subtitles/'),
    (r'\.(?i)sbv$', 'videos/subtitles/'),
    (r'\.(?i)ai$', 'images/illustrator/'),
    (r'\.(?i)jpeg$', 'images/jpg/'),
    (r'\.(?i)jpg$', 'images/jpg/'),
    (r'\.(?i)ico$', 'images/icons/'),
    (r'\.(?i)gif$', 'images/gif/'),
    (r'\.(?i)bmp$', 'images/bitmap/'),
    (r'\.(?i)png$', 'images/png/'),
    (r'\.(?i)psd$', 'images/photoshop/'),
    (r'\.(?i)svg$', 'images/svg/'),
    (r'\.(?i)xcf$', 'images/xcf/'),
    (r'\.(?i)tif$', 'images/tif/'),
    (r'\.(?i)webp$', 'images/webp/'),
    (r'\.(?i)rtf$', 'documents/writing/'),
    (r'\.(?i)nfo$', 'documents/info/'),
    (r'\.(?i)diz$', 'documents/info/'),
    (r'\.(?i)xls$', 'documents/spreadsheets/'),
    (r'\.(?i)xlr$', 'documents/spreadsheets/'),
    (r'\.(?i)xlsx$', 'documents/spreadsheets/'),
    (r'\.(?i)ods$', 'documents/spreadsheets/'),
    (r'\.(?i)tex$', 'documents/latex/'),
    (r'\.(?i)odt$', 'documents/writing/'),
    (r'\.(?i)doc$', 'documents/writing/'),
    (r'\.(?i)docx$', 'documents/writing/'),
    (r'\.(?i)wpd$', 'documents/writing/'),
    (r'\.(?i)wps$', 'documents/writing/'),
    (r'\.(?i)odb$', 'documents/databases/'),
    (r'\.(?i)key$', 'documents/presentations/'),
    (r'\.(?i)pps$', 'documents/presentations/'),
    (r'\.(?i)ppt$', 'documents/presentations/'),
    (r'\.(?i)pptx$', 'documents/presentations/'),
    (r'\.(?i)txt$', 'documents/plain_text/'),
    (r'\.(?i)pdf$', 'documents/pdf/'),
    (r'\.(?i)xps$', 'documents/xps/'),
    (r'\.(?i)msg$', 'documents/email/outlook/'),
    (r'\.(?i)msi$', 'installers/microsoft/'),
    (r'\.(?i)deb$', 'installers/debian/'),
    (r'\.(?i)exe$', 'installers/microsoft/'),
    (r'\.(?i)sis$', 'instalers/symbian/'),
    (r'\.(?i)apk$', 'instalers/android/'),
    (r'\.(?i)mht$', 'internet/saved_websites/'),
    (r'\.(?i)htm$', 'internet/saved_websites/'),
    (r'\.(?i)html$', 'internet/saved_websites/'),
    (r'\.(?i)url$', 'internet/url/'),
    (r'\.(?i)torrent$', 'internet/torrents/'),
    (r'\.(?i)vcs$', 'calendar/'),
    (r'\.(?i)vol$', 'virtual_encrypted_disk/'),
    (r'\.(?i)reg$', 'windows_system/registry/'),
    (r'\.(?i)lnk$', 'windows_system/shortcut/'),
    (r'\.(?i)ini$', 'windows_system/configuration/ini/'),
    (r'\.(?i)inf$', 'windows_system/configuration/inf/'),
    (r'\.(?i)c$', 'source_code/c/'),
    (r'\.(?i)cpp$', 'source_code/cpp/'),
    (r'\.(?i)py$', 'source_code/python/'),
    (r'\.(?i)java$', 'source_code/java/'),
    (r'\.(?i)cs$', 'source_code/csharp/'),
    (r'\.(?i)dat$', 'data_exchange/dat/'),
    (r'\.(?i)csv$', 'data_exchange/csv/'),
    (r'\.(?i)json$', 'data_exchange/json/'),
    (r'\.(?i)xml$', 'data_exchange/xml/'),
    (r'\.(?i)xpi$', 'applications/firefox/extensions/'),
    (r'\.(?i)jad$', 'applications/avame/jads/'),
    (r'\.(?i)fnt$', 'fonts/'),
    (r'\.(?i)fon$', 'fonts/'),
    (r'\.(?i)otf$', 'fonts/'),
    (r'\.(?i)ttf$', 'fonts/'),
    (r'\.(?i)gmx$', 'games/aoe_saved_games/'),
    (r'\.(?i)asb$', 'misc/hymn_assembler/'),
    (r'\.(?i)adr$', 'applications/opera/addressbook_backups/'),
    (r'\.(?i)p2p$', 'applications/peerguardian/lists/'),
    (r'\.(?i)vkp$', 'applications/sony_ericsson/patches/'),
    (r'\.(?i)hid$', 'applications/sony_ericsson/hid/'),
    (r'\.(?i)aswcs$', 'applications/avast/themes/'),
    (r'\.(?i)vcf$', 'contacts/'),
    (r'\.(?i)cer$', 'certificates/'),
]

RULES.extend(MIMETYPE_FALLBACKS)

RULES.extend([

    # wildcard patterns
    DIRECTORIES,
    FILES_WITH_EXTENSION,
    FILES_WITHOUT_EXTENSION,
    ('.*', impossible)
])
