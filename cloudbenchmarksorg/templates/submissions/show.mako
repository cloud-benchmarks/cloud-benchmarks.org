<%inherit file="../base.mako"/>
<%namespace name="lib" file="../lib.mako"/>

${submission.svg | n}
<pre>${submission.bundle_yaml}</pre>
