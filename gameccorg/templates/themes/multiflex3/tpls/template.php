<?php
// $Id: template.php,v 1.2.2.3 2009/05/11 08:26:46 hswong3i Exp $

/**
 * Return a cascade primary links.
 * Clone implementation from user_block().
 *
 * @return
 *   a themed cascade primary links.
 */
function phptemplate_primary() {
  $output = '<div id="primary-links-region">';
  $output .= menu_tree(variable_get('menu_primary_links_source', 'primary-links'));
  $output .= '</div>';
  return $output;
}

/**
 * Return a themed mission trail.
 *
 * @return
 *   a string containing the mission output, or execute PHP code snippet if
 *   mission is enclosed with <?php ?>.
 */
function phptemplate_mission() {
  $mission = theme_get_setting('mission');
  if (preg_match('/^<\?php/', $mission)) {
    $mission = drupal_eval($mission);
  }
  else {
    $mission = filter_xss_admin($mission);
  }
  return isset($mission) ? $mission : '';
}

/**
 * Return a themed breadcrumb trail.
 *
 * @param $breadcrumb
 *   An array containing the breadcrumb links.
 * @return a string containing the breadcrumb output.
 */
function phptemplate_breadcrumb($breadcrumb) {
  if (!empty($breadcrumb)) {
    return '<div class="breadcrumb">'. implode('', $breadcrumb) .'</div>';
  }
}

/**
 * Generates IE CSS links for LTR and RTL languages.
 */
function phptemplate_get_ie_styles() {
  global $language;

  $iecss = '<link type="text/css" rel="stylesheet" media="all" href="'. base_path() . path_to_theme() .'/fix-ie.css" />';
  if (defined('LANGUAGE_RTL') && $language->direction == LANGUAGE_RTL) {
    $iecss .= '<style type="text/css" media="all">@import "'. base_path() . path_to_theme() .'/fix-ie-rtl.css";</style>';
  }

  return $iecss;
}
