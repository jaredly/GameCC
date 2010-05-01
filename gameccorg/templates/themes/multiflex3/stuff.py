/<?php print \$\(\w\+\)\s*?>/{% block \1 %} {% endblock %}/g
%s/<?php if ($\(\w\+\)): ?>/{% if \1 %}/g
%s/<?php if (€kb(\$\(\w\w€kb+\)): \€kb?>/{% if %€kb\1 %}/g

<? endif; ?> {% endif %}
