""" Implements SMS push via api.sms24x7.ru """

import pycurl
from urllib import urlencode, quote
from json import JSONDecoder

api_target = "https://api.sms24x7.ru/"

class smsapi_exception(Exception):
	""" General class for smsapi exceptions. """
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class smsapi_interface_exception(smsapi_exception):
	""" Raised in case something goes wrong in interacting with api
	like being impossible to connect or getting unexpected api response """
	pass

class smsapi_auth_exception(smsapi_exception):
	""" Raised if user has problems with authentication when logging in """
	pass

class smsapi_nologin_exception(smsapi_exception):
	""" Raised if action is impossible, because logging in is required """
	pass

class smsapi_balance_exception(smsapi_exception):
	""" Raised if account is out of money """
	pass

class smsapi_spam_exception(smsapi_exception):
	""" Raised if message could not be sent because of being filtered
	for impermissible content """
	pass

class smsapi_encoding_exception(smsapi_exception):
	""" Raised if data, passed as message text, does not match
	requested encoding. """
	pass

class smsapi_nogate_exception(smsapi_exception):
	""" Raised if it's impossible to route a message to specified
	destination """
	pass

class smsapi_other_exception(smsapi_exception):
	""" Used to identify a situation when api method returns error
	status, unexpected and thus not handled by other exceptions """
	pass


