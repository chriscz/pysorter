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
        - RULE:      ('.*\.pdf', 'pdfs/')
          BEHAVIOUR: file1.pdf --> pdfs/file1.pdf

        - RULE:      ('.*\.pdf', 'pdfs')
          BEHAVIOUR: file1.pdf --> pdfs

    This applies similarly to directories

    More Examples:
        - Use predefined actions:
          - RULE:      (r'file1\.pdf', action.Skip)
          BEHAVIOUR: file1.pdf --> No action
          - RULE:      (r'/pdfs/', action.SkipRecure)
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
from pysorter import action

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
    raise RuntimeError("This pattern should never match a path: {}".format(path))


RULES = [
    (r'\.a2w$', 'alice_projects/'),
    (r'\.gz$', 'archives/'),
    (r'\.ace$', 'archives/'),
    (r'\.zip$', 'archives/'),
    (r'\.cab$', 'archives/windowscab/'),
    (r'\.tar$', 'archives/'),
    (r'\.rar$', 'archives/'),
    (r'\.7z$', 'archives/'),
    (r'\.bz2$', 'archives/'),
    (r'\.jar$', 'archives/jars/'),
    (r'\.aup$', 'projects/audacity_projects/'),
    (r'\.bwg$', 'projects/brain_wave_generator_projects/'),
    (r'\.sbk$', 'projects/scrapbook_factory/'),
    (r'\.cdr$', 'projects/corel/'),
    (r'\.mp3$', 'audio/'),
    (r'\.amr$', 'audio/amr/'),
    (r'\.m3u$', 'audio/playlist/'),
    (r'\.wav$', 'audio/'),
    (r'\.ogg$', 'audio/'),
    (r'\.midi$', 'audio/midi/'),
    (r'\.mid$', 'audio/midi/'),
    (r'\.wma$', 'audio/'),
    (r'\.flac$', 'audio/'),
    (r'\.m4a$', 'audio/'),
    (r'\.m4p$', 'audio/'),
    (r'\.m4r$', 'audio/'),
    (r'\.mp4$', 'videos/'),
    (r'\.wmv$', 'videos/'),
    (r'\.flv$', 'videos/flash/'),
    (r'\.avi$', 'videos/'),
    (r'\.3gp$', 'videos/3gp/'),
    (r'\.swf$', 'flash/swf/'),
    (r'\.m2ts$', 'videos/'),
    (r'\.m1v$', 'videos/'),
    (r'\.m2v$', 'videos/'),
    (r'\.mkv$', 'videos/'),
    (r'\.mov$', 'videos/'),
    (r'\.mp2$', 'videos/'),
    (r'\.mpe$', 'videos/'),
    (r'\.mpg$', 'videos/'),
    (r'\.mpeg$', 'videos/'),
    (r'\.svi$', 'videos/'),
    (r'\.vob$', 'videos/'),
    (r'\.webm$', 'videos/'),
    (r'\.srt$', 'videos/subtitles/'),
    (r'\.sub$', 'videos/subtitles/'),
    (r'\.sbv$', 'videos/subtitles/'),
    (r'\.ai$', 'images/illustrator/'),
    (r'\.jpeg$', 'images/jpg/'),
    (r'\.jpg$', 'images/jpg/'),
    (r'\.ico$', 'images/icons/'),
    (r'\.gif$', 'images/gif/'),
    (r'\.bmp$', 'images/bitmap/'),
    (r'\.png$', 'images/png/'),
    (r'\.psd$', 'images/photoshop/'),
    (r'\.svg$', 'images/svg/'),
    (r'\.xcf$', 'images/xcf/'),
    (r'\.tif$', 'images/tif/'),
    (r'\.webp$', 'images/webp/'),
    (r'\.rtf$', 'documents/writing/'),
    (r'\.nfo$', 'documents/info/'),
    (r'\.diz$', 'documents/info/'),
    (r'\.xls$', 'documents/spreadsheets/'),
    (r'\.xlr$', 'documents/spreadsheets/'),
    (r'\.xlsx$', 'documents/spreadsheets/'),
    (r'\.ods$', 'documents/spreadsheets/'),
    (r'\.tex$', 'documents/latex/'),
    (r'\.odt$', 'documents/writing/'),
    (r'\.doc$', 'documents/writing/'),
    (r'\.docx$', 'documents/writing/'),
    (r'\.wpd$', 'documents/writing/'),
    (r'\.wps$', 'documents/writing/'),
    (r'\.odb$', 'documents/databases/'),
    (r'\.key$', 'documents/presentations/'),
    (r'\.pps$', 'documents/presentations/'),
    (r'\.ppt$', 'documents/presentations/'),
    (r'\.pptx$', 'documents/presentations/'),
    (r'\.txt$', 'documents/plain_text/'),
    (r'\.pdf$', 'documents/pdf/'),
    (r'\.xps$', 'documents/xps/'),
    (r'\.msg$', 'documents/email/outlook/'),
    (r'\.msi$', 'installers/microsoft/'),
    (r'\.deb$', 'installers/debian/'),
    (r'\.exe$', 'installers/microsoft/'),
    (r'\.sis$', 'instalers/symbian/'),
    (r'\.apk$', 'instalers/android/'),
    (r'\.mht$', 'internet/saved_websites/'),
    (r'\.htm$', 'internet/saved_websites/'),
    (r'\.html$', 'internet/saved_websites/'),
    (r'\.url$', 'internet/url/'),
    (r'\.torrent$', 'internet/torrents/'),
    (r'\.xml$', 'xml/'),
    (r'\.vcs$', 'calendar/'),
    (r'\.vol$', 'virtual_encrypted_disk/'),
    (r'\.reg$', 'windowssystem/registry/'),
    (r'\.lnk$', 'windowssystem/shortcut/'),
    (r'\.ini$', 'windowssystem/configuration/ini/'),
    (r'\.inf$', 'windowssystem/configuration/inf/'),
    (r'\.c$', 'source/c/'),
    (r'\.cpp$', 'source/cpp/'),
    (r'\.py$', 'source/python/'),
    (r'\.java$', 'source/java/'),
    (r'\.c#$', 'source/c#/'),
    (r'\.dat$', 'data_files/'),
    (r'\.csv$', 'data_files/'),
    (r'\.iso$', 'disc_images/iso/'),
    (r'\.xpi$', 'firefox/extensions/'),
    (r'\.jad$', 'javame/jads/'),
    (r'\.fnt$', 'fonts/'),
    (r'\.fon$', 'fonts/'),
    (r'\.otf$', 'fonts/'),
    (r'\.ttf$', 'fonts/'),
    (r'\.gmx$', 'games/aoe_saved_games/'),
    (r'\.asb$', 'misc/hymn_assembler/'),
    (r'\.adr$', 'opera/addressbook_backups/'),
    (r'\.p2p$', 'peerguardian/lists/'),
    (r'\.vkp$', 'sony_ericsson/patches/'),
    (r'\.hid$', 'sony_ericsson/hid/'),
    (r'\.aswcs$', 'avast/themes/'),
    (r'\.vcf$', 'contacts/'),
    (r'\.cer$', 'certificates/'),

    DIRECTORIES,
]

RULES.extend(MIMETYPE_FALLBACKS)

RULES.extend([

    # wildcard patterns
    DIRECTORIES,
    FILES_WITH_EXTENSION,
    FILES_WITHOUT_EXTENSION,
    ('.*', impossible)
])
