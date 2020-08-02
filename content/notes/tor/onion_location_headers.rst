tor browser can now redirect clearnet sites to onion services
=============================================================

:date: 2020-06-03
:summary: tor browser has a new feature that redirects clearnet sites to their
          onion services

On Monday the Tor Project released_ version 9.5 of the tor browser and with it
a long-awaited new feature. The update will tell you if a website you visit in
the browser has a corresponding onion service.

Initially, when you visit one of these websites (such as this one), the URL bar
will display this label:

.. image:: /static/onion_location.png
   :alt: Tor Browser displaying '.onion available' in URL bar.

Clicking on this label will take you to the onion service version of the
website.

And the cool part: you can set tor browser to always redirect you to these
onion services, by finding this preference and setting it to 'Always':

.. image:: /static/onion_location_pref.png
   :alt: Tor Browser onion-location pref

This functionality depends on websites setting a :code:`Onion-Location` HTTP
header containing the link to their onion service. For example, all I had to do
was add this line into my nginx.conf in my clearnet site's server block:

.. code-block:: sh

    add_header Onion-Location http://mcolxyzogp3cy4czf52oa2svu2vjge3otm3shxmtvwshyum47sis3iid.onion$request_uri;

(In case of overflow: that is one line.)

That header is all it takes for tor browser users to use onions by default on
all sites that host them, removing any need for manual identification of
whether websites that they visit host onion services.

By improving awareness and accessibility of onion services in this way, not
only can we discover more onions for popular websites that may have them, but
we legitimise and encourage the use of onion services as a simple means of
making the web more accessible for those who experience internet censorship.


.. _released : https://blog.torproject.org/new-release-tor-browser-95
