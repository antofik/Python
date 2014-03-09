cd /server/www/photos.mfst.pro;svn up; supervisorctl stop photos.mfst.pro; supervisorctl start photos.mfst.pro; chmod 777 uwsgi.sock

