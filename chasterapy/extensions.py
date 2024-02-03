import requests as _requests

class Extension:
	def __init__(self, token, slug):
		self._token = token
		self._slug = slug
	def getToken(self):
		return self._token
	def getSlug(self):
		return self._slug
	def getAuthHeader(self):
		return {"Authorization": f"Bearer {self.getToken()}"}
	def getAllLocks(self):
		last_id = None
		has_more = True
		locks = []
		while has_more:
			request = {
				"status": "locked",
				"extensionSlug": self.getSlug(),
				"limit": 15
			}
			if last_id != None:
				request["paginationLastId"] = last_id
			response = _requests.post(
				f"https://api.chaster.app/api/extensions/sessions/search",
				json=request,
				headers=self.getAuthHeader())
			response.raise_for_status()
			response = response.json()
			for session in response["results"]:
				locks += [ExtensionLock(self, session)]
			has_more = response["hasMore"]
			if has_more:
				last_id = response["results"][-1]["paginationId"]
		return locks

class ExtensionLock:
	def __init__(self, extension, data):
		self._data = data
		self._extension = extension
	def getId(self):
		return self._data["sessionId"]
	def _doAction(self, params):
		response = _requests.post(
			f"https://api.chaster.app/api/extensions/sessions/{self.getId()}/action",
			json={"action": params},
			headers=self._extension.getAuthHeader())
		response.raise_for_status()
	def addTime(self, secs):
		if secs < 1:
			raise ValueError()
		self._doAction({"name": "add_time", "params": secs});
	def removeTime(self, secs):
		if secs < 1:
			raise ValueError()
		self._doAction({"name": "remove_time", "params": secs});
	def freeze(self):
		self._doAction({"name": "freeze"});
	def unfreeze(self):
		self._doAction({"name": "unfreeze"});
	def toggle_freeze(self):
		self._doAction({"name": "toggle_freeze"});
	def pillory(self, secs, reason):
		if secs < 300 or secs > 86400 or type(reason) != str:
			raise ValueError()
		self._doAction({"name": "pillory", "params": {
				"duration": secs,
				"reason": reason
			}})
