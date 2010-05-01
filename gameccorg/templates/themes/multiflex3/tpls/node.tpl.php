<?php
// $Id: node.tpl.php,v 1.2.2.2 2008/06/19 08:14:41 hswong3i Exp $
?>
<div class="node<?php print $sticky ? ' sticky' : '' ?><?php print $status ? '' : ' node-unpublished' ?>">
  <?php if (!$page): ?><h2 class="title"><a href="<?php print $node_url ?>" title="<?php print $title ?>"><?php print $title ?></a></h2><?php endif; ?>
  <div class="meta meta-header">
    <?php if ($picture): print $picture; endif; ?>
    <?php if (node_access('update', $node)): ?><a href="<?php print url('node/'. $node->nid .'/edit') ?>" class="editlink" title="<?php print t('Edit') ?>"> </a><?php endif; ?>
    <?php if ($submitted): ?><div class="submitted"><?php print $submitted ?></div><?php endif; ?>
    <?php if ($terms): ?><div class="terms"><?php print $terms ?></div><?php endif; ?>
  </div>
  <div class="content">
    <?php print $content?>
    <div class="meta meta-footer">
      <?php if ($links): ?><?php print $links ?><?php endif; ?>
    </div>
  </div>
</div>
