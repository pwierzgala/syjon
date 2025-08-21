############
Syjon Readme
############

*******************
Database (Postgres)
*******************

How to restore Postgres database from file created by django-dbbackup
=====================================================================

..  code-block::

    Open PgAdnmin
    Go to plugins -> PSQL Console
    \i /path/to/yourfile.sql
    Press Enter

How to run postgres using docker?
=================================

..  code-block::

    docker run --name pgsql-dev -e POSTGRES_PASSWORD=xxx -p 5432:5432 postgres


*************
Cache (Redis)
*************


How to run redis server on production?
======================================

..  code-block::

    systemctl start redis-server


Redis doesn't automatically start on boot
=========================================

..  code-block::

    sudo systemctl enable redis-server


How to run redis server locally?
================================

#.  Create and start container:

    ..  code-block::

        docker run --name redis-syjon -p 6379:6379 -d redis

#.  Start created container:

    ..  code-block::

        docker start redis-syjon

***********
HTTP Server
***********

How to restart the application?
===============================

..  code-block::

    service gunicorn restart
    service nginx restart


Where are nginx logs?
=====================

..  code-block::

    tail -f /var/log/nginx/access.log
    tail -f /var/log/nginx/error.log
    tail -f /var/log/nginx/syjon-error.log


Where are upstart scripts
=========================

..  code-block::

    /etc/init/


Where is gunicorn configuration?
================================

..  code-block::

    cat /etc/systemd/system/gunicorn.service


********
Commands
********

How to copy a course?
=====================

#.  Copy a course using management script:

    ..  code-block::

        python manage.py copy_course <course_id> <year to>

#.  Copy learning outcomes using management script:

    ..  code-block::

        python manage.py copy_clos_2019 <course_from_id> <course_to_id>

#.  Add new didactic offer object in administration panel ``merovingian > didactic offer``.

    ..  code-block::

        Set the active didactic offer to the current one.

#.  Update courses using management script:

    ..  code-block::

        python manage.py refresh_courses

#.  Add permissions to newly added courses

    ..  code-block::

        merovingian > administrators
        trinity > administrators
