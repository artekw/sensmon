{% extends "base.tpl" %}
{% block title %}Upload{% end %}
{% block content %}
    <h1>Upload</h1>
    <p>Zdalne wysyłanie firmware do sensbase! Wkrótce...<p>
    {#
    http://bottlepy.org/docs/dev/tutorial.html#request-data
    http://jeelabs.org/2013/01/30/remote-compilation/
    https://gist.github.com/cjgiridhar/3735543
    #}
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="data" />
    </form>
{% end %}
