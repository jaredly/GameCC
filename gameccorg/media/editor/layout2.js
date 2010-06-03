
var layouts = {
    'main' : {
        layout: 'border',
        items: [
        {
            region: 'north',
            height: 30,
            margins: '0 0 5 0',
            items: {
                xtype: 'toolbar',
                items: [{
                        text:'Project',
                        menu:{
                            items:[
                                {text: 'Open'},
                                {text: 'Clone'},
                                {text: 'SaveAs'},
                                {text: 'Export'}
                            ]
                        }
                    }, {
                        text: 'View',
                        menu: {
                            items: [
                                { text: 'Flash - Preview' },
                                { text: 'HTML5 - Preview' }
                            ]
                        }
                    }, {
                        text: 'New Sprite'
                    }, {
                        text: 'New Object'
                    }, {
                        text: 'New Map'
                    }
                ]
            }
        }, /*{
            region: 'south',
            split: true,
            height: 200,
            minSize: 100,
            maxSize: 300,
            // collapsible: true,
            margins: '0 0 0 0', 
            items: {
                xtype: 'tabpanel',
                border: false,
                activeTab: 0,
                tabPosition: 'top',
                items: [{
                    title: 'Project Info',
                    html: '<p> A form or such goes here</p>'
                }, {
                    title: 'Browse Media',
                    html: '<p>this will probably have sub-tabs [maybe] for Images, Objects, and Maps.</p>'
                }]
            }
        },*/ {
            region: 'west',
            id: 'west-panel', // see Ext.getCmp() below
            title: 'Assets',
            split: true,
            width: 200,
            minSize: 175,
            maxSize: 400,
            collapsible: true,
            margins: '0 0 0 5',
            layoutConfig: {
                pack:'start',
                align:'stretch'
            },
            items: [{
                title: 'General',
                collapsible: false,
                border: false,
                contentEl: 'general-nav'
            }, {
                xtype: 'treepanel',
                title: 'Sprites',
                rootVisible: false,
                collapsible: true,
                border: false,
                iconCls: 'sprites-tree',
                root: {xtype:'treenode'}
            }, {
                xtype: 'treepanel',
                title: 'Objects',
                rootVisible: false,
                collapsible: true,
                border: false,
                iconCls: 'objects-tree',
                root: {xtype:'treenode'}
            }, {
                xtype: 'treepanel',
                title: 'Maps',
                rootVisible: false,
                collapsible: true,
                border: false,
                iconCls: 'maps-tree',
                root: {xtype:'treenode'}
            }]
        },
        {
            xtype: 'panel',
            region: 'center',
            layout: 'card',
            id: 'main-content',
            border: false,
            activeItem: 0,
            items: [{ // project info
              id: 'project-info',
              xtype: 'form',
              margins: '10px',
              defaultType: 'textfield',
              items: [{
                fieldLabel: 'Title',
                name: 'title'
              }, {
                fieldLabel: 'Version',
                name: 'version'
              }, {
                fieldLabel: 'Categories',
                name: 'categories',
                xtype: 'multiselect',
                store: [],
                allowBlank: true
              }, {
                fieldLabel: 'Status',
                name: 'status',
                xtype: 'combo',
                forceSelection: true,
                editable: false,
                triggerAction:'all',
                store: [[1, 'Pre-Alpha'],
                  [2, 'Alpha'],
                  [3, 'Beta'],
                  [4, 'Release']]
              }, {
                fieldLabel: 'Description',
                name: 'description',
                xtype: 'textarea',
                grow: true,
                width: '50%',
              }]
            }, {
              id: 'media-manager',
              items: [{
                  title: 'Images',
                  contentEl: 'media-images'
                }, {
                  title: 'Fonts'
                }, {
                  title: 'Sounds'
                }
              ]
            }, {
              xtype: 'panel',
              layout: 'border',
              anchor: '-10',
              id: 'image-content',
              border: false,
              items: [{
                  region: 'west',
                  split:true,
                  width: 200,
                  contentEl: 'sprite-info'
              }, {
                  region: 'center',
                  tbar: [
                  { text: '&nbsp;&nbsp;+&nbsp;&nbsp;' },
                  { text: '&nbsp;&nbsp;-&nbsp;&nbsp;' }
                  ],
                  contentEl: 'sprite-subimages'
              }]
            }, {
                html:'some stuff'
            }]
        }]
    },
    'loader': {

    },
    'new-image': {
        title: 'New Image',
        id: 'new-image-dlg',
        closable: false,
        modal: true,
        width: 400,
        height: 150,
        resizable: false,
        buttons: [{
            xtype: 'button',
            text: 'Ok'
        }, {
            xtype: 'button',
            text: 'Cancel'
        }],
        items: {
            xtype: 'tabpanel',
            activeTab: 0,
            // padding:'10px',
            items: [{
                title: 'Upload',
                layout:'fit',
                html: '<iframe src="/editor/upload/image/"></iframe>'
            }, {
                title: 'Url',
                xtype: 'form',
                padding:'10px',
                height: 100,
                // layout: 'fit',
                items: [{
                    xtype:'textfield',
                    fieldLabel:'Url',
                    height:30,
                    width:250
                }]
            }]
        }
    }
};


