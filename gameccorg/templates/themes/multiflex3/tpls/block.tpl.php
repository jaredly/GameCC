<?php
// $Id: block.tpl.php,v 1.2.2.1 2008/06/16 03:45:37 hswong3i Exp $
?>
<div id="block-<?php print $block->module .'-'. $block->delta ?>" class="block block-<?php print $block->module ?> block-<?php print $block_id ?>">
  <?php if ($block->subject) : ?>
    <div class="corner-top-left"></div><div class="corner-top-right"></div>
    <h1><?php print $block->subject ?></h1>
  <?php endif; ?>
  <div class="content"><?php print $block->content ?></div>
</div>
