<%inherit file="full.mako"/>

<table class="table">
  <thead>
    <tr>
      <th>
        Date
      </th>
    </tr>
  </thead>
  <tbody>
  %for s in submissions_query:
    <tr>
      <td>${s.created_at}</td>
    </tr>
  %endfor
  </tbody>
</table>
