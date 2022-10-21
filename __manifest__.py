{
    'name': 'LIMS',
    'version': '0.0.0900',
    'author':'Lucas Chagas Lima do Carmo',
    'category': 'Technical',
    'summary': 'Laboratory tools',
    'description': """Laboratory Management Tools""",
    'depends': ['mail','product','uom', 'maintenance','stock'],
    'sequence': 0,
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/criteria_view.xml',
        'views/inspection_view.xml',
        'views/product_specification.xml',
        'views/analysis_view.xml',
        'views/specification_view.xml',
        'data/sequence_data.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
