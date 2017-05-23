from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
import arcpy, zipfile, StringIO
from gis.models import Articles
import os
import sqlite3

def home(request):
    # return HttpResponse('Hello, world')
    articles = Articles.objects.all()
    context = {
        'articles': articles
    }

    return render(request, 'gis/home.html', context)


def about(request):
    return render(request, 'gis/about.html')


def show_articles(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    return render(request, 'gis/article.html', {'article': article})


def mymap(request):
    return render(request, 'gis/test.html')


def search_form(request):
    return render_to_response('gis/search_form.html')


def search(request):
    #if 'q' in request.GET:
        arcpy.env.workspace = r"C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\myfgdb.gdb"
        arcpy.env.overwriteOutput = True
        value=str(request.GET['q'])
        arcpy.MakeFeatureLayer_management(r"C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\myfgdb.gdb\hydro", "Copyhydro", '"TYPE_LUT"='+ value )
        arcpy.CopyFeatures_management('Copyhydro', r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\rofl\rofle.shp')
        arcpy.Delete_management("Copyhydro")
        filenames = [r"C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\rofl\rofle.dbf", r"C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\rofl\rofle.prj", r"C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\rofl\rofle.sbn", r"C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\rofl\rofle.sbx", r"C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\rofl\rofle.shp", r"C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\rofl\rofle.shp.xml", r"C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\rofl\rofle.shx"]
        zip_subdir = "somefiles"
        zip_filename = "%s.zip" % zip_subdir
        s = StringIO.StringIO()
        zf = zipfile.ZipFile(s, "w")
        for fpath in filenames:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)

            # Add file, at correct path
            zf.write(fpath, zip_path)
        zf.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        return resp

def search2(request):
    valuez = str(request.GET['w'])
    con = sqlite3.connect(r'C:\Users\S1mple\Desktop\djangoGIS\db.sqlite3')
    cur = con.cursor()
    arcpy.env.workspace = r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\shape2'
    arcpy.env.overwriteOutput = True
    arcpy.MakeFeatureLayer_management(r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\shape2\kek.shp', 'Copykek')
    arcpy.CopyFeatures_management('Copykek', r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\vihlop2\vihod.shp')
    arcpy.Delete_management("Copykek")
    cur.execute("SELECT X,Y,type FROM gis_points WHERE type = '%s'" % valuez)
    cursor = arcpy.da.InsertCursor(r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\vihlop2\vihod.shp', ['SHAPE@XY', 'type'])
    for row in cur:
        a = ((row[0], row[1]), '%s' % row[2])
        cursor.insertRow(a)
    con.close()
    del cursor
    filenames2=[r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\vihlop2\vihod.dbf',r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\vihlop2\vihod.prj',r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\vihlop2\vihod.sbn',r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\vihlop2\vihod.sbx',r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\vihlop2\vihod.shp',r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\vihlop2\vihod.shp.xml',r'C:\Users\S1mple\Desktop\djangoGIS\gis\dev_static\vihlop2\vihod.shx']
    zip_subdir = "somefiles2"
    zip_filename = "%s.zip" % zip_subdir
    s = StringIO.StringIO()
    zf = zipfile.ZipFile(s, "w")
    for fpath in filenames2:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp2 = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp2['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp2