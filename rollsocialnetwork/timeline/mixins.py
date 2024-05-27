"""
timeline mixins
"""
from typing import (
    Any,
    Optional,
)
from django.db.models.query import QuerySet
from .models import Post

class TimelineViewMixin:
    """
    timeline view mixin
    """
    slice_kwarg = "slice"
    slice_get_queryset_attr = "get_queryset"

    def _retrive_slice_value(self) -> Optional[str]:
        qs = getattr(self, self.slice_get_queryset_attr)()
        if qs.count() == 0:
            return None
        return str(qs[0].pk)

    def fill_slice_value(self) -> Optional[str]:
        """
        fill slice value
        """
        return self.get_slice_value() or self._retrive_slice_value()

    def get_slice_value(self) -> Optional[str]:
        """
        get slice value
        """
        return self.request.GET.get(self.slice_kwarg)  # type: ignore[attr-defined]

    def fill_has_new_post_out_slice(self) -> bool:
        """
        fill has new post out slice
        """
        slice_value = self.get_slice_value()
        if not slice_value:
            return False
        return Post.objects.filter(pk__gt=slice_value).count() > 0

    def build_sliced_queryset(self, queryset) -> QuerySet[Post]:
        """
        build sliced queryset
        """
        slice_value = self.get_slice_value()
        if not slice_value:
            return queryset
        return queryset.filter(pk__lte=slice_value)

    def build_context_data(self):
        """
        build context data
        """
        return {
            "slice_kwarg": self.slice_kwarg,
            "slice": self.fill_slice_value(),
            "has_new_post_out_slice": self.fill_has_new_post_out_slice(),
        }

    def get_context_data(self, *, object_list=None, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        get context data
        """
        context_data = super().get_context_data(object_list=object_list,  # type: ignore[misc]
                                                **kwargs)
        context_data.update(self.build_context_data())
        return context_data
