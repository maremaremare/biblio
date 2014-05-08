from sitetree.utils import tree, item

# Be sure you defined `sitetrees` in your module.
sitetrees = (
    # Define a tree with `tree` function.
    tree('authors', items=[
        # Then define items and their children with `item` function.
        item('Authors', 'shop', children=[
            item('Author named "{{ author.name }}"', 'shop-author', in_menu=True, in_sitetree=True),
            
        ])
    ]),
    # ... You can define more than one tree for your app.
)