<%inherit file="../base.mako"/>
<%namespace name="lib" file="../lib.mako"/>

<table class="table">
  <thead>
    <tr>
      <th>Service</th>
    </tr>
  </thead>
  <tbody>
  %for row in services:
    <tr>
      <td><a href="/services/${row.service}">${row.service}</a></td>
    </tr>
  %endfor
  </tbody>
</table>
