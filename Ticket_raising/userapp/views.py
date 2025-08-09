from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password,make_password



# Sign in function
def sign_in(request):
    global role,agent_id,Emp_id,admin_name
    
    role =request.POST.get('role')
    if request.method == 'POST':
        if role == 'Agent':
             agent_id=request.POST.get('name_id')
             agent_password=request.POST.get('password')
             try:    
                 if agent_id != '':    
                        agent=Agent_signup.objects.get(agent_id=agent_id)
                        agent. password = make_password(agent_password )
                        agent.save()
                 if check_password(agent_password, agent.password):      
                            request.session['agent_id']=agent.agent_id                            
                            messages.success(request, f'{agent} Log-in successfull')
                            return redirect('agent_index')     
                    
                 else:
                        messages.error(request, 'Incorrect password') 
             except ValueError:
                messages.error(request, "Agent ID must be a number")
             except Agent_signup.DoesNotExist:
                 messages.error(request, f'{agent_id} id not found')
           
            
        elif role == 'User':
             Emp_id=request.POST.get('name_id')
             Emp_password=request.POST.get('password')
             try:       
                 user=User_signup.objects.get(Emp_id=Emp_id)
                 user. emp_password = make_password(Emp_password )
                 user.save()
                 if Emp_id != '': 
                    if check_password(Emp_password, user.emp_password):
                        print("Login success")    
                        request.session['Emp_id']=user.Emp_id                                
                        messages.success(request, f'{user.Emp_name} Log-in successfull')
                        return redirect('user')     
                
                    else:
                        print("Login nooot success")
                        messages.error(request, 'Incorrect password')  
             except ValueError:
                messages.error(request, "Employee ID must be a number")
                    
             except User_signup.DoesNotExist:
                 messages.error(request, f'{Emp_id} id not found')
                
        else:
            admin_name = request.POST.get('name_id')
            password = request.POST.get('password')
            print("Admin Name:", admin_name, "Password:", password,role)
            if admin_name == '' and password == '' :
                messages.error(request,'Please Fill all the feild !!')
                return redirect ('sign_in')
            
            try:
                 admin = Admin_reg.objects.get(admin_name=admin_name)
                 admin.password = make_password(password )
                 admin.save()
                
                 if check_password(password, admin.password):
                     print("Login success")
                     request.session['admin_name'] = admin.admin_name  
                     messages.success(request, f'{admin_name} Log-in successful !!!..')
                     return redirect('admin') 
                     
                 else:
                     print("Login not successful")
                     messages.error(request, 'Incorrect password')  
            except Admin_reg.DoesNotExist:
                     messages.error(request, f' "{admin_name}" not found')       
             
             
    return render(request,'sign_in.html',{'role':role})

#-----------------------------------------------------------------------------------------------#Admin
# Admin index page
def admin_index(request):
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')

    adminname = request.session['admin_name']
    all_users = User_signup.objects.all().order_by('-id')
    all_admins = Admin_reg.objects.all().order_by('-id')
    all_agents = Agent_signup.objects.all().order_by('-id')
    tickets = Ticket.objects.select_related('user', 'assigned_agent').order_by('-created_at')
    feedbacks = TicketFeedback.objects.select_related('user').order_by('-created_at')

    return render(request, 'Admin/Admin_index.html', {
        'admin_name': adminname,
        'all_users': all_users,
        'all_admins': all_admins,
        'all_agents': all_agents,
        'tickets': tickets,
        'feedbacks': feedbacks
    })


