# Webcam image with weather data

This examples shows how to put actual weather data onto a webcam image.

In this example is:
* `webcam.jpg` the original webcam image as downloaded from the webcam
* `webcam.svg.tmp` the template file for the WeeWX CheetahGenerator
* `webcam.svg` the SVG file created by CheetahGenerator
* `webcam.png` the final PNG file including the webcam image and the 
  weather data

![webcam image width weather data](webcam.png)

To adapt this example to your needs replace the width and height values
in the `<svg>` and `<image>` tags by the real size of your webcam image. 
Also replace the two last values at `viewport` by the width and height
of the webcam image.

You can additionally resize the webcam image by setting the width and
height in the `<svg>` tag to the new size, while the `<image>` tag and
`viewport` contain the original size. You should obey the aspect
ration if doing so.

Another way to resize the image is to specify a size in `skin.conf`
in the `[SVGtoPNGGenerator]` section.
