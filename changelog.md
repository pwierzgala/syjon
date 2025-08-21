# 2020-03-20, vesrion 2.0.0
    - Added learning outcomes for subjects
    - Updated syllabuses to refelect changes from 2019 reform.
    - Code updated to handle changes in logic with minimal influence on the enduser. 
      The system has already 9 years and new courses need to be updated without changing
      logic for old courses.
  
# 2019-10-20
    - Removed fabric script for automatic deployment due to incompatibility with 
      python3. It should be replaced with Ansible script.
    - Removed celery.
    - Updated strings concenring new learning outcomes. 

# 2017-05-04
    - Removed applications: orb, pythia, morpheus, megacity

# 2016-01-31
    - Upgrade from Django 1.8.7 to 1.9.1.

# 2016-01-22
    - Update from python 2.7 to python 3.4.
    - Changed all urlpatterns to a plain list instead of django.conf.urls.url() instances (deprecated since 1.8).
    - Added namespaces to metacortex urls.

# 2016-01-13
    - Removed CourseDegreeProfile and CourseDiagnosticInfo from merovingian.

# 2016-01-11
    - Ubuntu version ugraded from 12.04 to 14.04.

# 2016-01-09
    - Added redis as cache and session storage.
    - Removed AUTH_PROFILE_MODULE from settings (deprecated in django 1.5).

# 2016-01-05
    - Displaying search engine results optimised by 304% (2902.02ms -> 954.48ms).
    - Displaying syllabus details optimised by 202% (409.04ms -> 204.42ms).

# 2016-01-02
    - Link application moved to other server.
    - All {{ STATIC_URL }} occurances in templates replaced with "static" template tag.

# 2015-12-28
    - M2M relation between Course and EducationArea moved from EducationArea to Course.
    - M2M relation between Course and KnowledgeArea moved from KnowledgeArea to Course.
    - M2M relation between Course and EducationField moved from EducationField to Course.
    - M2M relation between Course and EducationDiscipline moved from EducationDiscipline to Course.
    - FK relation between EducationField and EducationDiscipline moved from EducationField to EducationDiscipline.
    - Displaying Course Learning Outcomes optimised by 949% (6276ms -> 661ms).
    - Displaying Module Learning Outcomes optimised by 160% (855ms -> 534ms).
    - General update of Trinity code.
    - Removed context processor with applications versions.
    - Custom database tables and columns names changed to default.

# 2015-12-21
    - M2M relation between Module and SGroup changed to ForeignKey on Module to SGroup.

# 2015-12-20
    - Fixed password resetting procedure (due to changes in Django 1.6).

# 2015-12-19
    - Removed MerovingianNews model from Merovingian.
    - Removed MetacortexProfile model from Metacortex.
    - Removed MetacortexNews model from Metacortex.
    - Added ISCED code to Module model.
    - Removed ERASMUS code from Subject model.

# 2015-12-12
    - Added new PDF rendering functions basing on weasyprint package.

# 2015-12-07
    - Changed names of conflicting merovingian custom queryset methods from "latest" to "newest".

# 2015-12-06
    - Updated QuerySets and Managers for Merovingian models.

# 2015-12-05
    - Upgrade from Django 1.4.2 to Django 1.8.7.
    - Added quotations to {% url %} tags.
    - Changed "from django.conf.urls.defaults import [...]" to "from django.conf.urls import [...]".
    - Admin "queryset" methods changed to "get_queryset".
    - Added missing "fields/exclude" attributes on meta classes of model forms.
    - Changed "transaction.commit_on_success" to "transaction.atomic".
    - Removed "MANAGERS" from settings.
    - Removed "ADMINS" from settings.
    - Removed "TEMPLATE_LOADERS" from settings.
    - Settings variable "PROJECT_PATH" changed to "BASE_DIR".
    - User model method "get_profile()" changed to attribute "userprofile".
    - Keyword argument on HttpResponse changed from "mimetype" to "content_type"