<%inherit file="../base.mako"/>
<%namespace name="lib" file="../lib.mako"/>

<table class="table">
  <thead>
    <tr>
      <th>Cloud</th>
    </tr>
  </thead>
  <tbody>
  %for row in environments:
    <tr>
      <td><a href="/environments/${row.name}">${row.name}</a></td>
    </tr>
  %endfor
  </tbody>
</table>
