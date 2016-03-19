from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from timetable.utils import avatar, pointsumm, getrank, handle_uploaded_file
from achievements.models import Action, Achievement, AchUnlocked
from timetable.utils import addAction, setAch, checkAchievements, isOnline, UpdateStatus
from .models import Attendance, Duty, BonusPoints
from inventory.models import *
import pymorphy2
import math


def getProfileInfo(id):
	user = User.objects.get(id = id)
	username = user.first_name + ' ' + user.last_name
	avt = avatar(user)
	morph = pymorphy2.MorphAnalyzer()

	semester = settings.SEMESTER

	#Онлайн
	is_online = isOnline(user)
	last_visit = user.userprofile.last_visit

	points = pointsumm(user)
	points_morph = morph.parse('очко')[0]

	friends = []
	friends_list = User.objects.all().filter(is_active = True).exclude(id = id).order_by('-userprofile__last_visit')
	for friend in friends_list:
		fr_user = User.objects.get(id = friend.id)
		is_friend_online = isOnline(fr_user)
		current = {
			'user_id': friend.id,
			'username': '%s %s' % (friend.first_name, friend.last_name),
			'avatar': avatar(friend),
			'is_online': is_friend_online,
		}
		friends.append(current)

	#получение звания пользователя
	rank = getrank(user)

	#получение удобочитаемого номера
	last_phone = user.userprofile.phone
	phone = '+7 (%s)-%s-%s-%s' % (last_phone[0:3], last_phone[3:6], last_phone[6:8], last_phone[8:10])

	act_list = Action.objects.all().filter(login = user).order_by('-pub_date')[:50]
	act_count = Action.objects.filter(login = user).count()
	actions_morph = morph.parse('действие')[0]
	actions = []
	for action in act_list:		
		user = action.login		
		avt = avatar(user)
		cur_action = {
			'avatar': avt,
			'username': username,
			'user_id': user.id,
			'action_text': action.text,
			'pub_date': action.pub_date,
		}
		actions.append(cur_action)

	my_last_achievements = []
	#try:
	my_ach = AchUnlocked.objects.all().filter(login = user).order_by('-pub_date')
	last_achievements = my_ach[:5]
	for ach in last_achievements:
		my_last_achievements.append({
			'title': ach.ach_id.title,
			'icon': ach.ach_id.icon,
			'description': ach.ach_id.description,
		})


	ach_counter_morph = morph.parse('достижение')[0]

	#Получение процента посещаемости
	all_visiting = Attendance.objects.all().filter(lesson__semester = semester).filter(Q(group = 0) | Q(group = (user.userprofile.group))).count()
	my_visits = Attendance.objects.all().filter(lesson__semester = semester).filter(Q(group = 0) | Q(group = (user.userprofile.group))).filter(visitor = user).count()
	if all_visiting == 0: all_visiting = 1
	attendance_percent = round(my_visits / all_visiting * 100)

	#Получение процента задолжностей
	all_duties = Duty.objects.all().filter(lesson__semester = semester).filter(Q(group = 0) | Q(group = (user.userprofile.group))).count()
	my_not_duties = Duty.objects.all().filter(lesson__semester = semester).filter(visitors = user).filter(Q(group = 0) | Q(group = (user.userprofile.group))).count()
	if all_duties == 0: 
		all_duties = 1
		my_not_duties = 1
	duties_percent = round((1 - my_not_duties / all_duties) * 100)
	print(all_duties, my_not_duties)

	level = math.floor(act_count / 100) + 1

	percent = round(((act_count - 100 * (level - 1)) / 100) * 100)

	context = {
		'title': username,
		'user': user,
		'bodyclass': 'profile-page',
		'avatar': avt,
		'friends': friends,
		'actions': actions[:50],
		'act_count': act_count,
		'active_page': 1,
		'actions_morph': actions_morph.make_agree_with_number(len(act_list)).word,
		'xp': points,
		'level': level,
		'percent': percent,
		'xp_morph': points_morph.make_agree_with_number(points).word,
		'ach_counter': len(my_ach),
		'ach_counter_morph': ach_counter_morph.make_agree_with_number(len(my_ach)).word,
		'last_achievements': my_last_achievements,
		'rank': rank,
		'contacts': user.userprofile,
		'phone': phone,
		'is_online': is_online,
		'last_visit': last_visit,
		'attendance_percent': attendance_percent,
		'duties_percent': duties_percent,
	}

	return context

def getSmiles(user):
	smiles = []
	UserSmiles = UserInventoryItem.objects.all().filter(user = user).filter(type = 3)
	for sm_collection in UserSmiles:
		smilecollection = SmileCollection.objects.get(pk = sm_collection.item_id)
		smiles_list = smilecollection.smiles.all()
		for smile in smiles_list:
			smiles.append({
				'title': smile.title,
				'icon': smile.icon,
				'symbol': smile.symbol,
			})
	return smiles