from django.db.models.signals import post_save
from django.dispatch import receiver
from sitetree.models import TreeItem
from shop.models import Author, Category


@receiver(post_save, sender=Author)
def on_author_add(instance, created, **kwargs):
    if created:
        tree_item = TreeItem(title=instance.name, tree_id=2,
                             url=instance.get_absolute_url(), author = instance)
        tree_item.save(force_insert=True)
    else:
        tree_item = TreeItem.objects.get(author = instance)
        tree_item.title = instance.name
        tree_item.url = instance.get_absolute_url()
        tree_item.save(force_update=True)



@receiver(post_save, sender=Category)
def on_category_add(instance, created, **kwargs):
    parent_treeitem_id = TreeItem.objects.get(url=instance.author.get_absolute_url()).id
    if created:
        tree_item = TreeItem(
            title=instance.title, tree_id=2,  parent_id=parent_treeitem_id,
            url=instance.get_absolute_url())
        tree_item.save(force_insert=True)
    else:
        tree_item = TreeItem.objects.get(category = instance)
        tree_item.title = instance.title
        tree_item.url = instance.get_absolute_url()
        tree_item.save(force_update=True)
        