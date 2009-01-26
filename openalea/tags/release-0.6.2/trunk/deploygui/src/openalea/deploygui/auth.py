#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.DeployGui: OpenAlea installation frontend
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Authentification functions
"""

__license__= "CeCILL v2"
__revision__=" $Id$"


import cookielib, urllib, urllib2, urlparse


def cookie_login(login_url, values):
    """ Open a session
    login_url : the login url
    values : dictionnary containing login form field
    """
    
    # Enable cookie support for urllib2
    cookiejar = cookielib.CookieJar()
    urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    
    data = urllib.urlencode(values)
    request = urllib2.Request(login_url, data)
    url = urlOpener.open(request)  # Our cookiejar automatically receives the cookies
    page = url.read()
    urllib2.install_opener(urlOpener)


    # Make sure we are logged in by checking the presence of the cookie "session_ser".
    # (which is the cookie containing the session identifier.)
    if not 'session_ser' in [cookie.name for cookie in cookiejar]:
        print "Login failed !"
    else:
        print "We are logged in !"

        # Replace open_with_auth function
        import setuptools.package_index
        from setuptools.package_index import user_agent
        setuptools.package_index.open_with_auth = open_with_auth2




def open_with_auth2(url):
    """
    Open a urllib2 request, handling HTTP authentication
    In this version, user-agent is ignored
    """

    scheme, netloc, path, params, query, frag = urlparse.urlparse(url)

    if scheme in ('http', 'https'):
        auth, host = urllib2.splituser(netloc)
    else:
        auth = None

    if auth:
        auth = "Basic " + urllib2.unquote(auth).encode('base64').strip()
        new_url = urlparse.urlunparse((scheme,host,path,params,query,frag))
        request = urllib2.Request(new_url)
        request.add_header("Authorization", auth)
    else:
        request = urllib2.Request(url)

    # request.add_header('User-Agent', user_agent)
    fp = urllib2.urlopen(request)

    if auth:
        # Put authentication info back into request URL if same host,
        # so that links found on the page will work
        s2, h2, path2, param2, query2, frag2 = urlparse.urlparse(fp.url)
        if s2==scheme and h2==host:
            fp.url = urlparse.urlunparse((s2,netloc,path2,param2,query2,frag2))

    return fp
