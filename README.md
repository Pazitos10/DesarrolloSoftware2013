DesarrolloSoftware2013
======================

Objetivo
========

Sistematizar los procedimientos de prestación de servicio de limpieza que se realizan en la empresa Senda SRL, buscando optimizar la forma de llevarlos a cabo por medio de una herramienta informática que englobe los requerimientos más importantes.


Alcances y restricciones
========================

El presente trabajo se enfocó en los procesos relacionados con la presupuestación y contratación de servicio de limpieza en sus dos modalilidades: por tiempo determinado y eventual; también se trató la facturación de servicios y asignación de personal.

Al momento de realizar la cotización del valor del servicio requerido por el cliente no se consideró la cantidad de productos que se utilizarán para realizar los trabajos. Los productos sólo se considerarán cuando el empleado requiere cierta cantidad para cumplir con el servicio, por lo cual el tratamiento del stock será omitido, tomando que siempre existen productos disponibles para satisfacer los requerimientos de los empleados

Requerimientos
==============

Zenda requiere:

postgresql 9.3 (base de datos)
python 2.7 - python-pip - requirements.txt (instalar con pip)
wkhtmltopdf (binarios) -> http://wkhtmltopdf.org/

requirements.txt contiene
=========================
Django==1.5.4
argparse==1.2.1
diff-match-patch==20110725.1
django-crispy-forms==1.4.0
django-import-export==0.2.2
django-localflavor==1.0
django-notify==1.1.2
django-pagination==1.0.7
django-selectable==0.7.0
django-wkhtmltopdf==1.2.2
ipdb==0.8
ipython==0.13.2
psycopg2==2.5.2
python-dateutil==2.2
simplejson==3.3.3
six==1.6.1
tablib==0.9.11
wsgiref==0.1.2
xlwt==0.7.5

Powered By ZendaTeam
