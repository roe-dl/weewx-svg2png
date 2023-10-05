# weewx-svg2png
Convert SVG to PNG during skin creation

The core purpose of this generator is to create thumbnail images for
the web pages created by WeeWX.

It is intended to create the SVG files by the CheetahGenerator
functionality of WeeWX.

## Prerequisites

First, install CairoSVG, if it is not already there.

```
sudo apt-get install cairosvg
```

This will install `python3-cairosvg` as well.

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

## Fonts

If you want to use special fonts within your SVG files you need to
inform the system about the existence of those fonts. This is done
by linking the font files or the directory containing the font files
to `/usr/local/share/fonts`. After that you have to update the
font cache.

Assuming your fonts reside in `/etc/weewx/skins/Belchertown/lib/fonts/`
you will enter:

```
cd /usr/local/share/fonts
sudo ln -s /etc/weewx/skins/Belchertown/lib/fonts belchertown-fonts
sudo fc-cache /usr/local/share/fonts
```

Please note, that this requires to download the fonts and store them
locally.

Now you can reference your fonts within the `<style>` section of your
SVG file template. Assuming your font is called `Roboto` (a font provided
by Google and used within the Belchertown skin) you would write:

```
    text {
        font-family: Roboto, sans-serif;
    }
```

## Usage

See the examples directory for example WeeWX templates to create an
SVG file.

[Examples](examples)

### Thumbnail or preview image for social media references

In social media posts that reference web pages you often see a preview
image of the web page shown below the post. You may have wondered how 
this is done.

It is quite easy. You only need a thumbnail image as created by this
generator and a special `<meta>` statement within the header section
of your web page referencing it. Assuming your thumbnail is named
`index_thumbnail.png` and your domain is `example.com` this reads 
like this:

```
        <meta name="twitter:image" content="https://www.example.com/index_thumbnail.png" />
        <meta property="og:image" content="https://www.example.com/index_thumbnail.png" />
```

You can also specify wether the thumbnail is shown as a small image
besides the page description or as a large image above the page
description.

* for small thumbnails

  ```
        <meta name="twitter:card" content="summary" />
  ```

* for large thumbnails

  ```
        <meta name="twitter:card" content="summary_large_image" />
  ```

## References

* [WeeWX website](https://www.weewx.com)
* [WeeWX information in german](https://www.woellsdorf-wetter.de/software/weewx.html)
* [WeeWX customization guide](https://www.weewx.com/docs/customizing.htm)
  (See this guide for writing templates.)
* [Calculation in templates](https://github.com/weewx/weewx/wiki/calculate-in-templates)
* [Tags for series](https://github.com/weewx/weewx/wiki/Tags-for-series)
* [CairoSVG website](https://cairosvg.org)
* [The Belchertown skin](https://github.com/poblabs/weewx-belchertown)
