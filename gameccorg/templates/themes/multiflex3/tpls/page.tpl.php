<?php
// $Id: page.tpl.php,v 1.2.2.9 2009/05/14 08:16:31 hswong3i Exp $
?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php print $language->language ?>" lang="<?php print $language->language ?>" dir="<?php print $language->dir ?>">

<head profile="http://gmpg.org/xfn/11">
  <title><?php print $head_title ?></title>
  <?php print $head ?>
  <?php print $styles ?>
  <?php print $scripts ?>
  <!--[if lt IE 7]>
    <?php print phptemplate_get_ie_styles(); ?>
  <![endif]-->
  <script type="text/javascript"><?php /* Needed to avoid Flash of Unstyle Content in IE */ ?> </script>
</head>

<body class="<?php print $body_classes ?>">
<div id="header-region" class="clear-block"><?php print $header ?></div>
<div id="wrapper"><!-- begin wrapper -->
<div id="container" class="clear-block"><!-- begin container -->
  <div id="header"><!-- begin header -->
    <?php if ($logo): ?><div id="logo"><a href="<?php print $front_page ?>" title="<?php print $site_name ?>"><img src="<?php print $logo ?>" alt="<?php print $site_name ?>" /></a></div><?php endif; ?>
    <div id="slogan-floater"><!-- begin slogan-floater -->
      <?php if ($site_name): ?><h1 class='site-name'><a href="<?php print $front_page ?>" title="<?php print $site_name ?>"><?php print $site_name ?></a></h1><?php endif; ?>
      <?php if ($site_slogan): ?><div class='site-slogan'><?php print $site_slogan ?></div><?php endif; ?>
    </div><!-- end slogan-floater -->
    <?php if (isset($secondary_links)) : ?><!-- begin secondary_links -->
      <?php print theme('links', $secondary_links, array('class' => 'secondary-links')) ?>
    <?php endif; ?><!-- end secondary_links -->
  </div><!-- end header -->
  <?php if (isset($primary_links)) : ?><!-- begin primary_links -->
    <?php print phptemplate_primary($primary_links); ?>
  <?php endif; ?><!-- end primary_links -->
  <div id="breadcrumb-search-region"><div class="right-corner"><div class="left-corner">
    <?php print $breadcrumb ?>
    <?php if ($search_box): ?><div class="block block-theme"><?php print $search_box ?></div><?php endif; ?>
    <?php if ($mission): print '<div id="mission">'. phptemplate_mission() .'</div>'; endif; ?>
  </div></div></div>
  <div id="main"><div class="right-corner"><div class="left-corner"><!-- begin main -->
  <?php if ($left) { ?>
    <div id="sidebar-left" class="sidebar"><!-- begin sidebar-left -->
      <?php print $left ?>
    </div><!-- end sidebar-left -->
  <?php } ?>
  <div id="center"><div id="squeeze"><!-- begin center -->
    <?php if ($title): print '<h2 class="title'. ($tabs ? ' with-tabs' : '') .'">'. $title .'</h2>'; endif; ?>
    <?php if ($tabs): print '<div class="tabs">'. $tabs .'</div>'; endif; ?>
    <?php if ($show_messages && $messages): print $messages; endif; ?>
    <?php print $help ?>
    <div class="clear-block">
      <?php print $content ?>
    </div>
    <?php print $feed_icons ?>
  </div></div><!-- end center -->
  <?php if ($right) { ?>
    <div id="sidebar-right" class="sidebar"><!-- begin sidebar-right -->
      <?php print $right ?>
    </div><!-- end sidebar-right -->
  <?php } ?>
  </div></div></div><!-- end main -->
  <div id="footer"><!-- start footer -->
    <?php print $footer_message ?>
    <?php print $footer ?>
    <!-- begin #287426 -->
      <span style="display: none;">&nbsp;</span>
    <!-- end #287426 -->
  </div><!-- end footer -->
</div><!-- end container -->
</div><!-- end wrapper -->
<?php print $closure ?>
</body>
</html>
