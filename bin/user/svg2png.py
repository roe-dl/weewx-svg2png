#!/bin/python3
# WeeWX generator to convert files from SVG to PNG using CairoSVG
# Copyright (C) 2023, 2025, 2026 Johanna Karen Roedenbeck

"""

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

"""

    The core purpose of this generator is to create thumbnail images for
    the web pages created by WeeWX.

    First, install CairoSVG, if it is not already there.
    
    This is for use in skins. Add a reference to this generator to the
    `generator_list` key in `skin.conf`:
    
    ```
    [Generators]
        generator_list = ..., user.svg2png.SVGtoPNGGenerator
    ```
    
    Then, add a section to `skin.conf` to configure the files to be
    converted:
    
    ```
    [SVGtoPNGGenerator]
        [[file1]]
            # file name without extension (optional)
            file = replace_me
            # image width in pixels (optional)
            width = replace_me
            # image height in pixels (optional)
            height = replace_me
            # load external files (optional)
            unsafe = True
            # background color (optional, newer CairoSVG versions only)
            background_color = '#fff'
            # negate colors (optional, newer CairoSVG versions only)
            negate_colors = false
            # invert image (optional, newer CairoSVG versions only)
            invert_images = false
            # parent width and height (optional)
            parent_width = None
            parent_height = None
            # dpi setting (optional)
            dpi = 96
            # scale factor (optional)
            scale = 1
            # converter to use ('cairosvg' or 'rsvg2')
            converter = cairosvg
    ```
    
    If width and height are not provided, they will be taken out of the 
    SVG file header.
    
    If the `file` key is missing, the section name is used instead.
    
    It is intended to create the SVG files by the CheetahGenerator
    functionality of WeeWX.
    
"""

VERSION = "0.3"

import weewx
import weewx.reportengine
import weeutil.weeutil
import weeutil.config
import os.path
import configobj
import time
import subprocess

import weeutil.logger
import logging
log = logging.getLogger("user.svg2png")
def logdbg(msg):
    log.debug(msg)
def loginf(msg):
    log.info(msg)
def logerr(msg):
    log.error(msg)

try:
    import cairosvg
    has_cairosvg = True
except ImportError:
    has_cairosvg = False

class SVGtoPNGGenerator(weewx.reportengine.ReportGenerator):

    OPTIONS = (
        ('background_color',str),
        ('negate_colors',weeutil.weeutil.to_bool),
        ('invert_images',weeutil.weeutil.to_bool),
        ('dpi',weeutil.weeutil.to_int),
        ('parent_width',weeutil.weeutil.to_int), 
        ('parent_height',weeutil.weeutil.to_int),
        ('scale',weeutil.weeutil.to_float)
    )

    def run(self):
        
        if not has_cairosvg:
            logerr('Missing CairoSVG. Install it to use this extension.')
            return
        
        # determine how much logging is desired
        log_success = weeutil.weeutil.to_bool(weeutil.config.search_up(self.skin_dict, 'log_success', True))
        log_failure = weeutil.weeutil.to_bool(weeutil.config.search_up(self.skin_dict, 'log_failure', True))

        # where to find the files
        target_path = os.path.join(
            self.config_dict['WEEWX_ROOT'],
            self.skin_dict['HTML_ROOT'])
        
        # configuration section for this generator
        generator_dict = self.skin_dict.get('SVGtoPNGGenerator',configobj.ConfigObj())
        
        rsvg_cmd = generator_dict.get('rsvg_cmd','/usr/bin/rsvg-convert')
        
        start_ts = time.time()
        ct = 0
        pids = []
        for section in generator_dict.sections:
            # file name
            file = generator_dict[section].get('file',section)
            # PNG image width in pixels
            width = generator_dict[section].get('width',None)
            # PNG image height in pixels
            height = generator_dict[section].get('height',None)
            # Load external files
            unsafe = weeutil.weeutil.to_bool(generator_dict[section].get('unsafe',True))
            # Converter
            converter = generator_dict[section].get('converter',generator_dict.get('converter','cairosvg'))
            try:
                if file.endswith('.svg'):
                    fn = file[:-4]
                else:
                    fn = file
                source = os.path.join(
                    target_path,
                    fn+'.svg')
                target = os.path.join(
                    target_path,
                    fn+'.png')
                if converter.lower()=='cairosvg':
                    parameters = { 'url':source,
                                 'write_to':target,
                                 'output_width':width,
                                 'output_height':height,
                                 'unsafe':unsafe }
                    for para in SVGtoPNGGenerator.OPTIONS:
                        if para[0] in generator_dict[section]:
                            parameters[para[0]] = para[1](generator_dict[section][para[0]])
                    cairosvg.svg2png(**parameters)
                    ct += 1
                elif converter.lower()=='rsvg2':
                    parameters = [rsvg_cmd]
                    if width is not None:
                        parameters.extend(['-w',str(width)])
                    if height is not None:
                        parameters.extens(['-h',str(height)])
                    parameters.extend([
                        source,
                        '-o',
                        target
                    ])
                    pids.append(subprocess.Popen(parameters))
                logdbg('%s --> %s' % (source,target))
            except (LookupError,TypeError,ValueError,OSError) as e:
                if log_failure:
                    logerr('%s %s' % (e.__class__.__name__,e))
        if pids:
            # wait for the processes to finish, at most 5 seconds
            t = 5
            while pids and t:
                time.sleep(1)
                for pid in pids:
                    if pid.poll() is not None:
                        pids.remove(pid)
                        ct += 1
                t -= 1
        end_ts = time.time()
        if log_success:
            loginf('Created %s PNG file%s in %.2f seconds' % (ct,'' if ct==1 else 's',end_ts-start_ts))
