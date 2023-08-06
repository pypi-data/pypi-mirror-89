# BDF (Glyph Bitmap Distribution Format) Bitmap Font File Parser in Python
# Copyright (c) 2017-2021 Tom CHEN (tomchen.org), MIT License
# https://font.tomchen.org/bdfparser_py/


import re
import io
import warnings
from sys import version_info as python_version


def format_warning(message, category, filename, lineno, file=None, line=None):
    return '%s:%s\n%s: %s\n' % (filename, lineno, 'bdfparser warning', message)


warnings.formatwarning = format_warning


class Font(object):

    __PATTERN_VVECTOR_DELIMITER = re.compile(r'[,\s]+')

    __META_TITLES = [
        'glyphname',
        'codepoint',
        'bbw',
        'bbh',
        'bbxoff',
        'bbyoff',
        'swx0',
        'swy0',
        'dwx0',
        'dwy0',
        'swx1',
        'swy1',
        'dwx1',
        'dwy1',
        'vvectorx',
        'vvectory',
        'hexdata',
    ]

    def __init__(self, *argv):

        if python_version < (3, 7, 0):
            from collections import OrderedDict as ordered_dict
        else:
            ordered_dict = dict
        self.glyphs = ordered_dict()

        self.headers = {}
        self.props = {}

        self.__glyph_count_to_check = None
        self.__curline_startchar = None
        self.__curline_chars = None

        l = len(argv)
        if l == 1:
            arg = argv[0]
            if isinstance(arg, str):
                self.load_file_path(arg)
            elif isinstance(arg, io.IOBase):
                self.load_file_obj(arg)

    def load_file_path(self, file_path):
        with open(file_path) as file_obj:
            self.load_file_obj(file_obj)
        return self

    def load_file_obj(self, file_obj):
        self.__f = file_obj
        self.__parse_headers()
        return self

    def __parse_headers(self):

        while 1:

            line = next(self.__f)
            kvlist = line.split(None, 1)
            l = len(kvlist)

            if l == 2:
                key = kvlist[0]
                value = kvlist[1].strip()
                if key == 'STARTFONT':
                    self.headers['bdfversion'] = float(value)
                elif key == 'FONT':
                    self.headers['fontname'] = value
                elif key == 'SIZE':
                    nlist = value.split()
                    self.headers['pointsize'] = int(nlist[0])
                    self.headers['xres'] = int(nlist[1])
                    self.headers['yres'] = int(nlist[2])
                elif key == 'FONTBOUNDINGBOX':
                    nlist = value.split()
                    self.headers['fbbx'] = int(nlist[0])
                    self.headers['fbby'] = int(nlist[1])
                    self.headers['fbbxoff'] = int(nlist[2])
                    self.headers['fbbyoff'] = int(nlist[3])
                elif key == 'STARTPROPERTIES':
                    self.__parse_headers_after()
                    self.__parse_props()
                    return
                elif key == 'COMMENT':
                    comment = 'comment'
                    if comment not in self.headers:
                        self.headers[comment] = []
                    self.headers[comment].append(value)
                elif key == 'SWIDTH':
                    nlist = value.split()
                    self.headers['swx0'] = int(nlist[0])
                    self.headers['swy0'] = int(nlist[1])
                elif key == 'DWIDTH':
                    nlist = value.split()
                    self.headers['dwx0'] = int(nlist[0])
                    self.headers['dwy0'] = int(nlist[1])
                elif key == 'SWIDTH1':
                    nlist = value.split()
                    self.headers['swx1'] = int(nlist[0])
                    self.headers['swy1'] = int(nlist[1])
                elif key == 'DWIDTH1':
                    nlist = value.split()
                    self.headers['dwx1'] = int(nlist[0])
                    self.headers['dwy1'] = int(nlist[1])
                elif key == 'VVECTOR':
                    nlist = self.__PATTERN_VVECTOR_DELIMITER.split(value)
                    self.headers['vvectorx'] = int(nlist[0])
                    self.headers['vvectory'] = int(nlist[1])
                elif key == 'METRICSSET' or key == 'CONTENTVERSION':
                    self.headers[key.lower()] = int(value)
                elif key == 'CHARS':
                    warnings.warn(
                        "It looks like the font does not have property block beginning with 'STARTPROPERTIES' keyword")
                    self.__parse_headers_after()
                    self.__curline_chars = line
                    self.__parse_glyph_count()
                    return
                elif key == 'STARTCHAR':
                    warnings.warn(
                        "It looks like the font does not have property block beginning with 'STARTPROPERTIES' keyword")
                    warnings.warn("Cannot find 'CHARS' line")
                    self.__parse_headers_after()
                    self.__curline_startchar = line
                    self.__prepare_glyphs()
                    return

            if l == 1 and kvlist[0].strip() == 'ENDFONT':
                warnings.warn(
                    "It looks like the font does not have property block beginning with 'STARTPROPERTIES' keyword")
                warnings.warn("This font does not have any glyphs")
                return

    def __parse_headers_after(self):
        if 'metricsset' not in self.headers:
            self.headers['metricsset'] = 0

    def __parse_props(self):

        while 1:

            line = next(self.__f)
            kvlist = line.split(None, 1)
            l = len(kvlist)

            if l == 2:
                key = kvlist[0]
                value = kvlist[1].strip(' "\'\t\r\n')
                if key == 'COMMENT':
                    comment = 'comment'
                    if comment not in self.props:
                        self.props[comment] = []
                    self.props[comment].append(value)
                else:
                    self.props[key.lower()] = value
            elif l == 1:
                key = kvlist[0].strip()
                if key == 'ENDPROPERTIES':
                    self.__parse_glyph_count()
                    return
                if key == 'ENDFONT':
                    warnings.warn("This font does not have any glyphs")
                    return
                else:
                    self.props[key] = None

    def __parse_glyph_count(self):

        if self.__curline_chars is None:
            line = next(self.__f)
        else:
            line = self.__curline_chars
            self.__curline_chars = None

        if line.strip() == 'ENDFONT':
            warnings.warn("This font does not have any glyphs")
            return

        kvlist = line.split(None, 1)
        if kvlist[0] == 'CHARS':
            self.__glyph_count_to_check = int(kvlist[1].strip())
        else:
            self.__curline_startchar = line
            warnings.warn(
                "Cannot find 'CHARS' line next to 'ENDPROPERTIES' line")
        self.__prepare_glyphs()

    def __prepare_glyphs(self):

        glyph_meta = []
        glyph_bitmap = []
        glyph_bitmap_is_on = False

        STARTCHAR_used = ENCODING_used = BBX_used = SWIDTH_used = DWIDTH_used = SWIDTH1_used = DWIDTH1_used = VVECTOR_used = BITMAP_used = glyph_end = False

        while 1:
            if self.__curline_startchar is None:
                line = next(self.__f, None)
            else:
                line = self.__curline_startchar
                self.__curline_startchar = None

            if line is None:
                warnings.warn("This font does not have 'ENDFONT' keyword")
                self.__prepare_glyphs_after()
                return

            kvlist = line.split(None, 1)
            l = len(kvlist)

            if l == 2:
                key = kvlist[0]
                value = kvlist[1].strip()
                if not STARTCHAR_used and key == 'STARTCHAR':
                    glyph_meta = [None] * 17
                    glyph_meta[0] = value
                    STARTCHAR_used = True
                    glyph_end = False
                elif not ENCODING_used and key == 'ENCODING':
                    glyph_codepoint = int(value)
                    glyph_meta[1] = glyph_codepoint
                    ENCODING_used = True
                elif not BBX_used and key == 'BBX':
                    nlist = value.split()
                    glyph_meta[2] = int(nlist[0])
                    glyph_meta[3] = int(nlist[1])
                    glyph_meta[4] = int(nlist[2])
                    glyph_meta[5] = int(nlist[3])
                    BBX_used = True
                elif not SWIDTH_used and key == 'SWIDTH':
                    nlist = value.split()
                    glyph_meta[6] = int(nlist[0])
                    glyph_meta[7] = int(nlist[1])
                    SWIDTH_used = True
                elif not DWIDTH_used and key == 'DWIDTH':
                    nlist = value.split()
                    glyph_meta[8] = int(nlist[0])
                    glyph_meta[9] = int(nlist[1])
                    DWIDTH_used = True
                elif not SWIDTH1_used and key == 'SWIDTH1':
                    nlist = value.split()
                    glyph_meta[10] = int(nlist[0])
                    glyph_meta[11] = int(nlist[1])
                    SWIDTH1_used = True
                elif not DWIDTH1_used and key == 'DWIDTH1':
                    nlist = value.split()
                    glyph_meta[12] = int(nlist[0])
                    glyph_meta[13] = int(nlist[1])
                    DWIDTH1_used = True
                elif not VVECTOR_used and key == 'VVECTOR':
                    nlist = self.__PATTERN_VVECTOR_DELIMITER.split(value)
                    glyph_meta[14] = int(nlist[0])
                    glyph_meta[15] = int(nlist[1])
                    VVECTOR_used = True

            elif l == 1:
                key = kvlist[0].strip()
                if not BITMAP_used and key == 'BITMAP':
                    glyph_bitmap = []
                    glyph_bitmap_is_on = True
                    BITMAP_used = True
                elif key == 'ENDCHAR':
                    glyph_bitmap_is_on = False
                    glyph_meta[16] = glyph_bitmap
                    self.glyphs[glyph_codepoint] = glyph_meta
                    STARTCHAR_used = ENCODING_used = BBX_used = SWIDTH_used = DWIDTH_used = SWIDTH1_used = DWIDTH1_used = VVECTOR_used = BITMAP_used = False
                    glyph_end = True
                elif glyph_end and key == 'ENDFONT':
                    self.__prepare_glyphs_after()
                    return
                elif glyph_bitmap_is_on:
                    glyph_bitmap.append(key)

    def __prepare_glyphs_after(self):
        l = len(self.glyphs)
        if self.__glyph_count_to_check != l:
            if self.__glyph_count_to_check is None:
                warnings.warn(
                    "The glyph count next to 'CHARS' keyword does not exist")
            else:
                warnings.warn(
                    "The glyph count next to 'CHARS' keyword is " +
                    str(self.__glyph_count_to_check) +
                    ", which does not match the actual glyph count " + str(l)
                )
                # Use old style for Python 3.5 support. For 3.6+:
                # f"The glyph count next to 'CHARS' keyword is {str(self.__glyph_count_to_check)}, which does not match the actual glyph count {str(l)}"

    def length(self):
        return len(self.glyphs)

    def __len__(self):
        return self.length()

    def itercps(self, order=1, r=None):
        # https://font.tomchen.org/bdfparser_py/font/#iterglyphs

        ks = self.glyphs.keys()
        if order == 1:
            retiterator = iter(sorted(ks))
        elif order == 0:
            retiterator = iter(ks)
        elif order == 2:
            retiterator = iter(sorted(ks, reverse=True))
        elif order == -1:
            try:
                retiterator = reversed(ks)
            except TypeError:
                retiterator = reversed(list(ks))  # Python <=3.7
        if r is not None:
            def f(cp):
                if isinstance(r, int):
                    return cp < r
                elif isinstance(r, tuple):
                    return cp <= r[1] and cp >= r[0]
                elif isinstance(r, list):
                    for t in r:
                        if cp <= t[1] and cp >= t[0]:
                            return True
                    return False
            retiterator = filter(f, retiterator)
        return retiterator

    def iterglyphs(self, order=1, r=None):
        for cp in self.itercps(order, r):
            yield self.glyphbycp(cp)

    def glyphbycp(self, codepoint):
        if codepoint not in self.glyphs:
            raise Exception(
                "Glyph \"" + chr(codepoint) + "\" (codepoint " +
                str(codepoint) + ") does not exist in the font"
            )
            # Use old style for Python 3.5 support. For 3.6+:
            # f"Glyph \"{chr(codepoint)}\" (codepoint {str(codepoint)}) does not exist in the font"
        return Glyph(dict(zip(self.__META_TITLES, self.glyphs[codepoint])), self)

    def glyph(self, character):
        return self.glyphbycp(ord(character))

    def drawcps(self, cps, linelimit=512, mode=1, direction='lrtb', usecurrentglyphspacing=False):
        # https://font.tomchen.org/bdfparser_py/font#draw

        dire_shortcut_dict = {
            'lr': 'lrtb',
            'rl': 'rltb',
            'tb': 'tbrl',
            'bt': 'btrl',
        }
        dire = dire_shortcut_dict.get(direction) or direction
        dire_dict = {
            'lr': 1,
            'rl': 2,
            'tb': 0,
            'bt': -1,
        }
        dire_glyph_str = dire[0:2]
        dire_line_str = dire[2:4]
        if dire_glyph_str in dire_dict and dire_line_str in dire_dict:
            dire_glyph = dire_dict[dire_glyph_str]
            dire_line = dire_dict[dire_line_str]
        else:
            dire_glyph = 1
            dire_line = 0

        if dire_line == 0 or dire_line == 2:  # 'xxtb' or 'xxrl'
            align_glyph = 1  # bottom or left
        elif dire_line == 1 or dire_line == -1:  # 'xxlr' or 'xxbt'
            align_glyph = 0  # right or top

        if dire_glyph == 1 or dire_glyph == -1:  # 'lrxx' or 'btxx'
            align_line = 1  # left or bottom
        elif dire_glyph == 2 or dire_glyph == 0:  # 'rlxx' or 'tbxx'
            align_line = 0  # right or top

        if mode == 1:  # dwidth / dwidth1 mode
            # 'lrxx'/'rlxx' else 'tbxx'/'btxx'
            fbbsize = self.headers['fbbx'] if dire_glyph > 0 else self.headers['fbby']

            if dire_glyph > 0:  # 'lrxx'/'rlxx'
                # interglyph_keyword = 'DWIDTH'
                interglyph_str = 'dwx0'
                interglyph_str2 = 'dwy0'
            else:  # 'tbxx'/'btxx'
                # interglyph_keyword = 'DWIDTH1'
                interglyph_str = 'dwx1'
                interglyph_str2 = 'dwy1'

            if interglyph_str in self.headers:
                interglyph_global = self.headers[interglyph_str]
            elif interglyph_str2 in self.headers:
                interglyph_global = self.headers[interglyph_str2]
            else:
                interglyph_global = None
                # warnings.warn("The font do not have `" + interglyph_keyword + "`, glyph spacing adjustment could be skipped unless present in individual glyphs")
                # # Use old style for Python 3.5 support. For 3.6+:
                # # warnings.warn(f"The font do not have `{interglyph_keyword}`, glyph spacing adjustment could be skipped unless present in individual glyphs")

        list_of_bitmaplist = []
        bitmaplist = []
        list_of_offsetlist = []
        offsetlist = []
        size = 0

        def append_bitmaplist_and_offsetlist():
            list_of_bitmaplist.append(bitmaplist)
            if usecurrentglyphspacing:
                offsetlist.pop(0)
            else:  # use previous glyph spacing (default)
                offsetlist.pop()
            list_of_offsetlist.append(offsetlist)

        cpsiter = iter(cps)
        skip = False
        while 1:
            if skip:
                skip = False
            else:
                cp = next(cpsiter, None)
                if cp is None:
                    break

                glyph = self.glyphbycp(cp)
                bitmap = glyph.draw()
                w = bitmap.width()

                offset = 0
                if mode == 1:
                    interglyph = glyph.meta[interglyph_str] or glyph.meta[interglyph_str2]
                    if interglyph is None:
                        interglyph = interglyph_global
                    if interglyph is not None:
                        offset = interglyph - fbbsize

            size += w + offset
            if size <= linelimit:
                bitmaplist.append(bitmap)
                offsetlist.append(offset)
            else:
                if len(bitmaplist) == 0:
                    raise Exception(
                        "`linelimit` (" + linelimit + ") is too small the line can't even contain one glyph: \"" +
                        glyph.chr() + "\" (codepoint " + cp + ", width: " + w + ")"
                    )
                    # Use old style for Python 3.5 support. For 3.6+:
                    # f"`linelimit` ({linelimit}) is too small the line can't even contain one glyph: \"{glyph.chr()}\" (codepoint {cp}, width: {w})"
                append_bitmaplist_and_offsetlist()
                size = 0
                bitmaplist = []
                offsetlist = []
                skip = True
        if len(bitmaplist) != 0:
            append_bitmaplist_and_offsetlist()

        list_of_bitmap_line_lists = [Bitmap.concatall(bitmaplist, direction=dire_glyph, align=align_glyph,
                                                      offsetlist=list_of_offsetlist[i]) for i, bitmaplist in enumerate(list_of_bitmaplist)]

        return Bitmap.concatall(list_of_bitmap_line_lists, direction=dire_line, align=align_line)

    def draw(self, string, linelimit=512, mode=1, direction='lrtb', usecurrentglyphspacing=False):
        return self.drawcps((ord(cp) for cp in string), linelimit, mode, direction, usecurrentglyphspacing)

    def drawall(self, order=1, r=None, linelimit=512, mode=0, direction='lrtb', usecurrentglyphspacing=False):
        return self.drawcps(self.itercps(order, r), linelimit, mode, direction, usecurrentglyphspacing)