# Create Admin --------------------------------------Admin---------
def create_admin(request): 
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        print("Admin session not created") 
        return redirect('sign_in') 
    admin_name = ''
    admin_mail = ''
    password = ''
    all_admins = Admin_reg.objects.all().order_by('-id')
    all_users = User_signup.objects.all().order_by('-id')
    all_agents = Agent_signup.objects.all().order_by('-id')
    adminname = request.session['admin_name'] 
    tickets = Ticket.objects.all().order_by('-created_at')
    feedbacks = TicketFeedback.objects.select_related('user').order_by('-created_at')

    if request.method == 'POST':
        admin_name=request.POST.get('admin_name')  
        admin_mail=request.POST.get('admin_mail')
        password=request.POST.get('password')
        
        if Admin_reg.objects.filter(admin_name=admin_name).exists():
            messages.error(request,f"User {admin_name} already exists")
        elif Admin_reg.objects.filter(admin_mail=admin_mail).exists():
            messages.error(request,f"User {admin_mail}  already exists")
        elif not admin_name or not admin_mail or not password:
            messages.error(request, "Please fill all the fields")
                     
        else:
            admin_in=Admin_reg(
                      admin_name=admin_name,
                      admin_mail=admin_mail,
                      password=password)      
            admin_in.save()
            messages.success(request,f'{admin_name} created Successfully')
            return redirect('admin')
    
    return render(request,'Admin/Admin_index.html',
                  {'all_admins':all_admins,'admin_name': adminname,'admin_name':admin_name,'all_users': all_users,'all_agents': all_agents,
                   'feedbacks': feedbacks,
                   'admin_mail':admin_mail,'password':password,'tickets':tickets})

def admin_list(request):
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        print("Admin session not created") 
        return redirect('sign_in') 
    all_admins = Admin_reg.objects.all().order_by('-id')
    return render(request, 'Admin/Admin_index.html', {'all_admins': all_admins,'admin_name': admin_name,})

def delete_admin(request, admin_id):
    if Admin_reg.objects.count() == 1:
        messages.error(request, "At least one admin must remain.")
        return redirect('admin')

    admin = Admin_reg.objects.get(id=admin_id)
    admin.delete()
    messages.success(request, "Admin deleted successfully.")
    return redirect('admin')

def update_admin(request, admin_id):
     all_admins = Admin_reg.objects.all().order_by('-id')
     try:
        admin = Admin_reg.objects.get(id=admin_id)
        if request.method == 'POST':
            admin.admin_name = request.POST.get('admin_name')
            admin.role = request.POST.get('role')
            admin.admin_mail = request.POST.get('admin_mail')
            admin.password = request.POST.get('password')
            admin.save()
            messages.success(request, f'Admin {admin.admin_name} updated successfully')
            return redirect('admin')  # safer option
        return render(request, 'Admin/Admin_index.html', {'all_admins': all_admins,'admin_name': admin_name,})  
     except Admin_reg.DoesNotExist:
        messages.error(request, f'Admin not found')
        return redirect('admin_sign_up')

# Create user-----------------------------------user---------
def create_user(request):
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        print("Admin session not created") 
        return redirect('sign_in') 
    Emp_name = ''
    Emp_id = ''
    Sys_id = ''
    Emp_email = ''
    emp_password = ''
    all_admins = Admin_reg.objects.all().order_by('-id')
    all_users = User_signup.objects.all().order_by('-id')
    all_agents = Agent_signup.objects.all().order_by('-id')
    adminname = request.session['admin_name'] 
    tickets = Ticket.objects.all().order_by('-created_at')
    if request.method == 'POST':
        Emp_name=request.POST.get('Emp_name')  
        Emp_id=request.POST.get('Emp_id') 
        Sys_id=request.POST.get('Sys_id')
        Emp_email=request.POST.get('emp_mail')
        emp_password=request.POST.get('password')
        
        if User_signup.objects.filter(Emp_name=Emp_name).exists():
            messages.error(request,f"User {Emp_name} already exists")
        elif User_signup.objects.filter(Emp_email=Emp_email).exists():
            messages.error(request,f"User {Emp_email}  already exists")
        elif Emp_name == '' and Emp_id == '' and Emp_email == '' and emp_password == '' and Sys_id == '':
            messages.error(request, "Please fill all the fields")
        else:
            user_in=User_signup(
                      Emp_name=Emp_name,
                      Emp_id=Emp_id,
                      Sys_id=Sys_id,
                      Emp_email=Emp_email,
                      emp_password=emp_password)      
            user_in.save()
            messages.success(request,f'{Emp_name} created Successfully')
            return redirect('admin')
    return render(request,'Admin/Admin_index.html',
            {'all_admins':all_admins,'admin_name':adminname,'all_agents':all_agents,
             'all_users':all_users,'Emp_name':Emp_name,'Emp_id':Emp_id,'Sys_id':Sys_id,
             'Emp_email':Emp_email,'emp_password':emp_password,'tickets': tickets,})
    
