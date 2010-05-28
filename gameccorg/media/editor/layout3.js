Ext.onReady(function () {
new Ext.Viewport({
    layout: 'border',
    items: [{
        title: 'South Region is resizable',
        region: 'south',     // position for region
        height: 100,
        split: true,         // enable resizing
        minSize: 75,         // defaults to 50
        maxSize: 150,
        margins: '0 5 5 5'
    },{
        // xtype: 'panel' implied by default
        title: 'West Region is collapsible',
        region:'west',
        margins: '5 0 0 5',
        width: 200,
        collapsible: true,   // make collapsible
        cmargins: '5 5 0 5', // adjust top margin when collapsed
        id: 'west-region-container',
        layout: 'fit',
        unstyled: true
    },{
        title: 'Center Region',
        region: 'center',     // center region is required, no width/height specified
        xtype: 'container',
        layout: 'fit',
        margins: '5 5 0 0'
    }]
});
});