class Glyph(object):

    def __init__(self, meta_dict, font):
        self.meta = meta_dict
        self.font = font

    def __str__(self):
        return str(self.draw())

    def __repr__(self):
        return 'Glyph(' + str(self.meta) + ', ' + str(self.font) + ')'

    def cp(self):
        return self.meta['codepoint']

    def chr(self):
        return chr(self.cp())

    def draw(self, mode=0, bb=None):
        # https://font.tomchen.org/bdfparser_py/glyph#draw

        if mode == 0:
            retbitmap = self.__draw_fbb()
        elif mode == 1:
            retbitmap = self.__draw_bb()
        elif mode == 2:
            retbitmap = self.__draw_original()
        elif mode == -1 and bb is not None:
            retbitmap = self.__draw_user_specified(bb)
        elif mode == -1 and bb is None:
            raise Exception(
                'Parameter bb in draw() method must be set when mode=-1')
        return retbitmap

    def __draw_user_specified(self, fbb):
        bbxoff = self.meta.get('bbxoff')
        bbyoff = self.meta.get('bbyoff')
        (fbbx, fbby, fbbxoff, fbbyoff) = fbb
        bitmap = self.__draw_bb()
        return bitmap.crop(fbbx, fbby, - bbxoff + fbbxoff, - bbyoff + fbbyoff)

    def __draw_original(self):
        return Bitmap([bin(int(h, 16))[2:].zfill(len(h) * 4) for h in self.meta.get('hexdata')])

    def __draw_bb(self):
        bbw = self.meta.get('bbw')
        bbh = self.meta.get('bbh')
        bitmap = self.__draw_original()
        bindata = bitmap.bindata
        l = len(bindata)
        if l != bbh:
            raise Exception(
                "Glyph \"" + str(self.meta.get('glyphname')) + "\" (codepoint " + str(self.meta.get(
                    'codepoint')) + ")'s bbh, " + str(bbh) + ", does not match its hexdata line count, " + str(l)
            )
            # Use old style for Python 3.5 support. For 3.6+:
            # f"Glyph \"{str(self.meta.get('glyphname'))}\" (codepoint {str(self.meta.get('codepoint'))})'s bbh, {str(bbh)}, does not match its hexdata line count, {str(l)}"
        bitmap.bindata = [b[0:bbw] for b in bindata]
        return bitmap

    def __draw_fbb(self):
        fh = self.font.headers
        return self.__draw_user_specified((fh['fbbx'], fh['fbby'], fh['fbbxoff'], fh['fbbyoff']))

    def origin(self, mode=0, fromorigin=False, xoff=None, yoff=None):
        # https://font.tomchen.org/bdfparser_py/glyph#origin

        bbxoff = self.meta.get('bbxoff')
        bbyoff = self.meta.get('bbyoff')
        if mode == 0:
            fh = self.font.headers
            ret = (fh['fbbxoff'], fh['fbbyoff'])
        elif mode == 1:
            ret = (bbxoff, bbyoff)
        elif mode == 2:
            ret = (bbxoff, bbyoff)
        elif mode == -1 and (xoff is not None and yoff is not None):
            ret = (xoff, yoff)
        elif mode == -1 and (xoff is None or yoff is None):
            raise Exception(
                'Parameter xoff and yoff in origin() method must be all set when mode=-1')
        return ret if fromorigin else (0 - ret[0], 0 - ret[1])