def user_list(request):
    all_users = User_signup.objects.all().order_by('-id')
    return render(request, 'Admin/Admin_index.html', {'all_users': all_users})

def delete_user(request, user_id):
    try:
        user = User_signup.objects.get(id=user_id)
        user.delete()
        messages.success(request, f'User {user.Emp_name} deleted successfully')
    except User_signup.DoesNotExist:
        messages.error(request, f'User {user.Emp_name} not found')
    
    return redirect('create_user')

def update_user(request, user_id):
     try:
        user = User_signup.objects.get(id=user_id)
        if request.method == 'POST':
            user.Emp_name = request.POST.get('Emp_name')
            user.Emp_id = request.POST.get('Emp_id')
            user.Sys_id = request.POST.get('Sys_id')
            user.Emp_email = request.POST.get('emp_mail')
            user.emp_password = request.POST.get('password')
            user.save()
            messages.success(request, f'User {user.Emp_name} updated successfully')
            return redirect('create_user')  # safer option
        return render(request, 'Admin/Admin_index.html', {'user': user})  
     except User_signup.DoesNotExist:
        messages.error(request, f'User not found')
        return redirect('create_user')


# Create agent------------------------------------agent---------
def create_agent(request):
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin session was not created')
        print("Admin session not created") 
        return redirect('sign_in') 
    agent_name=""
    agent_id=""
    agent_mail=""
    tickets = Ticket.objects.all().order_by('-created_at')
    all_admins = Admin_reg.objects.all().order_by('-id')
    all_users = User_signup.objects.all().order_by('-id')
    all_agents = Agent_signup.objects.all().order_by('-id')
    adminname = request.session['admin_name'] 
    if request.method == 'POST':
        
        agent_name=request.POST.get('agent_name')  
        agent_id=request.POST.get('agent_id') 
        agent_mail=request.POST.get('agent_mail')
        password=request.POST.get('password')
        
        if Agent_signup.objects.filter(agent_name=agent_name).exists():
            messages.error(request,f"User {agent_name} already exists")
        elif Agent_signup.objects.filter(agent_mail=agent_mail).exists():
            messages.error(request,f"User {agent_mail}  already exists")
        elif agent_name == '' and agent_id == '' and agent_mail == '' and password == '':
            messages.error(request, "Please fill all the fields")
                  
        else:
            agent_in=Agent_signup(
                      agent_name=agent_name,
                      agent_id=agent_id,
                      agent_mail=agent_mail,
                      password=password)      
            agent_in.save()
            messages.success(request,f'{agent_name} created Successfully')
            return redirect('admin')
    
    return render(request,'Admin/Admin_index.html',{'agent_name':agent_name,'agent_id':agent_id,'agent_mail':agent_mail,
            'all_admins':all_admins,'admin_name':adminname,'all_users':all_users,'all_agents':all_agents,'tickets': tickets,})
    
