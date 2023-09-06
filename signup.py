def SignupBackend(request):
    if request.method =='POST':
            uname = request.POST["uname"]
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            studentID = request.POST["studentID"]
            regNO=request.POST['regNO']
            password=request.POST['password']
            
            
            # create the user
            user = User.objects.create_user(uname, studentID, regNO, password)
            user.first_name=fname
            user.last_name=lname
            user.studentID = studentID
            user.regNO = regNO
            user.save()
            userprofile.user = user
            userprofile.save()
            messages.success(request," Your account has been successfully created")
            return redirect("studentlogin")
    else:
        return HttpResponse('404 - NOT FOUND ')