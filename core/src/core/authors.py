# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAleaLab
#
#       Copyright 2015 INRIA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.github.io
#
###############################################################################

"""

.. warning ::

    This file is not complete. Only appears authors added manually by community or author themselves.
    So, other authors, not in this list, may have contribute to this code. Please have look to README, AUTHORS, ABOUT
    files, source code files and other official documents to have a reliable information about authors.

.. warning ::

    If your are a contributor and do not appear in this list or information are wrong, please fix it or send a message to ask to fix it.



If you have contributed in openalea one day and want to be cited, please fill your information here

    fname = {'name': u"First name Family name", additional fields}

fname: first letter of your first name + first fullname
If you have multiple first name: use one letter for each name. Example: Jean-Philippe -> jp
If you have multiple family names: use at least first family name and then as you want for additional names
Ex: Dufour-Kowalski -> dufourko, dufour, dufourkowalski, ...

Additional fields:
  * email
  * employer
  * department
  * team
  * note
"""

# Define authors and contributors
##########################################################################

vmirabet = {'email': u'vincent.mirabet@ens-lyon.fr', 'name': u'Vincent Mirabet'}
akonig = {'email': u'alizon.konig@inria.fr', 'name': u'Alizon K\xf6nig'}
fboudon = {'email': u'frederic.boudon@cirad.fr', 'name': u'Frederic Boudon'}
jchopard = {'name': u'Jérôme Chopard', 'email': u'jerome.chopard@inria.fr'}
tcokelaer = {'name': u'Thomas Cokelaer'}
dbarbeau = {'email': u'daniel.barbeau@inria.fr', 'name': u'Daniel Barbeau'}
jdiener = {'name': u'Julien Diener'}
sdufourko = {'email': u'samuel.dufour@cirad.fr', 'name': u'Samuel Dufour-Kowalski'}
rfernandez = {'name': u'Romain Fernandez'}
gbaty = {'email': u'guillaume.baty@inria.fr', 'name': u'Guillaume Baty'}
gcerutti = {'email': u'guillaume.cerutti@inria.fr', 'name': u'Guillaume Cerutti'}
gmalandain = {'name': u'Grégoire Malandain', 'email': u'gregoire.malandain@inria.fr'}
gmichelin = {'name': u'Gaël Michelin', 'email': u'gael.michelin@inria.fr'}
cgodin = {'email': u'christophe.godin@inria.fr', 'name': u'Christophe Godin'}
jcoste = {'email': u'julien.coste@inria.fr', 'name': u'Julien Coste'}
jlegrand = {'email': u'jonathan.legrand@ens-lyon.fr', 'name': u'Jonathan Legrand'}
lguignard = {'email': u'leo.guignard@inria.fr', 'name': u'L\xe9o Guignard'}
emoscardi = {'name': u'Eric Moscardi'}
oali = {'email': u'olivier.ali@inria.fr', 'name': u'Olivier Ali'}
pfernique = {'email': u'pierre.fernique@inria.fr', 'name': u'Pierre Fernique'}
cpradal = {'email': u'christophe.pradal@inria.fr', 'name': u'Christophe Pradal'}
sribes = {'email': u'sophie.ribes@inria.fr', 'name': u'Sophie Ribes'}

# Add institute / company information
##########################################################################
ENS = [jlegrand]

CIRAD = [fboudon, sdufourko, cpradal]
for member in CIRAD:
    member.setdefault('employer', []).append('Cirad')

INRIA = [akonig, jchopard, dbarbeau, gbaty, gcerutti, gmalandain, gmichelin, cgodin, jcoste, lguignard, sribes]
for member in INRIA:
    member.setdefault('employer', []).append('INRIA')


# Add team information
##########################################################################
VIRTUALPLANTS = [akonig, fboudon, jchopard, tcokelaer, dbarbeau, jdiener, sdufourko, rfernandez, gbaty, gcerutti,
                 cgodin, jcoste, jlegrand, lguignard, emoscardi, oali, pfernique, cpradal, sribes]
for member in VIRTUALPLANTS:
    member.setdefault('team', []).append('VirtualPlants')

MORPHEME = [gmalandain, gmichelin]
for member in MORPHEME:
    member.setdefault('team', []).append('Morpheme')
