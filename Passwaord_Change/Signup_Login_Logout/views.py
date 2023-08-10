from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash


def user_signup(request):
  if not request.user.is_authenticated:
    if request.method == 'POST':
       fm=SignupForm(request.POST)
       if fm.is_valid():
            messages.success(request,'Your Signup is Successfully !!')
            fm.save()
            return HttpResponseRedirect('/login/')

    else:
        fm=SignupForm()
    return render(request,'login/signup.html',{'form':fm})
  else:
        return HttpResponseRedirect('/login/')


#  Login veiws Function 

def user_login(request):
  if not request.user.is_authenticated:
    if request.method == 'POST':
        fm=AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password']
            user=authenticate(username=uname,password=upass)

            if user is not None:
                login(request,user)
                messages.success(request,'Login Successfully !!!')
                return HttpResponseRedirect('/profile/')

    else:       
     fm=AuthenticationForm()
    return render (request,'login/login.html',{'form':fm})
  
  else:
        return HttpResponseRedirect('/profile/')


# Show User Profile
def user_profile(request):
    if request.user.is_authenticated:
     return render(request,'login/profile.html',{'name':request.user})
    
    else:
        return HttpResponseRedirect('/login/')


# Logout Already Logined User
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')



# Change Password with Old Password    ChangePasswordForm

def user_changepass(request):
  if request.user.is_authenticated:
    if request.method == "POST":
      fm=PasswordChangeForm(user=request.user, data=request.POST)
      if fm.is_valid():
        fm.save()
        update_session_auth_hash(request,fm.user) # Sassion Maintain 
        messages.success(request,'Password Changed Successfully !!') 
        return HttpResponseRedirect('/profile/')
    else:        
     fm=PasswordChangeForm(user=request.user)
    return render(request,'login/changepassword.html',{'form':fm})
  else:
        return HttpResponseRedirect('/login/')
  



  #Change Password Using SetPasswordForm with Old Password 
def user_setpass(request):
    if request.user.is_authenticated:
      if request.method == "POST":
        fm=SetPasswordForm(user=request.user, data=request.POST)
        if fm.is_valid():
          fm.save()
          update_session_auth_hash(request,fm.user) # Sassion Maintain 
          messages.success(request,'Password Changed Successfully !!') 
          return HttpResponseRedirect('/profile/')
      else:        
       fm=SetPasswordForm(user=request.user)
      return render(request,'login/change_setpassword.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')
      
    