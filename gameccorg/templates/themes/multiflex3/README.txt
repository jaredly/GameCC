// $Id: README.txt,v 1.2.2.5 2009/12/17 20:18:09 hswong3i Exp $

ABOUT MULTIFLEX-3
----------------------

This is a re-implementation of the Multiflex-3 theme by Gerhard. This is
a tableless, multi-column, fluid width layout. Parts of the design are
ported from Contented7, Internet Services and Interactive Media theme.

Official MULTIFLEX-3 project page:
  http://www.1234.info/webtemplates/multiflex3/

Drupal Multiflex-3 project page:
  http://drupal.org/project/multiflex3/
  http://pantarei-design.com/projects/multiflex3/

Sponsored by:
  http://pantarei-design.com/


HOWTO CUSTOMIZE THIS THEME?
----------------------

For theme customization usually you will need to change the style.css.
By the way this traditional method is not too flexible.

This theme provide a hook called as custom.css. The custom.css will always
override default style.css setting, and will not be covered during version
upgrade. Benefit of using this hook including:

  1. Your customization will NOT get mixed with original theme style.
  2. Your customization will NOT be override during theme upgrade.

This theme also provide some example for customization within
custom.example.css, divided into section by section. You can copy-and-paste
them to your custom.css and feel free to change it.


HOW THE MISSION HACK FUNCTION?
----------------------

By default, mission statement is protected by filter_xss_admin() so no
PHP script is allowed. On the other hand, all tags that can be used inside
an HTML body is allowed.

This theme provide a fancy hack so PHP script will able to execute if
mission statement starting with "<?php", or else will preform as default
style.

One example usage is combine with adsense module so only display a
skyscraper (120x600) at top page; another example is combine with banner
module so you will have a benner rotation as mission statement; or even
just execute a simple PHP code snippet as welcome message when user login.


HOW THE CASCADE PRIMARY LINKS HACK FUNCTION?
----------------------

The cascade primary links is one of the most spotlight feature of original
Multiflex-3 theme design. This Drupal re-implementation also come with a
special hack for it. In order to activate it, please follow this procedure:

  1. Define your primary links with cascaded items.
  2. Set the parent item as "Expanded".

There is also some limitation of this implementation:

  1. Don't support IE6. Since IE6 need a special hack with "table", which
     will be unnecessary complicated the implementation. Moreover, some
     special CSS hack is required, too.
  2. Only support maximum 4 level of menus; others will looks buggy.

It is completely independent with original Drupal's primary/secondary links
handling. Set the primary and secondary links as same source will just
function as other typical Drupal themes.


ABOUT RTL SUPPORT (>=6.x)
----------------------

This theme is RTL supported, and fully tested with Acid2 compatible
browsers, e.g. FireFox3, Opera9.2 and Safari3. However, other browser
such as FireFox2 and Internet Explorer 6/7 may looks buggy.

As the implementation is validate with XHTML and CSS2 coding standard,
I am not going to provide browser-specific hack, for both LTR and RTL.

For more information about Acid2:
  http://en.wikipedia.org/wiki/Acid2

To test your browser with Acid2:
  http://www.webstandards.org/files/acid2/test.html


LIST OF MAINTAINERS
----------------------

PROJECT OWNER
M: Edison Wong <hswong3i@gmail.com>
S: maintained
W: http://edin.no-ip.com/
