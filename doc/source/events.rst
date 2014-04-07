
Créer un event
==============

.. code::

   curl -X POST http://127.0.0.1:8000/events/ \ 
     -d '{"name": "print 456", "osmid": 6565, "changeset": 65, "rule": 1}' \
     -H "Content-Type: application/json"
