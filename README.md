# CrowdHydrology
Aggregates water level height measurements from rivers and other water bodies across the U.S by receiving text messages with measurements from passerby citizen-scientists

__Front-end website URL:__ crowdhydrology.geology.buffalo.edu<br>

## Important Server Information for Future Developers

`ssh user@crowdhydrology.geology.buffalo.edu`<br><br>

To restart the Django server do: <br>`touch /htdocs/www/crowdhydrology_django_backend/crowd_hydrology/crowd_hydrology/wsgi.py` <br><br>
To restart the apache service do (necessary after editing the django.config file):<br>`sudo service httpd restart` - contact UB Admin Dave Yearke to perform this command for you. <br><br>

__UB Server URL:__ crowdhydrology.geology.buffalo.edu<br>
__Django backend website URL:__ http://crowdhydrology.geology.buffalo.edu:8020/admin<br>
__Django server files location:__ /htdocs/www/crowdhydrology_django_backend/<br>
__Django server configuration file location__: /etc/httpd/conf.d/django.conf<br>
Other server configurations under the CrowdHydrology project is located at the bottom of: /etc/httpd/conf/httpd.conf<br><br>

I followed the ['How To Serve Django Applications with Apache and mod_wsgi on Ubuntu 14.04'](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04) tutorial to set up the University at Buffalo server. Note that the UB server is Centos 6 REHL, not Ubuntu 14.04.<br>

Contact Dave Yearke at yearke@buffalo.edu if you need admin / UB server technical support, he is very familiar with the CrowdHydrology work.<br><br>

### Please view the poster below to help your understanding of the CrowdHydrology project and the flow of data<br><br>

<img src="/readme-pics/research-poster.png" alt="CrowdHydrology Research Poster" width="850"/>
