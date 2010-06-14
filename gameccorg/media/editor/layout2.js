
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
                items: [/*{
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
                    },*/ {
                        text: 'New Sprite',
                        id: 'new-sprite-button'
                    }, {
                        text: 'New Object',
                        id: 'new-object-button'
                    }, {
                        text: 'New Map',
                        id: 'new-map-button'
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
                    title: 'Sprites',
                    xtype: 'treepanel',
                    rootVisible: false,
                    enableDD: true,
                    ddGroup: 'sprites',
                    collapsible: true,
                    dataUrl: '/editor/ajax/project/folder/blank/',
                    border: false,
                    iconCls: 'sprites-tree',
                    id: 'sprites-tree',
                    root: {xtype:'treenode'}
                }, {
                    title: 'Objects',
                    xtype: 'treepanel',
                    rootVisible: false,
                    enableDD: true,
                    ddGroup: 'objects',
                    collapsible: true,
                    dataUrl: '/editor/ajax/project/folder/blank/',
                    border: false,
                    iconCls: 'objects-tree',
                    id: 'objects-tree',
                    root: {xtype:'treenode'}
                }, {
                    title: 'Maps',
                    xtype: 'treepanel',
                    rootVisible: false,
                    enableDD: true,
                    ddGroup: 'maps',
                    collapsible: true,
                    dataUrl: '/editor/ajax/project/folder/blank/',
                    border: false,
                    iconCls: 'maps-tree',
                    id: 'maps-tree',
                    root: {xtype:'treenode'}
            }]
        },
        {
            region: 'center',
            xtype: 'panel',
            layout: 'card',
            id: 'main-content',
            border: false,
            activeItem: 0,
            items: [{ // project info
                    id: 'project-info',
                    xtype: 'form',
                    margins: '10px',
                    defaultType: 'textfield',
                    buttons: [{
                        xtype: 'button',
                        text: 'Save'
                    }],
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
                        id: 'project-categories',
                        store: [],
                        allowBlank: true
                    }, {
                        fieldLabel: 'Status',
                        name: 'status',
                        xtype: 'combo',
                        id: 'project-status',
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
                    id: 'sprite-editor',
                    xtype: 'panel',
                    layout: 'border',
                    border: false,
                    items: [
                        {
                            region: 'west',
                            split: false,
                            width: 200,
                            contentEl: 'sprite-info'
                        }, {
                            region: 'center',
                            tbar: [
                            { text: '&nbsp;&nbsp;+&nbsp;&nbsp;' },
                            { text: '&nbsp;&nbsp;-&nbsp;&nbsp;' }
                            ],
                            contentEl: 'sprite-subimages'
                        }
                    ]
                }, {
                    id: 'object-editor',
                    xtype: 'panel',
                    border: false,
                    layout: 'border',
                    items: [
                        {
                            region: 'west',
                            split: false,
                            width: 200,
                            margin: 5,
                            contentEl: 'object-info'
                        }, {
                            region: 'center',
                            border: false,
                            layout: 'border',
                            items: [
                                {
                                    title: 'Events',
                                    region: 'west',
                                    split: false,
                                    width: 210,
                                    contentEl: 'object-events'
                                }, {
                                    title: 'Actions',
                                    id: 'object-acqions',
                                    region: 'center',
                                    split: false,
                                    xtype: 'treepanel',
                                    rootVisible: false,
                                    root: {xtype:'treenode'}
                                }, {
                                    region: 'east',
                                    id: 'action-plugins',
                                    split: true,
                                    xtype: 'tabpanel',
                                    width: 300,
                                    maxWidth: 500,
                                    items: []
                                }
                            ]
                        }
                    ]
                }, {
                    id: 'map-editor',
                    xtype: 'panel',
                    border: false,
                    layout: 'border',
                    items: [
                        {
                            region: 'west',
                            width: 200,
                            contentEl: 'map-info'
                        }, {
                            region: 'center',
                            border: false,
                            layout: 'border',
                            items: [{
                                region: 'west',
                                id: 'map-lefts',
                                width: 200,
                                collapsible: true,
                                title: 'Objects',
                                layout: 'card',
                                items: [{
                                    contentEl: 'map-objects',
                                    title: 'objects',
                                    collapsible: true
                                }]
                            }, {
                                region: 'center',
                                contentEl: 'map-main'
                            }]
                        }
                    ]
                }
            ]
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


