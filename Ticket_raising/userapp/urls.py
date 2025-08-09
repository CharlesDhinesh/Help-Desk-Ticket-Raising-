from django.urls import path
from .views import *

urlpatterns=[
    path('',sign_in,name='sign_in'),
    # admin urls
    path('admin/',admin_index,name='admin'),
    
    path('admin/create_admin/',create_admin,name='admin_sign_up'),
    path('delete_admin/<int:admin_id>/',delete_admin,name='delete_admin'),
    path('update_admin/<int:admin_id>/',update_admin,name='update_admin'),
    path('admin/admin_list/',admin_list,name='admin_list'),
    
    
    path('admin/create_user/',create_user,name='create_user'),
    path('delete_user/<int:user_id>/',delete_user,name='delete_user'),
    path('update_user/<int:user_id>/',update_user,name='update_user'),
    path('admin/user_list/',user_list,name='user_list'),
    
    path('admin/create_agent/',create_agent,name='create_agent'),
    path('delete_agent/<int:agent_id>/',delete_agent,name='delete_agent'),
    path('update_agent/<int:agent_id>/',update_agent,name='update_agent'),
    
    path('admin/ticket_monitoring/',ticket_monitor,name='ticket_monitor'),
    path("mark_tickets_seen/", mark_tickets_seen, name="mark_tickets_seen"),
    path('admin/assign-ticket/<int:ticket_id>/', assign_ticket, name='assign_ticket'),
    
    
    path('user/',user_index,name='user'),
    path('user/profile_update/<int:user_id>/',profile_update_user,name='profile_update'),
    path('user/create_ticket/',ticket_raising,name='create_ticket'),
    path('delete_ticket/<int:ticket_id>/',delete_ticket, name='delete_ticket'),
    path('user/feedback/', submit_feedback, name='submit_feedback'),

    
    # path('agent/',agent_index,name='agent_index'),
    path('agent/profile_update/<int:agent_id>/', profile_update_agent, name='profile_update_agent'),
    path('agent/', assigned_ticket, name='agent_index'),
    path('agent/update_ticket_status/<int:ticket_id>/', update_ticket_status, name='update_ticket_status'),


    path('logout/',logout,name='logout'),
]
   
