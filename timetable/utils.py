from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from achievements.models import Action, AchUnlocked, Rank, Achievement
import datetime

class DTControl:
	def __init__(self):
		self.today = datetime.datetime.today()
		self.now = datetime.datetime.now()
		self.year = self.today.year
		self.month = self.today.month
		self.weekday = self.today.weekday() + 1
		self.day = self.today.day
		self.weeknumber = datetime.date(self.year, self.month, self.day).isocalendar()[1]
		self.week = 1
		if (self.weeknumber + settings.WEEK_SHIFT) % 2 == 0: self.week = 2
		self.hour = self.now.hour
		self.minute = self.now.minute
		self.timesumm = self.hour * 60 + self.minute

	def gettimesummstart(self, lessonnum):
		if lessonnum == 1: return 500
		elif lessonnum == 2: return 600
		elif lessonnum == 3: return 705
		elif lessonnum == 4: return 840
		elif lessonnum == 5: return 945
		elif lessonnum == 6: return 1040
		elif lessonnum == 7: return 1135

	def gettimesummend(self, lessonnum):
		if lessonnum == 1: return 590
		elif lessonnum == 2: return 690
		elif lessonnum == 3: return 795
		elif lessonnum == 4: return 930
		elif lessonnum == 5: return 1035
		elif lessonnum == 6: return 1130
		elif lessonnum == 7: return 1225

	def ifpause(self, time):
		pauses = [[590, 600], [690, 705], [795, 840], [930, 945], [1035, 1040], [1130, 1135]]
		for p in pauses:
			if time < p[1] and time > p[0]: return True
		return False

	def getTimeFromNum(self, lessonnum):
		if lessonnum == 1: return '8:20'
		elif lessonnum == 2: return '10:00'
		elif lessonnum == 3: return '11:45'
		elif lessonnum == 4: return '14:00'
		elif lessonnum == 5: return '15:45'
		elif lessonnum == 6: return '17:20'
		elif lessonnum == 7: return '18:55'

def addAction(user, action_text):
	action = Action()
	action.login = user
	action.text = action_text
	action.save()

def avatar(user):
	try:
		avatar = user.userprofile.avatar.url
	except ObjectDoesNotExist:
		return settings.NO_AVATAR
	return avatar

def pointsumm(user):
	summ = 0
	actions_list = Action.objects.all().filter(login = user)
	try:
		my_ach_list = AchUnlocked.objects.all().filter(login = user)
		for ach in my_ach_list:
			summ += ach.ach_id.xp
	except ObjectDoesNotExist:
		pass
	summ += actions_list.count()
	return summ

def getrank(user):
	summ = pointsumm(user)
	rank = '???'
	try:
		rank_list = Rank.objects.get(start_points__lte = summ, end_points__gte = summ)
		rank = rank_list.rank
	except ObjectDoesNotExist:
		rank = '???'
	return rank

def setAch(user, id):
	try:
		achievement = Achievement.objects.get(id = id)
		if not AchUnlocked.objects.filter(login = user, ach_id = achievement).exists():
			user_unlock = AchUnlocked()
			user_unlock.login = user
			user_unlock.ach_id = achievement
			user_unlock.save()
			addAction(user, 'получил достижение<div class="comments"><div class="comment"><span class="avatar"><img src="%s"></span><div class="content"><span class="author">%s</span><div class="text">%s</div></div></div></div>' % (achievement.icon, achievement.title, achievement.description))
	except ObjectDoesNotExist:
		pass

def handle_uploaded_file(f):
	now = timezone.now()
	url = '/media/img/%s/%s/%s%s%s' % (now.year, now.month, now.day, now.hour, now.minute)
	with open(url, 'wb+') as destination:
		for chunck in f.chunck():
			destination.write(chunk)
			user = request.user
			user.userprofile.avatar = url
			user.save()

def checkAchievements(user, params = ['404', 'actives', 'admin', 'comments', 'visiter', 'contacts']):
	if '404' in params:
		summ = pointsumm(user)
		if summ >= 404:
			setAch(user, 16)
	if 'actives' in params:
		actions = Action.objects.all().filter(login = user)
		summ = len(actions)
		if summ >= 75:
			setAch(user, 15)
		elif summ >= 25 and summ < 75:
			setAch(user, 10)
		elif summ >= 10 and summ < 25:
			setAch(user, 5)
	if 'admin' in params:
		if getrank(user) == 'Шаман':
			setAch(user, 12)
	if 'comments' in params:
		from notes.models import NoteComment
		from polls.models import PollComment
		comments_notes = NoteComment.objects.all().filter(login = user).count()
		comments_polls = PollComment.objects.all().filter(login = user).count()
		summ = comments_notes + comments_polls
		if summ >= 5:
			setAch(user, 7)
	if 'visiter' in params:
		from events.models import UserVisitEvent
		events_visit = UserVisitEvent.objects.all().filter(login = user).count()
		if events_visit >= 3:
			setAch(user, 13)
	if 'contacts' in params:
		from user.models import UserProfile
		my_profile = UserProfile.objects.get(user = user)
		if my_profile.vk or my_profile.facebook or my_profile.twitter:
			setAch(user, 9)
		if my_profile.phone:
			setAch(user, 11)