def update_agent(request, agent_id):
     try:
        agent = Agent_signup.objects.get(id=agent_id)
        if request.method == 'POST':
            agent.agent_name = request.POST.get('agent_name')
            agent.agent_id = request.POST.get('agent_id')
            agent.agent_mail = request.POST.get('agent_mail')
            agent.password = request.POST.get('password')
            agent.save()
            messages.success(request, f'Agent {agent.agent_name} updated successfully')
            return redirect('create_agent') 
        return render(request, 'Admin/Admin_index.html', {'agent': agent})  
     except Agent_signup.DoesNotExist:
        messages.error(request, f'Agent not found')
        return redirect('create_agent')
    
def delete_agent(request, agent_id):
    try:
        agent = Agent_signup.objects.get(id=agent_id)
        agent.delete()
        messages.success(request, f'Agent {agent.agent_name} deleted successfully')
    except Agent_signup.DoesNotExist:
        messages.error(request, f'Agent {agent.agent_name} not found')
    
    return redirect('create_agent')

# Ticket Monitering
def ticket_monitor(request):
    all_agents = Agent_signup.objects.all()
    all_admins = Admin_reg.objects.all().order_by('-id')
    all_users = User_signup.objects.all().order_by('-id')
    adminname = request.session['admin_name']
    if 'admin_name' not in request.session:
        messages.error(request, "Admin not logged in.")
        return redirect('admin_sign_up')

    tickets = Ticket.objects.all().order_by('-created_at')
    Ticket.objects.filter(seen_by_admin=False).update(seen_by_admin=True)  
    unseen_ticket_count = Ticket.objects.filter(seen_by_admin=False).count()
    return render(request, 'Admin/Admin_index.html', 
                  {'tickets': tickets,
                   'section': 'ticket_monitor',
                   'all_agents': all_agents,
                    'all_admins':all_admins,
                    'all_users':all_users,
                    'admin_name':adminname,
                    'unseen_ticket_count': unseen_ticket_count
                   })

def assign_ticket(request, ticket_id):
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin not logged in.')
        return redirect('admin_sign_up')

    adminname = request.session['admin_name']
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    all_agents = Agent_signup.objects.all()
    all_admins = Admin_reg.objects.all().order_by('-id')
    all_users = User_signup.objects.all().order_by('-id')
    tickets = Ticket.objects.all().order_by('-created_at')
    

    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        if agent_id:  
            agent = get_object_or_404(Agent_signup, id=agent_id)
            ticket.assigned_agent = agent
            ticket.status = 'In Progress'
            ticket.is_seen_by_agent = False
            ticket.save()
            messages.success(request, f"Ticket assigned to {agent.agent_name}")
            return redirect('ticket_monitor')  
        else:
            messages.error(request, "No agent selected.")

    return render(request, 'Admin/Admin_index.html', {
        'ticket': ticket,
        'tickets': tickets,
        'all_agents': all_agents,
        'section': 'assign_ticket',
        'all_admins': all_admins,
        'all_users': all_users,
        'admin_name': adminname
    })

# Make ticket seen
def mark_tickets_seen(request):
    if request.method == "POST" and request.session.get('admin_name'):
        Ticket.objects.filter(seen_by_admin=False).update(seen_by_admin=True)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"})

# Admin view the feedback
def admin_view_feedback(request):
    if 'admin_name' not in request.session:
        messages.error(request, 'Admin login required.')
        return redirect('sign_in')

    all_feedback = TicketFeedback.objects.select_related('user').order_by('-created_at')
    return render(request, 'Admin/Admin_index.html', {'feedbacks': all_feedback})

#-----------------------------------------------------------------------------------------------#User
# User index page
def user_index(request):
    if 'Emp_id' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')
    
    Emp_id = request.session['Emp_id']
    try:
        user = User_signup.objects.get(Emp_id=Emp_id)
    except User_signup.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('sign_in')

    status_filter = request.GET.get('status', 'all')
    section = request.GET.get('section', 'dashboard')

    if status_filter == 'all':
        tickets = Ticket.objects.filter(user=user).order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(user=user, status=status_filter).order_by('-created_at')

    return render(request, 'User/User_index.html', {
        'user': user,
        'tickets': tickets,
        'status_filter': status_filter,
         'section': section 
    })


