<%def name="service_list(submission)">
  <ul class="services">
  %for c in submission.services(filtered=False):
    <li><a href="/services/${c.charm_name}">${c.charm_name} (${c.unit_count})</a></li>
  %endfor
  </ul>
</%def>

<%def name="format_result(result)">
  ${result['value']} ${result.get('units', '')}
</%def>

<%def name="submissions_table(submissions)">
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
  %for s in submissions:
    <tr>
      <td>${s.created_at}</td>
      <td><a href="/environments/${s.environment.name}">${s.environment.name}</a></td>
      <td>${service_list(s)}</td>
      <td>${format_result(s.result)}</td>
    </tr>
  %endfor
  </tbody>
</table>
</%def>
