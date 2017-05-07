import re
import base64
import urllib
import requests
import getpass
import logging

USERNAME = ''
PASSWORD = ''

URLS = {
 'acorn': 'http://acorn.utoronto.ca/',
 'weblogin': 'https://weblogin.utoronto.ca/',
 'relay': 'https://idp.utorauth.utoronto.ca/PubCookie.reply',
 'acorn_spACS': 'https://acorn.utoronto.ca/spACS',
 'complete_academic_history': 'https://acorn.utoronto.ca/sws/' +
                              'transcript/academic/main.do' +
                              '?main.dispatch&mode=complete',
 'logout': 'https://acorn.utoronto.ca/sws/auth/logout.do?logout.dispatch'
}

def perform_SSO(username, password):

  session = requests.session()

  acorn_redirect_to_auth = session.get(URLS['acorn'])

  payload, headers = prepare_login_form_data(acorn_redirect_to_auth.text,
                                             username, password)
  login_redirect_to_loggedin = session.post(URLS['weblogin'],
                                            headers=headers, data=payload)

  if "Authentication Failed" in login_redirect_to_loggedin.text:
    print("ERROR: Are your credentials correct?")
    exit()

  form_inputs = extract_form_data(login_redirect_to_loggedin.text)
  loggedin_redirect_to_SSO_idp = session.post(URLS['relay'], data=form_inputs)

  form_inputs = extract_form_data(loggedin_redirect_to_SSO_idp.text)
  SSO_idp_redirect_to_acorn = session.post(URLS['acorn_spACS'], data=form_inputs)

  return session

def prepare_login_form_data(login_markup, user, pw):
  form_data = extract_form_data(login_markup)
  form_inputs = extract_b64_form_data(form_data['pubcookie_g_req'])
  form_inputs['user'] = user
  form_inputs['pass'] = pw
  form_inputs['login'] = ''
  form_inputs['relay_url'] = URLS['relay']
  form_inputs['reply'] = '1'
  payload = urllib.parse.urlencode(form_inputs)
  headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
  return payload, headers

def extract_form_data(raw_markup):
  form_regex = '<input type=hidden name=([^\ ]*) value=([^>]*)'
  raw_markup = raw_markup.replace('"', '')
  pattern = re.compile(form_regex)
  matches = pattern.findall(raw_markup)
  form_data = {}
  for form_input in matches:
    form_data[str(form_input[0])] = str(form_input[1])
  return form_data

def extract_b64_form_data(b64_str):
  form_data = (base64.b64decode(b64_str)).decode('utf-8')
  raw_data = [key_val for key_val in form_data.split('&')]
  parsed_data = {}
  for data in raw_data:
    current = data.split('=')
    parsed_data[current[0]] = current[1]
  return parsed_data

def retrieve_complete_academic_history(session):
  complete_history = session.get(URLS['complete_academic_history'])
  marks_regex = '<div.*?courses blok.*?>([^<]*)</div>'
  pattern = re.compile(marks_regex)
  all_marks = pattern.findall(complete_history.text)

  gpa_regex = '<div.*?gpa-listing.*?>([^<]*)</div>'
  pattern = re.compile(gpa_regex)
  all_gpas = pattern.findall(complete_history.text)
  return all_marks, all_gpas

def logout(session):
  response = session.get(URLS['logout'])
  return 'You have logged out of ACORN' in response.text

if __name__ == '__main__':
  if USERNAME == '' or PASSWORD == '':
    USERNAME = input("Please enter your UTORid: ")
    PASSWORD = getpass.getpass("Please enter your password: ")

  print('Processing...\n')

  authed_session = perform_SSO(USERNAME, PASSWORD)

  marks, gpas = retrieve_complete_academic_history(authed_session)

  for semester in marks:
    print(semester)
  print('\n')
  for semester in gpas:
    print(semester)

  print('\n')

  if logout(authed_session):
    print('Logged out!')
  else:
    print('Logout unsuccessful')


