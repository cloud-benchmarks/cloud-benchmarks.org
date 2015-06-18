<%inherit file="../base.mako"/>

<%def name="service_list(submission)">
  <ul class="charms">
  %for c in submission.charms(filtered=False):
    <li><a href="/charms/${c.name}">${c.name} (${c.count})</a></li>
  %endfor
  </ul>
</%def>

<%def name="format_result(result)">
  ${result['value']} ${result.get('units', '')}
</%def>

<table class="table">
  <thead>
    <tr>
      <th>Date</th>
      <th>Cloud</th>
      <th>Workload</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
  %for s in submissions_query:
    <tr>
      <td>${s.created_at}</td>
      <td><a href="/clouds/${s.cloud_name}">${s.cloud_name}</a></td>
      <td>${service_list(s)}</td>
      <td>${format_result(s.result)}</td>
    </tr>
  %endfor
  </tbody>
</table>