class smsapi:
	def _wrf(self,data):
		self.http_response += data

	def _communicate(self, request, usecookie = None):
		"""
			Queries API with values from request dictionary, 'format'
		key is overridden for specifying output format. If `usecookie`
		is set, passes cookie raw data in request.
			Returns ((err_code(int), type(int), text), data) by parsing
		response 'msg' and 'data' sections. 'data' is passed as a
		dictionary, msg is converted into tuple, where type is turned
		into int by severity level. """
		global api_target
		if type(request) != dict:
			raise ValueError("Expecting dict as request")
		request['format'] = "json"
		postdata = urlencode(request)
		curl=pycurl.Curl()
		if self.debug:
			def echof(a,b):
				print a,b
			curl.setopt(pycurl.DEBUGFUNCTION, echof)
			curl.setopt(pycurl.VERBOSE, True)
		curl.setopt(pycurl.URL, api_target)
		curl.setopt(pycurl.POST, True)
		curl.setopt(pycurl.POSTFIELDS, postdata)
		if usecookie != None:
			curl.setopt(pycurl.COOKIE, usecookie)
		self.http_response = ""
		def voidf(data):
			pass
		curl.setopt(pycurl.WRITEFUNCTION, self._wrf)
		curl.setopt(pycurl.HEADERFUNCTION, voidf)
		try:
			curl.perform()
		except pycurl.error as e:
			raise smsapi_interface_exception("cURL request failed: %i. %s"%(e[0], e[1]))
		try:
			json_struct = self.JD.decode(self.http_response) # Decoding in UTF-8, by default
		except ValueError:
			raise smsapi_interface_exception("Could not parse JSON, returned by API")
		try:
			responsedict = json_struct['response']
			#ensuring these sections are set
			msg = responsedict['msg']
			data = responsedict['data']
			try:
				err_code = int(msg['err_code'])
			except ValueError:
				raise smsapi_interface_exception("In response JSON msg -> err_code could not be parsed into int")
			type_str = msg['type']
			try:
				type_ = {'message':0, 'notice':1, 'error':2}[type_str]
			except KeyError:
				raise smsapi_interface_exception("In response JSON msg -> error has unexpected value (%s)"%(repr(type_str)))
			text = msg['text']
		except KeyError:
			raise smsapi_interface_exception("Malformed JSON received from API")
		return ((err_code, type_, text), data)


	def __init__(self, email, password, debug=False):
		""" Constructs an object, setting email and password for future
		use. If debug is True, prints underlying curl communications. """
		if type(email) != str or type(password) != str or len(email) == 0 or len(password) == 0:
			raise ValueError("`username` and `password` parameters must be non-empty strings!")
		self.email = email
		self.password = password
		self.debug = debug
		self.nologin_uses = 0
		self.cookie = None # Session cookie to be set after logging in
		self.JD = JSONDecoder()

	def login(self):
		""" Authenticates to api to get session ID for future use. Exceptions: auth, interface. """
		resp = self._communicate({'method':'login', 'email':self.email, 'password':self.password})
		if resp[0][0] != 0:
			raise smsapi_auth_exception(resp[0][0])
		try:
			sid = str(resp[1]['sid'])
		except KeyError:
			raise smsapi_interface_exception("Login request OK, but no 'sid' set")
		self.cookie = "sid=%s"%(quote(sid))


	def push_msg(self, text, phone, sender_name = None, Unicode = None,
		Type = None, validity = None, dlr_mask = None, dlr_url = None,
		nologin = False):
		"""
			Sends SMS message via api.
			Parameters 'text' and 'phone' are mandatory, text is 
		supposed to be either ASCII string, or raw UTF-8 string, or 
		Unicode python string to be converted. Parameters 'sender_name',
		'Unicode', 'Type', 'validity', 'dlr_mask', 'dlr_url' do not need
		to be set. Parameter 'nologin', when set to True, identifies
		that authentication and message sending shall take place in one
		query and no session shall be created for authentication reuse.
		Otherwise being logged in is required, smsapi_nologin_exception
		is raised if logging in is required (which may also happen in
		case of expired session).
			Returns (n_raw_sms, credits) - number of SMS parts
		the message was split into and price for one such part.
			Using `nologin` option while being logged in is forbidden.
		Calling nologin method more than one time is forbidden. This is
		the wrong way of using the class.
			Regular exceptions: nologin, auth, balance, spam, encoding,
		nogate.
			Other exceptions to consider: interface, other.
			Also throws ancestor (smsapi_exception) exception, if
		class used the wrong way, will not hapen if class is used the
		proper way.
		"""
		if nologin:
			if self.cookie != None:
				raise smsapi_exception("Using nologin option of push_msg while being logged in is the wrong way and thus forbidden")
			if self.nologin_uses > 0:
				raise smsapi_exception("Using nologin option of push_msg more than one time is forbidden, log in once and push messages after instead")
			self.nologin_uses += 1
		if type(text) == str:
			# OK
			pass
		elif type(text) == unicode:
			text = text.encode("UTF-8")
		else:
			raise ValueError("text variable is of improper type")
		req = {"method":"push_msg", "text":text, "phone":phone}
		if sender_name != None: req['sender_name']=sender_name
		if Unicode != None: req['unicode']=int(Unicode)
		if Type != None: req['type']=Type
		if validity != None: req['validity']=int(validity)
		if dlr_mask != None: req['dlr_mask']=int(dlr_mask)
		if dlr_url != None: req['dlr_url']=dlr_url

		if nologin:
			req ['email'] = self.email
			req ['password'] = self.password
			usecookie = None
		else:
			if self.cookie != None:
				usecookie = self.cookie
			else:
				raise smsapi_nologin_exception("Not logged in")

		resp = self._communicate(req, usecookie)
		if resp[0][0] == 36:
			raise smsapi_balance_exception("No money")
		if resp[0][0] == 3:
			if nologin:
				raise smsapi_auth_exception("Failed to authenticate to server using email and password")
			else:
				raise smsapi_nologin_exception("Failed to authenticate to server using session ID, log in again")
		if resp[0][0] == 37 or resp[0][0] == 38:
			raise smsapi_spam_exception(resp[0][0])
		if resp[0][0] == 35:
			raise smsapi_encoding_exception(resp[0][0])
		if resp[0][0] == 29:
			raise smsapi_nogate_exception("No gate to send your message to destination")
		if resp[0][0] != 0:
			raise smsapi_other_exception(resp[0][0])

		try:
			n_raw_sms = int(resp[1]['n_raw_sms'])
			Credits = float(resp[1]['credits'])
		except KeyError:
			raise smsapi_interface_exception("Could not find 'n_raw_sms' or 'credits' in successful push_msg response")
		except ValueError:
			raise smsapi_interface_exception("'n_raw_sms' or 'credits' could not be converted into int and float respectively")

		return (n_raw_sms, Credits)
