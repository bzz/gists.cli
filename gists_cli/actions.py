#!/usr/bin/env python

import sys, api, log, util, os, defaults, textwrap
from texttable import Texttable

#-------------------------------------------

_cmds = defaults.cmds
_supress = False

#-------------------------------------------

def supress( s ):
  global _supress
  _supress = s
  log.debug ("_supress: " + str(_supress))


#-------------------------------------------

def updateCredentials ():
  api.updateCredentials()
  sys.exit(0)

#-------------------------------------------

def list ():
  api.getCredentials()
  log.debug ("Command: List.")

  url = "/gists"
  gists = api.get(url)
  public_count = 0
  private_count = 0

  table = Texttable(max_width=defaults.max_width)
  table.set_deco(Texttable.HEADER | Texttable.HLINES)
  table.set_cols_align(["l", "l", "l", "l", "l"])
  table.set_cols_width([4, 30, 6, 20, 30])

  table.header( ["","Files","Public", "Gist ID",  "Description"] )

  for (i, gist) in enumerate(gists):
    private = False
    file_list = ''
    for (file, data) in gist['files'].items():
      file_list += file 
    if gist['public']:
      public_count += 1
    else:
      private_count += 1
    table.add_row( [i+1, file_list, str(gist['public']), gist['id'], gist['description']] )

  print table.draw()

  print ''
  print "You have %i Gists. (%i Private)" % (len(gists), private_count)

#-------------------------------------------

def new (public=None,description=None,content=None,filename=None):
  api.getCredentials()
  log.debug ("Command: New: public: '{0}' description: '{1}' filename: '{2}' content: '{3}'.".format(str(public), str(description), str(filename), str(content)))

  if public == None:
    if _supress:
      public = defaults.public
    else:
      public = util.parseBool( util.readConsole(prompt='Public Gist? (y/n):', bool=True) )

  if description == None:
    if _supress:
      description = defaults.description
    else:
      description = util.readConsole(prompt='Description:', required=False)

  if content == None and filename != None:
    if os.path.isfile( filename ):
      content = util.readFile(filename)
    else:
      print "Sorry, filename '{0}' is actually a Directory.".format(filename)
      sys.exit(0)

  if content == None:
    if _supress:
      content = defaults.content
    else:
      content = util.readConsole()

  if filename == None:
    filename = 'file.md'

  log.debug ("Creating Gist using content: \n" + content)

  url = '/gists'
  data = {'public': str(public).lower(), 'description': description, 'files': { os.path.basename(filename): { 'content': content } } }
  log.debug ('Data: ' + str(data))

  gist = api.post(url, data=data)

  pub_str = 'Public' if gist['public'] else 'Private'
  print "{0} Gist created with Id '{1}' and Url: {2}".format(pub_str, gist['id'], gist['html_url'])


#-------------------------------------------

def update (id):
  api.getCredentials()
  log.debug ("Command: Update: " + id)

#-------------------------------------------

def append (id):
  api.getCredentials()
  log.debug ("Command: Append: " + id)

#-------------------------------------------

def delete (id):
  api.getCredentials()
  log.debug ("Command: Delete: " + id)

#-------------------------------------------

def backup ():
  api.getCredentials()
  log.debug ("Command: Backup.")

#-------------------------------------------

def search ():
  api.getCredentials()
  log.debug ("Command: Search.")

#-------------------------------------------

def _get_gist(id):
  api.getCredentials()
  log.debug ("Internal: _get_gist: " + id) 

  url = "/gists/" + id
  gist = api.get(url)
  return gist

#-------------------------------------------

def view (id):
  print ("Fetching Gist with Id '%s'." % id)
  gist = _get_gist(id)
  for (file, data) in gist['files'].items():
    content = data['content']
    util.line()
    print 'Gist: {0} File: {1}'.format(id, file)
    util.line()
    print content
    util.line()

#-------------------------------------------

def get (id, path):
  log.debug ("Downloading Gist with Id '%s' to '%s'." % (id, path))

  gist = _get_gist(id)
  target = os.path.join(path,id)

  print ('Gist \'{0}\' has {1} file(s)'.format(id, len(gist['files'])))
  for file in gist['files']:
    print ('  ' + file)
  confirm = raw_input ("Download to (1) './' or (2) '{0}'?: ".format(target))
  if confirm in ('1', '2'):
    try:
      if not os.path.isdir(path):
        os.makedirs(path)
      if confirm == '1':
        target = path
      else:
        os.makedirs(target)
      for (file, data) in gist['files'].items():
        content = data['content']
        filepath = os.path.join(target,file)
        file = open( filepath , 'w')
        file.write(content)
        file.close()
        log.debug( 'Wrote file:' + filepath )
      print 'Download complete.'
    except Exception as e:
      print "Insufficient privilages to write to %s." % target
      print "Error message: " + str(e)
  else:
    print 'Ok. I won\'t download the Gist.'


#-------------------------------------------

def _getHelpTableRow (action, args='', help=''):
  l = []
  l.append(action)
  l.append(util.fileName + ' ' + '|'.join(_cmds[action]) + ' ' + args)
  l.append(help)
  return l
  
#-------------------------------------------

def help ():
  log.debug ("Help command.")

  print 'Gists.CLI'
  print ''
  print textwrap.fill('An easy to use CLI to manage your GitHub Gists. Create, edit, append, view, search and backup your Gists.', defaults.max_width)
  print ''
  print 'Author: Nik Khilnani - https://github.com/khilnani/gists.cli'
  print ''

  table = Texttable(max_width=defaults.max_width)
  table.set_deco(Texttable.HEADER | Texttable.HLINES)
  table.set_cols_align(["l", "l", "l"])
  table.set_cols_width([8, 45, 37])

  table.header( ["Action","Usage", "Description"] )
  
  table.add_row( _getHelpTableRow("Help", help='Display the help documentation') )

  table.add_row( _getHelpTableRow("Token", 'TOKEN', help='Save your Github  OAuth Token. Will be prefeered over ~/.git-credentials to avoid user/password prompts. Saves to ~/.gists') )

  table.add_row( _getHelpTableRow("List", help='Lists your public and private Gists') )

  table.add_row( _getHelpTableRow("View", 'GIST_ID', help='Displays contents of a Gist on screen.') )

  table.add_row( _getHelpTableRow("Download", 'GIST_ID [PATH]', help='Get or Download the files in a Gist to (1) Current Directory, or (2) Directory with Gist ID as its name.') )

  table.add_row( _getHelpTableRow("New", '[PUBLIC_BOOL] [DESCRIPTION] [CONTENT|FILE]', help='Create a new Gist. Will prompt for Public/Private, Description etc. if not provided as arguments. Default is Private.') )

  table.add_row( _getHelpTableRow("Update", help='Update the content of a Gist. NOT IMPLEMENTED') )

  table.add_row( _getHelpTableRow("Append", help='Will append  content to a Gist. NOT IMPLEMENTED') )

  table.add_row( _getHelpTableRow("Delete", help='Delete a Gist. NOT IMPLEMENTED') )

  table.add_row( _getHelpTableRow("Backup", help='Backup or Export all Gists. NOT IMPLEMENTED') )

  table.add_row( _getHelpTableRow("Search", help='Text search the content of your Gists. NOT IMPLEMENTED') )

  table.add_row( _getHelpTableRow("Supress", help='Supress prompts. Defaults will be used.') )

  table.add_row( _getHelpTableRow("Debug", help='Output Debug info. NOTE - Reveals sesnitive info such as OAuth tokens.') )

  print table.draw()

#-------------------------------------------