def profile_update_user(request,user_id):
   
    if 'Emp_id' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')
    else:
        Emp_id = request.session['Emp_id']    
        all_users = User_signup.objects.all().order_by('-id')
        try:
           user = User_signup.objects.get(id=user_id)
           if request.method == 'POST':
                user.Emp_name = request.POST.get('Emp_name')
                user.Emp_id = request.POST.get('Emp_id')
                user.Sys_id = request.POST.get('Sys_id')
                user.Emp_email = request.POST.get('emp_mail')
                user.emp_password = request.POST.get('password')
                user.save()
                messages.success(request, f'User {user.Emp_name} updated successfully')
                return redirect('profile_update', user_id=user.id)
           tickets = Ticket.objects.filter(user=user).order_by('-created_at')  
           return render(request,'User/User_index.html',{'Emp_id':user.Emp_id,'all_users':all_users,'user':user,'tickets': tickets})
        except User_signup.DoesNotExist:
              messages.error(request, f'User not found')
              return redirect('create_user') 
          
def ticket_raising(request):
    if 'Emp_id' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')

    Emp_id = request.session['Emp_id']
    try:
        user = User_signup.objects.get(Emp_id=Emp_id)
    except User_signup.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('sign_in')
    
    tickets = Ticket.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        title = request.POST.get('ticket_title')
        description = request.POST.get('ticket_description')
        attachment = request.FILES.get('image')
        category = request.POST.get('ticket-Category')
        priority = request.POST.get('ticket_priority')

        if not title or not description or not category or not priority:
            messages.error(request, "All the fields are required")
            return redirect('create_ticket')
        ticket = Ticket(
            title=title,
            description=description,
            user=user,
            category=category,
            priority=priority,
            seen_by_admin=False
        )

        if attachment:
            ticket.attachment = attachment

        ticket.save()
        messages.success(request, 'Ticket raised successfully!!!')
        return redirect('create_ticket')

    return render(request, 'User/User_index.html', {'user': user, 'tickets': tickets})

    
def ticket_history(request):
    if 'Emp_id' not in request.session:
        messages.error(request, 'Admin session was not created')
        return redirect('sign_in')
    else:
        Emp_id = request.session['Emp_id']    
        user = User_signup.objects.get(Emp_id=Emp_id)
        tickets = Ticket.objects.filter(user=user).order_by('-created_at')
        
        return render(request, 'User/User_index.html', {'user': user, 'tickets': tickets})
    
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Ticket deleted successfully.")
    return redirect('create_ticket')

