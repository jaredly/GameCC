
Ext.onReady(function() {
      new Ext.Viewport({
          layout: 'border',
          items: [{
              region: 'north',
              height: 100,
              // title: 'The Page Header',
              // autoEl: { tag: 'div', html: 'ho' }
          }, {
              region: 'west',
              width: 300,
              minSize: 100,
              collapsible: true,
              split: true,
              title: 'Navigation Panel',
              items: {
                  xtype: 'treepanel',
                  rootVisible: false,
                  root: new Ext.tree.AsyncTreeNode({
                      children: [{
                          text: 'Menu 1'
                      },{
                          text: 'Menu 2'
                      },{
                          text: 'Menu 3'
                      }]
                  })
              }
          }, {
              region: 'center',
              title: 'Page Content'
          }, {
              region: 'south',
              height: 300,
              minSize: 100,
              collapsible: true,
              collapsed: true,
              split: true,
              title: 'Information'
          }]
      });
  });
