<!DOCTYPE html>

<%def name="active(path)">
  %if request.path == path:
    active
  %endif
</%def>

<html>
  <head>
    <title>cloud-benchmarks.org</title>
    <link href='http://fonts.googleapis.com/css?family=Ubuntu:300,400,700' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-material-design/0.3.0/css/material-fullpalette.min.css">
    <link rel="stylesheet" href="/static/css/app.css">
  </head>
  <body>
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/">Cloud Benchmarks</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li class="${active('/')}"><a href="/">Home</a></li>
            <li class="${active('/submissions')}"><a href="/submissions">Results</a></li>
            <li class="${active('/environments')}"><a href="/environments">Clouds</a></li>
            <li class="${active('/services')}"><a href="/services">Services</a></li>
            <li><a href="http://cloud-benchmarks.github.io">Blog</a></li>
          </ul>
          <!--
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">Log in</a></li>
          </ul>
          -->
        </div>
      </div>
    </nav>
    <div class="container">
      ${next.body()}
    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-material-design/0.3.0/js/material.min.js"></script>
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
         (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
           m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
             })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-64826479-2', 'auto');
        ga('send', 'pageview');

    </script>
  </body>
</html>
