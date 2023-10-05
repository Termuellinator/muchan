from rest_framework.exceptions import PermissionDenied


DEFAULT_CATEGORY_ID = 1

class DenyDeletionOfDefaultCategoryMixin:
    # We want to get the category's id that is about to be deleted
    # We want to compare the id with the DEFAULT_CATEGORY_ID
    # If True, we want to raise an exception

    def get_queryset(self): # get the queryset for Listing
        queryset = super().get_queryset()
        if (
            not hasattr(self, "action") or # if called by normal view, action is not present
            self.action == 'destroy'):  # is set by viewsets
            pk = self.kwargs['pk']
            deleted_query = queryset.get(pk=pk) # to make sure the requested object even exists
            if deleted_query.pk == DEFAULT_CATEGORY_ID:
                raise PermissionDenied("Default Category cannot be deleted")

        return queryset