class Bitmap(object):

    def __init__(self, bin_bitmap_list):
        self.bindata = bin_bitmap_list

    def __str__(self):
        return '\n'.join(self.bindata).replace('0', '.').replace('1', '#').replace('2', '&')

    def __repr__(self):
        return 'Bitmap([\'' + '\',\n        \''.join(self.bindata) + '\'])'

    def width(self):
        return len(self.bindata[0])

    def height(self):
        return len(self.bindata)

    def clone(self):
        bindata = [l[:] for l in self.bindata]  # 2D list deep copy
        return self.__class__(bindata)

    @classmethod
    def __crop_string(cls, s, start, length):
        stemp = s
        l = len(s)
        left = 0
        if start < 0:
            left = 0 - start
            stemp = stemp.zfill(left + l)
        if start + length > l:
            stemp = stemp.ljust(start + length - l + len(stemp), '0')
        newstart = start + left
        return stemp[newstart: newstart + length]

    @classmethod
    def __string_offset_concat(cls, s1, s2, offset=0):
        if offset == 0:
            return s1 + s2
        len1 = len(s1)
        len2 = len(s2)
        s2start = len1 + offset
        s2end = s2start + len2
        finalstart = min(0, s2start)
        finalend = max(len1, s2end)
        news1 = cls.__crop_string(s1, finalstart, finalend - finalstart)
        news2 = cls.__crop_string(
            s2, finalstart - s2start, finalend - finalstart)
        return ''.join(str(int(b) or int(a)) for a, b in zip(news1, news2))

    @classmethod
    def __listofstr_offset_concat(cls, list1, list2, offset=0):
        if offset == 0:
            return list1 + list2
        width = len(list1[0])
        len1 = len(list1)
        len2 = len(list2)
        s2start = len1 + offset
        s2end = s2start + len2
        finalstart = min(0, s2start)
        finalend = max(len1, s2end)
        retlist = []
        for i in range(finalstart, finalend):
            if i < 0 or i >= len1:
                s1 = '0' * width
            else:
                s1 = list1[i]
            if i < s2start or i >= s2end:
                s2 = '0' * width
            else:
                s2 = list2[i-s2start]
            retlist.append(''.join(str(int(b) or int(a))
                                   for a, b in zip(s1, s2)))
        return retlist

    @classmethod
    def __crop_bitmap(cls, bitmap, w, h, xoff, yoff):
        retlist = []
        l = len(bitmap)
        for n in range(h):
            bn = l - yoff - h + n
            if bn < 0 or bn >= l:
                retlist.append('0' * w)
            else:
                retlist.append(cls.__crop_string(bitmap[bn], xoff, w))
        return retlist

    def crop(self, w, h, xoff=0, yoff=0):
        self.bindata = self.__crop_bitmap(self.bindata, w, h, xoff, yoff)
        return self

    def overlay(self, bitmap):
        bindata_a = self.bindata  # no mutation, do not need deep copy
        bindata_b = bitmap.bindata
        if len(bindata_a) != len(bindata_b):
            warnings.warn("the bitmaps to overlay have different height")
        if len(bindata_a[0]) != len(bindata_b[0]):
            warnings.warn("the bitmaps to overlay have different width")
        # b over a
        self.bindata = [''.join(str(int(b) or int(a)) for a, b in zip(
            la, lb)) for la, lb in zip(bindata_a, bindata_b)]
        return self

    @classmethod
    def concatall(cls, bitmaplist, direction=1, align=1, offsetlist=None):
        # https://font.tomchen.org/bdfparser_py/bitmap#bitmapconcatall

        if direction > 0:  # horizontal

            maxsize = max(bitmap.height() for bitmap in bitmaplist)
            ret = [''] * maxsize

            def stroffconcat(s1, s2, offset):
                if direction == 1:  # right
                    return cls.__string_offset_concat(s1, s2, offset)
                elif direction == 2:  # left
                    return cls.__string_offset_concat(s2, s1, offset)

            for i in range(maxsize):
                if align:  # bottom
                    ireal = -i - 1
                else:  # top
                    ireal = i

                offset = 0

                for bi, bitmap in enumerate(bitmaplist):

                    if offsetlist and bi != 0:
                        offset = offsetlist[bi - 1]

                    if i < bitmap.height():
                        ret[ireal] = stroffconcat(
                            ret[ireal], bitmap.bindata[ireal], offset)
                    else:
                        ret[ireal] = stroffconcat(
                            ret[ireal], '0' * bitmap.width(), offset)

        else:  # vertical

            maxsize = max(bitmap.width() for bitmap in bitmaplist)
            ret = []
            offset = 0

            for bi, bitmap in enumerate(bitmaplist):

                if offsetlist and bi != 0:
                    offset = offsetlist[bi - 1]

                bd = bitmap.bindata
                w = bitmap.width()
                if w != maxsize:
                    if align:  # left
                        xoff = 0
                    else:  # right
                        xoff = w - maxsize
                    bd = cls.__crop_bitmap(
                        bd, maxsize, bitmap.height(), xoff, 0)

                if direction == 0:  # down
                    ret = cls.__listofstr_offset_concat(ret, bd, offset)
                else:  # up
                    ret = cls.__listofstr_offset_concat(bd, ret, offset)

        return cls(ret)

    def __add__(self, bitmap):
        return self.__class__.concatall([self, bitmap])

    def concat(self, bitmap, direction=1, align=1, offsetlist=None):
        self.bindata = self.__class__.concatall(
            [self, bitmap], direction, align, offsetlist).bindata
        return self

    @classmethod
    def __enlarge_bindata(cls, bindata, x=1, y=1):
        bindata_temp = [l[:] for l in bindata]
        if x > 1:
            for i, l in enumerate(bindata_temp):
                bindata_temp[i] = ''.join(p * x for p in l)
        if y > 1:
            bindata_temp = [l for l in bindata_temp for _ in range(y)]
        return bindata_temp

    def enlarge(self, x=1, y=1):
        self.bindata = self.__class__.__enlarge_bindata(self.bindata, x, y)
        return self

    def __mul__(self, mul):
        if isinstance(mul, int):
            x = y = mul
        else:  # isinstance(mul, tuple)
            (x, y) = mul
        return self.__class__(self.__class__.__enlarge_bindata(self.bindata, x, y))

    def replace(self, substr, newsubstr):
        if isinstance(substr, int):
            substr = str(substr)
        if isinstance(newsubstr, int):
            newsubstr = str(newsubstr)
        self.bindata = [l.replace(substr, newsubstr) for l in self.bindata]
        return self

    def shadow(self, xoff=1, yoff=-1):
        bitmap_shadow = self.clone()
        w = self.width()
        h = self.height()
        w += abs(xoff)
        h += abs(yoff)
        bitmap_shadow.bindata = [l.replace('1', '2')
                                 for l in bitmap_shadow.bindata]

        if xoff > 0:
            resized_xoff = 0
            shadow_xoff = -xoff
        else:
            resized_xoff = xoff
            shadow_xoff = 0

        if yoff > 0:
            resized_yoff = 0
            shadow_yoff = -yoff
        else:
            resized_yoff = yoff
            shadow_yoff = 0

        self.crop(w, h, resized_xoff, resized_yoff)
        bitmap_shadow.crop(w, h, shadow_xoff, shadow_yoff)
        bitmap_shadow.overlay(self)
        self.bindata = bitmap_shadow.bindata
        return self

    def glow(self):
        w = self.width()
        h = self.height()
        w += 2
        h += 2
        self.crop(w, h, -1, -1)
        b = self.todata(2)
        for i_line, line in enumerate(b):
            for i_pixel, pixel in enumerate(line):
                if pixel == 1:
                    b[i_line][i_pixel - 1] = (b[i_line][i_pixel - 1] or 2)
                    b[i_line][i_pixel + 1] = (b[i_line][i_pixel + 1] or 2)
                    b[i_line - 1][i_pixel] = (b[i_line - 1][i_pixel] or 2)
                    b[i_line + 1][i_pixel] = (b[i_line + 1][i_pixel] or 2)
        self.bindata = [''.join(str(p) for p in l) for l in b]
        return self

    def bytepad(self, bits=8):
        # https://font.tomchen.org/bdfparser_py/bitmap#bytepad

        w = self.width()
        h = self.height()
        mod = w % bits
        if mod == 0:
            return self
        return self.crop(w + bits - mod, h)

    def todata(self, datatype=1):
        # https://font.tomchen.org/bdfparser_py/bitmap#todata

        if datatype == 0:
            return '\n'.join(self.bindata)
        elif datatype == 1:
            return self.bindata
        elif datatype == 2:
            return [[int(p) for p in l] for l in self.bindata]
        elif datatype == 3:
            return [int(p) for l in self.bindata for p in l]
        elif datatype == 4:
            # if there are '2's, it will throw error
            return [hex(int(l, 2))[2:].zfill(-1 * self.width() // 4 * -1) for l in self.bindata]
        elif datatype == 5:
            # if there are '2's, it will throw error
            return [int(l, 2) for l in self.bindata]

    def tobytes(self, mode='RGB', bytesdict=None):
        # https://font.tomchen.org/bdfparser_py/bitmap#tobytes

        if mode == '1':

            if bytesdict == None:
                bytesdict = {
                    0: 1,
                    1: 0,
                    2: 0,
                }
            # For PIL Image mode '1', if the line bit count is not multiples of 8, it must be padded with 0 to the right
            bits = []
            w = self.width()
            bitcount = 8
            mod = w % bitcount
            padcount = bitcount - mod
            for l in self.bindata:
                for p in l:
                    bits.append(int(p))
                if mod != 0:
                    bits.extend(0 for _ in range(padcount))
            octets = (bits[i:i+8] for i in range(0, len(bits), 8))

            def bits2byte(octet):
                res = 0
                for bit in octet:
                    res <<= 1
                    res |= bytesdict[bit]
                return res

            return bytes(bits2byte(octet) for octet in octets)

        else:

            if mode == 'L':
                bytesdict = bytesdict or {
                    0: b'\xff',
                    1: b'\x00',
                    2: b'\x7f',
                }
            elif mode == 'RGBA':
                bytesdict = bytesdict or {
                    0: b'\xff\xff\xff\x00',
                    1: b'\x00\x00\x00\xff',
                    2: b'\xff\x00\x00\xff',
                }
            else:
                if mode != 'RGB':
                    warnings.warn("Unknown mode, fallback to RGB")
                bytesdict = bytesdict or {
                    0: b'\xff\xff\xff',
                    1: b'\x00\x00\x00',
                    2: b'\xff\x00\x00',
                }

            retbytes = b''
            for l in self.bindata:
                for p in l:
                    retbytes += bytesdict[int(p)]
            return retbytes
