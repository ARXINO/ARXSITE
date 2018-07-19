from django.shortcuts import render, redirect, render_to_response
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
import datetime
suanki_saat=datetime.datetime.now()
duyurular = []
mesajlar = []
zaman={#Bütün zamanlar farklı olmak ZORUNDA!
    'bekle':0,
    'tohum_ara':10,
    'tohum_dik':20,
    'hasat_yap':1,
    'fidan_dik':1,
    'agac_kes':1,
    'meyve_topla':1,
    'sula':1,
}
dikme_durum=""


def home(request):

    admin_list = []
    for admin in User.objects.filter(is_superuser=True).values_list('username', flat=True).distinct():
        admin_list.append(admin)

    if request.user.is_authenticated:
        giris_durum=1
    else:
        giris_durum=0

    if request.method == 'POST':
        if 'duyuru' in request.POST:
            gonderilen_saat = datetime.datetime.now()
            admin_duyuru = request.user.username +" ("+str(gonderilen_saat.strftime('%H:%M'))+")  :  " +str(request.POST['duyuru'])
            print(admin_duyuru)
            duyurular.append(admin_duyuru)
        if 'mesaj' in request.POST:
            gonderilen_saat = datetime.datetime.now()
            kullanici_mesaj = request.user.username +" ("+str(gonderilen_saat.strftime('%H:%M'))+") :  "+str(request.POST['mesaj'])
            print(kullanici_mesaj)
            mesajlar.append(kullanici_mesaj)
        return redirect("/home")
    args = {'user':request.user,'giris_durum':giris_durum,"duyurular":list(reversed(duyurular)),"admin_list":admin_list,"kullanici_mesaj":list(reversed(mesajlar))}
    return render(request, 'accounts/home.html', args)

def register(request):
    if request.method == 'POST':    #Eğer kullanıcı veri gönderiyorsa
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home/login')
        else:
            return redirect('/home/register/hatali_form')

    else:
        form = RegistrationForm
        args={'form':form}
        return render(request, 'accounts/reg_form.html', args)

def hatali_form(request):
    args = {}
    return render(request, 'accounts/hatali_form.html', args)

@login_required(login_url='/home/login/')
def logout_view(request):
    logout(request)
    return redirect('/home')







@login_required(login_url='/home/login/')
def game(request):
    mesaj_url='home/message'
    karakter = UserProfile.objects.get(user__username__iexact=request.user.username)
    zaman_gonder=zaman['bekle']
    dikilen_arpa=0
    dikilen_elma=0
    hata_mesaji=""

    if karakter.karakter_gorunus != "x":
        sayfa="game_bahce"

    if request.method == 'POST':    #Eğer kullanıcı veri gönderiyorsa
        print("gelen veri", request.POST)
        if 'harita_goster' in request.POST:
            sayfa = request.POST['harita_goster']
            print("sa",sayfa)
        elif 'mesaj' in request.POST:
            gonderilen_saat = datetime.datetime.now()
            kullanici_mesaj = request.user.username +" ("+str(gonderilen_saat.strftime('%H:%M'))+") :  "+str(request.POST['mesaj'])
            print(kullanici_mesaj)
            mesajlar.append(kullanici_mesaj)
        elif 'tohum_ara' in request.POST:
            print(request.POST)
            karakter.karakter_durum = 'Tohum Topluyor'
            karakter.save()
            zaman_gonder=zaman['tohum_ara']
        elif 'tohum_dik' in request.POST:
            karakter.karakter_durum = 'Tohum Dikiyor'
            karakter.save()
            zaman_gonder = zaman['tohum_dik']
        elif 'hasat_yap' in request.POST:
            karakter.karakter_durum = 'Hasat Yapıyor'
            karakter.save()
            zaman_gonder = zaman['hasat_yap']
        elif 'fidan_dik' in request.POST:
            karakter.karakter_durum = 'Fidan Dikiyor'
            karakter.save()
            zaman_gonder = zaman['fidan_dik']
        elif 'agac_kes' in request.POST:
            karakter.karakter_durum = 'Ağaç Kesiyor'
            karakter.save()
            zaman_gonder = zaman['agac_kes']
        elif 'meyve_topla' in request.POST:
            karakter.karakter_durum = 'Meyve/Sebze Topluyor'
            karakter.save()
            zaman_gonder = zaman['meyve_topla']
        elif 'sula' in request.POST:
            karakter.karakter_durum = 'Sulama Yapıyor'
            karakter.save()
            zaman_gonder = zaman['sula']
        elif 'gonder_yazi' in request.POST:
            karakter.karakter_durum = 'Boş Bekliyor'
            karakter.save()
            return redirect("/home/game")

        elif 'arpa_ek' in request.POST:
            if karakter.arpa_tohumu_sure+int(request.POST["arpa_ek"])<=150:
                karakter.karakter_durum = 'Arpa Tohumu Dikiliyor'
                karakter.arpa_tohumu_sure+=int(request.POST["arpa_ek"])
                karakter.arpa_tohumu-=int(request.POST["arpa_ek"])
                karakter.save()
                dikilen_arpa=int(request.POST["arpa_ek"])
                zaman_gonder = zaman['tohum_dik']
                hata_mesaji = ""
            else:
                karakter.karakter_durum = 'Boş Bekliyor'
                hata_mesaji="Maximum limite ulaştınız. Daha fazla dikemezsiniz."
        elif 'elma_ek' in request.POST:
            if karakter.elma_tohumu_sure + int(request.POST["elma_ek"]) <= 20:
                karakter.karakter_durum = 'Elma Tohumu Dikiliyor'
                karakter.elma_tohumu_sure += int(request.POST["elma_ek"])
                karakter.elma_tohumu-=int(request.POST["elma_ek"])
                karakter.save()
                dikilen_elma = int(request.POST["elma_ek"])
                zaman_gonder = zaman['tohum_dik']
                hata_mesaji = ""
            else:
                karakter.karakter_durum = 'Boş Bekliyor'
                hata_mesaji = "Maximum limite ulaştınız. Daha fazla dikemezsiniz."
        else:
            karakter.karakter_durum = 'Boş Bekliyor'
            karakter.save()
            return redirect("/home/game")
    print("deneme",karakter.karakter_durum)
    args = {"range_sayac":range(50),"hata_mesaji":hata_mesaji,"dikilen_arpa":dikilen_arpa,"dikilen_elma":dikilen_elma,'name': request.user.username,"kullanici_mesaj":mesajlar,'karakter':karakter,'money': karakter.money, 'sayfa': sayfa, 'karakter_durum':karakter.karakter_durum,"zaman":zaman_gonder}
    return render(request, 'accounts/game.html', args)

