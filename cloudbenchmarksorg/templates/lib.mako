<%def name="service_list(submission)">
  <ul class="services">
  %for c in submission.services().values():
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

<%def name="environment_link(env)">
  %if env.region:
    <a href="/environments/${env.provider_type}">${env.provider_type}</a>:<a href="/environments/${env.name}">${env.region}</a>
  %else:
    <a href="/environments/${env.name}">${env.name}</a>
  %endif
</%def>

<%def name="submissions_table(submissions_query)">
<table class="table">
  <thead>
    <tr>
      <th>Date</th>
      <th>Cloud</th>
      <th>Workload</th>
      <th>Result</th>
      <th>Benchmark</th>
      <th>Rank</th>
    </tr>
  </thead>
  <tbody>
  %for s, a_rank, d_rank in submissions_query:
    <tr>
      <td>${s.created_at}</td>
      <td>${environment_link(s.environment)}</td>
      <td>${service_list(s)}</td>
      <td><a href="/submissions/${s.id}">${format_result(s.result)}</a></td>
      <td>${s.benchmark_name}</td>
      <td>${a_rank if s.result.get('direction', 'asc') == 'asc' else d_rank}</td>
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