# Feedback
def submit_feedback(request):
    if 'Emp_id' not in request.session:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('sign_in')

    Emp_id = request.session['Emp_id']
    user = get_object_or_404(User_signup, Emp_id=Emp_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating:
            feedback= TicketFeedback.objects.create(
                user=user,
                rating=rating,
                comment=comment
            )
            feedback.save()
            messages.success(request, "Thanks for your feedback!")
            return redirect('user')
        else:
            messages.error(request, "Please provide a rating.")

    return render(request, 'User/User_index.html')


#-----------------------------------------------------------------------------------------------#Agent
# Agent index page
def agent_index(request):
    if 'agent_id' not in request.session:
        messages.error(request, 'Agent session was not created')
        return redirect('sign_in')
    
    agent_id = request.session['agent_id'] 

    try:
        agent = Agent_signup.objects.get(agent_id=agent_id) 
    except Agent_signup.DoesNotExist:
        messages.error(request, 'Agent not found')
        return redirect('sign_in')

    return render(request, 'Agent/Agent_index.html', {
        'agent_id': agent_id,
        'agent': agent
    })

def profile_update_agent(request, agent_id):
    if 'agent_id' not in request.session:
        messages.error(request, 'Agent not logged in.')
        return redirect('sign_in')
    
    session_agent_id = request.session['agent_id']
    if int(agent_id) != int(session_agent_id):
        messages.error(request, "Unauthorized access.")
        return redirect('sign_in')
    
    try:
        agent = Agent_signup.objects.get(id=agent_id)
        
        if request.method == 'POST':
            agent.agent_name = request.POST.get('agent_name')
            agent.agent_id = request.POST.get('agent_id')
            agent.agent_mail = request.POST.get('agent_mail')
            agent.password = request.POST.get('password')
            agent.save()
            messages.success(request, f'Agent {agent.agent_name} updated successfully')
            return redirect('profile_update_agent', agent_id=agent.id)

        tickets = Ticket.objects.filter(assigned_agent=agent).order_by('-created_at')
        all_users = User_signup.objects.all().order_by('-id')
        return render(request, 'Agent/Agent_index.html', {
            'agent_id': agent.agent_id,
            'agent': agent,
            'tickets': tickets,
            'all_users': all_users
        })

    except Agent_signup.DoesNotExist:
        messages.error(request, 'Agent not found')
        return redirect('sign_in')

# Assigned Ticket 
def assigned_ticket(request):
    if 'agent_id' not in request.session:
        messages.error(request, "Agent not logged in.")
        return redirect('sign_in')
    
    agent_id = request.session['agent_id'] 
    agent = Agent_signup.objects.get(agent_id=agent_id)
    tickets = Ticket.objects.filter(assigned_agent=agent).order_by('-created_at')
    all_users = User_signup.objects.all().order_by('-id')
    
    Ticket.objects.filter(assigned_agent=agent, is_seen_by_agent=False).update(is_seen_by_agent=True)
    assigned_tickets = Ticket.objects.filter(assigned_agent=agent).order_by('-created_at')
    unseen_count = Ticket.objects.filter(assigned_agent=agent, is_seen_by_agent=False).count()
    
    return render(request, 'Agent/Agent_index.html', {
        'assigned_tickets': tickets,  
        'section': 'Ticket-Dashboard',
        'agent_id': agent_id,
        'tickets': assigned_tickets,
        'agent': agent,
        'all_users': all_users,
        'unseen_count': unseen_count,
    })
    
# Update Ticket status

def update_ticket_status(request, ticket_id):
    if 'agent_id' not in request.session:
        messages.error(request, "Agent not logged in.")
        return redirect('sign_in')
    else:
        agent_id = request.session['agent_id']
        agent = Agent_signup.objects.get(agent_id=agent_id)
        tickets = Ticket.objects.filter(assigned_agent=agent).order_by('-created_at')
        all_users = User_signup.objects.all().order_by('-id')
        
        if request.method == 'POST':
            new_status = request.POST.get('status')
            ticket = get_object_or_404(Ticket, id=ticket_id)
            ticket.status = new_status
            ticket.save()
            messages.success(request, f"Ticket raised by  {ticket.user.Emp_name} in system no. {ticket.user.Sys_id} is {new_status}")
            return redirect('agent_index')  
        else:
            messages.error(request, "Invalid request.")
            
        return render(request,'Agent/Agent_index.html',{
            'ticket':ticket,
            'assigned_tickets': tickets,  
            'section': 'Ticket-Dashboard',
            'agent_id': agent_id,
            'agent': agent,
            'all_users': all_users
    })
        
def agent_ticket_history(request):
    
    agent_id = request.session.get('agent_id')  
    if not agent_id:
        return redirect('sign_in')  
    
    try:
        agent = Agent_signup.objects.get(agent_id=agent_id)
    except Agent_signup.DoesNotExist:
        return redirect('sign_in') 
    
    tickets = Ticket.objects.filter(assigned_agent=agent).order_by('-created_at')
    
    return render(request, 'agent/Agent_index.html', {'tickets': tickets})

    
def logout(request):
     request.session.flush()
     messages.success(request, "You Logged out successfully")
     return redirect('sign_in')    