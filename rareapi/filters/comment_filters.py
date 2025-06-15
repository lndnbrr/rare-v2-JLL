import django_filters
from rareapi.models import Comment


class CommentFilter(django_filters.FilterSet):
    post = django_filters.NumberFilter(
        field_name='post',
        help_text='Filter comments by post ID'
    )

    author = django_filters.NumberFilter(
        field_name='author',
        help_text='Filter comments by author ID'
    )

    class Meta:
        model = Comment
        fields = ['post', 'author']

    # @property
    # # Redefining the queryset property on filterset in comments view to order by creation date, applies to all comment filters at the moment
    # def qs(self):
    #     parent = super().qs
    #     return parent.order_by('-created_on')
