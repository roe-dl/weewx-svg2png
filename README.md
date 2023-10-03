# weewx-svg2png
Convert SVG to PNG during skin creation

The core purpose of this generator is to create thumbnail images for
the web pages created by WeeWX.

It is intended to create the SVG files by the CheetahGenerator
functionality of WeeWX.

## Prerequisites

First, install CairoSVG, if it is not already there.

## Installation instructions

1) download

   ```
   wget -O weewx-svg2png.zip https://github.com/roe-dl/weewx-svg2png/archive/master.zip
   ```

2) run the installer

   ```
   sudo wee_extension --install weewx-svg2png.zip
   ```

3) edit configuration in `skin.conf`

   See section "Configuration instructions"

5) restart weewx

   ```
   sudo /etc/init.d/weewx stop
   sudo /etc/init.d/weewx start
   ```

## Configuration instructions
    
This is for use in skins. Add a reference to this generator to the
`generator_list` key in `skin.conf`:
    
```
[Generators]
    generator_list = ..., user.svg2png.SVGtoPNGGenerator
```
    
Then, add a section to `skin.conf` to configure the files to be
created as SVG and converted to PNG (replace `index_thumbnail` by
your file name and `file1` to something reasonable for you):
    
```
[CheetahGenerator]
    ...
    [[ToDate]]
        ...
        [[[file1]]]
            template = index_thumbnail.svg.tmpl
...
[SVGtoPNGGenerator]
    [[file1]]
        # file name without extension (optional)
        file = index_thumbnail
        # image width in pixels (optional)
        width = replace_me
        # image height in pixels (optional)
        height = replace_me
    ...
```
    
If width and height are not provided, they will be taken out of the 
SVG file header.
    
If the `file` key is missing, the section name is used instead.
    
## Usage

See the examples directory for an example WeeWX template to create an
SVG file.

Add a thumbnail reference to the header section of the web page like this:

```
        <meta name="twitter:image" content="https://www.example.com/index_thumbnail.png" />
        <meta name="og:image" content="https://www.example.com/index_thumbnail.png" />
```
