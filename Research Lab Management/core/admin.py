from django . contrib import admin
from . models import Project , Equipment , Inventory , Staff
admin . site . register ( Project )
admin . site . register ( Equipment )
admin . site . register ( Inventory )
admin . site . register ( Staff )