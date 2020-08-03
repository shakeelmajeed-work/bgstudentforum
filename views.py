from django.shortcuts import render
from .models import ad
import random
from .forms import AdForm
def ad_view(request):
	# grab the max id in the database
	ads = list(ad.objects.all())
	#print(ads)
	random_ad = random.choice(ads)
	#print(random_ad)
	return render(request,"personal/home.html", {'ads': random_ad})
def ad_registration(request):
	if request.method == "POST":
		form = AdForm(request.POST or None)
		if form.is_valid():
			form.save()
		return render(request, "ad_registration.html", {})
	else:
		return render(request, "ad_registration.html", {})
