from django.shortcuts import render

# Create your views here.

def home_page(request):
    # cnt = Resources.objects.all().count()
    # user_cnt = User.objects.filter(is_active=True).count()
    # res_per_cat = Resources.objects.values("cat_id__cat").annotate(cnt=Count("cat_id"))
    
    context = {
        # "cnt": cnt,
        # "user_cnt": user_cnt,
        # "res_per_cat": res_per_cat
    }
    return render(
        request=request, 
        template_name="index.html", 
        context=context
    )