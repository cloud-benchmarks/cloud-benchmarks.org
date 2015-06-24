<%def name="service_list(submission)">
  <ul class="services">
  %for c in submission.services(filtered=False):
    <li><a href="/services/${c.charm_name}">${c.charm_name} (${c.unit_count})</a></li>
  %endfor
  </ul>
</%def>

<%def name="format_result(result)">
  %if isinstance(result, dict) and 'value' in result:
    ${result['value']} ${result.get('units', '')}
  %else:
    ${result}
  %endif
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
      <td><a href="/submissions/${s.id}">${format_result(s.result)}</a></td>
    </tr>
  %endfor
  </tbody>
</table>
</%def>

<%def name="keyval_table(pairs, headers=None, caption=None)">
<% headers = headers or ('Key', 'Value') %>
<table class="table">
  %if caption:
    <caption>${caption}</caption>
  %endif
  <thead>
    <tr>
      %for h in headers or ('Key', 'Value'):
      <th>${h}</th>
      %endfor
    </tr>
  </thead>
  <tbody>
  %for key, val in pairs:
    <tr>
      <td>${key}</td>
      <td>${format_result(val)}</td>
    </tr>
  %endfor
  </tbody>
</table>
</%def>