@login_required(login_url='/home/login/')
def profile(request):
    karakter = UserProfile.objects.get(user__username__iexact=request.user.username)
    args = {'user':request.user, 'karakter':karakter}
    return render(request, 'accounts/profile.html', args)

@login_required(login_url='/home/login/')
def profile_karakter(request):
    karakter = UserProfile.objects.get(user__username__iexact=request.user.username)
    a1 = karakter.karakter_gorunus[0]
    a2 = karakter.karakter_gorunus[1]
    a3 = karakter.karakter_gorunus[2]

    args = {'user':request.user, 'karakter':karakter, 'a1':a1, 'a2':a2, 'a3':a3}
    return render(request, 'accounts/profile_karakter.html', args)

@login_required(login_url='/home/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/home/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form' : form}
        return render(request, 'accounts/edit_profile.html', args)



#Oyun içi sayfalar#
@login_required(login_url='/home/login/')
def game_menu(request):
    karakter = UserProfile.objects.get(user__username__iexact=request.user.username)
    args = {}

    if karakter.karakter_gorunus == 'x':
        if request.method == 'POST':    #Eğer kullanıcı veri gönderiyorsa
            data = request.POST['ozellikler']
            karakter = UserProfile.objects.get(user__username__iexact=request.user.username)
            karakter.karakter_gorunus = data
            karakter.save()
            return redirect('game_bayir')
    return render(request, 'accounts/game_menu.html', args)


@login_required(login_url='/home/login/')
def game_bayir(request):
    karakter = UserProfile.objects.get(user__username__iexact=request.user.username)
    oyuncular = User.objects.all()
    oyuncu_listesi = []
    oyuncu_sayisi = 0
    gelen_id = []
    durum=karakter.karakter_durum
    secili_karakter="karakter"

    for x,y in enumerate(oyuncular):
        if str(request.user.username) == str(y):
            secili_karakter+=str(x)
        oyuncu_listesi.append(y.username)
        gelen_id_veri = 'karakter'+str(oyuncu_sayisi)
        oyuncu_sayisi += 1
        gelen_id.append(gelen_id_veri)

    print(secili_karakter)

    args = {'user':request.user, "secili_karakter":secili_karakter, 'oyuncular' : oyuncu_listesi,'oyuncu_sayisi':oyuncu_sayisi,'gelen_id':gelen_id,"durum":durum,"karakter":karakter}
    return render(request, 'accounts/game_bayir.html', args)

def nasiloynanir(request):
    args = {}
    return render(request, 'accounts/howtoplay.html', args)

def hakkimizda(request):
    args = {}
    return render(request, 'accounts/about-us.html', args)

@login_required(login_url='/home/login/')
def message(request):
    args = {'mesajlar':list(reversed(mesajlar))}
    return render(request, 'accounts/message.html', args)

@login_required(login_url='/home/login/')
def announcement(request):
    args = {'duyurular':list(reversed(duyurular))}
    return render(request, 'accounts/announcement.html', args)

@login_required(login_url='/home/login/')
def game_bahce(request):
    karakter = UserProfile.objects.get(user__username__iexact=request.user.username)
    args = {"karakter":karakter,"arpa_tohum_range":range(karakter.arpa_tohumu_sure),"elma_tohum_range":range(karakter.elma_tohumu_sure)}
    return render(request, 'accounts/game_bahce.html', args)

def change_password(request):
    if request.method == "POST":
        form=PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/home/profile')
        else:
            return redirect('/home/profile/password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/sifre_degistir.html', args)
